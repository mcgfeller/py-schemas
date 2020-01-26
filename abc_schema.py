""" Protocol for Schema """

import abc
import typing
import typing_extensions
import collections.abc
import enum
import dataclasses

NotAvailable = NotImplementedError('method not available in this class')


class SchemedObject(metaclass=abc.ABCMeta):
    """ An object with a Schema, supporting the __get_schema__ method.
    """

    @classmethod
    @abc.abstractmethod
    def __get_schema__(cls) -> "AbstractSchema":
        pass


class WellknownRepresentation(enum.Enum):

    # fmt: off
    python  = "__python__"  # internal python structures
    pickle  = "application/python-pickle"
    json    = "application/json"
    xml     = "application/xml"
    sql     = "application/sql"
    html    = "text/html"
    # fmt: on


class AbstractSchema(collections.abc.Iterable):
    """ The AbstractSchema does not prescribe how the Schema is organized, and
        only prescribes that the AbstractSchemaElement may be obtained by iterating
        over the Schema.
    """

    SupportedRepresentations: typing.ClassVar[typing.Set["WellknownRepresentation"]] = {
        WellknownRepresentation.python
    }

    SupportsCallableIO:bool = False # must be overwritten if callable input / output is supported

    def get_name(self) ->typing.Optional[str]:
        """ get name of Schema or None """
        return getattr(self,'name',None)

    @abc.abstractmethod
    def to_external(
        self,
        obj: SchemedObject,
        destination: WellknownRepresentation,
        writer_callback: typing.Optional[typing.Callable] = None,
        **params,
    ) -> typing.Optional[typing.Any]:
        """ Method to convert a Python structure to the destination 

            If *writer_callback* is None (the default), the external representation
            is returned as result.

            If *writer_callback* is not None, then it can be called any number
            of times with some arguments. No result is returned.

            (inspired by PEP-574 https://www.python.org/dev/peps/pep-0574/#producer-api)
        """
        self.check_supported_output(destination,writer_callback)
        pass

    @abc.abstractmethod
    def from_external(
        self,
        external: typing.Union[typing.Any, typing.Callable],
        source: WellknownRepresentation,
        **params,
    ) -> SchemedObject:

        """
            If *external* is bytes, they are consumed as source representation.

            If *external* is a Callable, then it can be called any number
            of times with some arguments to obtain parts of the source representation.

        """
        self.check_supported_input(source,external)
        pass

    @abc.abstractmethod
    def validate_internal(self, obj: SchemedObject, **params) -> SchemedObject:
        pass
            

    @classmethod
    def check_supported_input(cls,source : WellknownRepresentation, external: typing.Union[typing.Any, typing.Callable]):
        """ check whether representation is supported, raise an error otherwise """
        if source not in cls.SupportedRepresentations:
            raise NotImplementedError(f"Input representation {source} not supported; choose one of {', '.join([str(r) for r in cls.SupportedRepresentations])}")
        if not cls.SupportsCallableIO and callable(external):
            raise NotImplementedError(f"Callable input not supported by {cls.__name__}")
            
        return
    @classmethod
    def check_supported_output(cls,destination : WellknownRepresentation, writer_callback: typing.Optional[typing.Callable] = None):
        """ check whether representation is supported, raise an error otherwise """
        if destination not in cls.SupportedRepresentations:
            raise NotImplementedError(f"Input representation {destination} not supported; choose one of {', '.join([str(r) for r in cls.SupportedRepresentations])}")
        if not cls.SupportsCallableIO and writer_callback is not None:
            raise NotImplementedError(f"Callable output not supported by {cls.__name__}")
            
        return



    @abc.abstractmethod
    def __iter__(self) -> typing.Iterator["AbstractSchemaElement"]:
        """ iterator through SchemaElements in this Schema """
        pass

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
    @abc.abstractmethod
    def from_schema(cls, schema: "AbstractSchema") -> "AbstractSchema":
        """ Create a new Schema (in the Schema dialect of the cls) from
            a schema in any Schema Dialect.
        """
        pass

    def add_element(self, element: "AbstractSchemaElement") -> "AbstractSchemaElement":
        """ Optional API: Add a Schema element (in any Schema Dialect) to this Schema
            and returns the created element. 
        """
        raise NotAvailable


class AbstractSchemaElement(metaclass=abc.ABCMeta):
    """ Holds one SchemaElement of a Schema. No represenation is prescribed, hence there is no constructor.
        The SchemaTypeAnnotation, however, prescribes a representation. It can either be attached to the 
        SchemaElement, or generated from it when queried by .get_annotation(). 
    """
    @abc.abstractmethod
    def get_schema(self) -> typing.Optional[AbstractSchema]:
        """ get associated schema or None """
        pass

    @abc.abstractmethod
    def get_name(self) -> str:
        """ get name useable as variable name """
        pass

    @abc.abstractmethod
    def get_python_type(self) -> type:
        """ get Python type of this AbstractSchemaElement """
        pass

    @abc.abstractmethod
    def get_annotation(self) -> typing.Optional['SchemaTypeAnnotation']:
        """ Optional: get SchemaTypeAnnotation of this AbstractSchemaElement """
        return



    def get_metadata(self) -> typing.Mapping[str, typing.Any]:
        """ return metadata (aka payload data) for this SchemaElement.

            Metadata is not used at all by the Schema, and is provided as a third-party 
            extension mechanism. Multiple third-parties can each have their own key, 
            to use as a namespace in the metadata.
            (similar to and taken from dataclasses.Field)

            Can be refined; by default an empty dict is returned.
        """
        return {}

    @classmethod
    @abc.abstractmethod
    def from_schema_element(
        cls, schema_element: "AbstractSchemaElement", parent_schema: typing.Optional[AbstractSchema] = None,
    ) -> "AbstractSchemaElement":
        """ Optional API: create a new AbstractSchemaElement (in the Schema dialect of the cls) from
            a AbstractSchemaElement in any Schema Dialect.
            parent_schema is the new schema parent of the element. 
        """
        pass


    def get_annotated(self) -> type:
        """ get PEP-593 typing.Annotated type """
        return typing_extensions.Annotated[self.get_python_type(),self.get_annotation()]

    # TODO:USE?
    @staticmethod
    def split_annotated(annotated : type) -> typing.Tuple[type,typing.Optional['SchemaTypeAnnotation']]:
        """ from a typing.Annotated, return tuple of (type,annotation)
            Note that there may be multiple Annotations, we take the first one that is a SchemaTypeAnnotation.
        """ 
        pt = annotated.__args__[0]
        # 1st SchemaTypeAnnotation, or None:
        ann = next((a for a in annotated.__metadata__ if isinstance(a,SchemaTypeAnnotation)),None) 
        return pt,ann

class _MISSING_TYPE:
    """ A sentinel object to detect if a parameter is supplied or not.  Use a class to give it a better repr. """
    def __repr__(self):
        return 'MISSING'
MISSING = _MISSING_TYPE()


class SchemaTypeAnnotation:
    """ Annotation holding SchemaElement typing information to go as 2nd parameter into typing_extensions.Annotated.
        Unlike the AbstractSchemaElement, the SchemaTypeAnnotation is concrete and prescribes a minimal representation.
        
    """

    def __init__(self,required : bool=False ,default : typing.Any=MISSING,
        to_external: typing.Optional[typing.Callable] =None, 
        from_external: typing.Optional[typing.Callable] =None, 
        validate_internal: typing.Optional[typing.Callable] =None,                 
        metadata: typing.Mapping[str, typing.Any] = {}):
        """ SchemaTypeAnnotation 
            default is the internal form of the default value, or MISSING
            from_external, to_external and validate_internal are callables with signature of the methods below, which they overwrite.
        """
        self.required = required
        self.default = default
        if to_external is not None: 
            self.to_external = to_external
        if from_external is not None:
            self.from_external = from_external
        if validate_internal is not None:
            self.validate_internal = validate_internal
        self.metadata = metadata

    def __repr__(self):
        return f'{self.__class__.__name__}(required={self.required}, default={self.default})'


    @staticmethod # can be overritten by passing a function to the constructor
    def to_external(annotation: 'SchemaTypeAnnotation', schemaElement : AbstractSchemaElement, value: typing.Any, writer_callback: typing.Optional[typing.Callable] = None,
        **params) -> typing.Optional[typing.Any]:
        """ Validation method, to transform external and validate it. Returns internal form, or raises error.
            The arguments are the same as in AbstractSchema.from_external(). Params must be passed down. 

            Default implementation:
            
            Passes external to schemaElement.get_python_type() by default.
        """

    @staticmethod # can be overritten by passing a function to the constructor
    def from_external(annotation: 'SchemaTypeAnnotation', schemaElement : AbstractSchemaElement, external: typing.Union[typing.Any, typing.Callable], source: WellknownRepresentation, **params) -> typing.Any:
        """ Validation method, to transform external and validate it. Returns internal form, or raises error.
            The arguments are the same as in AbstractSchema.from_external(). Params must be passed down. 

            Default implementation:
            
            Passes external to schemaElement.get_python_type() by default.
        """
        

    @staticmethod # can be overritten by passing a function to the constructor
    def validate_internal(annotation: 'SchemaTypeAnnotation', schemaElement : AbstractSchemaElement, value: typing.Any, **params) -> typing.Any:
        """ Validation method, to transform external and validate it. Returns internal form, or raises error.
            The arguments are the same as in AbstractSchema.from_external(). Params must be passed down. 

            Default implementation:
            
            Passes external to schemaElement.get_python_type() by default.
        """
        if not value:
            if annotation.default is not MISSING:
                value = annotation.default
            elif annotation.required:
                raise ValidationError(f'required element {schemaElement.get_name()} must be supplied')
        else:
            pt = schemaElement.get_python_type()
            basetype = getattr(pt, "__origin__", pt) # typing type.__origin__ is Python class
            try:
                value = basetype(value)
            except Exception as e:
                raise ValidationError(str(e),original_error=e)
        return value

class SchemaError(Exception):
    """ Base class for all schema-related errors. """
    def __init__(self,message,original_error=None):
        self.message = message
        self.original_error = original_error
        return

class ValidationError(SchemaError,ValueError):
    """ Denotes invalid data """
    ...
    