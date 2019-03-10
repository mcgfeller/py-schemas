""" ABC Marshmallow Schema examples """
import marshmallow_schema as mms
import marshmallow as mm
import dataclasses

class Person(mms.SchemedObject):

    class Schema(mms.Schema):
        name = mm.fields.Str(required=True)
        email = mm.fields.Email(missing=None)
        sex = mm.fields.Str(validate=mm.fields.validate.OneOf(('m','f','o','?')),missing='?')
        education = mm.fields.Dict(values=mm.fields.Date(), keys=mm.fields.Str())

    __annotations__ = Schema().as_annotations()

p=Person()

for se in p.__get_schema__():
    print(se.get_name(),se.get_python_type())


@dataclasses.dataclass
class DCPerson(Person):
     __annotations__ = Person.Schema().as_field_annotations()

dcp = DCPerson(name='Martin',email='mgf@acm.org',sex='m',education={})

dcp_s = dcp.__get_schema__()
j = dcp_s.to_external(dcp,mms.abc_schema.WellknownRepresentation.json)
o = dcp_s.from_external(j,mms.abc_schema.WellknownRepresentation.json)
dcp_s.validate_internal(dcp)