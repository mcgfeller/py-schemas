# Definitions

These defintions should be minumal in the sense that they do not prescribe an implementation. 

## Schema and Elements
- A *Schema* is a collection of elements.
  - The Schema itself may or may not have properties indepenent of its elements
  - The form of the Schema is not defined here; common forms are classes, class instances, or dictionaries.
- A *Schema Element (or Element)* constrains an individual data item, which may be a Python fundamental type or a class instance. 
The Schema element contains 
  - a type (e.g., int) and 
  - optional further constraints (e.g., a set of allowed values, or a maximum and/or minimum value, or a validation callable). 
  - Types may correspond to Python types, or some other type notation.


## Object association

- A Schema may be associated with zero or many Python objects (mostly class instances, but potentially other objects such as dict or strings or streams representing a document), by a mechanism not specified in this proposal. 
- Vice versa, a Python object or a Python class instance may be associated with a Schema. 
  - In fact, we proposal a _protocol_ to retrieve the Schema associated with Python class. 
