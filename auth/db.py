# https://flask.palletsprojects.com/en/2.2.x/tutorial/database

# TODO: set a google OAuth client ID on the server

"""
This file is support some basic database functionality and user management.
Maybe later it also will be store posts.
"""

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """
    This method is used to connect to the request.
    """

    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            "sqlite_db", detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Closed before the response is sent.
    """

    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """
    This method just run the SQL commands to the db.py file.
    """

    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    """
    Clear the existing data and create new tables.
    """

    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
