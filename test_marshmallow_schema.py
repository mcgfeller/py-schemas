""" Marshmallow Schema Test """
import pytest
import marshmallow_schema 
import abc_schema
import marshmallow as mm  # type: ignore
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
        employed = mm.fields.Bool(missing=False)


    def __init__(self,**kw):
        self.__dict__.update(kw)

    
def test_as_annotations():
    """ Sets annotations for Person as side-effect """
    Person.__annotations__ = Person.__get_schema__().as_annotations()

def test_get_schema():
    
    p = Person()
    s = p.__get_schema__()
    # Schema manipulations:
    assert len({se.get_name(): se.get_python_type() for se in s}) == 6
    assert s.fields["name"].get_schema() is s
    assert s.fields["education"].get_metadata() == {"payload": "field metadata"}

    field = s.fields["education"]
    mm.fields.Field.from_schema_element(field)

def test_schema_from_schema():
    p = Person()
    s = p.__get_schema__()
    s2 = marshmallow_schema.MMSchema.from_schema(s)
    assert sorted([e.name for e in s]) == sorted([e.name for e in s2]),'element names do not match'
    return


def test_validation():
    o_good  = makePerson()
    o_conv  = makePerson(employed='Yes',dob=datetime.date(2001, 1, 1))
    o_bad   = makePerson(sex='x')


    s = Person.__get_schema__()
    assert s.validate_internal(o_good).sex == 'm'
    assert s.validate_internal(o_conv).dob == datetime.date(2001, 1, 1)
    assert s.validate_internal(o_conv).employed is True

    with pytest.raises(abc_schema.ValidationError) as excinfo:
        s.validate_internal(o_bad)
    return
        

def test_import_export():     
    o_conv  = makePerson(sex='m')
    s = Person.__get_schema__()
    ext = s.to_external(o_conv,destination=marshmallow_schema.abc_schema.WellknownRepresentation.python)
    assert ext['sex'] == 'm'
    assert s.from_external(ext,source=marshmallow_schema.abc_schema.WellknownRepresentation.python).sex == 'm'

    with pytest.raises(NotImplementedError) as excinfo: # xml conversion is not implemented
        s.to_external(o_conv,destination=marshmallow_schema.abc_schema.WellknownRepresentation.xml).sex == 'm'

def makePerson(name="Martin", email="mgf@acm.org", sex="m", dob=None, education={'Gymnasium Raemibuehl': datetime.date(1981, 9, 1)}, employed=False):
    p = Person(name=name,email=email,sex=sex,dob=dob,education=education,employed=employed)
    return p

if __name__ == '__main__':
    test_as_annotations()
    test_get_schema()
    test_schema_from_schema()
    test_validation()
    test_import_export()