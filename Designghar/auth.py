"""
In this file we define a blueprint for registration/login
on both customer and designer side

"""
import functools
from flask import (Blueprint,flash,g, redirect,render_template,request,
session,url_for
)
from werkzeug.security import check_password_hash,generate_password_hash
from Designghar.db import get_db


bp_auth=Blueprint("auth",__name__,url_prefix="/auth")


"""
We define 2 registration views:
1) Registration for customer
2)Registration for designer

Note: we redirect to login page after successful registration
      else we render the reg. page with error msg
"""
@bp_auth.route("/register/customer",methods=("GET","POST"))
def register_cust():
    if request.method =="POST":
        username=request.form["username"]
        password=request.form["password"]
        db=get_db()
        error=None

        if not username:
            error="Username is required"
        elif not password:
            error="Password is required" 
        elif db.execute("SELECT id FROM user_cus WHERE username=?",(username,)).fetchone() is not None:
            error="User {} is already registered".format(suername)

        if error is None:
            db.execute("INSERT INTO user_cus (username,password) VALUES (?,?)",(username,generate_password_hash(password)))
            db.commit()
            return redirect(url_for("auth.login"))

        flash(error)
    return render_template("auth/register/customer.html")   


@bp_auth.route("/register/designer",methods=("GET","POST"))
def register_des():
    if request.method =="POST":
        username=request.form["username"]
        password=request.form["password"]
        db=get_db()
        error=None

        if not username:
            error="Username is required"
        elif not password:
            error="Password is required"
        elif db.execute("SELECT id FROM user_des WHERE username=?",(username,)).fetchone() is not None:
            error="Username {} already taken.".format(username)

        if  error is None:
            db.execute("INSERT INTO user_des (username,password) VALUES (?,?)",(username,generate_password_hash(password))) 
            db.commit()
            return redirect(url_for("auth.login"))    

        flash(error)

    return render_template("auth/register/designer.html")        
    
