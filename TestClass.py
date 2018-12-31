

import typing
import marshmallow as mm
import dataclasses

class Person:

    name : str
    email : str
    sex : str = '?'
    age : int


class PersonSchema(mm.Schema):
    name = mm.fields.Str()
    email = mm.fields.Email()
    sex = mm.fields.Str(validate=mm.fields.validate.OneOf(('m','f','o','?')))
    education = mm.fields.Dict(values=mm.fields.Date(), keys=mm.fields.Str())


""" Now adapt Marshmallow by some monkey patching """
import decimal
import datetime


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
        r[name] = field.get_native_class()
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


class MMtext(typing.Generic):

    def __getitem__(self, params):
        print(self,params)
        return super().__getitem__(params)
    

