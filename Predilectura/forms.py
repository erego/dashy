"""Form object declaration."""
from flask_wtf import FlaskForm
from wtforms import BooleanField,StringField, PasswordField, SubmitField, SelectField
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
        'Name',
        validators=[DataRequired()]
    )
    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    is_admin = BooleanField(
        'Admin', default=False
    )

    submit = SubmitField('Register')


class FormLogin(FlaskForm):
    """User Log-in Form."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Log In')
