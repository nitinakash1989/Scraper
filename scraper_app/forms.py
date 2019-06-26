# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 04:44:25 2019

@author: nitin
"""
from flask_wtf import FlaskForm
from wtforms import  SubmitField


class ScrapyForm(FlaskForm):
    "Form class with only one field."
    
    submit = SubmitField('Download Data')
