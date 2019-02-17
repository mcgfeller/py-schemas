

import typing
import marshmallow as mm
import dataclasses
import decimal
import datetime


class Person:

    name : str
    email : str
    sex : str = '?'
    age : int


class PersonSchema(mm.Schema):
    name = mm.fields.Str(required=True)
    email = mm.fields.Email(missing=None)
    sex = mm.fields.Str(validate=mm.fields.validate.OneOf(('m','f','o','?')),missing='?')
    education = mm.fields.Dict(values=mm.fields.Date(), keys=mm.fields.Str())


class PersonFields:

    name : str
    email : str
    sex : dataclasses.field(default='?',compare=False,metadata={'validator':mm.fields.validate.OneOf(('m','f','o','?'))})
    age : int

""" Now adapt Marshmallow by some monkey patching """



def get_python_type(self) -> type:
    """ get native class of field, can be overwritten """
    return self.python_type

def get_name(self) -> str:
    return field.name
    

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

def _dict_get_python_type(self):
    """ get native classes of containers and build Dict type
        Simplified - either container is a Field, or we use Any.
    """
    kt = self.key_container.get_python_type() if isinstance(self.key_container,mm.fields.FieldABC) else typing.Any
    vt = self.value_container.get_python_type() if isinstance(self.value_container,mm.fields.FieldABC) else typing.Any
    return typing.Dict[kt,vt]

mm.fields.Dict.get_python_type = _dict_get_python_type 



def _schema_as_annotations(cls):
    r = {}
    for name,field in cls._declared_fields.items():
        nclass = field.get_python_type()
        if not field.required:
            if field.missing is not mm.missing: # this is dummy!
                nclass = typing.Union[nclass,type(field.missing)]
        r[name] = nclass
    return r

##@classmethod
def _annotation_items(cls):
    """ We would prefer a protocol, but we know that
        typing.get_type_hints() uses .items() on __annotations__
    """
    r = _schema_as_annotations(cls)
    return r.items()

mm.Schema.as_annotations = classmethod(_schema_as_annotations)
mm.Schema.items = _annotation_items


class AnnotatedPerson:
    
    __annotations__ = PersonSchema()


print(typing.get_type_hints(AnnotatedPerson))

@dataclasses.dataclass
class DCPerson:
    __annotations__ = PersonSchema()

DCPerson(name='martin',email='mgf@acm.org',sex='m',education={})


def MMtype(name, mmfield):
    nt = typing.NewType(name,mmfield.get_python_type())
    nt._mmfield = mmfield
    return nt

class MMtypedPerson:
    name : MMtype('name',mm.fields.Str(required=True))
    


