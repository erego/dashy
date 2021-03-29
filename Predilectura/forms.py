"""Form object declaration."""
from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField


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
    submit = SubmitField('Aceptar')
