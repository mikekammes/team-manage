from flask import Flask, render_template, flash, get_flashed_messages, request, redirect, url_for
import datetime
from wtforms import StringField, SubmitField, SelectField, RadioField, TextAreaField, SelectMultipleField, DateField, \
    DateTimeField
from flask.ext.wtf import Form
from wtforms.validators import DataRequired
from dbfunctions import open_db_connection, close_db_connection, add_event, get_all_events, get_event_for_user, \
    add_team, get_all_players, get_players_for_team, add_players, create_user, get_all_teams

now = datetime.datetime.now()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoyoyoyoyo!'
app.config['SERVER_NAME'] = '127.0.0.1:5000'
app.config['WTF_CSRF_ENABLED'] = False


# Form Classes

class EventCreationForm(Form):
    title = StringField('Title of event', validators=[DataRequired()])
    location = StringField('Location of event', validators=[DataRequired()])
    date = DateTimeField('Date of event', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S', default=now.date())
    time = StringField('Time of Event', validators=[DataRequired()], default='12 PM')
    eventType = SelectField('Event Type', validators=[DataRequired()],
                            choices=[('1', 'Game'), ('2', 'Practice'), ('3', 'Workout'), ('4', 'Team Bonding Event')])
    team = SelectField('Select Team', validators=[DataRequired()])
    submit = SubmitField('Create Event')


class TeamCreationForm(Form):
    name = StringField('Name of team', validators=[DataRequired()])
    coachEmail = StringField("Coach's email", validators=[DataRequired()])
    submit = SubmitField('Create Team')


class AddPlayerForm(Form):
    fname = StringField('First name of player', validators=[DataRequired()])
    lname = StringField('Last name of player', validators=[DataRequired()])
    position = StringField('Player position', validators=[DataRequired()])
    number = StringField('Player number', validators=[DataRequired()])
    email = StringField('Email of player', validators=[DataRequired()])
    submit = SubmitField('Add Player')


class SignUpForm(Form):
    fname = StringField('First name', validators=[DataRequired()])
    lname = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


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


@app.route('/events/create/', methods=['GET', 'POST'])
def create_event():
    form = EventCreationForm()
    all_teams = get_all_teams()
    team_list = []
    for team in all_teams:
        team_list.append((str(team['TeamID']), team['Name']))
    form.team.choices = team_list
    if form.validate_on_submit():
        success = add_event(form.title.data, str(form.team.data), int(form.eventType.data), form.date.data,
                            form.location.data)
        if success:
            flash('Event added!', category='success')
            return render_template('base.html')
        else:
            flash('You\'re seriously screwed', category='danger')
    else:
        return render_template('create-event.html', form=form)


@app.route('/events/', defaults={'email': None})
@app.route('/events/<email>')
def see_events(email):
    if email is None:
        all_events = get_all_events()
        return render_template('show_events.html', events=all_events)
    else:
        events = get_event_for_user(email)
        return render_template('show_events.html', events=events)


@app.route('/players/', defaults={'team_id': None})
@app.route('/players/<team_id>')
def see_players(team_id):
    if team_id is None:
        all_players = get_all_players()
        return render_template('show_players.html', players=all_players)
    else:
        players = get_players_for_team(team_id)
        return render_template('show_players.html', players=players)


@app.route('/team/create/', methods=['GET', 'POST'])
def create_team():
    form = TeamCreationForm()

    if form.validate_on_submit():
        success, team_id = add_team(form.name.data, form.coachEmail.data)
        if success:
            flash('Team added!', category='success')
            return redirect(url_for('add_player', team_id=team_id))
        else:
            flash('You\'re seriously screwed', category='danger')
    else:
        return render_template('create-team.html', form=form)


@app.route('/team/add/<team_id>', methods=['GET', 'POST'])
def add_player(team_id):
    form = AddPlayerForm()

    if form.validate_on_submit():
        success = add_players(team_id, form.email.data, form.fname.data, form.lname.data, int(form.number.data),
                              form.position.data)
        if success:
            flash('Player added!', category='success')
            return render_template('add-player.html')
        else:
            flash('You\'re seriously screwed', category='danger')
    else:
        return render_template('add-player.html', form=form)


@app.route('/signup/', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()

    if form.validate_on_submit():
        success = create_user(form.email.data, form.fname.data, form.lname.data)
        if success:
            flash('Successful sign up!', category='success')
            return render_template('base.html')
        else:
            flash('You\'re seriously screwed', category='danger')
    else:
        return render_template('sign-up.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
