#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 22:40:45 2019

@author: JustinChen
"""

from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

import Parser

#%%

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fuck-this-shit'

class searchForm(FlaskForm):
    CLASS = StringField('Item', validators=[DataRequired()])


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
    return render_template("search.html", form=form)
        
if __name__ == "main":
    app.run(debug=True)
      