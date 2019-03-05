"""
In this file we deal with the databases associated 
with the platform

Please Note: The databases defined and their respective uses
are stated here. while adding/removing/modifying any database please
change the documentation here accordingly.The databases are defined in thier respective
sql files.

1)A table named users_cus storing customer username and passwords
2)A table named users_des storing designer unsernames and passwords

"""

import sqlite3
import click
from flask import current_app,g
from flask.cli import with_appcontext


def get_db():
    if "db" not in g:
        g.db=sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory=sqlite3.Row

    return g.db

def close_db(e=None):
    db=g.pop("db",None)

    if db is not None:
        db.close()


#We define a script to initialize the databases
def init_db():
    db=get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))


#we define a command line function "init-db" that 
#calls init_db and dsiplays success message
@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database")



#we define a function that takes an app adn registers
#init_db_command and close db with the app
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    

