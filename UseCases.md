# Schema Use Cases 

Some of the following Use Cases may be amenable to interoperability by defining protocols.

The Use Cases reliy on common minimal [definitions](definitions.md). 

## Use Case: Define a Schema 

### Common solutions

* Schema defined as class variables in a class
* Schema defined as a dictionary
* Schema defined as a Schema object

## Use Case: Attach a Schema to an object class 

### Common solutions
* Schema is nested in the class (as class attribute, class method returing it, inner class)
* Schema is defined separately and assigned to a class variable

### Proposed Protocol

* `cls.__get_schema__()` returns an object defining the Schema - an object that supports the Schema protocol.

## Use Case: Transform an object

An object can be transformed from an internal to one or more external representations and vice versa.

### Examples

* SqlAlchemy: To and from SQL
* Django Models: To and from SQL
* Marshmallow: To and from Python dicts, JSON
* Graphene: To and from GraphQL 

## Use Case: Validate an object

An object in _internal form_ can be dynamically validated to conform to a schema. Note: Validating an external representation is the _Transform an object_ Use Case. 

## Use Case: Static type checking

An object is being statically checked [mypy](http://mypy-lang.org/) to conform to its type annotation. See [PEP-484](https://www.python.org/dev/peps/pep-0484) for details.

## Use Case: Defining an individual data item

A Schema Element may be used to define an individual data item, independtly from any containing Schema. The definition may be used within Python or in another context (e.g., as a [Prop Type](https://vuejs.org/v2/guide/components-props.html#Prop-Types) in Vue.js). 

## Use Case: Transform Schema to another notation

A Schema may be transformed to another Schema notation; either within Python or to an external Schema-like definition (e.g., [XML Schema](https://en.wikipedia.org/wiki/XML_Schema_(W3C)), [JSON Schema](https://json-schema.org/), [OpenAPI SchemaObject](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#schemaObject)) 

## Use Case: Associate data with Schema or Schema Elements

A Schema or Schema Element may be used to hold additional data. Such data is specific to the Schema and not to any objects corresponding to the Schema. The associated data is not used for transformation,  validation or type checking. 

### Examples
- Hints for relationship to other schemas
- Hints for indexing
- Layout hints for presenting data

## Use Case: Form Generation and Validation

A schema can be used to generate and validate a form, either using HTML forms or another suitable input description language. This Use Case may use data associated with the schema.  

### Examples

* Django Models: HTML forms

## Use Case Diagram

![Image](https://yuml.me/3ec691c7.png)

http://yuml.me/edit/3ec691c7



