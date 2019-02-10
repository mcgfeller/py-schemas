# Rejected Alternatives

## Standardized representation, decoupled transformation

Instead of providing a transformation protocol, we could standardize the representation of the Schema and the Schema Elements, and leave
the transformation up to the implementation. 

This seems not viable because:
- [Existing solutions](ExistingSolutions.md) have a wide variety of representations, with minimal common ground
- External representations and other [use cases](UseCases.md) may vary in requirements for representation. Not all solution may 
support all use cases or all external representations, and hence may not need all details. 
