""" Marshmallow based conformant Schema.
    Marshmallow fields are monkey-patched.
    Marshmallow schema is subclassed. 
"""

import typing
import marshmallow as mm
import decimal
import datetime
import abc_schema
import dataclasses


""" Now adapt Marshmallow fields by some monkey patching """



def get_python_type(self) -> type:
    """ get native class of field, can be overwritten """
    return self.python_type

def get_name(self) -> str:
    return self.name
    

mm.fields.Field.get_python_type = get_python_type
mm.fields.Field.get_name = get_name
mm.fields.FieldABC.python_type = typing.Any
mm.fields.Str.python_type = str
mm.fields.Integer.python_type = int
mm.fields.Float.python_type = float
mm.fields.Decimal.python_type = decimal.Decimal
mm.fields.Boolean.python_type = bool
mm.fields.FormattedString.python_type = str
mm.fields.DateTime.python_type = datetime.datetime
mm.fields.Time.python_type = datetime.time
mm.fields.Date.python_type = datetime.date
mm.fields.TimeDelta.python_type = datetime.timedelta

def _dict_get_python_type(self) -> type:
    """ get native classes of containers and build Dict type
        Simplified - either container is a Field, or we use Any.
    """
    kt = self.key_container.get_python_type() if isinstance(self.key_container,mm.fields.FieldABC) else typing.Any
    vt = self.value_container.get_python_type() if isinstance(self.value_container,mm.fields.FieldABC) else typing.Any
    return typing.Dict[kt,vt]

mm.fields.Dict.get_python_type = _dict_get_python_type 


class SchemedObject:
    """ SchemedObject is the - entirely optional - superclass that can be used for classes that have an associated
        Schema. It defines one class method .__get_schema__, to return that Schema.
    """

    @classmethod
    def __get_schema__(cls):
        s = getattr(cls,'__schema',None)
        if s is None:
            sclass = getattr(cls,'Schema',None)
            if sclass is None:
                raise ValueError('Class must have Schema inner class')
            else:
                s = cls.__schema = sclass()
                s.__objclass__ = cls
        return s
                
abc_schema.SchemedObject.register(SchemedObject)


class Schema(mm.Schema):

    SupportedRepresentations: {abc_schema.WellknownRepresentation.python,abc_schema.WellknownRepresentation.json,}

    def to_external(self, obj : SchemedObject, destination : abc_schema.WellknownRepresentation, writer_callback : typing.Optional[typing.Callable]=None, **params) -> typing.Optional[typing.Any]:
        """
            If *writer_callback* is None (the default), the external representation
            is returned as result.

            If *writer_callback* is not None, then it can be called any number
            of times with some arguments. No result is returned.

            (inspired by PEP-574 https://www.python.org/dev/peps/pep-0574/#producer-api)
        """
        supported = {
            abc_schema.WellknownRepresentation.json : self.dumps,
            abc_schema.WellknownRepresentation.python : self.dump,
          }
        method = supported.get(destination)
        if not method:
            raise ValueError(f'destination {destination} not supported.')
        e = method(obj,**params)
        if writer_callback:
            return writer_callback(e)
        else:
            return e


    def from_external(self, external : typing.Union[typing.Any,typing.Callable], source : abc_schema.WellknownRepresentation, **params ) -> SchemedObject:

        """
            If *external* is bytes, they are consumed as source representation.

            If *external* is a Callable, then it can be called any number
            of times with some arguments to obtain parts of the source representation.

        """
        supported = {
            abc_schema.WellknownRepresentation.json : self.loads,
            abc_schema.WellknownRepresentation.python : self.load,
          }
        method = supported.get(source)
        if not method:
            raise ValueError(f'source {source} not supported.')
        if isinstance(external,typing.Callable):
            external = external(None)
        d = method(external, **params)
        o = self.object_factory(d)
            
        return o
        

    def validate_internal(self, obj : SchemedObject, **params, ) -> SchemedObject:
        s = self.validate(obj)
        return s


    def __iter__(self):
        """ iterator through SchemaElements in this Schema, sett """
        for name,field in self._declared_fields.items():
            field.name = name
            yield field

    def as_annotations(self):
        """ return Schema Elements in annotation format.
            Use as class.__annotations__ = schema.as_annotations()
            I would wish that __annotations__ is a protocol that can be provided, instead of simply assuming it is a mapping. 
        """
        r = {}
        for name,field in self._declared_fields.items():
            nclass = field.get_python_type()
            if not field.required:
                if field.missing is not mm.missing: # this is dummy!
                    nclass = typing.Union[nclass,type(field.missing)]
            r[name] = nclass
        return r


    def as_field_annotations(self):
        """ return Schema Elements in dataclass field annotation format.
            Use as class.__annotations__ = schema.as_annotations()
        """
        r = {}
        for name,field in self._declared_fields.items():
            nclass = field.get_python_type()
            default = None if field.missing is not mm.missing else field.missing
            metadata = None 
            dcfield = dataclasses.field(default=default,metadata=metadata)
            r[name] = dcfield
        return r

    def object_factory(self,d : dict) -> typing.Union[SchemedObject,dict]:
        """ return an object from dict, according to the Schema's __objclass__ """
        objclass = getattr(self,'__objclass__',None)
        if objclass:
            o = objclass(**d) # factory!
        else:
            o = d
        return o

abc_schema.AbstractSchema.register(Schema)


