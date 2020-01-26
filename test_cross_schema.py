""" Test cross-transfer between Marshmallow and Dataclasses Schema """
import pytest
import marshmallow_schema 
import dataclasses_schema 
import abc_schema
import marshmallow as mm  # type: ignore
import datetime
import json

from test_marshmallow_schema import Person,makePerson
from test_dataclasses_schema import InventoryItem



def test_dataclasses_from_mm():
    """ Transform dataclasses schema to Marshmallow schema """
    mms = Person.__get_schema__()
    dcs = dataclasses_schema.DCSchema.from_schema(mms)
    assert sorted([e.get_name() for e in mms]) == sorted([e.get_name() for e in dcs]),'element names do not match'
    dc = dcs.__objclass__(name='Martin',dob=datetime.date(1999,1,1))
    return

def test_export_mm_import_dc():
    """ Export Marshmallow object and import as dataclass """
    p1  = makePerson(sex='m')
    mms = Person.__get_schema__()
    ext = mms.to_external(p1,destination=abc_schema.WellknownRepresentation.python)

    dcs = dataclasses_schema.DCSchema.from_schema(mms)
    p2 = dcs.from_external(ext,source=abc_schema.WellknownRepresentation.python)
    assert p2.sex == 'm'

def test_mm_from_dataclasses():
    """ Transform Marshmallow schema to dataclasses schema """
    dcs = dataclasses_schema.DCSchema.get_schema(InventoryItem)
    mms = marshmallow_schema.MMSchema.from_schema(dcs)
    assert mms.__objclass__ is InventoryItem
    assert sorted([e.get_name() for e in mms]) == sorted([e.get_name() for e in dcs]),'element names do not match'
    return

def test_export_dc_import_mm():
    """ Export dataclass object and import as Marshmallow """
    inv1  = InventoryItem(name='name',unit_price='2.2')
    dcs = dataclasses_schema.DCSchema.get_schema(InventoryItem)
    ext = dcs.to_external(inv1,destination=abc_schema.WellknownRepresentation.python)

    mms = marshmallow_schema.MMSchema.from_schema(dcs)
    inv2 = mms.from_external(ext,source=abc_schema.WellknownRepresentation.python)
    assert inv2.unit_price == 2.2


def test_export_dc_import_mm_json():
    """ Export dataclass object, convert to json, and import as Marshmallow """
    inv1  = InventoryItem(name='name',unit_price='2.2')
    dcs = dataclasses_schema.DCSchema.get_schema(InventoryItem)
    ext = dcs.to_external(inv1,destination=abc_schema.WellknownRepresentation.python)
    ext_json = json.dumps(ext.__dict__) # DCS cannot export to JSON

    mms = marshmallow_schema.MMSchema.from_schema(dcs)
    inv2 = mms.from_external(ext_json,source=abc_schema.WellknownRepresentation.json)
    assert inv2.unit_price == 2.2



if __name__ == '__main__':
    test_dataclasses_from_mm()
    test_mm_from_dataclasses()
    test_export_dc_import_mm()
    test_export_mm_import_dc()
    test_export_dc_import_mm_json()