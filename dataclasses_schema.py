""" ABC Dataclasses Schema examples """
import abc_schema
import dataclasses
import datetime
import typing
import typing_extensions






class DCSchema(abc_schema.AbstractSchema):

    def __init__(self,dataclass):
        self.dataclass = dataclass
        

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
            If *writer_callback* is None (the default), the external representation
            is returned as result.

            If *writer_callback* is not None, then it can be called any number
            of times with some arguments. No result is returned.

            (inspired by PEP-574 https://www.python.org/dev/peps/pep-0574/#producer-api)
        """
        pass


    def from_external(
        self,
        external: typing.Union[typing.Any, typing.Callable],
        source: abc_schema.WellknownRepresentation,
        **params,
    ) -> abc_schema.SchemedObject:

        """
            If *external* is bytes, they are consumed as source representation.

            If *external* is a Callable, then it can be called any number
            of times with some arguments to obtain parts of the source representation.

        """
        pass


    def validate_internal(self, obj: abc_schema.SchemedObject, **params) -> abc_schema.SchemedObject:
        pass


    def __iter__(self) -> typing.Iterator['DCSchemaElement']:
        """ iterator through SchemaElements in this Schema """

        for name,field in self.dataclass.__dataclass_fields__.items():
            ann = abc_schema.SchemaTypeAnnotation(required=True,default=None) # XXX
            yield DCSchemaElement(self,name,field.type,ann,field.metadata)
            

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
    def from_schema(cls, schema: abc_schema.AbstractSchema) -> "DCSchema":
        """ Optional API: create a new DCSchema from
            a schema in any Schema Dialect.
        """
        pass


    def add_element(self, element: "DCSchemaElement"):
        """ Optional API: Add a Schema element (in any Schema Dialect) to this Schema. 
        """
        pass



            
            
class DCSchemaElement(abc_schema.AbstractSchemaElement):
    """ Holds one SchemaElement of a Schema. No represenation is prescribed, hence there is no constructor.
        The SchemaTypeAnnotation, however, prescribes a representation. It can either be attached to the 
        SchemaElement, or generated from it when queried by .get_annotation(). 
    """

    def __init__(self,schema,name,type,ann,meta):
        self.schema = schema
        self.name = name
        self.type = type
        self.ann = ann
        self.meta = meta

    def get_schema(self) -> DCSchema:
        """ get associated schema or None """
        return self.schema

    def get_name(self) -> str:
        """ get name useable as variable name """
        return self.name

    def get_python_type(self) -> type:
        """ get Python type of this AbstractSchemaElement """
        return self.type


    def get_annotation(self) -> typing.Optional[abc_schema.SchemaTypeAnnotation]:
        """ Optional: get SchemaTypeAnnotation of this AbstractSchemaElement """
        return self.ann



    def get_metadata(self) -> typing.Mapping[str, typing.Any]:
        """ return metadata (aka payload data) for this SchemaElement.

            Metadata is not used at all by the Schema, and is provided as a third-party 
            extension mechanism. Multiple third-parties can each have their own key, 
            to use as a namespace in the metadata.
            (similar to and taken from dataclasses.Field)

            Can be refined; by default an empty dict is returned.
        """
        return self.meta

    @classmethod
    def from_schema_element(
        cls, schema_element: abc_schema.AbstractSchemaElement
    ) -> 'DCSchemaElement':
        """ create a new DCSchemaElement from
            a AbstractSchemaElement in any Schema Dialect.
        """
        ann = schema_element.get_annotated()
        default = dataclasses.MISSING if ann.default is abc_schema.MISSING else ann.default # switch our MISSING to dataclasses.MISSING
        dcfield = dataclasses.field(default=default,metadata=self.get_metadata())
        dcfield.type = self.get_python_type()
        return dcfield


    def get_annotated(self) -> type:
        """ get PEP-593 typing.Annotated type """
        return typing_extensions.Annotated[self.type,self.ann]

   


@dataclasses.dataclass
class InventoryItem:
    """ Class for keeping track of an item in inventory. """
    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand

s = DCSchema.get_schema(InventoryItem)
s.as_annotations(include_extras=True)