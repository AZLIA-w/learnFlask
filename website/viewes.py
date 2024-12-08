from flask import Blueprint,render_template,request,flash,jsonify
from flask_login import login_required,current_user
from .models import Note,db
# use for delete note;cause note are sort as form,but json are recommanded
import json


views = Blueprint('views',__name__)

@views.route('/',methods = ['GET','POST'])
# wont't show homepage if not login
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!',category='error')
        else:
            new_note = Note(data = note,user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added',category='success')
    #check user login or not -> current_user
    return render_template("home.html",user = current_user)

@views.route('/delete-note',methods= ['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note :
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    # 因为语法需求，返回空字典
    return jsonify({})