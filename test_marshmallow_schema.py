""" Marshmallow Schema Test """
import pytest
import marshmallow_schema 
import abc_schema
import marshmallow as mm  # type: ignore
import dataclasses
import datetime
import typing


class Person(marshmallow_schema.SchemedObject):
    class Schema(marshmallow_schema.MMSchema):
        name = mm.fields.Str(required=True)
        email = mm.fields.Email(missing=None)
        dob = mm.fields.Date(missing=None)
        sex = mm.fields.Str(validate=mm.fields.validate.OneOf(("m", "f", "o", "?")), missing="?")
        education = mm.fields.Dict(
            keys=mm.fields.Str(), values=mm.fields.Date(), payload="field metadata"
        )


    
def test_as_annotations():
    """ Sets annotations for Person as side-effect """
    Person.__annotations__ = Person.Schema().as_annotations()

def test_get_schema():
    
    p = Person()
    s = p.__get_schema__()
    # Schema manipulations:
    assert len({se.get_name(): se.get_python_type() for se in s}) == 5
    assert s.fields["name"].get_schema() is s
    assert s.fields["education"].get_metadata() == {"payload": "field metadata"}

    field = s.fields["education"]
    mm.fields.Field.from_schema_element(field)

def test_schema_from_schema():
    p = Person()
    s = p.__get_schema__()
    s2 = marshmallow_schema.MMSchema.from_schema(s)   


def test_validation():
    o_good  = makePerson()
    o_conv  = makePerson(dob=datetime.date(2001, 1, 1))
    o_bad   = makePerson(sex='x')


    s = Person.__get_schema__()
    assert s.validate_internal(o_good).sex == 'm'
    assert s.validate_internal(o_conv).dob == datetime.date(2001, 1, 1)

    with pytest.raises(ValueError) as excinfo:
        s.validate_internal(o_bad).sex == 'm'
        

def test_import_export():     
    o_conv  = makePerson(sex='M')
    s = Person.__get_schema__()
    assert s.to_external(o_conv,destination=dataclasses_schema.abc_schema.WellknownRepresentation.python).sex == 'm'
    assert s.to_external(o_conv,destination=dataclasses_schema.abc_schema.WellknownRepresentation.python).sex == 'm'

    with pytest.raises(NotImplementedError) as excinfo: # xml conversion is not implemented
        s.to_external(o_conv,destination=dataclasses_schema.abc_schema.WellknownRepresentation.xml).sex == 'm'

def makePerson(name="Martin", email="mgf@acm.org", sex="m", dob=None, education={'Gymnasium Raemibuehl': datetime.date(1981, 9, 1)}):
    p = Person()
    p.__dict__.update({'name':name,'email':email,'sex':sex,'dob':dob,'education':education})
    return p

if __name__ == '__main__':
    test_as_annotations()
    test_get_schema()
    test_schema_from_schema()
    test_validation()
    test_import_export()