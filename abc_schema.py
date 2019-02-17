""" Protocol for Schemaa """

import abc
import typing
import collections.abc
import enum

class SchemedObject(metaclass=abc.ABCMeta):
    """ An object with a Schema, supporting the __get_schema__ method.
    """

    @abc.abstractmethod
    def __get_schema__(self) -> 'AbstractSchema':
        pass


class WellknownRepresentation(enum.Enum):

    python  = '__python__' # internal python structures
    pickle  = 'application/python-pickle'
    json    = 'application/json'
    xml     = 'application/xml'
    sql     = 'application/sql'
    html    = 'text/html'
               

class AbstractSchema(collections.abc.Iterable,metaclass=abc.ABCMeta):
    """ The AbstractSchema does not prescribe how the Schema is organizred, and
        only prescribes that the AbstractSchemaElement may be obtained by iterating
        over the Schema.
    """
    SupportedRepresentations: typing.ClassVar[typing.Set['WellknownRepresentation']] = {WellknownRepresentation.python}

    @abc.abstractmethod
    def to_external(self, obj : SchemedObject, destination : WellknownRepresentation, writer_callback : typing.Optional[typing.Callable]=None, **params) -> typing.Optional[typing.Any]:
        """
            If *writer_callback* is None (the default), the external representation
            is returned as result.

            If *writer_callback* is not None, then it can be called any number
            of times with some arguments. No result is returned.

            (inspired by PEP-574 https://www.python.org/dev/peps/pep-0574/#producer-api)
        """
        pass


    @abc.abstractmethod
    def from_external(self,external : typing.Union[typing.Any,typing.Callable], source : WellknownRepresentation, **params ) -> SchemedObject:

        """
            If *external* is bytes, they are consumed as source representation.

            If *external* is a Callable, then it can be called any number
            of times with some arguments to obtain parts of the source representation.

        """
        pass

    @abc.abstractmethod
    def validate_internal(self, obj : SchemedObject, **params, ) -> SchemedObject:
        pass

    @abc.abstractmethod
    def __iter__(self) -> typing.Iterator['AbstractSchemaElement'] :
        """ iterator through SchemaElements in this Schema """
        pass

    def as_annotations(self) -> typing.Dict[str,type]:
        """ return Schema Elements in annotation format.
            Use as class.__annotations__ = schema.as_annotations()
            I would wish that __annotations__ is a protocol that can be provided, instead of simply assuming it is a mapping. 
        """
        return {se.get_name() : se.get_python_type() for se in self}



class AbstractSchemaElement(metaclass=abc.ABCMeta):


    @abc.abstractmethod
    def get_schema(self) -> typing.Optional[AbstractSchema]:
        """ get associated schema or None """
        pass

    @abc.abstractmethod
    def get_python_type(self) -> type:
        """ get Python type of this AbstractSchemaElement """
        pass

    @abc.abstractmethod
    def get_name(self) -> str:
        """ get name useable as variable name """
        pass

    

         