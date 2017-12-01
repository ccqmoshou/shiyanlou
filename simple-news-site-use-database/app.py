#!/usr/bin/python3
# -*- coding:utf-8 -*-

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/shiyanlou'

db = SQLAlchemy(app)

class Files(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', uselist=False)
    content = db.Column(db.Text)

    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    files = db.relationship('Files')

    def __init__(self, name):
        self.name = name

def insert_datas():
    db.create_all()
    java = Category('Java')
    python = Category('Python')
    file1 = Files('Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
    file2 = Files('Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()

@app.route('/')
def index():
    return render_template('index.html', title_list=Files.query.all())


@app.route('/files/<int:file_id>')
def file(file_id):
    file_content = Files.query.get_or_404(file_id)
    return render_template('file.html', file_content=file_content)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
