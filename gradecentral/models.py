#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 21:10:08 2019

@author: JustinChen
"""
from gradecentral import db, login_manager
from flask_login import UserMixin

#%%
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#%%
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    _classes = db.Column(db.String(60)) #IDs
    
    def __repr__(self):
        return f"User('{self.email}')"
    
    
    @property
    def classes(self):
        return [int(x) for x in self._classes.split(';')]
    @classes.setter
    def classes(self, value):
        if self._classes == None:
            self._classes = str(value)
        else:
            self._classes += ';%s' % value