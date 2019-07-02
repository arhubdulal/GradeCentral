#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 22:40:45 2019

@author: JustinChen
"""

from flask import Flask
from flask import render_template, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy

import Parser
from forms import searchForm, registerForm, loginForm
#%%
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fuck-this-shit'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

#%%
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    _classes = db.Column(db.String, nullable=False, server_default="00000") #IDs
    
    def __repr__(self):
        return f"User('{self.email}')"
    
    @property
    def classes(self):
        return [int(x) for x in self._classes.split(';')]
    @classes.setter
    def classes(self, value):
        self._classes += ';%s' % value

#%%
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/search", methods=['GET', 'POST'])
def search():
    form = searchForm()
    if form.validate_on_submit():
        results = Parser.getResults(Parser.htmlString(form.CLASS.data))
        results = [x.json for x in results]
        return render_template("searchResults.html", results=results)
    return render_template("search.html", title='Search', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = registerForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        if form.email.data == 'hi@gmail.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'error')
    return render_template('login.html', title='Login', form=form)
        
if __name__ == "main":
    app.run(debug=True)
      