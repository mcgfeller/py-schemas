""" ABC Marshmallow Schema examples """
from marshmallow_schema import SchemedObject,MMSchema
import abc_schema
import marshmallow as mm # type: ignore
import dataclasses
import datetime

class Person(SchemedObject):

    class Schema(MMSchema):
        name = mm.fields.Str(required=True)
        email = mm.fields.Email(missing=None)
        sex = mm.fields.Str(validate=mm.fields.validate.OneOf(('m','f','o','?')),missing='?')
        education = mm.fields.Dict(values=mm.fields.Date(), keys=mm.fields.Str(),payload='field metadata')

    __annotations__ = Schema().as_annotations()

p=Person()

print({se.get_name() : se.get_python_type() for se in p.__get_schema__()})

s = p.__get_schema__()
assert s.fields['name'].get_schema() is s
assert s.fields['education'].get_metadata() == {'payload': 'field metadata'}


@dataclasses.dataclass
class DCPerson(Person):
     __annotations__ = Person.Schema().as_field_annotations()

dcp = DCPerson(name='Martin',email='mgf@acm.org',sex='m',education={})

dcp_s = dcp.__get_schema__()
j = dcp_s.to_external(dcp,abc_schema.WellknownRepresentation.json)
o = dcp_s.from_external(j,abc_schema.WellknownRepresentation.json)
dcp_s.validate_internal(dcp)