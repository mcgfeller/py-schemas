# Definitions

These definitions should be minimal in the sense that they do not prescribe an implementation. 

I use _object_ in the sense of an instance of an user defined class, noting of course, that every value in Python is an object. I use _value_ to denote all Python objects (such as numbers, dicts, lists, sets, etc.). 

## Schema and Elements
- A *Schema* is a collection of elements.
  - The Schema itself may or may not have properties independent of its elements
  - The form of the Schema is not defined here; common forms are classes, objects, or dictionaries.
- A *Schema Element (or Element)* constrains an individual data item, which may be a Python value of fundamental type or an object. 
The Schema Element contains: 
  - a type (e.g., int) and 
  - optional further constraints (e.g., a set of allowed values, or a maximum and/or minimum value, or a validation callable). 
  - Types may correspond to Python types, types defined in the `typing` module, or some other type notation altogether.
A Python Type and Type Annotation [PEP 593](https://www.python.org/dev/peps/pep-0593) may be obtained from a Schema Element. If provided, the Type Annotation is standardized, ensuring interoperability. 



## Object association

- A Schema may be associated with zero or many Python objects (mostly class instances, but potentially other values such as dict or strings or streams representing a document), by a mechanism not specified in this proposal. 
- Vice versa, a Python value or a Python object may be associated with a Schema. 
  - In fact, we propose a _protocol_ to retrieve the Schema associated with Python class. 

## Schema solution
- A library (or other mechanism) enabling to create and use a schema. See [Existing Solutions](ExistingSolutions.md).