

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


""" Now adapt Marshmallow by some monkey patching """



def _get_native_class(self):
    """ get native class of field, can be overwritten """
    return self.native_class

mm.fields.Field.get_native_class = _get_native_class
mm.fields.FieldABC.native_class = typing.Any
mm.fields.Str.native_class = str
mm.fields.Integer.native_class = int
mm.fields.Float.native_class = float
mm.fields.Decimal.native_class = decimal.Decimal
mm.fields.Boolean.native_class = bool
mm.fields.FormattedString.native_class = str
mm.fields.DateTime.native_class = datetime.datetime
mm.fields.Time.native_class = datetime.time
mm.fields.Date.native_class = datetime.date
mm.fields.TimeDelta.native_class = datetime.timedelta

def _dict_get_native_class(self):
    """ get native classes of containers and build Dict type
        Simplified - either container is a Field, or we use Any.
    """
    kt = self.key_container.get_native_class() if isinstance(self.key_container,mm.fields.FieldABC) else typing.Any
    vt = self.value_container.get_native_class() if isinstance(self.value_container,mm.fields.FieldABC) else typing.Any
    return typing.Dict[kt,vt]

mm.fields.Dict.get_native_class = _dict_get_native_class 



def _schema_as_annotation(cls):
    r = {}
    for name,field in cls._declared_fields.items():
        nclass = field.get_native_class()
        if not field.required:
            if field.missing is not mm.missing: # this is dummy!
                nclass = typing.Union[nclass,type(field.missing)]
        r[name] = nclass
    return r

@classmethod
def _annotation_items(cls):
    """ We would prefer a protocol, but we know that
        typing.get_type_hints() uses .items() on __annotations__
    """
    r = _schema_as_annotation(cls)
    return r.items()

mm.Schema.as_annotation = classmethod(_schema_as_annotation)
mm.Schema.items = _annotation_items


class AnnotatedPerson:
    
    __annotations__ = PersonSchema()


print(typing.get_type_hints(AnnotatedPerson))

@dataclasses.dataclass
class DCPerson:
    __annotations__ = PersonSchema()

DCPerson(name='martin',email='mgf@acm.org',sex='m',education={})


def MMtype(name, mmfield):
    nt = typing.NewType(name,mmfield.get_native_class())
    nt._mmfield = mmfield
    return nt

class MMtypedPerson:
    name : MMtype('name',mm.fields.Str(required=True))
    


