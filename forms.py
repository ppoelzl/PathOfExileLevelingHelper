from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ImportForm(FlaskForm):
    import_code = StringField("Input Path of Building Import Code or Pastebin.com link:", validators=[DataRequired()])
    submit = SubmitField("Calculate skill gems")
