# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 14:25:47 2016

@author: dfoley
"""

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length

class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me Logged in')
    submit = SubmitField('Log in')
    
    