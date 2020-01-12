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






class DCSchema(abc_schema.AbstractSchema):
    """ Schema for dataclasses: Light-weight, we just store a reference to the dataclass and
        re-create everything on the fly.
    """

    dataclass : type

    def __init__(self,dataclass):
        if dataclass and not dataclasses.is_dataclass(dataclass):
            raise TypeError(f'{dataclass} must be a dataclass')
        self.dataclass = dataclass

    def get_name(self) -> str:
        """ get name of Schema, which is the name of the dataclass """
        return self.dataclass.__name__
        

    @classmethod
    def get_schema(cls,dataclass) -> 'DCSchema':
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
        self.check_supported_output(destination,writer_callback)
        return self.validate_internal(obj,**params)



    def from_external(
        self,
        external: typing.Union[typing.Any, typing.Callable],
        source: abc_schema.WellknownRepresentation,
        **params,
    ) -> abc_schema.SchemedObject:

        """
            Dataclasses only support validation, so from_external is the same as internal_validation(). 

        """
        self.check_supported_input(source,external)
        return self.validate_internal(external,**params)


    def validate_internal(self, obj: abc_schema.SchemedObject, **params) -> abc_schema.SchemedObject:
        for element in self:
            ann = element.get_annotation()
            name = element.get_name()
            nobj = abc_schema.SchemaTypeAnnotation.validate_internal(ann,element,getattr(obj,name,None))
            if obj is not nobj:
                setattr(obj,name,nobj)
        return obj


    def __iter__(self) -> typing.Iterator['DCSchemaElement']:
        """ iterator through SchemaElements in this Schema """

        for field in dataclasses.fields(self.dataclass):
            yield DCSchemaElement(self,field)
            

    def as_annotations(self,include_extras: bool = False) -> typing.Dict[str, typing.Type]:
        """ return Schema Elements in annotation format.
            If include_extras (PEP-593) is True, the types returned are typing.Annotated types.

            Use as class.__annotations__ = schema.as_annotations()
            I would wish that __annotations__ is a protocol that can be provided,
            instead of simply assuming it is a mapping. 
        """
        return {se.get_name(): se.get_annotated() if include_extras else se.get_python_type() for se in self}


    def get_metadata(self) -> typing.Mapping[str, typing.Any]:
        """ return metadata (aka payload data) for this Schema.

            Meta data is not used at all by the Schema, and is provided as a third-party 
            extension mechanism. Multiple third-parties can each have their own key, 
            to use as a namespace in the metadata.
            (similar to and taken from dataclasses.Field)

            Can be refined; by default an empty dict is returned.

            There is a similar method defined on the AbstractSchemaElement for
            smetadata attached to a schema element. 
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
            field = DCSchemaElement.from_schema_element(element,parent_schema=dcschema).field
            fields.append((field.name,field.type,field))
            
        name = schema.get_name() or f'dc_{id(schema)}'
        dcschema.dataclass = dataclasses.make_dataclass(name, fields, namespace={'get_schema': lambda self,dcschema=dcschema:dcschema}, **kw) 
        return dcschema




            
            
class DCSchemaElement(abc_schema.AbstractSchemaElement):
    """ Holds one SchemaElement of a Schema. No represenation is prescribed, hence there is no constructor.
        The SchemaTypeAnnotation, however, prescribes a representation. It can either be attached to the 
        SchemaElement, or generated from it when queried by .get_annotation(). 
    """

    def __init__(self,schema : DCSchema,field : dataclasses.Field):
        if not isinstance(schema,DCSchema):
            raise TypeError(f'{schema} must be a DCSchema')
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
        """ get SchemaTypeAnnotation of this DCSchemaElement """
        default = self.field.default # substitute dataclass field missing with our missing
        if default is dataclasses.MISSING: 
            if self.field.default_factory is dataclasses.MISSING:
                default = abc_schema.MISSING
            else:
                default = self.field.default_factory

        return abc_schema.SchemaTypeAnnotation(required=default is abc_schema.MISSING,default=default,metadata=self.field.metadata)



    def get_metadata(self) -> typing.Mapping[str, typing.Any]:
        """ return metadata (aka payload data) for this SchemaElement.
        """
        return self.field.metadata

    @classmethod
    def from_schema_element(
        cls, schema_element: abc_schema.AbstractSchemaElement, parent_schema : DCSchema
    ) -> 'DCSchemaElement':
        """ create a new DCSchemaElement from
            a AbstractSchemaElement in any Schema Dialect.
            We create a dataclasses.Field and then wrap it within a DCSchemaElement.
        """
        ann = schema_element.get_annotation()
        default = dataclasses.MISSING if ann.default is abc_schema.MISSING else ann.default # switch our MISSING to dataclasses.MISSING
        if callable(default): # callables goes into default_factory for fields.
            default_factory = default
            default =  dataclasses.MISSING
        else:
            default_factory = dataclasses.MISSING
        # Make a dataclasses Field:
        dcfield = dataclasses.field(default=default,default_factory=default_factory, metadata=schema_element.get_metadata())
        dcfield.name = schema_element.get_name()
        dcfield.type = schema_element.get_python_type()
        return cls(parent_schema,dcfield)


    def get_annotated(self) -> type:
        """ get PEP-593 typing.Annotated type """
        return typing_extensions.Annotated[self.get_python_type(),self.get_annotation()]

