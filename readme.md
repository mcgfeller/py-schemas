# py-schemas


This is a working document to propose a unfication of Schemas used in Python. 

It expand on the ideas put forth in https://ict.swisscom.ch/2017/12/python-schema/ and on growing frustrations with special-purpose schemas. 

# Goals
## Compatibility with Python type declarations

Python typing only allows declaration of uniform value types for dictionaries (i.e., each value must be of the same type). Hence the most natural data typed with a schema is the object, with the schema attached to its class. The individual schema elements correspond to instance variables. 

* Declaring a schema on a class should declare the type of its instance variables.  
* Schema types should be subtypes of the Python types. 




## Interoperability between Schema solutions

# Approach

Have a Python Special Interest Group (SIG) like [DB SIG](https://www.python.org/community/sigs/current/db-sig/). [Known Schema solutions](https://github.com/mcgfeller/py-schemas/wiki/Some-existing-Schema-solutions) are candidates to participate. 





