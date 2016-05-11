from flask import Flask, render_template, flash, get_flashed_messages, request, redirect, url_for
import datetime
from wtforms import StringField, SubmitField, SelectField, RadioField, TextAreaField, SelectMultipleField, DateField, \
    DateTimeField, IntegerField
from flask.ext.wtf import Form
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from dbfunctions import open_db_connection, close_db_connection, add_event, get_all_events, get_event_for_user, \
    add_team, get_all_players, get_players_for_team, add_player_and_invite, create_user, get_all_teams, get_usersname, \
    create_rsvp, get_emails_from_team, RSVP, delete_event, get_team_invites, accept_invite, player_exists, \
    player_plays_for_team, invite_player, add_contact, get_event_types, setting_exists, create_setting,  update_setting\

now = datetime.datetime.now()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoyoyoyoyo!'
app.config['SERVER_NAME'] = '127.0.0.1:5000'
app.config['WTF_CSRF_ENABLED'] = False


# Form Classes

class EventCreationForm(Form):
    title = StringField('Title of event', validators=[DataRequired()])
    location = StringField('Location of event', validators=[DataRequired()])
    date = DateTimeField('Date of event', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S', default=now)
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
    number = IntegerField('Player number', validators=[DataRequired()])
    email = StringField('Email of player', validators=[DataRequired()])
    team = SelectField('Select Team', validators=[DataRequired()])

    submit = SubmitField('Add Player')


class SignUpForm(Form):
    fname = StringField('First name', validators=[DataRequired()])
    lname = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class GetTeamPlayersForm(Form):
    team = SelectField('Select Team', validators=[DataRequired()])
    submit = SubmitField('View Players')


class RSVPForm(Form):
    email = SelectField('Email', validators=[DataRequired()], choices=[])
    #email = StringField('TeamID', validators=[DataRequired()])
    #accept = SelectField('Do you want to play?', validators=[DataRequired()], choices=[(0, 'No'), (1, 'Yes')],
    #                                         coerce=str)
    attending = SelectField('Are you attending?', validators=[DataRequired()], choices=[('0', 'No'), ('1', 'Yes')],
                    coerce=str)
    submit = SubmitField('RSVP')


class JoinTeamForm(Form):
    #team = StringField('TeamID', validators=[DataRequired()])
    #accept = IntegerField('Accept', validators=[DataRequired()])
    team = SelectField('Team', validators=[DataRequired()], choices=[])
    accept = SelectField('Do you want to play?', validators=[DataRequired()], choices=[('0', 'No'), ('1', 'Yes')],
                         coerce=str)
    submit = SubmitField('Submit')


class CreateContactForm(Form):
    is_phone = SelectField('Contact type?', validators=[DataRequired()], choices=[('0', 'Email'), ('1', 'Phone')],
                         coerce=str)
    contact = StringField('Contact', validators=[DataRequired()])
    submit = SubmitField('Create contact')


class NotificationForm(Form):
    type = SelectField('Event Type', validators=[DataRequired()], choices=[])
    time = DateTimeField('Date of event', validators=[DataRequired()], format='%d %H:%M', default=now)
    submit = SubmitField('Set settings')


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
        success, event_id = add_event(form.title.data, str(form.team.data), int(form.eventType.data), form.date.data,
                                      form.location.data)
        if success:
            flash('Event added!', category='success')
            team_players = get_players_for_team(str(form.team.data))
            for player in team_players:
                create_rsvp(player['Email'], event_id)
            return render_template('base.html')
        else:
            flash('You\'re seriously screwed', category='danger')
            return render_template('create-event.html', form=form)
    else:
        return render_template('create-event.html', form=form)


@app.route('/events/delete/<event_id>')
def event_remover(event_id):
    success = delete_event(event_id)
    if success == 1:
        flash("Event Deleted", category='danger')
        return redirect(url_for('see_events'))
    else:
        return redirect(url_for('see_events'))


@app.route('/events/', defaults={'email': None})
@app.route('/events/<email>')
def see_events(email):
    if email is None:
        all_events = get_all_events()
        return render_template('show-events.html', events=all_events)
    else:
        events = get_event_for_user(email)
        user = get_usersname(email)
        first = user['first_name']
        last = user['last_name']
        name = first + ' ' + last
        return render_template('show-events.html', events=events, user=name)


@app.route('/team/players/', methods=['GET', 'POST'])
def get_players():
    form = GetTeamPlayersForm()
    all_teams = get_all_teams()
    team_list = []
    for team in all_teams:
        team_list.append((str(team['TeamID']), team['Name']))
    form.team.choices = team_list
    if form.validate_on_submit():
        return redirect(url_for('see_players', team_id=int(form.team.data)))
    else:
        return render_template('show-players-form.html', form=form)


@app.route('/team/players/<team_id>')
def see_players(team_id):
    if team_id is None:
        all_players = get_all_players()
        return render_template('show-players.html', players=all_players)
    else:
        players = get_players_for_team(team_id)
        team = ''
        for player in players:
            team = player['name']
        return render_template('show-players.html', players=players, team=team)


@app.route('/team/create/', methods=['GET', 'POST'])
def create_team():
    form = TeamCreationForm()

    if form.validate_on_submit():
        success, team_id = add_team(form.name.data, form.coachEmail.data)
        if success:
            flash('Team added!', category='success')
            return redirect(url_for('add_player'))
        else:
            flash('You\'re seriously screwed', category='danger')
            return render_template('create-team.html', form=form)
    else:
        return render_template('create-team.html', form=form)


@app.route('/team/add/', methods=['GET', 'POST'])
def add_player():
    form = AddPlayerForm()
    all_teams = get_all_teams()
    team_list = []
    for team in all_teams:
        team_list.append((str(team['TeamID']), team['Name']))
    form.team.choices = team_list
    if form.validate_on_submit():
        exists = player_exists(form.email.data)[0][0]
        if exists:
            plays_for_team = player_plays_for_team(form.email.data, form.team.data)[0][0]
            if plays_for_team:
                flash('Player already invited to your team!', category='danger')
                return render_template('add-player.html', form=form)
            else:
                success = invite_player(form.team.data, form.email.data, int(form.number.data), form.position.data)
        else:
            success = add_player_and_invite(form.team.data, form.email.data, form.fname.data, form.lname.data,
                                            form.number.data, form.position.data)
        if success:
            flash('Player added!', category='success')
            return render_template('add-player.html', form=form)
        else:
            flash('You\'re seriously screwed', category='danger')
            return render_template('add-player.html', form=form)
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
            return render_template('sign-up.html', form=form)
    else:
        return render_template('sign-up.html', form=form)


@app.route('/events/<event_id>/rsvp', methods=['GET', 'POST'])
def rsvp(event_id):
    form = RSVPForm()
    team_emails = get_emails_from_team(event_id)
    email_list = []
    for email in team_emails:
        email_list.append((email['email'], email['email']))
    form.email.choices = email_list
    print(form.email.choices)
    if form.validate_on_submit():
        success = RSVP(event_id, form.email.data, form.attending.data)
        if success == 1:
            flash("RSVP submitted successfully!", category='success')
            return render_template('base.html')
        else:
            flash('You RSVP\'d for multiple people', category='danger')
            return render_template('rsvp.html', form=form)
    else:
        return render_template('rsvp.html', form=form)


@app.route('/player/<player>/join', methods=['GET', 'POST'])
def join_team(player):
    form = JoinTeamForm()
    teams = get_team_invites(player)
    team_list = []
    for team in teams:
        team_list.append((str(team['teamid']), str(team['name'])))
    form.team.choices = team_list
    print(form.team.choices)
    if form.validate_on_submit():
        print("Validating")
        print(player, int(form.team.data), form.accept.data)
        success = accept_invite(player, int(form.team.data), int(form.accept.data))
        if success == 1:
            flash("Saved!", category='success')
            return render_template('base.html')
        else:
            print("Working")
            flash('Failed', category='danger')
            return render_template('join-team.html', form=form)
    else:
        flash("Dang it", category='danger')
    print("Not validating")
    return render_template('join-team.html', form=form)


@app.route('/contacts/<player>/create', methods=['GET', 'POST'])
def create_contact(player):
    form = CreateContactForm()
    if form.validate_on_submit():
        success, contact_id = add_contact(player, form.is_phone.data, form.contact.data)
        if success:
            print("Contact_id", contact_id)
            flash('Contact added!', category='success')
            return redirect(url_for('edit_notifications', contact_id=contact_id))
        else:
            flash('You\'re seriously screwed', category='danger')
            return render_template('create-contact.html', form=form)
    else:
        return render_template('create-contact.html', form=form)


@app.route('/contacts/<contact_id>', methods=['GET', 'POST'])
def edit_notifications(contact_id):
    form = NotificationForm()
    event_types = get_event_types()
    type_list = []
    for e_type in event_types:
        type_list.append((str(e_type['typeid']), e_type['description']))
    form.type.choices = type_list
    if form.validate_on_submit():
        print("Validated")
        exists = setting_exists(contact_id, form.type.data)[0][0]
        if exists:
            success = create_setting(contact_id, form.type.data, form.time.data)
        else:
            success = update_setting(contact_id, form.type.data, form.time.data)
        if success:
            flash('Setting saved', category='success')
            return render_template('create-contact.html', form=form)
        else:
            flash('You\'re seriously screwed', category='danger')
            return render_template('edit-notifications.html', form=form)
    else:
        flash("Not validating", category='danger')
        return render_template('edit-notifications.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
