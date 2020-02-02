""" Dataclasses Schema: dataclasses provide some automation based
    on instance type declarations in a class. There is no runtime validation
    except for argument presence.
"""
import abc
import abc_schema
import dataclasses
import datetime
import typing
import typing_extensions
import types


class DCSchema(abc_schema.AbstractSchema):
    """ Schema for dataclasses: Light-weight, we just store a reference to the dataclass in __objclass__ and
        re-create everything on the fly.
    """

    def __init__(self, dataclass):
        if dataclass and not dataclasses.is_dataclass(dataclass):
            raise TypeError(f"{dataclass} must be a dataclass")
        self.__objclass__ = dataclass  # assign dataclass to schema.__objclass__

    def get_name(self) -> str:
        """ get name of Schema, which is the name of the dataclass """
        return self.__objclass__.__name__

    @classmethod
    def get_schema(cls, dataclass) -> "DCSchema":
        """ create DCSchema from dataclass """
        return cls(dataclass)

    def to_external(
        self,
        obj: abc_schema.SchemedObject,
        destination: abc_schema.WellknownRepresentation,
        writer_callback: typing.Optional[typing.Callable] = None,
        **params,
    ) -> typing.Optional[typing.Any]:
        """
            Dataclasses only support validation, so to_external is the same as internal_validation(). 
        """
        self.check_supported_output(destination, writer_callback)
        return self.validate_internal(obj, **params)

    def from_external(
        self,
        external: typing.Union[typing.Any, typing.Callable],
        source: abc_schema.WellknownRepresentation,
        **params,
    ) -> abc_schema.SchemedObject:
        """
            Dataclasses only support validation, so from_external is identical to internal_validation()

        """
        self.check_supported_input(source, external)
        return self.validate_internal(external, **params)

    def validate_internal(
        self, obj: abc_schema.SchemedObject, **params
    ) -> abc_schema.SchemedObject:
        """ Perform validation by iterating over elements and
            calling SchemaTypeAnnotation.validate_internal
        """
        d = (
            obj.__dict__ if hasattr(obj, "__dict__") else obj
        )  # Python export may yield object
        for element in self:
            ann = element.get_annotation()
            name = element.get_name()
            newd = ann.validate_internal(
                ann, element, d.get(name, dataclasses.MISSING)
            )
            if newd is not dataclasses.MISSING:
                d[name] = newd

        obj = self.__objclass__(**d)  # instantiate object
        return obj

    def __iter__(self) -> typing.Iterator["DCSchemaElement"]:
        """ iterator through SchemaElements in this Schema """

        for field in dataclasses.fields(self.__objclass__):
            yield DCSchemaElement(self, field)

    def get_metadata(self) -> typing.Mapping[str, typing.Any]:
        """ Dataclasses have no metadata per Scheme, so return empty {}.
        """
        return {}

    @classmethod
    def from_schema(cls, schema: abc_schema.AbstractSchema, **kw: dict) -> "DCSchema":
        """ create a new DCSchema from
            a schema in any Schema Dialect.
        """
        dcschema = cls(None)
        fields = []
        for element in schema:
            field = DCSchemaElement.from_schema_element(
                element, parent_schema=dcschema
            ).field
            fields.append((field.name, field.type, field))

        # dataclasses fields with defaults must be ordered after those without, because the dataclass
        # contructor works with keyword arguments for defaults:
        fields = sorted(fields, key=lambda t: t[2].default is not dataclasses.MISSING)

        name = schema.get_name() or f"dc_{id(schema)}"
        dcschema.__objclass__ = dataclasses.make_dataclass(
            name,
            fields,
            namespace={"get_schema": lambda self, dcschema=dcschema: dcschema},
            **kw,
        )
        return dcschema


class DCSchemaElement(abc_schema.AbstractSchemaElement):
    """ Holds one SchemaElement of a Schema. No represenation is prescribed, hence there is no constructor.
        The SchemaTypeAnnotation, however, prescribes a representation. It can either be attached to the 
        SchemaElement, or generated from it when queried by .get_annotation(). 
    """
    Ann_meta_key:str = 'SchemaTypeAnnotation' # key of annotation in meta dict

    def __init__(self, schema: DCSchema, field: dataclasses.Field):
        if not isinstance(schema, DCSchema):
            raise TypeError(f"{schema} must be a DCSchema")
        self.schema = schema
        self.field = field

    def get_schema(self) -> DCSchema:
        """ get associated schema or None """
        return self.schema

    def get_name(self) -> str:
        """ get name useable as variable name """
        return self.field.name

    def get_python_type(self) -> type:
        """ get Python type of this AbstractSchemaElement """
        return self.field.type

    def get_annotation(self) -> abc_schema.SchemaTypeAnnotation:
        """ get SchemaTypeAnnotation of this DCSchemaElement.
            Get it from metadata, if available, else compute and cache.
        """
        ann = self.field.metadata.get(self.Ann_meta_key)
        if not ann:
            default = (
                self.field.default
            )  # substitute dataclass field missing with our missing
            if default is dataclasses.MISSING:
                if self.field.default_factory is dataclasses.MISSING:
                    default = abc_schema.MISSING
                else:
                    default = self.field.default_factory

            ann = abc_schema.SchemaTypeAnnotation(
                required=default is abc_schema.MISSING,
                default=default,
                metadata=self.field.metadata,
            )
            metadata = self._ensure_updateable(self.get_metadata())
            metadata[self.Ann_meta_key] = ann # cache ann
            self.field.metadata = metadata
        return ann

    def get_metadata(self) -> typing.Mapping[str, typing.Any]:
        """ return metadata (aka payload data) for this SchemaElement.
        """
        return self.field.metadata

    @staticmethod
    def _ensure_updateable(d : typing.Mapping) -> typing.Dict:
        """ ensure d is updatable, even if is a MappingProxy """
        if isinstance(d,types.MappingProxyType):
            # d is a mappingproxy, which cannot be updated
            d = d.copy() # but copied
        return d
 

    @classmethod
    def from_schema_element(
        cls, schema_element: abc_schema.AbstractSchemaElement, parent_schema: DCSchema
    ) -> "DCSchemaElement":
        """ create a new DCSchemaElement from
            a AbstractSchemaElement in any Schema Dialect.
            We create a dataclasses.Field and then wrap it within a DCSchemaElement.
        """
        ann = schema_element.get_annotation()
        default = (
            dataclasses.MISSING if ann.default is abc_schema.MISSING else ann.default
        )  # switch our MISSING to dataclasses.MISSING
        if callable(default):  # callables goes into default_factory for fields.
            default_factory = default
            default = dataclasses.MISSING
        else:
            default_factory = dataclasses.MISSING

        metadata = cls._ensure_updateable(schema_element.get_metadata())
        metadata[cls.Ann_meta_key] = ann
        # Make a dataclasses Field:
        dcfield = dataclasses.field(
            default=default,
            default_factory=default_factory,
            metadata=metadata,
        )
        dcfield.name = schema_element.get_name()
        dcfield.type = schema_element.get_python_type()
        return cls(parent_schema, dcfield)
