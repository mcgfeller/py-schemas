# py-schemas


This is a working document to propose a minimal standard for interoperability of Schemas used in Python. 

**The procotol is itself is introduced in the [Schema Protocol Jupyter Notebook](SchemaProtocol.ipynb)**, and is defined in  [abc_schema.py](abc_schema.py).

It expands on the ideas put forth in my [Dec 2017 Blog Post on Python Schemas](https://ict.swisscom.ch/2017/12/python-schema/) and on growing frustrations with special-purpose schemas. 

# Goals

Despite the popularity of "schema-less" databases, Schemas are needed to validate data and to exchange data with others. The primary goal of this proposal is **interoperability**: Use some package that employs a schema written in a schema solution, without re-coding the schema. 

For example, use an SQLalchemy-schemed object as a `Nested` field in a Marshmallow schema, allowing serialization to JSON. The emphasis is on using Schemas, without prescribing how Schema solutions organize their internals, and how schemas are constructed using these solutions. 

There is a large number of [pre-existing solutions](ExistingSolutions.md). Software created for specific new uses cases, such as GraphQL and some new web frameworks also seem to prefer creating new Schema solution instead of reusing an existing solution. There is no agreed leading solution, and no generic interoperability, but many ad-hoc 1-1 adapters. 

## PEP

The goal is to define an informational PEP on Schema interoperability similar to the DB-API [PEP 249](https://www.python.org/dev/peps/pep-0249/). 

## Compatibility with Python type declarations

Python typing only allows declaration of uniform value types for dictionaries (i.e., each value must be of the same type). Hence the most natural data typed with a schema is the object, with the schema attached to its class. The individual schema elements correspond to instance variables. 

* Declaring a schema on a class should declare the type of its instance variables.  
* Schema types should be subtypes of the Python types.
* Schema types use Type Annotations [PEP 593](https://www.python.org/dev/peps/pep-0593) to carry a minimal (and extensible) semantic representation of schema information.  


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
* Schema transformation:
  * Get an annotated Python type of a schema element (Type Annotations are defined in [PEP 593](https://www.python.org/dev/peps/pep-0593))
  * Construct a a Schema element from an annotated type
  * Construct a Schema from another Schema (from another Schema solution) by going through annotated types for each element. 
  * A complete round-trip fidelity between Schema solutions is not feasible, but basic field validation can be implemented. 
* Associate data with a Schema

The protocol doesn't provide a standard representation for Schemas or Schema Elements; it only provides standard access and use. However, it does provide standard Type Annotations for interoperability and minimal conversion of Schema features between Schema solutions. See also [Alternatives considered](alternatives.md).


## Allow wide variety of Use Cases and destinations

There are a number of [Use Cases](UseCases.md) and a large number of [pre-existing solutions](ExistingSolutions.md), serving a wide number of serialization targets. 

Using the Protocol for a single schema solution, such as Marshmallow, does not provide facilities superior over the native usage. However, if the protocol is implemented by several solutions, integration of solutions using different schema facilities becomes much easier. Adaptions to each other solution are replaced by one adaption to the standard protocol). 

# Approach to Consensus

Have a Python Special Interest Group (SIG) like [DB SIG](https://www.python.org/community/sigs/current/db-sig/). [Known Schema solutions](ExistingSolutions.md) are candidates to participate. 
