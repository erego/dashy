"""Form object declaration."""

from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import BooleanField, StringField, PasswordField, SubmitField, SelectField, RadioField, SelectMultipleField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional
)


class FormABT(FlaskForm):
    """Analysis Base Table Form."""
    id_user = BooleanField(
        'Identificador del usuario', default=True
    )
    premium = BooleanField(
        'Valor de premium', default=True
    )
    book = BooleanField(
        'Identificador del libro', default=True
    )
    language = BooleanField(
        'Idioma del libro', default=True
    )
    chapters_readings = BooleanField(
        'Número de capítulos leído', default=True
    )
    min_percent = BooleanField(
        'Mínimo porcentaje leído', default=True
    )
    max_percent = BooleanField(
        'Máximo porcentaje leido', default=True
    )
    avg_percent = BooleanField(
        'Porcentaje medio leido', default=True
    )
    num_words = BooleanField(
        'Número de palabras leídas', default=True
    )
    min_words = BooleanField(
        'Mínimo de palabras leídas', default=True
    )
    max_words = BooleanField(
        'Máximo de palabras leídas', default=True
    )
    avg_words = BooleanField(
        'Media de palabras leídas', default=True
    )
    devices_readings = BooleanField(
        'Dispositivos usados', default=True
    )
    versions_readings = BooleanField(
        'Versiones usadas', default=True
    )
    event_classes = BooleanField(
        'Clases de eventos', default=True
    )
    event_objs = BooleanField(
        'Objetos de eventos', default=True
    )
    event_types = BooleanField(
        'Tipos de eventos', default=True
    )
    devices_events = BooleanField(
        'Dispositivos usados', default=True
    )
    versions_events = BooleanField(
        'Versiones usadas', default=True
    )
    chapters_events = BooleanField(
        'Capítulos con eventos', default=True
    )

    output_format = SelectField(u'Formato de salida', choices=[('mongodb', 'Base de datos'), ('pandas', 'CSV')])

    submit = SubmitField('Aceptar')


class FormSignup(FlaskForm):
    """User Sign-up Form."""
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
    """User Log-in Form."""
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
    #TODO Set the validator
    #data_file = FileField(validators=[FileRequired()])
    data_file = FileField()
    cart_criterion = SelectField(u'Impurity Metrics', choices=[('entropy', 'Entropy'), ('gini', 'Gini index')])
    cart_select = BooleanField(
        'Select Cart algorithm to train', default=True
    )

    submit = SubmitField(lazy_gettext('Train'))


class FormHandlingQuality(FlaskForm):
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
