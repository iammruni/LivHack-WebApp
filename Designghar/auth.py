"""
Here we define the authentication function.the script reads 
data from the html doc and depending on whether the user is
a customer or a designer-accordingly stores data in the respective
database.

There are two pages that come under authentication:
1)Login
2)Register


"""



import functools
from flask import (Blueprint,flash,g,redirect,render_template,request,url_for,session)
from werkzeug.security import generate_password_hash, check_password_hash
from Designghar.db import get_db

bp_auth=Blueprint("auth",__name__,url_prefix="/auth")


"""
Here we define the register function.
Note: We check whether the customer is a desginer/customer 
      depending which we insert the data into the respective database

"""

@bp_auth.route("/register",methods=("GET","POST"))
def register():
    if request.method=="POST":
        username=request.form["name"]
        password=request.form["pass"]
        mail=request.form["email"]
        mobno=request.form["phone"]
        designation=request.form["desig"] #we check whether the person is a customer or designer
        db=get_db()
        error=None
        user="users_cus" if designation=="Customer" else "users_des"

        if not username:
            error="Username is required"
        elif not password:
            error="Password is required"
        elif not designation:
            error="Please chose your role"
        elif  db.execute(
            "SELECT id FROM {0} WHERE username=?".format(user),(username,)).fetchone() is not None:
            error="Username already taken"

        if error is None:
            db.execute(
                "INSERT INTO {0} (username, password,mail,mobno) VALUES (?,?,?,?)".format(user),
                (username,generate_password_hash(password),mail,mobno)
            )  
            db.commit()
            flash("WELCOME!")
            return redirect(url_for("auth.login"))  
        
        flash(error)

    return render_template("auth/register.html")    




#*********************Register function done*********************#


"""
Here we define the login function
Note: 1)We run queries in BOTH databases to search for the username.
        We use a check statement in between the queries to reduce computaional cost if possible
        (Change documentation/other code if this part is changed)

      2)For successful logins, we redirect them to their respective index
        pages. For failures, we reload

"""

@bp_auth.route("/login",methods=("GET","POST"))
def login():
    if request.method=="POST":
        username=request.form["your_name"]
        password=request.form["your_pass"]
        db=get_db()
        error=None
        found_in="users_cus"
        
        user=db.execute(
            "SELECT * FROM users_cus WHERE username=?",(username,)
        ).fetchone()

        if user== None:
            user=db.execute(
                "SELECT * FROM users_des WHERE username=?",(username,)
            ).fetchone()
            found_in="users_des"


        if user ==None:
            error="Incorrect Username"
        elif not check_password_hash(user["password"],password):
            error="Incorrect Password"


        if error==None:
            session.clear()
            session["user_id"]=user["id"]
            if found_in=="users_cus":
                return redirect(url_for("index/customer.html"))
            else:
                return redirect(url_for("index/designer.html")) 

        
        flash(error)

    return render_template("auth/login.html")    

#******************Login views finished***************************

"""
INCOMPLETE: The webpage doesnt load the user's information and makes it available to 
other views, if they are already logged in
"""     



#The Logout code:
@bp_auth.route("/logout")
def  logout():
    session.clear()
    return redirect(url_for("home"))



"""
We define a decorator to check whether the user is logged in or not
i.e. when any view is passed to it returns a wrapped view that checks for 
login
"""

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)    
    return weapped_view

