from flask_login import UserMixin

from db import get_db


class User(UserMixin):
    """
    This class has methods to get an existing user
    from the database and create a new user.

    Methods:
    ---------------
    get():
        Get an existing user from db.
    create():
        Create a new user if this user not in db.
    """

    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        """
        Get an existing user from database.

        :return user: existing user
        """

        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id),
            ).fetchone()
        if not user:
            return None
        
        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
            )
        return user

    @staticmethod
    def create(id_, name, email, profile_pic):
        """
        Create a new user if this user not in database.
        """

        db = get_db()
        db.execute(
            "INSERT INTO user (id, name, email, profile_pic) "
            "VALUES (?, ?, ?, ?)",
            (id_, name, email, profile_pic),
        )        
        db.commit()
        