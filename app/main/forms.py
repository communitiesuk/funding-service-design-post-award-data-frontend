from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovRadioInput, GovSubmitInput, GovSelect
from wtforms.fields import RadioField, SubmitField, StringField, SelectField
from wtforms.validators import InputRequired, DataRequired


class CookiesForm(FlaskForm):
    functional = RadioField(
        "Do you want to accept functional cookies?",
        widget=GovRadioInput(),
        validators=[
            InputRequired(message="Select yes if you want to accept functional cookies")
        ],
        choices=[("no", "No"), ("yes", "Yes")],
        default="no",
    )
    analytics = RadioField(
        "Do you want to accept analytics cookies?",
        widget=GovRadioInput(),
        validators=[
            InputRequired(message="Select yes if you want to accept analytics cookies")
        ],
        choices=[("no", "No"), ("yes", "Yes")],
        default="no",
    )
    save = SubmitField("Save cookie settings", widget=GovSubmitInput())


class DownloadForm(FlaskForm):
    file_format = SelectField(
        "File Format",
        widget=GovSelect(),
        validators=[InputRequired(message="Select the data format")],
        choices=[
            ("csv", "CSV"),
            ("xlsx", "XSLX (Excel)"),
            ("json", "JSON"),
            ("xml", "XML"),
        ],
        default="csv",
    )
    save = SubmitField("Download", widget=GovSubmitInput())
