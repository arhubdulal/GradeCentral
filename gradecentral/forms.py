#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 23:28:41 2019

"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from gradecentral.models import User

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
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email already exists. Please log in or choose a different email.')

class loginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
