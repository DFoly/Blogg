# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 13:56:38 2016

@author: dfoley
"""

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views