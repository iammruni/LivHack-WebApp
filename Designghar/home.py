"""
Here we deal with the landing home page.
"""

import functools
from flask import (Blueprint,flash,g,redirect,render_template,request,url_for,session)


bp_home=Blueprint("home",__name__)

@bp_home.route("/home",methods=("GET","POST"))
def home():
    return render_template("index.html")
