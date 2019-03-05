"""
Here, we build the applicaation factory
1)Any configuration, registration, and other setup the application 
needs will happen inside the function, then the application will be returned.
2) It also tells python to treat Designghar as a package
"""

#Importing packages
import os
from flask import Flask


def create_app(test_config=None):
    #In this funtion we create and configure the app

    app=Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path,"Designghar.sqlite")

    )
    if test_config is None:
        #if test config is none , we load instance config if it exits
        app.config.from_pyfile("config.py",silent=True)
    else:
        #load the test config if passed in
        app.config.from_mapping(test_config)
    
    #We have to ensure the instance folder exits
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass


    #We write a simple page that says hello cause polite
    @app.route("/hello")
    def hello():
        return "Hello World!"


    #we import and call the home function to render homepage
    from . import home
    app.register_blueprint(home.bp_home)

    #we import and call init_app to register the database 
    from  . import db
    db.init_app(app)

    #we import and register the authentication blueprint with the app
    from . import auth
    app.register_blueprint(auth.bp_auth)

    return app 
            
