"""Form object declaration."""

from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import BooleanField, StringField, PasswordField, SubmitField, SelectField, RadioField, SelectMultipleField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length
)


class FormABT(FlaskForm):
    """
        Analysis Base Table Form related
    """

    id_user = BooleanField(
        lazy_gettext('User ID'), default=True
    )
    premium = BooleanField(
        lazy_gettext('Premium value'), default=True
    )
    book = BooleanField(
        lazy_gettext('Book ID'), default=True
    )
    language = BooleanField(
        lazy_gettext('Language book'), default=True
    )
    chapters_readings = BooleanField(
        lazy_gettext('Number of chapters read'), default=True
    )
    min_percent = BooleanField(
        lazy_gettext('Minimum percentage read'), default=True
    )
    max_percent = BooleanField(
        lazy_gettext('Maximum percentage read'), default=True
    )
    avg_percent = BooleanField(
        lazy_gettext('Average percentage read'), default=True
    )
    num_words = BooleanField(
        lazy_gettext('Number of words read'), default=True
    )
    min_words = BooleanField(
        lazy_gettext('Minimum words read'), default=True
    )
    max_words = BooleanField(
        lazy_gettext('Maximum words read'), default=True
    )
    avg_words = BooleanField(
        lazy_gettext('Average number of words read'), default=True
    )
    devices_readings = BooleanField(
        lazy_gettext('Devices used'), default=True
    )
    versions_readings = BooleanField(
        lazy_gettext('Used versions'), default=True
    )
    event_classes = BooleanField(
        lazy_gettext('Types of events'), default=True
    )
    event_objs = BooleanField(
        lazy_gettext('Event objects'), default=True
    )
    event_types = BooleanField(
        lazy_gettext('Types of events'), default=True
    )
    devices_events = BooleanField(
        lazy_gettext('Devices used'), default=True
    )
    versions_events = BooleanField(
        lazy_gettext('Used versions'), default=True
    )
    chapters_events = BooleanField(
        lazy_gettext('Chapters with events'), default=True
    )

    output_format = SelectField(lazy_gettext(u'Output format'),
                                choices=[('pandas', lazy_gettext('CSV')), ('mongodb', lazy_gettext('Database')) ])

    output_path = StringField(
        lazy_gettext('File name'),
        validators=[DataRequired()]
    )

    submit = SubmitField(lazy_gettext('Apply'))


class FormSignup(FlaskForm):
    """
        User Sign-up Form
    """
    name = StringField(
        lazy_gettext('Name'),
        validators=[DataRequired()]
    )
    email = StringField(
        lazy_gettext('Email'),
        validators=[
            Length(min=6),
            Email(message=lazy_gettext('Enter a valid email')),
            DataRequired()
        ]
    )
    password = PasswordField(
        lazy_gettext('Password'),
        validators=[
            DataRequired(),
            Length(min=6, message=lazy_gettext('Select a stronger password'))
        ]
    )
    confirm = PasswordField(
        lazy_gettext('Confirm Your Password'),
        validators=[
            DataRequired(),
            EqualTo('password', message=lazy_gettext('Passwords must match'))
        ]
    )
    is_admin = BooleanField(
        lazy_gettext('Admin'), default=False
    )

    submit = SubmitField(lazy_gettext('Register'))


class FormLogin(FlaskForm):
    """
        User Log-in Form
    """
    email = StringField(
        lazy_gettext('Email'),
        validators=[
            DataRequired(),
            Email(message=lazy_gettext('Enter a valid email'))
        ]
    )
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired()])

    submit = SubmitField(lazy_gettext('Log In'))


class FormAlgorithm(FlaskForm):
    """
        Form to select algorithm to train
    """
    # TODO Set the validator
    # data_file = FileField(validators=[FileRequired()])
    data_file = FileField()
    cart_criterion = SelectField(u'Impurity Metrics', choices=[('entropy', 'Entropy'), ('gini', 'Gini index')])
    cart_select = BooleanField(
        'Select Cart algorithm to train', default=True
    )

    submit = SubmitField(lazy_gettext('Train'))


class FormHandlingQuality(FlaskForm):
    """
        Form related to handling quality issues in dataset
    """
    handler = RadioField('Label',
                         default='complete_case',
                         choices=[('complete_case', 'Complete Case Analysis'),
                                  ('drop_features', 'Drop Features'),
                                  ('imputation', 'Imputation'),
                                  ('clamp', 'Clamp Transformation')])
    imputation = SelectField(u'Type Of Imputation', choices=[('mean', 'mean'),
                                                             ('median', 'median')])

    features_select = SelectMultipleField(u'Select Features')
    submit = SubmitField(lazy_gettext('Apply'))
