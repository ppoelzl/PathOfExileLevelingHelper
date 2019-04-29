from validators import ImportValidator

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class ImportForm(FlaskForm):
    import_code = StringField(
        label="",
        description="Input Path of Building Import Code or Pastebin.com link:",
        validators=[ImportValidator(), InputRequired()],
    )
    submit = SubmitField("Calculate skill gems »")
