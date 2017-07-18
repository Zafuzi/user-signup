from flask import Flask, request, render_template, url_for, Session
from livereload import Server, shell
import re



app = Flask(__name__)
app.debug = True

server = Server(app)
server.watch('/templates/*.html', '/static/styles/*.css', 'main.py')

@app.route("/styles")
def styles():
    return url_for('static', filename='style.css')


@app.route("/")
def index():
    return render_template('index.html', name="", logged_in = False, username_is_valid = True, password_is_valid = True, email_is_valid = True)

@app.route("/", methods=['POST'])
def signup():
    username = request.form['username']
    pass1 = request.form['pass1']
    pass2 = request.form['pass2']
    email = request.form['email']

    name = ""
    logged_in = False
    password_is_valid = False
    username_is_valid = False
    email_is_valid = True

    if username and pass1 and pass2:
        if pass1 == pass2:
            if ' ' in username == False and ' ' in pass1 == False:
                name = username
                username_is_valid = True
                password_is_valid = True

                if email:
                    reg_ex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
                    if re.match(reg_ex, email) == None:
                        email_is_valid = False
                    else:
                        logged_in = True
                else:
                    logged_in = True

    return render_template('index.html', name = name, logged_in = logged_in, password_is_valid = password_is_valid, username_is_valid = username_is_valid, email_is_valid = email_is_valid)

server = Server(app.wsgi_app)
server.serve()