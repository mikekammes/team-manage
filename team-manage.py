from flask import Flask, render_template, flash, get_flashed_messages, request, redirect, url_for
import datetime
from wtforms import StringField, SubmitField, SelectField, RadioField, TextAreaField, SelectMultipleField, DateField, \
    DateTimeField
from flask.ext.wtf import Form
from wtforms.validators import DataRequired
from dbfunctions import open_db_connection, close_db_connection, add_event, get_all_events, get_event_for_user

now = datetime.datetime.now()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoyoyoyoyo!'
app.config['SERVER_NAME'] = '127.0.0.1:5000'
app.config['WTF_CSRF_ENABLED'] = False


# Form Classes

class EventCreationForm(Form):
    location = StringField('Location of event', validators=[DataRequired()])
    date = DateTimeField('Date of event', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S', default=now.date())
    time = StringField('Time of Event', validators=[DataRequired()], default='12 PM')
    eventType = SelectField('Event Type', validators=[DataRequired()],
                            choices=[('1', 'Game'), ('2', 'Practice'), ('3', 'Workout'), ('4', 'Team Bonding Event')])
    submit = SubmitField('Create Event')


# Routes


@app.route('/')
def home():
    return render_template('base.html', year=now.year)


@app.before_request
def before():
    open_db_connection()


@app.teardown_request
def after(exception):
    close_db_connection(exception)


@app.route('/events/create/<team_id>', methods=['GET', 'POST'])
def create_event(team_id):
    form = EventCreationForm()

    if form.validate_on_submit():
        success = add_event(int(team_id), int(form.eventType.data), form.date.data, form.location.data)
        if success:
            flash('Event added!', category='success')
            return render_template('base.html')
        else:
            flash('You\'re seriously screwed', category='danger')
    else:
        return render_template('create-event.html', form=form)


@app.route('/events/', defaults={'user_id': None})
@app.route('/events/<user_id>')
def see_events(user_id):
    if user_id is None:
        all_events = get_all_events()
        return render_template('show_events.html', events=all_events)
    else:
        events = get_event_for_user(user_id)
        return render_template('show_events.html', events=events)


if __name__ == '__main__':
    app.run(debug=True)
