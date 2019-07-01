#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 21:10:08 2019

@author: JustinChen
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

#%%

class searchForm(FlaskForm):
    CLASS = StringField('Item', validators=[DataRequired()])
    submit = SubmitField('Search')
    
class registerForm(FlaskForm):
    email = StringField('Email*',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password*', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password*',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class loginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')