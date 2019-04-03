from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class ImportForm(FlaskForm):
    import_code = StringField("Input Path of Building Import Code or Pastebin.com link:")
    submit = SubmitField("Calculate skill gems")
