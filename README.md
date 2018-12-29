# py-schemas
Draft Proposal for Python Schema unification

This is a working document to propose a unfication of Schemas used in Python. 

It expand on the ideas put forth in https://ict.swisscom.ch/2017/12/python-schema/ and on growing frustrations with special-purpose schemas. 

# Goals

# Approach

Have a SIG like SIG-DB. 


# Existing Schema Solutions

My own list, from https://ict.swisscom.ch/2017/12/python-schema/ - all interpretations are mine. 

Name | Framework | Main Purpose | Formats | Link | Comments
---- | --------- | ------------ | ------- | ---- | --------
Django Models | Django | ORM | SQL | https://docs.djangoproject.com/en/2.0/topics/db/models/ 
SQLAlchemy Mappings | SQLAlchemy | ORM | SQL | https://docs.sqlalchemy.org/en/latest/orm/mapping_styles.html 
Marshmallow | stand-alone | validation, serialization | Python dict | https://marshmallow.readthedocs.io/en/latest/ 
Graphene | Graphene | GraphQL implementation | JSON | https://graphene-python.org/ 
Cerberus | Eve | Document validation, REST API | Python dict | http://docs.python-cerberus.org/en/stable/ 
Colander | Pyramid | Serialization | XML, HTML, JSON | https://docs.pylonsproject.org/projects/colander/en/latest/ 
KIM | standalone | JSON serailization and validation | JSON | https://kim.readthedocs.io/en/latest/ 
schema | standalone | Python data validation | Python data | https://pypi.org/project/schema/
valider | standalone | Python data validation and adaption | Python dict | https://github.com/podio/valideer
voluptuous | standalone | Python data validation | Python dict | https://github.com/alecthomas/voluptuous



