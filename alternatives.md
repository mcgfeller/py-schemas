# Rejected Alternatives

Here I discuss some design decisions taken by presenting some alternatives that I rejected.

## Standardized representation, decoupled transformation

Instead of providing a transformation protocol, we could standardize the representation of the Schema and the Schema Elements, and leave
the transformation up to the implementation. 

This seems not viable because:
- [Existing solutions](ExistingSolutions.md) have a wide variety of representations, with minimal common ground
- External representations and other [use cases](UseCases.md) may vary in requirements for representation. Not all solution may 
support all use cases or all external representations, and hence may not need all details. 


## Standardized behavior for Schema Elements

Apart from the `.get_python_type()` and `.get_schema()` methods, there is no protocol defined for Schema Elements. In particular, a Schema is free on how to use its Schema Elements to achieve a transformation. This is necessary to enable streaming parsers (such as SAX for XML) where Schema Element methods are used as callbacks from the parser. 

# Alternatives for consideration

## Minimal Common Schema Element

Define a minimal common Schema Element (instead of using `dataclasses.Field`), which the following attributes:
- name
- Python type
- default
- required (and marker if value is absent)

and less straight-forward:
- validation function
- sub elements:
  - container type:
    - key, value
  - relation (reference)
  
This would allow better schema translation fidelity and make `SchemaElement.from_schema_element()` more useful.  
