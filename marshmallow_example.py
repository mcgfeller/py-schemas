""" ABC Marshmallow Schema examples """
from marshmallow_schema import SchemedObject, MMSchema
import abc_schema
import marshmallow as mm  # type: ignore
import dataclasses
import datetime
import typing


class Person(SchemedObject):
    class Schema(MMSchema):
        name = mm.fields.Str(required=True)
        email = mm.fields.Email(missing=None)
        dob = mm.fields.Date(required=False)
        sex = mm.fields.Str(
            validate=mm.fields.validate.OneOf(("m", "f", "o", "?")), missing="?"
        )
        education = mm.fields.Dict(
            values=mm.fields.Date(), keys=mm.fields.Str(), payload="field metadata"
        )

    __annotations__ = Schema().as_annotations()


p = Person()

# Schema manipulations:
print({se.get_name(): se.get_python_type() for se in p.__get_schema__()})

s = p.__get_schema__()
assert s.fields["name"].get_schema() is s
assert s.fields["education"].get_metadata() == {"payload": "field metadata"}

field = s.fields["education"]
mm.fields.Field.from_schema_element(field)

# create another Marshmallow schema from s, only using the protocol API to access s (round trip): 
s2 = MMSchema.from_schema(s)


@dataclasses.dataclass
class DCPerson(Person):
    __annotations__ = Person.Schema().as_field_annotations() # type: ignore # we cannot use another type in a subclass


# mypy cannot handle this dynamic typing without a plugin.
# Note we need to set dob=None, as dataclasses cannot handle optional fields, 
# but since the type is optional, it's a valid value.
dcp = DCPerson(name="Martin", email="mgf@acm.org", sex="m", dob=None, education={}) # type: ignore 


dcp_s = dcp.__get_schema__()
j = dcp_s.to_external(dcp, abc_schema.WellknownRepresentation.json)
o = dcp_s.from_external(j, abc_schema.WellknownRepresentation.json)
dcp_s.validate_internal(dcp)

# s2 validates as well, but will not recognize bad EMail, because there is no EMail field in Python
s2.validate_internal(dcp)
