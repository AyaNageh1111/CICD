from flask import Blueprint, render_template, request, flash, redirect, jsonify, url_for, session
from flask_login import login_required, current_user
import flask_msearch
from .models import *
from . import db, Search
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    page = request.args.get('page',1, type=int)
    brands = Brand.query.all()
    categories = Category.query.all()
    products =Product.query.order_by(Product.id.desc()).all()
    return render_template('index copy.html',user=current_user, products=products,brands=brands,categories=categories)


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

@views.route('/admin')
@login_required
def admin():
    products =Product.query.order_by(Product.id.desc()).all()
    print(products)
    return render_template('index.html',user=current_user, title='Admin page',products=products)


#__________________________________________________Cart_______________________________________

def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))

@views.route('/addcart', methods=['POST'])
@login_required
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        color = request.form.get('colors')
        product = product.query.filter_by(id=product_id).first()

        if request.method =="POST":
            DictItems = {product_id:{'name':product.name,'price':float(product.price),'discount':product.discount,'color':color,'quantity':quantity,'image':product.image_1, 'colors':product.colors}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
              
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@views.route('/carts')
@login_required
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('views.home'))
    subtotal = 0
    grandtotal = 0
    for key,product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax =("%.2f" %(.06 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))
    return render_template('carts.html',tax=tax, grandtotal=grandtotal,brands=brands(),categories=categories())

@views.route('/updatecart/<int:code>', methods=['POST'])
@login_required
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method =="POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key , item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Item is updated!')
                    return redirect(url_for('views.getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('views.getCart'))

@views.route('/deleteitem/<int:id>')
@login_required
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('views.home'))
    try:
        session.modified = True
        for key , item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('views.getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('views.getCart'))

@views.route('/clearcart')
@login_required
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('views.home'))
    except Exception as e:
        print(e)

#__________________________________________________Brands____________________________________
@views.route('/brands')
def brands():
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('brand.html',user=current_user, title='brands',brands=brands)

@views.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page',1, type=int)
    brands = Brand.query.all()
    categories = Category.query.all()
    get_brand = Brand.query.filter_by(id=id).first_or_404()
    get_brand_prod = Product.query.filter_by(brand=get_brand).paginate(page=page, per_page=8)
    return render_template('index.html',user=current_user,products=get_brand_prod,brands=brands,categories=categories,get_brand=get_brand)

@views.route('/addbrand',methods=['GET','POST'])
def addbrand():
    if request.method =="POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} was added to your database','success')
        db.session.commit()
        return redirect(url_for('views.brands'))
    return render_template('addbrand.html',user=current_user, title='Add brand',brands='brands')

@views.route('/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method =="POST":
        updatebrand.name = brand
        flash(f'The brand {updatebrand.name} was changed to {brand}','success')
        db.session.commit()
        return redirect(url_for('views.brands'))
    brand = updatebrand.name
    return render_template('addbrand.html',user=current_user, title='Udate brand',brands='brands',updatebrand=updatebrand)

@views.route('/deletebrand/<int:id>', methods=['GET','POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        flash(f"The brand {brand.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('views.brands'))
    flash(f"The brand {brand.name} can't be  deleted from your database","warning")
    return redirect(url_for('views.brands'))

#_________________________________________________Categories__________________________
@views.route('/categories')
def categories():
    products = Product.query.order_by(Product.id.desc()).all()
    print(products)
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('brand.html',user=current_user, title='categories',categories=categories)

@views.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page',1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Product.query.filter_by(category=get_cat).paginate(page=page, per_page=8)
    return render_template('index.html',user=current_user,products=get_cat_prod,brands=brands(),categories=categories(),get_cat=get_cat)

@views.route('/addcat',methods=['GET','POST'])
def addcat():
    if request.method =="POST":
        getcat = request.form.get('category')
        category = Category(name=getcat)
        db.session.add(category)
        flash(f'The brand {getcat} was added to your database','success')
        db.session.commit()
        return redirect(url_for('views.categories'))
    return render_template('addbrand.html',user=current_user, title='Add category')

@views.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')  
    if request.method =="POST":
        updatecat.name = category
        flash(f'The category {updatecat.name} was changed to {category}','success')
        db.session.commit()
        return redirect(url_for('views.categories'))
    category = updatecat.name
    return render_template('addbrand.html',user=current_user, title='Update cat',updatecat=updatecat)

@views.route('/deletecat/<int:id>', methods=['GET','POST'])
def deletecat(id):
    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        flash(f"The brand {category.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('views.categories'))
    flash(f"The brand {category.name} can't be  deleted from your database","warning")
    return redirect(url_for('views.categories'))

#_________________________________________________Products__________________________
@views.route('/result')
def result():
    brands = Brand.query.all()
    categories = Category.query.all()
    searchword = request.args.get('q')
    products = Product.query.filter_by(Name=searchword)
    return render_template('result.html',user=current_user, products=products,brands=brands,categories=categories)

@views.route('/product/<int:id>')
def single_page(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Product.query.get_or_404(id)
    return render_template('single_page.html',user=current_user ,product=product,brands=brands,categories=categories)

@views.route('/addproduct', methods=['GET','POST'])
def addproduct():
     brands = Brand.query.all()
     categories = Category.query.all()
     if request.method == 'POST':
        Name = request.form.get('Name')
        Price = request.form.get('Price')
        Producer = request.form.get('Producer')
        description = request.form.get('description')
        discount =  request.form.get('discount')
        stock =  request.form.get('stock')
        colors =  request.form.get('colors') 
        brand = request.form.get('brand')
        category = request.form.get('category')

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
        elif len(colors) < 1:
            flash('Enter a Vlid Colors', category='error')
        elif len(discount) < 1 and len(discount) > 3:
            flash('Enter a Vlid Answer for Discount.', category='error')
        elif stock.isnumeric() ==False:
            flash('Enter a Valid stock.', category='error')
        else:
            new_product = Product(Name=Name , Price=Price, Producer=Producer, description=description,
                                  colors=colors,
                                  stock=stock,
                                  category_id=category,
                                  brand_id=brand,
                                  Admin_id=current_user.id)
            db.session.add(new_product)
            db.session.commit()
            flash('The Product was added Successfully!', category='success')
            products = Product.query.order_by(Product.date_modified).all()
            return render_template('index copy.html', products=products, user=current_user, brands=brands,categories=categories)
     return render_template("addproduct.html", user=current_user, title='Add a Product', brands=brands,categories=categories)

@views.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updateproduct(id):
    product = Product.query.get_or_404(id)
    brands = Brand.query.all()
    categories = Category.query.all()
    prod = Product.query.order_by(Product.date_modified).all()  
    if request.method == 'POST':
        product.Name = request.form['Name']
        if request.form['Price'].isnumeric() ==False:
            flash('Enter a Valid Price.', category='error')
        else:
            product.Price = request.form['Price']
            product.Producer = request.form['Producer']
            product.description = request.form['description']
            product.stock = request.form['stock']
            product.colors= request.form['colors'] 
            product.brand_id= request.form.get('brand')
            product.category_id= request.form.get('category')
            if len(product.Name ) < 1:
                flash('Enter a valid Name.', category='error')
            elif len(product.description) < 1:
                flash('Enter a Vlid description.', category='error')
            elif len(product.Producer) < 1:
                flash('Enter a Vlid Producer.', category='error')
            elif len(product.colors) < 1:
                flash('Enter a Vlid Producer.', category='error')
            elif len(product.discount) < 1 and len(product.discount) > 3:
                flash('Enter a Vlid Answer for Discount.', category='error')
            elif product.stock.isnumeric() ==False:
                flash('Enter a Valid stock.', category='error')
            else:
                try:
                    db.session.commit()
                    flash('The Product has Updated Successfully', category='success')
                    prod = Product.query.order_by(Product.date_modified).all()
                    return redirect(url_for('views.admin'))
                except:
                    flash('There was an issue updating your task', category='error')
                    return redirect(url_for('views.admin'))

    return render_template('update.html', Products=product, products=prod, user=current_user, brands=brands,categories=categories)

@views.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Product.query.get_or_404(id)
    if request.method =="POST":
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.Name} was delete from your record','success')
        return redirect(url_for('views.admin'))
    flash(f'Can not delete the product','success')
    return redirect(url_for('views.admin'))


