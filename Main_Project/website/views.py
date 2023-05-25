from flask import Blueprint, render_template, request, flash, redirect, jsonify
from flask_login import login_required, current_user
from .models import *
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
     if request.method == 'POST':
        Name = request.form.get('Name')
        Price = request.form.get('Price')
        Producer = request.form.get('Producer')
        description = request.form.get('description')
        prod = Product.query.order_by(Product.date_modified).all()
        product = Product.query.filter_by(Name=Name).first()
        if product:
            flash('Product already exists.', category='error')
        elif len(Name) < 1:
            flash('Enter a valid Name.', category='error')
        elif Price.isnumeric() ==False:
            flash('Enter a Valid Price.', category='error')
        elif len(description) < 1:
            flash('Enter a Vlid description.', category='error')
        elif len(Producer) < 1:
            flash('Enter a Vlid Producer.', category='error')
        else:
            new_product = Product(Name=Name , Price=Price, Producer=Producer, description=description, Admin_id=current_user.id)
            db.session.add(new_product)
            db.session.commit()
            flash('The Product was added Successfully!', category='success')
            prod = Product.query.order_by(Product.date_modified).all()
            return render_template('home.html', products=prod, user=current_user)
     return render_template("home.html", user=current_user, products=prod)


@views.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    product = Product.query.get(id)
    prod = Product.query.order_by(Product.date_modified).all()  
    if request.method == 'POST':
        product.Name = request.form['Name']
        product.Price = request.form['Price']
        product.Producer = request.form['Producer']
        product.description = request.form['description']

        if len(product.Name ) < 1:
            flash('Enter a valid Name.', category='error')
        elif product.Price.isnumeric() ==False:
            flash('Enter a Valid Price.', category='error')
        elif len(product.description) < 1:
            flash('Enter a Vlid description.', category='error')
        elif len(product.Producer) < 1:
            flash('Enter a Vlid Producer.', category='error')
        else:
            try:
                db.session.commit()
                flash('The Product has Updated Successfully', category='success')
                prod = Product.query.order_by(Product.date_modified).all()
                return render_template('home.html', products=prod, user=current_user)
            except:
                flash('There was an issue updating your task', category='error')
                return 

    return render_template('update.html', Products=product, products=prod, user=current_user)


@views.route('/delete/<int:id>')
@login_required
def delete(id):
    product_to_delete = Product.query.get_or_404(id)
    prod = Product.query.order_by(Product.date_modified).all()
    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        flash('The Product has deleted Successfully', category='success')
        prod = Product.query.order_by(Product.date_modified).all()
        return render_template('home.html', products=prod, user=current_user)
    except:
        flash('There was a problem deleting that task', category='error')
        return 
    
    return render_template("home.html", user=current_user, products=prod)


@views.route('/support', methods=['GET', 'POST'])
@login_required
def support():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Comment is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("support.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
