""" Examples """

import marshmallow_schema aa mms
import marshmallow as mm


class PersonSchema(mms.Schema):
    name = mm.fields.Str(required=True)
    email = mm.fields.Email(missing=None)
    sex = mm.fields.Str(validate=mm.fields.validate.OneOf(('m','f','o','?')),missing='?')
    education = mm.fields.Dict(values=mm.fields.Date(), keys=mm.fields.Str())