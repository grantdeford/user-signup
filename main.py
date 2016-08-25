#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

signup_form = """
<DOCTYPE html>
<html>
    <head>
    <title>Signup Assignment 3(2) LC109WF</title>
        </head>
<body>
    <h2>Signup:</h2>
    <form method = "POST">

    <label>Username
        <input type = "text" name = "username" value = "%(username)s">
        <span style = "color: red">%(error_un)s</span>
            </label>
    <br>
    <label>Password
        <input type = "password" name = "password" value = "">
        <span style = "color: red">%(error_pwd)s</span>
            </label>
    <br>
    <label>Verify Password
        <input type = "password" name = "verify" value = "">
        <span style = "color: red">%(error_verify)s</span>
            </label>
    <br>
    <label>Email (optional)
        <input type = "text" name = "email" value = "%(email)s">
        <span style = "color: red">%(error_email)s</span>
            </label>
    <br>
    <input type = "submit">
        </form>
    </body>
</html>
"""
#value for password left open"" ?
welcome_form = """
<DOCTYPE html>
<html>
    <head>
        <title>Welcome Assignment 3(2) LC109WF</title>
            </head>
<body>
    <h2>Welcome, %s!</h2>
    </body>
</html>
"""

def escape_html(s):
    return cgi.escape(s, quote = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]$")

#(s)?
def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASS_RE.match(password)

def valid_email(email):
    if email:
        return EMAIL_RE.match(email)
    else:
        return ""

def valid_verify(verify):
    if verify == password:
        return verify


class SignupHandler(webapp2.RequestHandler):
#are my passwords supposed to be in write form?
    def write_form(self, username = "", error_un = "", password = "", error_pwd = "" ),
                        verify = "", error_verify = "", email = "", error_email = ""):
        self.response.out.write(signup_form % {"username": escape_html(username),
                                                "error_un": error_un,
                                                "password": escape_html(password),
                                                "error_pwd": error_pwd,
                                                "verify": escape_html(verify),
                                                "error_verify":  error_verify,
                                                "email": escape_html(email),
                                                "error_email": error_email })

    def get(self):
        self.write_form()

    def post(self):
#Uda named form values for valid input
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        un = valid_username(username)
        pwd = valid_password(password)
        el = valid_email(email)
        vy = valid_verify(verify)

        error_un = ""
        error_pwd = ""
        error_verify = ""
        error_email = ""

        if not un:
            error_un = "That's not a valid username."
        if not pwd:
            error_pwd = "That's not a valid password."
        elif not vy:
            error_verify = "Your passwords didn't match."
        if not el:
            error_email = "That's not a valid email."

        if not(un, and pwd, and verify, and email):
            self.write_form(username, error_un, "", error_pwd, "", error_verify,
                            email, error_email)
        else:
            self.redirect('/signup')
#passwords out of self.write_form?            


class WelcomeHandler(webapp2.RequestHandler):

    def get(self):
        username = self.request.get("username")
        self.response.out.write(welcome_form % username)

app = webapp2.WSGIApplication([
    ('/signup', SignupHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
