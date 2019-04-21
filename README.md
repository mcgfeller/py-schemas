# py-schemas


This is a working document to propose a minimal standard for interoperability of Schemas used in Python. 

It expand on the ideas put forth in my [Dec 17 Blog Post on Python Schemas](https://ict.swisscom.ch/2017/12/python-schema/) and on growing frustrations with special-purpose schemas. 

# Goals

Despite the popularity of "schema-less" databases, Schemas are needed to validate data and to exchange data with others. The primary goal of this proposal is **interoperability**: Use some package that employs a schema written in a schema solution, without re-coding the schema. 

For example, use an SQLalchemy-schemed object as a `Nested` field in a Marshmallow schema, allowing serialization to JSON. The emphasis is on using Schemas, without prescribing how Schema libraries organize their internals, and how schemas are constructed using these libraries.  

## PEP

The goal is to define an informational PEP on Schema interoperability similar to the DB-API [PEP 249](https://www.python.org/dev/peps/pep-0249/). 

## Compatibility with Python type declarations

Python typing only allows declaration of uniform value types for dictionaries (i.e., each value must be of the same type). Hence the most natural data typed with a schema is the object, with the schema attached to its class. The individual schema elements correspond to instance variables. 

* Declaring a schema on a class should declare the type of its instance variables.  
* Schema types should be subtypes of the Python types. 


## Interoperability between Schema solutions

The current proposal is contained in a Jupyter Notebook: [A minimal standard for interoperable Schemas](SchemaProtocol.ipynb).

The minimal standard is defined as a Protocol, with some Abstract Base Classes. The protocol is minimal in that it provides for the most common 
[Use Cases](UseCases.md):
* Serialization to an external representation
* Deserialization from an external representation
* Validation
* Obtaining Schema elements
* Static type checking
  * Get the Python type of a schema element 
* Minimal Schema transformation:
  * Get [dataclasses.Field](https://docs.python.org/3/library/dataclasses.html#dataclasses.Field) of a schema element
  * Construct a a Schema element from dataclasses.Field
  * Construct a Schema from another Schema (from another Schema solution) by going through dataclasses.Field for each element. 
* Associate data with Schema

The protocol doesn't provide a standard representation for Schemas or Schema Elements; it only provides standard access and use. It does provide minimal conversion of arbitrary Schema features between schema libraries, as it provides conversion to Python static types and dataclasses.Fields. See [Alternatives considered](alternatives.md).



## Allow wide variety of Use Cases and destinations

There are a number of [Use Cases](UseCases.md) and a large number of [pre-existing solutions](ExistingSolutions.md), serving a wide number of serialization targets. 

Using the Protocol for a single schema library, such as Marshmallow, does not provide facilities superior over the native usage. However, if the protocol is implemented by several libraries, integration of libraries using different schema facilities becomes much easier.

# Approach

Have a Python Special Interest Group (SIG) like [DB SIG](https://www.python.org/community/sigs/current/db-sig/). [Known Schema solutions](ExistingSolutions.md) are candidates to participate. 





