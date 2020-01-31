""" Test dataclassen_schema """
import pytest
import dataclasses_schema
import dataclasses
import abc_schema


@dataclasses.dataclass
class InventoryItem:
    """ Test dataclass """

    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand


def test_schema_from_class():
    s = dataclasses_schema.DCSchema.get_schema(InventoryItem)
    s.get_annotations(include_extras=True)


def test_schema_from_schema():
    s = dataclasses_schema.DCSchema.get_schema(InventoryItem)
    s2 = dataclasses_schema.DCSchema.from_schema(s)


def test_validation():
    o_good = InventoryItem(name="name", unit_price=2.2)
    o_conv = InventoryItem(name="name", unit_price="2.2")
    o_bad = InventoryItem(name="name", unit_price="bla")

    s = dataclasses_schema.DCSchema.get_schema(InventoryItem)
    assert s.validate_internal(o_good).unit_price == 2.2
    assert s.validate_internal(o_conv).unit_price == 2.2

    with pytest.raises(abc_schema.ValidationError) as excinfo:
        s.validate_internal(o_bad).unit_price == 2.2


def test_export_import():
    o_conv = InventoryItem(name="name", unit_price="2.2")
    s = dataclasses_schema.DCSchema.get_schema(InventoryItem)
    ext = s.to_external(
        o_conv, destination=dataclasses_schema.abc_schema.WellknownRepresentation.python
    )
    assert ext.unit_price == 2.2
    assert (
        s.from_external(
            ext, source=dataclasses_schema.abc_schema.WellknownRepresentation.python
        ).unit_price
        == 2.2
    )

    with pytest.raises(
        NotImplementedError
    ) as excinfo:  # json conversion is not implemented
        s.to_external(
            o_conv,
            destination=dataclasses_schema.abc_schema.WellknownRepresentation.json,
        ).unit_price == 2.2


if __name__ == "__main__":
    test_schema_from_class()
    test_schema_from_schema()
    test_validation()
    test_export_import()
