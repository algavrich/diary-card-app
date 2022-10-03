"""CRUD functions."""

from model import (SentReminder, db, connect_to_db, User, Urge, Action,
                   DiaryEntry, UrgeEntry, ActionEntry, MedEntry)
import helpers
from datetime import date, datetime, timedelta
from sqlalchemy import cast, DATE
from random import randint, choice
import math

# CREATE

def create_user(
        fname: str, email: str, password: str,
        phone_number: str, entry_reminders: bool,
        med_tracking: bool, med_reminders: bool) -> User:
    """Create and return a new user.
    
    Takes in user data (preferences),
    returns User object based on given data.

    """

    user = User(
        fname=fname,
        email=email, 
        password=password, 
        phone_number=phone_number, 
        entry_reminders=entry_reminders, 
        med_tracking=med_tracking, 
        med_reminders=med_reminders
    )

    return user


def create_urge(user_id: int, description: str) -> Urge:
    """Create and return a new urge.
    
    Takes in a user's ID and a short description of the urge that they
    want to track,
    returns Urge object with their ID and given description.

    """

    urge = Urge(
        user_id=user_id, 
        description=description,
        active = True
    )

    return urge


def create_action(user_id: int, description: str) -> Action:
    """Create and return a new action.
    
    Takes in a user's ID and a short description of the action that they
    want to track,
    returns Action object with their ID and given description.
    
    """

    action = Action(
        user_id=user_id, 
        description=description,
        active = True
    )

    return action


def create_account_helper(
        fname: str, email: str, password: str, phone_number: str,
        entry_reminders: bool, med_tracking: bool,
        med_reminders: bool, urge_1: str, urge_2: str, urge_3: str,
        action_1: str, action_2: str) -> None:
    """Create new User, Urge, and Action objects and commit to database.
    
    Takes in all information necessary to initialize a user,
    instantiates a User using create_user and adds to database,
    makes lists of Urge and Action instances with the user's descriptions,
    and adds those to the database as well.

    """

    new_user = create_user(fname, email, password, phone_number,
                           entry_reminders, med_tracking, 
                           med_reminders)

    db.session.add(new_user)
    db.session.commit()

    new_user = get_user_by_email(email)
    new_urges = []
    new_actions = []

    for urge in [urge_1, urge_2, urge_3]:
        new_urges.append(create_urge(new_user.user_id, urge))

    for action in [action_1, action_2]:
        new_urges.append(create_action(new_user.user_id, action))

    db.session.add_all(new_urges)
    db.session.add_all(new_actions)
    db.session.commit()


def create_diary_entry(
        user_id: int, dt: datetime, sad_score: int,
        angry_score: int, fear_score: int, happy_score: int,
        shame_score: int, skills_used: int) -> DiaryEntry:
    """Create and return a new diary entry.
    
    Takes in all of the information needed for a User object,
    instantiates and returns a User object.

    """

    d_entry = DiaryEntry(
        user_id=user_id, 
        dt=dt, 
        sad_score=sad_score, 
        angry_score=angry_score, 
        fear_score=fear_score, 
        happy_score=happy_score, 
        shame_score=shame_score, 
        skills_used=skills_used
    )

    return d_entry


def create_urge_entry(
        urge_id: int, d_entry_id: int, user_id: int,
        dt: datetime, score: int) -> UrgeEntry:
    """Create and return a new urge entry.

    Takes in all of the information needed for an urge entry,
    instantiates and returns an UrgeEntry object.

    """

    u_entry = UrgeEntry(
        urge_id=urge_id, 
        d_entry_id=d_entry_id,
        user_id=user_id, 
        dt=dt,
        score=score
    )

    return u_entry


def create_action_entry(
        action_id: int, d_entry_id: int, user_id: int,
        dt: datetime, score: int) -> ActionEntry:
    """Create and return a new action entry.
    
    Takes in all of the information needed for an action entry,
    instantiates and returns an ActionEntry object.
    
    """

    a_entry = ActionEntry(
        action_id=action_id, 
        d_entry_id=d_entry_id, 
        user_id=user_id, 
        dt=dt,
        score=score
    )

    return a_entry


def create_d_u_a_entries_helper(
        user_id: int, sad_score: int, angry_score: int,
        fear_score: int, happy_score: int, shame_score: int,
        urge_1_score: int, urge_2_score: int, urge_3_score: int,
        action_1: bool, action_2: bool, used_skills: int) -> None:
    """Create new Diary, Urge, and Action entries and commit to database.
    
    Takes in all of the information needed to make a set of
    DiaryEntry, UrgeEntry, and ActionEntry objects,
    instantiates them using helper functions,
    and adds and commits them to the database.
    
    """

    new_d_entry = create_diary_entry(
        user_id,
        datetime.now(),
        sad_score,
        angry_score,
        fear_score,
        happy_score,
        shame_score,
        used_skills
    )

    db.session.add(new_d_entry)
    db.session.commit()

    new_d_entry = get_diary_entry_by_user_date(
        user_id, 
        date.today()
    )

    user_urges = get_urges_by_user_id(user_id)
    urge_scores = [urge_1_score, urge_2_score, urge_3_score]
    new_entries = []
    for i in range(3):
        new_entries.append(create_urge_entry(
            user_urges[i].urge_id, 
            new_d_entry.entry_id, 
            user_id,
            datetime.now(),
            urge_scores[i]
        ))

    user_actions = get_actions_by_user_id(user_id)
    action_scores = [action_1, action_2]
    for i in range(2):
        new_entries.append(create_action_entry(
            user_actions[i].action_id,
            new_d_entry.entry_id,
            user_id,
            datetime.now(),
            action_scores[i]
        ))

    db.session.add_all(new_entries)
    db.session.commit()


def add_med_entry_to_db(user_id: int) -> None:
    """Create and commit new MedEntry to database."""

    m_entry = MedEntry(
        user_id=user_id, 
        dt=datetime.now()
    )

    db.session.add(m_entry)
    db.session.commit()


def add_new_rem_to_db(user_id: int) -> None:
    """Create a new SentReminder object and commit it to database.
    
    Takes in a user ID,
    calls create_sent_rem to instantiate a SentReminder,
    adds and commits that object to the database.
    
    """

    new_reminder = SentReminder(
        user_id=user_id,
        dt=datetime.now()
    )

    db.session.add(new_reminder)
    db.session.commit()

# READ

def get_user_by_id(user_id: int) -> User:
    """Return user with given ID."""

    return User.query.get(user_id)


def get_user_by_email(email: str) -> User:
    """Return user with given email."""

    return User.query.filter(User.email == email).first()


def get_users_entry_reminders() -> list[User]:
    """Return all users who opted in to entry reminders."""

    return User.query.filter(User.entry_reminders == True).all()


# def get_users_med_reminders():
#     """Return all users who opted in to med reminders."""

#     return User.query.filter(User.med_reminders == True).all()


# def get_fav_trend_by_user_id(user_id):
#     """Return user's favorite trend when given their ID."""

#     user = get_user_by_id(user_id)

#     return user.fav_trend


# def get_diary_entries_by_user_id(user_id: int) -> list[DiaryEntry]:
#     """Return list of user's diary entries when given their ID.
    
#     Takes in a user's ID,
#     returns a list of all of that user's DiaryEntry objects.
    
#     """

#     user = get_user_by_id(user_id)
    
#     return user.diary_entries


# def get_med_entries_by_user_id(user_id):
#     """Return list of user's med entries when given their ID."""

#     user = get_user_by_id(user_id)
    
#     return user.med_entries


def get_urges_by_user_id(user_id: int) -> list[Urge]:
    """Return a list of user's urges when given their ID."""

    user = get_user_by_id(user_id)
    active_urges = []
    for urge in user.urges:
        if urge.active:
            active_urges.append(urge)

    return active_urges


def get_actions_by_user_id(user_id: int) -> list[Action]:
    """Return a list of user's actions when given their ID."""

    user = get_user_by_id(user_id)
    active_actions = []
    for action in user.actions:
        if action.active:
            active_actions.append(action)

    return active_actions


def get_urge_desc_by_id(urge_id: int) -> str:
    """Return urge description when given it's ID."""

    return db.session.query(
        Urge.description
    ).filter(
        Urge.urge_id == urge_id
    ).first()[0]


def get_action_desc_by_id(action_id: int) -> str:
    """Return action description when given it's ID."""

    return db.session.query(
        Action.description
    ).filter(
        Action.action_id == action_id
    ).first()[0]


def get_urge_by_id(urge_id: int) -> Urge:
    """Return Urge object with given ID."""

    return Urge.query.get(urge_id)


def get_action_by_id(action_id: int) -> Action:
    """Return Action object with given ID."""

    return Action.query.get(action_id)


def get_diary_entry_by_user_date(user_id: int, q_date: date) -> DiaryEntry:
    """Return a user's diary entry for a given date."""

    return DiaryEntry.query.filter(
        DiaryEntry.user_id == user_id,
        cast(DiaryEntry.dt, DATE) == q_date
    ).first()


def get_given_week_for_user(
        user_id: int, start_date: date) -> list[DiaryEntry]:
    """Return user's entries for the week with the given start date."""

    entries = []

    for i in range(7):
        date_get = start_date + timedelta(days=(i))
        diary_entry = get_diary_entry_by_user_date(user_id, date_get)
        if diary_entry:
            entries.append(diary_entry)
        else:
            entries.append(None)

    return entries

def get_this_week_for_user(user_id: int) -> list[DiaryEntry]:
    """Return a list of a user's entries for the past week.
    
    Takes in a user's ID,
    calls get_given_week_for_user starting at 6 days ago
    to get the past week,
    returns the resulting list.
    
    """

    return get_given_week_for_user(
        user_id, (date.today() - timedelta(days=6))
    )


def check_entry_today(user_id: int) -> bool:
    """Return True if user made an entry already, False if not."""

    if get_diary_entry_by_user_date(user_id, date.today()):
        return True

    return False


def check_entry_past_24(user_id: int) -> bool:
    """Return True if user made an entry in the past day, False if not."""

    if DiaryEntry.query.filter(
        DiaryEntry.user_id == user_id,
        DiaryEntry.dt > (datetime.now() - timedelta(days=1))
    ).first():
        return True

    return False


def check_med_entry_today(user_id: int) -> bool:
    """Return True if user made a med entry today, False if not."""

    if MedEntry.query.filter(
        MedEntry.user_id == user_id,
        cast(MedEntry.dt, DATE) == date.today()
    ).first():
        return True

    return False


def check_for_reminder(user_id: int) -> bool:
    """Return True if user has been reminded in the past day, False if not."""

    if SentReminder.query.filter(
        SentReminder.user_id == user_id,
        SentReminder.dt > (datetime.now() - timedelta(days=1))
    ).first():
        return True

    return False


def get_dict_for_weeks(user_id: int) -> dict:
    """Return dictionary representing the weeks from first entry to now.
    
    Takes in a user's ID,
    returns a dictionary of strings representing the start dates
    of every week since the week of the oldest entry.
    
    """
    
    oldest_entry = DiaryEntry.query.filter(
        DiaryEntry.user_id == user_id
    ).order_by(
        DiaryEntry.dt
    ).first()
    todays_date = date.today()

    if not oldest_entry or ((datetime.now() - oldest_entry.dt).days < 7):
        week_start_date = (todays_date - timedelta(days=6))
        start_date_string1 = date.strftime(
            week_start_date,
            "%d_%m_%Y"
        )
        start_date_string2 = date.strftime(
            week_start_date,
            "%b %-d"
        )

        return {
            start_date_string1: f"Week of {start_date_string2}"
        }

    else:
        earliest_date = datetime.date(oldest_entry.dt)
        days_diff = todays_date - earliest_date
        num_weeks = math.ceil(days_diff.days/7)

        weeks = {}

        for i in range(num_weeks):
            week_start_date = (todays_date - timedelta(weeks=(i), days=6))
            start_date_string1 = date.strftime(
                week_start_date,
                "%d_%m_%Y"
            )
            start_date_string2 = date.strftime(
                week_start_date,
                "%b %-d"
            )
            weeks[start_date_string1] = f"Week of {start_date_string2}"

        return weeks


def get_given_week_for_user_from_date_string(
        user_id: int, date_string: str) -> list[DiaryEntry]:
    """Return list of a user's entries for the week with given start date.
    
    Takes in a user's ID and a string representation of a date,
    returns a list of DiaryEntry objects for the week with that start date.
    
    """

    start_date = datetime.date(datetime.strptime(date_string, "%d_%m_%Y"))

    return get_given_week_for_user(user_id, start_date)

# UPDATE

def update_today_entry(
        current_user_id: int, sad_score: int, angry_score: int,
        fear_score: int, happy_score: int, shame_score: int,
        urge_1_score: int, urge_2_score: int, urge_3_score: int,
        action_1: bool, action_2: bool, used_skills: int) -> None:
    """Updates Diary, Urge, and Action entries for the current day."""
    
    current_d_entry = get_diary_entry_by_user_date(
        current_user_id, 
        date.today()
    )

    new_u_scores = [
        urge_1_score,
        urge_2_score,
        urge_3_score
    ]
    current_u_entries = current_d_entry.urge_entries

    new_a_scores = [
        action_1,
        action_2
    ]
    current_a_entries = current_d_entry.action_entries

    current_d_entry.sad_score = sad_score
    current_d_entry.angry_score = angry_score
    current_d_entry.fear_score = fear_score
    current_d_entry.happy_score = happy_score
    current_d_entry.shame_score = shame_score
    current_d_entry.sad_score = sad_score
    current_d_entry.skills_used = used_skills

    for i in range(3):
        current_u_entries[i].score = new_u_scores[i]

    for i in range(2):
        current_a_entries[i].score = helpers.convert_radio_to_bool(new_a_scores[i])

    db.session.commit()


def update_user(
        user_id: int, fname: str, email: str,
        phone_number: str, entry_reminders: bool,
        med_tracking: bool, med_reminders: bool) -> None:
    """Update User record for user with given user_id."""

    user = get_user_by_id(user_id)
    
    user.fname = fname
    user.email = email
    user.phone_number = phone_number
    user.entry_reminders = entry_reminders
    user.med_tracking = med_tracking
    user.med_reminders = med_reminders

    db.session.commit()


def update_urge(user_id: int, old_urge_id: int, new_urge_desc: str) -> None:
    """Create new Urge record for new urge and deactivate old one."""
  
    old_urge_record = get_urge_by_id(old_urge_id)

    if old_urge_record.description != new_urge_desc:
        new_urge_record = create_urge(user_id, new_urge_desc)
        old_urge_record.active = False
        db.session.add(new_urge_record)
        db.session.commit()


def update_action(
        user_id: int, old_action_id: int, new_action_desc: str) -> None:
    """Create new Action record for new action and deactivate old one."""

    old_action_record = get_action_by_id(old_action_id)

    if old_action_record.description != new_action_desc:
        new_action_record = create_action(user_id, new_action_desc)
        old_action_record.active = False
        db.session.add(new_action_record)
        db.session.commit()


def update_password(user_id: int, new_password: str) -> None:
    """Update User's password attribute and commit to database."""

    current_user = get_user_by_id(user_id)
    current_user.password = new_password
    db.session.commit()

# POPULATE TEST DATABASE

def example_data() -> None:
    """Add example data to DB for Lucy's user."""

    lucy = create_user(
    "Lucy", "annalgav@gmail.com", "password",
    "5108469189", True, False, False)
    db.session.add(lucy)
    db.session.commit()

    urges = []
    for i in range(3):
            urges.append(create_urge(1, f"Urge {i}"))
    db.session.add_all(urges)

    actions = []
    for j in range(2):
        actions.append(create_action(1, f"Action {j}"))
    db.session.add_all(actions)
    db.session.commit()

    for k in range(30, 0, -1):
        dt = datetime.now() - timedelta(days=(k - 1))

        diary_entry = create_diary_entry(
            1, dt, randint(0, 5), randint(0, 5), randint(0, 5),
            randint(0, 5), randint(0, 5), randint(0, 5))
        db.session.add(diary_entry)
        db.session.commit()

        current_date = dt.date()
        diary_entry = get_diary_entry_by_user_date(1, current_date)
        d_entry_id = diary_entry.entry_id
        urge_entries = []
        for m in range(3):
            urge_entries.append(
                create_urge_entry(
                    (m + 1), d_entry_id, 1, dt, randint(0, 5)
                )
            )
        db.session.add_all(urge_entries)

        action_entries = []
        for n in range(2):
            action_entries.append(
                create_action_entry(
                    (n + 1), d_entry_id, 1, dt, choice([True, False])
                )
            )
        db.session.add_all(action_entries)
        db.session.commit()



if __name__ == '__main__':
    from server import app
    connect_to_db(app, db_uri="postgresql:///test-db")