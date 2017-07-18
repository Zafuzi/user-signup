#!/usr/bin/env python
from flask import Flask, request, render_template, url_for, Session
from livereload import Server, shell
import re

__author__ = "Zachary Foutz"
__copyright__ = "Copyright 2017, Kitsap Developers"
__credits__ = ["Zachary Foutz", "Launchcode"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Zachary Foutz"
__email__ = "contact@kitsapdevelopers.com"
__status__ = "Production"

app = Flask(__name__)
app.debug = True

server = Server(app)
server.watch('/templates/*.html', '/static/styles/*.css', 'main.py')

@app.route("/styles")
def styles():
    """ Routes static stylesheet assest """
    return url_for('static', filename='style.css')

@app.route("/")
def index():
    """ Routes to main page if no post method """
    return render_template('index.html',
                                name = "",
                                username = "",
                                email = "",
                                logged_in = False,
                                username_is_valid = True,
                                password_is_valid = True,
                                email_is_valid = True)
# Routes to main page if post method
@app.route("/", methods=['POST'])
def signup():
    # Grab username, password, confirmation password, and email from form
    username = request.form['username']
    pass1 = request.form['pass1']
    pass2 = request.form['pass2']
    email = request.form['email']

    name = ""
    logged_in = False
    password_is_valid = False
    username_is_valid = False
    email_is_valid = True
    passwords_match = False

    # If a username and both passwords were found in the form
    if username and pass1 and pass2:
        # and if both passwords match
        if pass1 == pass2:
            passwords_match = True
            # as long as there are no spaces in the username or password
            # then username and password are valid
            if ' ' not in username:
                name = username
                username_is_valid = True
                logged_in = False
                
            if ' ' not in pass1:
                password_is_valid = True
                if username_is_valid:
                    logged_in = True
            else:
                logged_in = False

            # if an email was found then validate it and log in
            if email:
                # regex to check for valid email if not valid, do not login
                reg_ex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
                if re.match(reg_ex, email) == None:
                    email_is_valid = False
                    logged_in = False
            
                    

    return render_template('index.html',
                            name = name,
                            username = username,
                            email = email,
                            logged_in = logged_in,
                            password_is_valid = password_is_valid,
                            username_is_valid = username_is_valid,
                            email_is_valid = email_is_valid,
                            passwords_match = passwords_match)

server = Server(app.wsgi_app)
server.serve()