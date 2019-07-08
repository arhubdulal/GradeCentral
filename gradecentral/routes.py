#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 23:21:44 2019

@author: JustinChen
"""
from flask import Flask
from flask import render_template, redirect, flash, url_for, session, request
from gradecentral import app, db, bcrypt

from gradecentral.forms import searchForm, registerForm, loginForm
from gradecentral.models import User
from flask_login import login_user, current_user, logout_user, login_required
import gradecentral.Parser

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = registerForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.email.data}! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = loginForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'error')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')