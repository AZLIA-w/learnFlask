from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from website._init_ import db
# 此导入用于区别以登陆与未登录用户，决定navbar的展示内容，only login，sightUp，or，home，logout
from flask_login import login_user,login_required,logout_user,current_user


auth = Blueprint('auth',__name__)

@auth.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # 从database中取user
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('logged in successfully!!!',category='success')
                # 标记此user为以登陆
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Inccrrect password,try again',category='error')
        else:
            flash('Email does not exist',category='error')
    return render_template("login.html",user = current_user)

@auth.route('/sign_up',methods = ['GET','POST'])
def sign_up():    
    #只处理POST请求（request），即便上方methods中可接受get与post
    #直接刷新login界面以测试get请求；submit以测试post请求
    #旨在从用户输入中提取信息
    # post_data = request.form
    # print(post_data)
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('FirstName')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        # 从database中取user
        user = User.query.filter_by(email = email).first()
        if user:
            flash('Email alread exists',category='error')
        elif len(email) < 4:
            flash('email must be greater than 4 characters',category='error')
        elif len(firstName) < 2:
            flash('firstname must be greater than 2 characters',category='error')
        elif len(password) < 7:
            flash('password must be greater than 7 characters',category='error')           
        elif password2 != password:
            flash('password you entered twice not equal',category='error')           
        else :
            #add to database
            new_user  = User(email = email,first_name = firstName,password = generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            login_user(user,remember=True)
            flash('Account created!',category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html",user = current_user)

@auth.route('/logout')
# 此装饰器旨在确认当前是以登录状态，否则logout方法不生效
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
