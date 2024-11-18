from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash

class AccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    hashed_password = TextAreaField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField('Submit')

    def hash_password(self):
        """
        Hash the password before saving it.
        This method can be called when processing the form data.
        """
        return generate_password_hash(self.hashed_password.data)