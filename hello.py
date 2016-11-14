# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 10:29:01 2016

@author: dfoley
// be careful wtform import Form is wrong
"""
from flask import Flask, render_template, redirect, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form 
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)



@app.route('/index', methods = ['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Have you changed your name?')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form = form, name = session.get('name'),
                           current_time = datetime.utcnow())
    
    
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name = name,
                           current_time = datetime.utcnow())
    

@app.errorhandler(404)
def page_not_Found(e):
    return render_template('404.html'), 404
    
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


class NameForm(Form):
    name = StringField('What is your name?', validators = [DataRequired()])
    submit = SubmitField('Submit')
    

    
if __name__ == '__main__':
    app.run(debug=True)