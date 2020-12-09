from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from . import db

item = Blueprint('item', __name__)

# add user id to the route
@item.route('/additem', methods=['POST'])
def item_post():
    new_name = request.form.get('fname')
    new_estate = request.form.get('estate')
    new_acceptGap = request.form.get('agap')

    # filter it by the user id pass in the link 
    user = User.query.filter_by(email=email).first()

    # do the lookup here

    # pass in to the home page item list

    return redirect(url_for('main.profile'))