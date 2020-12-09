from flask import Blueprint, render_template, redirect, request, flash, current_app
from flask_login import login_required, current_user
from .models import User, Item
from . import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
import os
from werkzeug.utils import secure_filename

class NameForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    budget = DecimalField(validators=[DataRequired()])
    estate = DecimalField(validators=[DataRequired()])
    submit = SubmitField('Confirm')

class ItemForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    price = DecimalField(validators=[DataRequired()])
    link = StringField(validators=[DataRequired()])
    submit = SubmitField('Confirm')

class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Confirm')

main = Blueprint('main', __name__)

start_index = 0
numOfItem = 0

@main.route('/')
@login_required
def index():
    user = User.query.get(current_user.id)
    items = user.items.all()
    full_filename = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.profile_pic)
    total_spent = 0
    global numOfItem
    numOfItem = len(items)
    
    return render_template('index.html', 
                        name = current_user.name, 
                        estate = current_user.estate,
                        items = items,
                        start = start_index,
                        end = start_index + 11,
                        numOfItem = len(items),
                        profile = full_filename,
                        budget = current_user.budget,
                        remaining = current_user.remaining)

@main.route('/inc')
def inc():
    global start_index
    if numOfItem - start_index > 11:
        start_index += 11
        print(numOfItem - start_index)
    return redirect('/final_proj_1')

@main.route('/dec')
def dec():
    global start_index
    if start_index == 0:
        return redirect('/final_proj_1')
    start_index -= 11
    return redirect('/final_proj_1')

@main.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = ItemForm()
    item_update = Item.query.get_or_404(id)

    if form.validate_on_submit():
        if request.method == "POST":
            user = User.query.get(current_user.id)
            new_estate = int(user.estate) - int(request.form['price']) + int(item_update.price)
            new_remaining = int(user.remaining) - int(request.form['price']) + int(item_update.price)
            user.estate = new_estate
            user.remaining = new_remaining

            item_update.name = request.form['name']
            item_update.price = request.form['price']
            item_update.link = request.form['link']
            try:
                db.session.commit()
                return redirect('/final_proj_1')
            except :
                return "there was an error updating your item"
    else:
        return render_template('update.html', form=form, item_update=item_update)

@main.route('/delete/<int:id>')
@login_required
def delete(id):
    item_delete = Item.query.get_or_404(id)

    try:
        user = User.query.get(current_user.id)
        new_estate = int(user.estate) + int(item_delete.price)
        new_remaining = int(user.remaining) + int(item_delete.price)
        user.estate = new_estate
        user.remaining = new_remaining

        db.session.delete(item_delete)
        db.session.commit()
        return redirect('/final_proj_1')
    except:
        return "there was an error deleting your ingredient"

@main.route('/profile', methods=["POST", "GET"])
@login_required
def profile():
    form = NameForm()
    form2 = ItemForm()
    form3 = PhotoForm()
    # add upload image here

    if request.method == "POST":
        if form.validate_on_submit() or form2.validate_on_submit() or form3.validate_on_submit():
            if form2.validate_on_submit():
                itemName = request.form['name']
                price = request.form['price']
                link = request.form['link']
                new_item = Item(name = itemName, price = price, link = link, user_id = current_user.id)
                db.session.add(new_item)

                user = User.query.get(current_user.id)
                new_estate = int(user.estate) - int(price)
                new_remaining = int(user.remaining) - int(price) 
                user.estate = new_estate
                user.remaining = new_remaining

            if form.validate_on_submit():
                name = request.form['name']
                budget = request.form['budget']
                estate = request.form['estate']
                # user = User.query.filter_by(id=current_user.id).first()
                current_user.name = name
                current_user.estate = estate
                current_user.budget = budget
                current_user.remaining = budget
            
            if form3.validate_on_submit():
                filename = secure_filename(form3.photo.data.filename)
                print(current_app.config['UPLOAD_FOLDER'] + filename)
                form3.photo.data.save(current_app.config['UPLOAD_FOLDER'] + '\\' + filename)
                user = User.query.get(current_user.id)
                user.profile_pic = filename

        else:
            flash('Please validate your input')
            print('Please validate your input')
            return redirect('/final_proj_1/profile')
        
        try:
            db.session.commit()
            return redirect('/final_proj_1/profile')
        except:
            return "there was an error updating"
    else:
        user = User.query.get(current_user.id)
        return render_template('profile.html', 
                                name=current_user.name, 
                                profile = current_app.config['UPLOAD_FOLDER'] + '\\' + current_user.profile_pic, 
                                form = form, form2 = form2, form3 = form3, current_user = user)

# add method here to add item