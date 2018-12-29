# py-schemas
Draft Proposal for Python Schema unification

This is a working document to propose a unfication of Schemas used in Python. 

It expand on the ideas put forth in https://ict.swisscom.ch/2017/12/python-schema/ and on growing frustrations with special-purpose schemas. 

# Goals

# Approach

Have a Python Special Interest Group (SIG) like [DB SIG](https://www.python.org/community/sigs/current/db-sig/). 


# Existing Schema Solutions

My own list, from https://ict.swisscom.ch/2017/12/python-schema/ - all interpretations are mine. 

Name | Framework | Main Purpose | Formats | Link | Comments
---- | --------- | ------------ | ------- | ---- | --------
[Django Models](https://docs.djangoproject.com/en/2.0/topics/db/models/) | Django | ORM | SQL
[SQLAlchemy Mappings](https://docs.sqlalchemy.org/en/latest/orm/mapping_styles.html) | SQLAlchemy | ORM | SQL |  
[Marshmallow](https://marshmallow.readthedocs.io/en/latest/) | stand-alone | validation, serialization | Python dict | 
[Graphene](https://graphene-python.org/) | Graphene | GraphQL implementation | JSON | 
[Cerberus](http://docs.python-cerberus.org/en/stable/) | Eve | Document validation, REST API | Python dict | 
[Colander](https://docs.pylonsproject.org/projects/colander/en/latest/) | Pyramid | Serialization | XML, HTML, JSON |  
[KIM](https://kim.readthedocs.io/en/latest/) | standalone | JSON serailization and validation | JSON | 
[schema](https://pypi.org/project/schema/) | standalone | Python data validation | Python data | 
[valider](https://github.com/podio/valideer) | standalone | Python data validation and adaption | Python dict | 
[voluptuous](https://github.com/alecthomas/voluptuous) | standalone | Python data validation | Python dict | 



