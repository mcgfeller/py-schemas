""" Marshmallow based conformant Schema.
    Marshmallow fields are monkey-patched.
    Marshmallow schema is subclassed. 
"""

import marshmallow as mm  # type: ignore
import decimal
import datetime
import abc_schema
import dataclasses
import typing
import typing_extensions




class SchemedObject:
    """ SchemedObject is the - entirely optional - superclass that can be used for classes that have an associated
        Schema. It defines one class method .__get_schema__, to return that Schema.

        By convention of this implementation, the Schema is obtained as an inner class named Schema.
        The Schema is instantiated and cached as .__schema. __objclass__ is set in the Schema so
        that .object_factory() can create an instance. 
    """

    @classmethod
    def __get_schema__(cls):
        """ get schema attached to class, and cached in cls.__schema. If not cached, instantiate .Schema """
        s = getattr(cls, "__schema", None)
        if s is None:
            sclass = getattr(cls, "Schema", None)
            if sclass is None:
                raise ValueError("Class must have Schema inner class")
            else:
                s = cls.__schema = sclass()  # instantiate
                s.__objclass__ = cls  # assign this class to schema.__objclass__
        return s


abc_schema.SchemedObject.register(SchemedObject)

class _MMSchemaMeta(mm.schema.SchemaMeta,type(abc_schema.AbstractSchema)):
    """ Combined meta class from Marshmallow and abc.ABCMeta, so we can inherit from both """
    ...



class MMSchema(mm.Schema,abc_schema.AbstractSchema,metaclass=_MMSchemaMeta):

    SupportedRepresentations = {
        abc_schema.WellknownRepresentation.python,
        abc_schema.WellknownRepresentation.json,
    }

    SupportsCallableIO:bool = True # callable input / output is supported

    def get_name(self) -> typing.Optional[str]:
        """ get name of Schema as the name of its __objclass__, if assigned. """
        c = getattr(self,'__objclass__',None)
        return c.__name__ if c else None
        

    def to_external(
        self,
        obj: SchemedObject,
        destination: abc_schema.WellknownRepresentation,
        writer_callback: typing.Optional[typing.Callable] = None,
        **params,
    ) -> typing.Optional[typing.Any]:
        """
            If *writer_callback* is None (the default), the external representation
            is returned as result.

            If *writer_callback* is not None, then it can be called any number
            of times with some arguments. No result is returned.

            (inspired by PEP-574 https://www.python.org/dev/peps/pep-0574/#producer-api)
        """
        supported = {
            abc_schema.WellknownRepresentation.json: self.dumps,
            abc_schema.WellknownRepresentation.python: self.dump,
        }
        
        self.check_supported_output(destination,writer_callback)
        method = supported[destination]
        e = method(obj, **params)
        if writer_callback:
            return writer_callback(e)
        else:
            return e

    def from_external(
        self,
        external: typing.Union[typing.Any, typing.Callable],
        source: abc_schema.WellknownRepresentation,
        **params,
    ) -> typing.Union[SchemedObject, typing.Dict[typing.Any, typing.Any]]:

        """
            If *external* is bytes, they are consumed as source representation.

            If *external* is a Callable, then it can be called any number
            of times with some arguments to obtain parts of the source representation.

        """
        supported = {
            abc_schema.WellknownRepresentation.json: self.loads,
            abc_schema.WellknownRepresentation.python: self.load,
        }
        self.check_supported_input(source,external)
        method = supported[source]
        if callable(external):
            external = external(None)
        d = method(external, **params)
        o = self.object_factory(d)

        return o

    def validate_internal(self, obj: SchemedObject, **params) -> SchemedObject:
        """ Marshmallow doesn't provide validation on the object - we need to dump it.
            As Schema.validate returns a dict, but we want an error raised, we call .load() instead.
            However, if the validation doesn't raise an error, we return the argument obj unchanged. 
        """
        dummy = self.load(self.dump(obj))  # may raise an error
        return obj

    def __iter__(self)  -> mm.fields.FieldABC:
        """ iterator through SchemaElements in this Schema, sett """
        for name, field in self._declared_fields.items():
            field.name = name
            yield field

##    def as_annotations(self,include_extras: bool = False) -> typing.Dict[str, typing.Type]:
##        """ return Schema Elements in annotation format.
##            Need to define in MMSchema, as MMSchema does not inheritc from AbstractSchema.
##        """
##        return {se.get_name(): se.get_annotated() if include_extras else se.get_python_type() for se in self}

    def object_factory(self, d: dict) -> typing.Union[SchemedObject, dict]:
        """ return an object from dict, according to the Schema's __objclass__ """
        objclass = getattr(self, "__objclass__", None)
        if objclass:
            o = objclass(**d)  # factory!
        else:
            o = d
        return o


    def get_metadata(self) -> typing.MutableMapping[str, typing.Any]:
        """ return metadata (aka payload data) for this Schema.
            Meta data is not used at all by the Schema, and is provided as a third-party 
            extension mechanism. Multiple third-parties can each have their own key, 
            to use as a namespace in the metadata (similar to and taken from dataclasses.Field)
        """
        return self.context

    @classmethod
    def from_schema(cls, schema: abc_schema.AbstractSchema) -> "MMSchema":
        """ Create a new Marshmallow Schema from a schema in any Schema Dialect.
            Unfortunately, Marshmallow has no API to add fields, so we use internal APIs. 
            See https://github.com/marshmallow-code/marshmallow/issues/1201.
        """
        s = MMSchema(context=schema.get_metadata())  # base Schema
        # add fields
        s.declared_fields = {
            element.get_name(): mm.fields.Field.from_schema_element(element)
            for element in schema
        }
        s._init_fields()  # invoke internal API to bind fields 
        return s

    def add_element(self, element: abc_schema.AbstractSchemaElement):
        """ Add a Schema element to this Schema.
            We're afraid to use internal API to add additional fields.
            See https://github.com/marshmallow-code/marshmallow/issues/1201.
            This API is optional, after all.
        """
        raise NotImplementedError("Marshmallow API doesn't support adding fields")


abc_schema.AbstractSchema.register(MMSchema)

""" Methods for Marshmallow fields (will be monkey-patched) """


class MMfieldSuper(abc_schema.AbstractSchemaElement):


    FieldType_to_PythonType: typing.Dict[mm.fields.FieldABC, typing.Type] = {
        # fmt: off
        mm.fields.Integer:          int,
        mm.fields.Float:            float,
        mm.fields.Decimal:          decimal.Decimal,
        mm.fields.Boolean:          bool,
        mm.fields.Email:            str,    
        mm.fields.Str:              str, # least specific last
        mm.fields.DateTime:         datetime.datetime,
        mm.fields.Time:             datetime.time,
        mm.fields.Date:             datetime.date,
        mm.fields.TimeDelta:        datetime.timedelta,
        mm.fields.Mapping:          typing.Mapping,
        mm.fields.Dict:             typing.Dict,
        # fmt: on
    }

    # reverse list, least specific overwrites most specific:
    PythonType_to_FieldType = {pt: ft for ft, pt in FieldType_to_PythonType.items()}

    # Types from typing have a _name field - I found no other way to determine what typing.Dict actually is:
    TypingName_to_FieldType: typing.Dict[str, mm.fields.FieldABC] = {
        # fmt: off
        'Dict':                     mm.fields.Dict,
        # fmt: on
    }

    def get_schema(self) -> typing.Optional["MMSchema"]:
        """ return the Schema or None """
        return self.root


    def get_name(self) -> str:
        return self.name


    def get_python_type(self) -> typing.Type:
        """ get native type of field. 

        """
        return self.FieldType_to_PythonType.get(self.__class__, typing.Type[typing.Any])

    def get_annotation(self) -> abc_schema.SchemaTypeAnnotation:
        """ get SchemaTypeAnnotation  """ 
        default = abc_schema.MISSING if self.missing is mm.missing else self.missing
        return abc_schema.SchemaTypeAnnotation(required=self.required,default=default,metadata=self.get_metadata())


    ##def get_python_field(self) -> dataclasses.Field:
    ##    """ REMOVE
    ##        get Python dataclasses.Field corresponding to SchemaElement.
    ##        Fills default if provided in field. If field is not required and there is no default, make type Optional.
    ##    """
    ##    pytype = self.get_python_type()
    ##    # mm.missing -> dataclasses.MISSING>
    ##    default = dataclasses.MISSING if self.missing is mm.missing else self.missing
    ##    
    ##    if (not self.required) and default is dataclasses.MISSING:
    ##        pytype = typing.Optional[pytype]  # type: ignore # I don't understand mypy's problem here!
    ##    dcfield = dataclasses.field(default=default, metadata=self.get_metadata())
    ##    dcfield.type = pytype
    ##    return dcfield


    def get_metadata(self) -> typing.Mapping[str, typing.Any]:
        """ return metadata (aka payload data) for this SchemaElement.
        """
        return self.metadata

    
    @classmethod
    def from_schema_element(
        cls, schema_element: abc_schema.AbstractSchemaElement
    ) -> mm.fields.Field:
        """ Classmethod: Create a new Marshmallow Field from
            a AbstractSchemaElement in any Schema Dialect.

            In a real implementation, we could return schema_element unchanged
            if isinstance(schema_element,mm.fields.Field). However, we only
            rely on the protocol API here. 

        """
        ann = schema_element.get_annotation()
        pt = schema_element.get_python_type()
        mmf = cls.from_python_type(pt, ann.required, ann.default, ann.metadata)
        if mmf:
            return mmf
        else:
            raise ValueError(
                f"Cannot determine Marshmallow field for {schema_element}"
            )


    @classmethod
    def from_python_type(cls, 
        pt: type, required: bool = True, default: typing.Any = dataclasses.MISSING, metadata: typing.Mapping[str, typing.Any] = None
    ) -> typing.Optional[mm.fields.Field]:
        """ Create a new Marshmallow Field from a python type, either type, class, or typing.Type.
            We first check the special _name convention for typing.Type, 
            then check whether the FieldType has a _type_factory or is constructed by its class.
        """
        pt_name = getattr(pt, "_name", None)
        if pt_name:
            field_class = cls.TypingName_to_FieldType.get(pt_name)
        else:
            field_class = None
        if not field_class:
            field_class = cls.PythonType_to_FieldType.get(pt)
            if not field_class:
                return None

        if default is abc_schema.MISSING:  # convert abc_schema.MISSING ->  mm.missing
            default = mm.missing

        type_factory = getattr(field_class, "_type_factory", None)
        if type_factory:
            mmf = type_factory(pt, required=required, default=default, metadata=metadata)
        else:
            mmf = field_class(
                required=required, missing=default, default=default, metadata=metadata
            )
        return mmf


# monkey-patch Field by adding superclass:
mm.fields.Field.__bases__ += (MMfieldSuper,)




class MMmappingSuper(abc_schema.AbstractSchemaElement):

    def get_python_type(self) -> type:
        """ get native classes of containers and build Dict type
            Simplified - either container is a Field, or we use Any.
        """
        kt = (
            self.key_field.get_python_type()
            if isinstance(self.key_field, mm.fields.FieldABC)
            else typing.Type[typing.Any]
        )
        vt = (
            self.value_field.get_python_type()
            if isinstance(self.value_field, mm.fields.FieldABC)
            else typing.Type[typing.Any]
        )
        return typing.Mapping[kt, vt]  # type: ignore # mypy cannot handle this dynamic typing without a plugin!

    @classmethod
    def type_factory(
        cls, pt: typing.Type, required: bool, default: typing.Any, metadata: dict
    ) -> mm.fields.Field:
        """ get MM fields.Dict from Python type. 
            get key class and value class (both can be None), then construct Dict.
        """
        kc = cls.from_python_type(pt.__args__[0])
        vc = cls.from_python_type(pt.__args__[1])
        return cls(
            keys=kc, values=vc, required=required, missing=default, default=default, metadata=metadata
        )

# monkey-patch Mapping by adding superclass:
mm.fields.Mapping.__bases__ += (MMmappingSuper,)

