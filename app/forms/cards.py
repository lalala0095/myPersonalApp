from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, Optional

class CardForm(FlaskForm):
    card_name = StringField("Card Name", validators=[DataRequired()])
    card_type = StringField("Card Type", validators=[DataRequired()])
    account_number = StringField("Account Number", 
                                 validators=[DataRequired(),
                                             Length(min=16,max=16),
                                             Regexp(r'^\d+$', message="Account number must be numeric")])
    expiration = StringField("Expiration", validators=[Optional(),
                                                    Length(min=0, max=4),
                                                    Regexp(r'^\d+$', message="Expiration must be numeric MMYY")])
    cvv = PasswordField("CVV", validators=[Optional(), Length(max=3)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])

    submit = SubmitField("Submit")
