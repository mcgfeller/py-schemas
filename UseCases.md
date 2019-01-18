# Scehma Use Cases 

Some of the following Use Cases may be amenable to interoperability by defining protocols.

## Use Case: Define a schema 

### Common solutions

* Schema defined as class variables in a class
* Schema defined as a dictionary
* Schema defined as a Schema object

## Use Case: Attach a Schema to an object 

### Common solutions
* Schema is nested in the class (as class attribute, class method returing it, inner class)
* Schema is defined separately and assigned to a class variable

### Proposed Protocol

* `cls.__get_schema__()` returns an object defining the Schema - an object that supports the Schema protocol.

## Use Case: Transform an object

An object can be transformed from an internal to one or more external representations. 

### Examples

* SqlAlchemy: To and from SQL
* Django Models: To and from SQL
* Marshmallow: To and from Python dicts, JSON
* Graphene: To and from GraphQL 

## Use Case: Validate an object

An object in _internal form_ can be dynamically validated to conform to a schema. Note: Validating an external representation is the _Transform an object_ Use Case. 

## Use Case: Static type checking

An object is being statically checked [mypy](http://mypy-lang.org/) to conform to its type annotation. See [PEP-484](https://www.python.org/dev/peps/pep-0484) for details.

## Use Case: Form Generation and Validation

### Examples

* Django Models: HTML forms





