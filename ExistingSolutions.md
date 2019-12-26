My own list, from https://ict.swisscom.ch/2017/12/python-schema/ - all interpretations are mine. There are now many tools, each with strengths and weaknesses, geared to a primary usage domain. The many solutions underline the importance of interoperability.  


Name | Framework | Main Purpose | Formats | Validation | Un/Serialization | Object recreation | Contact | Comments
---- | --------- | ------------ | ------- | ---------- | ---------------- | ----------------- | --------| --------
[Django Models](https://docs.djangoproject.com/en/2.0/topics/db/models/) | Django | ORM | SQL | - | x | x | [Technical Board?](https://www.djangoproject.com/foundation/teams/#technical-board-team) |
[SQLAlchemy Mappings](https://docs.sqlalchemy.org/en/latest/orm/mapping_styles.html) | SQLAlchemy | ORM | SQL  | - | x | x | ‎[@sqlalchemy](https://twitter.com/sqlalchemy), [Mailing List](https://groups.google.com/forum/#!forum/sqlalchemy) |
[Marshmallow](https://marshmallow.readthedocs.io/en/latest/) | stand-alone | validation, serialization | Python dict | x | x | x | [Steven Loria](https://github.com/sloria) |
[Graphene](https://graphene-python.org/) | Graphene | GraphQL implementation | JSON  | x | x | by code | [Github Issue](https://github.com/graphql-python/graphene)  |
[Strawberry](https://github.com/strawberry-graphql/strawberry) | Strawberry | GraphQL | GraphQL | x | x | - | [Patrick Arminio](patrick.arminio@gmail.com) | Uses Python types |
[Cerberus](http://docs.python-cerberus.org/en/stable/) | Eve | Document validation, REST API | Python dict  | x | - | - | [Mailing List](https://groups.google.com/forum/?hl=en#!forum/python-eve) |
[Colander](https://docs.pylonsproject.org/projects/colander/en/latest/) | Pyramid | Serialization | XML, HTML, JSON  | x | x | x | [Github Issue](https://github.com/Pylons/colander/issues) |
[KIM](https://kim.readthedocs.io/en/latest/) | standalone | JSON serialization and validation | JSON  | x | x | x | Abandoned? [Github Issue](https://github.com/mikeywaites/kim/issues) |
[Pydantic](https://pydantic-docs.helpmanual.io/) | standalone | Data validation using Python types | Python, JSON | x | x | x | [Samuel Colvin](S@muelColvin.com) | mypy, JSON schema support | 
[schema](https://pypi.org/project/schema/) | standalone | Python data validation | Python data | x | via converters | - | [Vladimir Keleshev](mailto:vladimir@keleshev.com) |
[Schematics](https://schematics.readthedocs.io/en/latest/) | standalone | Validation, conversion | Python, language agnostic | x | x | x | [Kalle Tuure](kalle@goodtimes.fi) | "for Humans" philosophy. |
[TypeSystem](https://www.encode.io/typesystem/)| Encode | validation, du/serialization, forms | Python dict , JSON, YAML | x | x | ? | [Tom Christie](mailto:tom@tomchristie.com) |
[valider](https://github.com/podio/valideer) | standalone | Python data validation and adaption | Python dict | x | x | | [George Sakkis](https://github.com/gsakkis) | extensible | 
[voluptuous](https://github.com/alecthomas/voluptuous) | standalone | Python data validation | Python dict | x | - | - | [Alec Thomas](alec@swapoff.org)|
[DB API type codes](https://www.python.org/dev/peps/pep-0249/#description) | DB API | SQL interface | SQL | - | x | x | . | | on single fields | 
[PEP 593](https://www.python.org/dev/peps/pep-0593) | Python typing | Flexible function and variable annotations | Python types | - | - | - | [Till Varoquaux](till@fb.com), [Konstantin Kashin](kkashin@fb.com) |  | 


There are doubtless many others, which I haven't encountered yet. 