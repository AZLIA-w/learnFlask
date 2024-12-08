from flask import Blueprint,render_template
from flask_login import login_required,current_user

views = Blueprint('views',__name__)

@views.route('/')
# wont't show homepage if not login
@login_required
def home():
    #check user login or not -> current_user
    return render_template("home.html",user = current_user)