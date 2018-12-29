# py-schemas
Draft Proposal for Python Schema unification

This is a working document to propose a unfication of Schemas used in Python. 

It expand on the ideas put forth in https://ict.swisscom.ch/2017/12/python-schema/ and on growing frustrations with special-purpose schemas. 

# Goals
## Compatibility with Python type declarations

Python typing only allows declaration of uniform value types for dictionaries (i.e., each value must be of the same type). Hence the most natural data typed with a schema is the object, with the schema attached to its class. The individual schema elements correspond to instance variables. 

* Declaring a schema on a class should declare the type of its instance variables.  
* Schema types should be subtypes of the Python types. 




## Interoperability between Schema solutions

# Approach

Have a Python Special Interest Group (SIG) like [DB SIG](https://www.python.org/community/sigs/current/db-sig/). 


# Some existing Schema Solutions

My own list, from https://ict.swisscom.ch/2017/12/python-schema/ - all interpretations are mine. 

Name | Framework | Main Purpose | Formats | Validation | Un/Serialization | Object recreation | Comments
---- | --------- | ------------ | ------- | ---------- | ---------------- | ----------------- | --------
[Django Models](https://docs.djangoproject.com/en/2.0/topics/db/models/) | Django | ORM | SQL | - | x | x |
[SQLAlchemy Mappings](https://docs.sqlalchemy.org/en/latest/orm/mapping_styles.html) | SQLAlchemy | ORM | SQL  | - | x | x |  
[Marshmallow](https://marshmallow.readthedocs.io/en/latest/) | stand-alone | validation, serialization | Python dict | x | x | x |
[Graphene](https://graphene-python.org/) | Graphene | GraphQL implementation | JSON  | x | x | by code |
[Cerberus](http://docs.python-cerberus.org/en/stable/) | Eve | Document validation, REST API | Python dict  | x | - | - |
[Colander](https://docs.pylonsproject.org/projects/colander/en/latest/) | Pyramid | Serialization | XML, HTML, JSON  | x | x | x |  
[KIM](https://kim.readthedocs.io/en/latest/) | standalone | JSON serialization and validation | JSON  | x | x | x |  
[schema](https://pypi.org/project/schema/) | standalone | Python data validation | Python data | x | via converters | - |  
[valider](https://github.com/podio/valideer) | standalone | Python data validation and adaption | Python dict | x | x | extensible | 
[voluptuous](https://github.com/alecthomas/voluptuous) | standalone | Python data validation | Python dict | x | - | - |



