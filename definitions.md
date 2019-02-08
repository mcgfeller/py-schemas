# Definitions

These defintions should be minumal in the sense that they do not prescribe an implementation. 

## Schema and Elements
- A *Schema* is a collection of elements.
-- The Schema itself may or may not have properties indepenent of its elements
-- The form of the Schema is not defined here; common forms are classes, objects, or dictionaries.
- A *Schema Element (or Element)* constrains an individual data item, which may be a Python builtin type or a Python object. 
The Schema element contains a datatype (e.g., int) and optional further constraints 
(e.g., a set of allowed values, or a maximum and/or minimum value, or a validation callable).


## Object association

- A Schema may be associated with zero or many Python objects, by a mechanism not specified in this proposal. 
- A Python object or a Python class may be associated with a Schema. 
