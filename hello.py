# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 10:29:01 2016

@author: dfoley
// be careful wtform import Form is wrong
"""
import os
from flask import Flask, render_template, redirect, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form 
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_script import Shell
from flask_migrate import Migrate, MigrateCommand


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app) 
bootstrap = Bootstrap(app)
moment = Moment(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

def make_shell_context():
    return dict(app=app,db=db,User=user,Role=Role)
    
manager.add_command('shell', Shell(make_context=make_shell_context))

@app.route('/index', methods = ['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form = form,
                           name = session.get('name'),
                            known = session.get('known', False),
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
    

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    users = db.relationship('User', backref = 'role')
    
    def __repr__(self):
        return '<Role %r>' % self.name
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return 'User %r' % self.username

    
if __name__ == '__main__':
    #app.run(debug=True)
    manager.run()