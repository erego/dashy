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
    #data_file = FileField()

    abts = SelectField(u'Select ABT')

    cart_criterion = SelectField(lazy_gettext(u'Impurity Metrics'), choices=[('entropy', lazy_gettext('Entropy')),
                                                                             ('gini', lazy_gettext('Gini index'))])
    cart_select = BooleanField(
        lazy_gettext('Select CART algorithm to train'), default=True
    )

    c4dot5_select = BooleanField(
        lazy_gettext('Select C4.5 algorithm to train'), default=True
    )

    random_forest_select = BooleanField(
        lazy_gettext('Select Random Forest to train'), default=True
    )

    kmeans_select = BooleanField(
        lazy_gettext('Select KMeans algorithm to train'), default=True
    )

    kmeans_algorithm = SelectField(lazy_gettext(u'Algorithm to use'), choices=[('elkan', 'Elkan'),
                                                                               ('full', 'Full')])

    knearestneighbours_select = BooleanField(
        lazy_gettext('Select KNN algorithm to train'), default=True
    )

    knearestneighbours_weights = SelectField(lazy_gettext(u'Weight function to use'),
                                            choices=[('uniform', lazy_gettext('Uniform')),
                                                     ('distance', lazy_gettext('Distance'))])

    naivebayes_select = BooleanField(
        lazy_gettext('Select Naive Bayes algorithm to train'), default=True
    )

    mlp_select = BooleanField(
        lazy_gettext('Select Multilayer Perceptron to train'), default=True
    )

    submit = SubmitField(lazy_gettext('Train'))


class FormABTDetail(FlaskForm):
    """
        Form related to show ABT details
    """

    abts = SelectField(u'Select ABT')

class FormHandlingQuality(FlaskForm):
    """
        Form related to handling quality issues in dataset
    """

    abts = SelectField(u'Select ABT')

    filename = StringField(
        lazy_gettext('Output filename(If blank will be overwrite)'),
    )

    handler = RadioField('Label',
                         default='complete_case',
                         choices=[('complete_case', lazy_gettext('Complete Case Analysis(all rows with value NaN will be deleted)')),
                                  ('drop_features', lazy_gettext('Drop Features')),
                                  ('imputation', lazy_gettext('Imputation')),
                                  ('clamp', lazy_gettext('Clamp Transformation')),
                                  ('missing_reading', lazy_gettext('Reading event missing indicator(Include a indicator for reading event, NaN values will be set to 0)'))])
    imputation = SelectField(u'Type Of Imputation', choices=[('mean', lazy_gettext('mean')),
                                                             ('median', lazy_gettext('median'))])

    features_select = SelectMultipleField(lazy_gettext(u'Select Features'))
    submit = SubmitField(lazy_gettext('Apply'))
