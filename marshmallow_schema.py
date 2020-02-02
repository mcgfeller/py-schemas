""" Marshmallow based conformant Schema.
    Marshmallow fields handling is coded in a mixin class, which is monkey-patched as a base class of the Marshmallow Field class.
    This allows to control the behavior of all fields, without trating them individually. 
    The Marshmallow schema is subclassed. 
"""

import marshmallow as mm  # type: ignore
import decimal
import datetime
import abc_schema
import typing
import typing_extensions


class SchemedObject(abc_schema.SchemedObject):
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


class _MMSchemaMeta(mm.schema.SchemaMeta, abc_schema.abc.ABCMeta):
    """ Combined meta class from Marshmallow and abc.ABCMeta, so we can inherit from both """
    ...


class MMSchema(mm.Schema, abc_schema.AbstractSchema, metaclass=_MMSchemaMeta):
    """ Marshmallow Schema, supporting the AbstracSchema protocol. 
    """

    SupportedRepresentations = {
        abc_schema.WellknownRepresentation.python,
        abc_schema.WellknownRepresentation.json,
    }

    SupportsCallableIO = True  # callable input / output is supported

    def get_name(self) -> typing.Optional[str]:
        """ get name of Schema as the name of its __objclass__, if assigned. """
        c = getattr(self, "__objclass__", None)
        return c.__name__ if c else None

    def to_external(
        self,
        obj: abc_schema.SchemedObject,
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

        self.check_supported_output(destination, writer_callback)
        method = supported[destination]
        try:  # translate error
            e = method(obj, **params)
        except mm.exceptions.ValidationError as verror:
            raise abc_schema.ValidationError(str(verror), original_error=verror)
        if writer_callback:
            return writer_callback(e)
        else:
            return e

    def from_external(
        self,
        external: typing.Union[typing.Any, typing.Callable],
        source: abc_schema.WellknownRepresentation,
        **params,
    ) -> typing.Union[abc_schema.SchemedObject, typing.Dict[typing.Any, typing.Any]]:
        """
            If *external* is bytes, they are consumed as source representation.

            If *external* is a Callable, then it can be called any number
            of times with some arguments to obtain parts of the source representation.

        """
        supported = {
            abc_schema.WellknownRepresentation.json: self.loads,
            abc_schema.WellknownRepresentation.python: self.load,
        }
        self.check_supported_input(source, external)
        method = supported[source]

        if callable(external):
            external = external(None)
        elif hasattr(external, "__dict__"):  # Python export may yield object
            external = external.__dict__

        try:  # translate error        
            d = method(external, **params)
        except mm.exceptions.ValidationError as verror:
            raise abc_schema.ValidationError(str(verror), original_error=verror)
        o = self.object_factory(d)

        return o

    def validate_internal(
        self, obj: abc_schema.SchemedObject, **params
    ) -> SchemedObject:
        """ Marshmallow doesn't provide validation on the object - we need to dump it.
            We want conversion of values, such as Bool alternatives, so we dump/load and reapply the object_factory.
            Validation errors are raised.
        """
        try:  # translate error
            d = self.load(self.dump(obj))  # may raise an error
        except mm.exceptions.ValidationError as verror:
            raise abc_schema.ValidationError(str(verror), original_error=verror)
        obj = self.object_factory(d)  # we have to re-convert to an object
        return obj

    def __iter__(self) -> typing.Iterator[mm.fields.Field]:
        """ iterator through SchemaElements in this Schema, sets field.name """
        for name, field in self.declared_fields.items():
            field.name = name
            yield field

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
        """
        return self.context

    @classmethod
    def from_schema(cls, schema: abc_schema.AbstractSchema) -> "MMSchema":
        """ Create a new Marshmallow Schema from a schema in any Schema Dialect.
            Unfortunately, Marshmallow has no API to add fields, so we use internal APIs. 
            See https://github.com/marshmallow-code/marshmallow/issues/1201.
        """
        s = MMSchema(context=schema.get_metadata())  # base Schema
        s.__objclass__ = schema.__objclass__  # obj class is same
        # iterate through fields and add the to our schema's declared_fields:
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


class MMfieldSuper(abc_schema.AbstractSchemaElement):
    """ Mixin class (for monkey-patching base class so we don't have to reinherit all Fields """

    FieldType_to_PythonType: typing.Dict[mm.fields.FieldABC, typing.Type] = {
        # fmt: off
        mm.fields.Integer:          int,
        mm.fields.Float:            float,
        mm.fields.Decimal:          decimal.Decimal,
        mm.fields.Boolean:          bool,
        mm.fields.Email:            str,    
        mm.fields.Str:              str, # least specific last for reversal below
        mm.fields.DateTime:         datetime.datetime,
        mm.fields.Time:             datetime.time,
        mm.fields.Date:             datetime.date,
        mm.fields.TimeDelta:        datetime.timedelta,
        mm.fields.Mapping:          typing.Mapping,
        mm.fields.Dict:             typing.Dict,
        mm.fields.List:             typing.List,
        # fmt: on
    }

    # reverse list, least specific overwrites most specific:
    PythonType_to_FieldType = {pt: ft for ft, pt in FieldType_to_PythonType.items()}

    # Types from typing have an __origin__ field of the underlying class (as typing.Dict[x,y] reveal typing.Dict):
    PythonType_to_FieldType.update({
        # fmt: off
        dict:                       mm.fields.Dict,
        list:                       mm.fields.List,
        # fmt: on
        })

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
        default = abc_schema.MISSING if self.missing is mm.missing else self.missing # convert missing
        return abc_schema.SchemaTypeAnnotation(
            required=self.required, default=default, metadata=self.get_metadata(),
            validate_internal= None
        )

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
            raise ValueError(f"Cannot determine Marshmallow field for {schema_element}")

    @classmethod
    def from_python_type(
        cls,
        pt: type,
        required: bool = True,
        default: typing.Any = mm.missing,
        metadata: typing.Mapping[str, typing.Any] = None,
    ) -> typing.Optional[mm.fields.Field]:
        """ Create a new Marshmallow Field from a python type, either type, class, or typing.Type.
            We first check the special __origin__ convention for typing.Type to reveal its base type,
            then check whether the FieldType has a _type_factory or is constructed by its class.
        """
        basetype = typing.get_origin(pt) or pt  # typing type.__origin__ is Python class
        field_class = cls.PythonType_to_FieldType.get(basetype)
        if not field_class:
            return None

        if default is abc_schema.MISSING:  # convert abc_schema.MISSING ->  mm.missing
            default = mm.missing

        type_factory = getattr(field_class, "_type_factory", None)
        if type_factory:
            mmf = type_factory(
                pt, required=required, default=default, metadata=metadata
            )
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
        return typing.Dict[
            kt, vt
        ]  # type: ignore # mypy cannot handle this dynamic typing without a plugin!

    @classmethod
    def _type_factory(
        cls, pt: typing.Type, required: bool, default: typing.Any, metadata: dict
    ) -> mm.fields.Field:
        """ get MM fields.Dict from Python type. 
            get key class and value class (both can be None), then construct Dict.
        """
        kc = cls.from_python_type(typing.get_args(pt)[0])
        vc = cls.from_python_type(typing.get_args(pt)[1])
        return cls(
            keys=kc,
            values=vc,
            required=required,
            missing=default,
            default=default,
            metadata=metadata,
        )


# monkey-patch Mapping by adding superclass:
mm.fields.Mapping.__bases__ = (MMmappingSuper,) + mm.fields.Mapping.__bases__


class MMlistSuper(abc_schema.AbstractSchemaElement):
    def get_python_type(self) -> type:
        """ get native classes of containers and build List type
            Simplified - either container is a Field, or we use Any.
        """
        vt = (
            self.inner.get_python_type()
            if isinstance(self.inner, mm.fields.FieldABC)
            else typing.Type[typing.Any]
        )
        return typing.List[
            vt
        ]  # type: ignore # mypy cannot handle this dynamic typing without a plugin!

    @classmethod
    def _type_factory(
        cls, pt: typing.Type, required: bool, default: typing.Any, metadata: dict
    ) -> mm.fields.Field:
        """ get MM fields.List from Python type. 
            get value class (can be None), then construct mm.fields.List.
        """
        vc = cls.from_python_type(typing.get_args(pt)[0])
        return cls(
            vc, required=required, missing=default, default=default, metadata=metadata
        )


# monkey-patch Mapping by adding superclass:
mm.fields.List.__bases__ = (MMlistSuper,) + mm.fields.List.__bases__

