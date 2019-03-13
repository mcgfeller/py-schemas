My own list, from https://ict.swisscom.ch/2017/12/python-schema/ - all interpretations are mine. 

Name | Framework | Main Purpose | Formats | Validation | Un/Serialization | Object recreation | Contact | Comments
---- | --------- | ------------ | ------- | ---------- | ---------------- | ----------------- | --------| --------
[Django Models](https://docs.djangoproject.com/en/2.0/topics/db/models/) | Django | ORM | SQL | - | x | x | |
[SQLAlchemy Mappings](https://docs.sqlalchemy.org/en/latest/orm/mapping_styles.html) | SQLAlchemy | ORM | SQL  | - | x | x |  |
[Marshmallow](https://marshmallow.readthedocs.io/en/latest/) | stand-alone | validation, serialization | Python dict | x | x | x | [Steven Loria](https://github.com/sloria) |
[Graphene](https://graphene-python.org/) | Graphene | GraphQL implementation | JSON  | x | x | by code |  |
[Cerberus](http://docs.python-cerberus.org/en/stable/) | Eve | Document validation, REST API | Python dict  | x | - | - | |
[Colander](https://docs.pylonsproject.org/projects/colander/en/latest/) | Pyramid | Serialization | XML, HTML, JSON  | x | x | x |  |
[KIM](https://kim.readthedocs.io/en/latest/) | standalone | JSON serialization and validation | JSON  | x | x | x |  |
[schema](https://pypi.org/project/schema/) | standalone | Python data validation | Python data | x | via converters | - |  |
[valider](https://github.com/podio/valideer) | standalone | Python data validation and adaption | Python dict | x | x | | extensible | 
[voluptuous](https://github.com/alecthomas/voluptuous) | standalone | Python data validation | Python dict | x | - | - | |
[DB API type codes](https://www.python.org/dev/peps/pep-0249/#description) | DB API | SQL interface | SQL | - | x | x | . | | on single fields | 

