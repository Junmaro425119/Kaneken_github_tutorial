from datetime import datetime,date

from flask import Flask,render_template,request,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy

from __init__ import app,db

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(30),nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime,nullable=False)

@app.route('/')
def show_entries():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            print('ユーザー名が異なります')

        elif request.form['password'] != app.config['PASSWORD']:
            print('パスワードが異なります')

        else:
            session['logged_in'] = True
            return redirect('/')
    return render_template('login.html')                

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    return redirect('/')        

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.due).all()
        return render_template('index.html',posts=posts,today=date.today())

    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due') 

        due = datetime.strptime(due, '%Y-%m-%d')
        new_post = Post(title=title,detail=detail,due=due)

        db.session.add(new_post)
        db.session.commit()

        return redirect('/')

@app.route('/create')
def create():
    return render_template('create.html')    

@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)
    return render_template('detail.html',post=post)     

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html',post=post)
        #updateページへ

    else:
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'),'%Y-%m-%d')

        db.session.commit()
        return redirect('/') 



@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')