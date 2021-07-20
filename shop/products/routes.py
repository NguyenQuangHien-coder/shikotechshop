from flask import render_template,session, request,redirect,url_for,flash,current_app
from shop import app,db,photos, search
from .models import Category,Brand,Addproduct
from .forms import Addproducts
import secrets
import os


def brands():
    
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands

def categories():
    
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return categories



@app.route('/')
def home():
    page = request.args.get('page',1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=8)
    return render_template('products/index.html', products=products,brands=brands(),categories=categories())

@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword, fields=['name','desc'] , limit=6)
    return render_template('products/result.html',products=products,brands=brands(),categories=categories())

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template('products/single_page.html',product=product,brands=brands(),categories=categories())




@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page',1, type=int)
    get_brand = Brand.query.filter_by(id=id).first_or_404()
    brand = Addproduct.query.filter_by(brand=get_brand).paginate(page=page, per_page=8)
    return render_template('products/index.html',brand=brand,brands=brands(),categories=categories(),get_brand=get_brand)


@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page',1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproduct.query.filter_by(category=get_cat).paginate(page=page, per_page=8)
    return render_template('products/index.html',get_cat_prod=get_cat_prod,brands=brands(),categories=categories(),get_cat=get_cat)


@app.route('/addbrand',methods=['GET','POST'])
def addbrand():
    if 'email' not in session:
        flash(f'Vui lòng đăng nhập trước','danger')
        return redirect(url_for('login'))
    if request.method =="POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'Thương hiệu {getbrand} đã được thêm','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', title='Add brand',brands='brands')

@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Vui lòng đăng nhập trước','danger')
        return redirect(url_for('login'))
    if 'email' not in session:
        flash('Vui lòng đăng nhập','danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method =="POST":
        updatebrand.name = brand
        flash(f'Thương hiệu {updatebrand.name} được đổi thành {brand}','success')
        db.session.commit()
        return redirect(url_for('brands'))
    brand = updatebrand.name
    return render_template('products/addbrand.html', title='Udate brand',brands='brands',updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=['GET','POST'])
def deletebrand(id):
    if 'email' not in session:
        flash(f'Vui lòng đăng nhập trước','danger')
        return redirect(url_for('login'))
    brand = Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        flash(f"Thương hiệu {brand.name} đã được xóa","success")
        db.session.commit()
        return redirect(url_for('brands'))
    flash(f"Thương hiệu {brand.name} không thể xóa","warning")
    return redirect(url_for('admin'))

@app.route('/addcat',methods=['GET','POST'])
def addcat():
    if 'email' not in session:
        flash(f'Vui lòng đăng nhập trước','danger')
        return redirect(url_for('login'))
    if request.method =="POST":
        getcat = request.form.get('category')
        category = Category(name=getcat)
        db.session.add(category)
        flash(f'Danh mục {getcat} đã được thêm','success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html', title='Add category')


@app.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Vui lòng đăng nhập trước','danger')
        return redirect(url_for('login'))
    if 'email' not in session:
        flash('Vui lòng đăng nhập','danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')  
    if request.method =="POST":
        updatecat.name = category
        flash(f'Danhh mục {updatecat.name} đã được đổi tên thành {category}','success')
        db.session.commit()
        return redirect(url_for('categories'))
    category = updatecat.name
    return render_template('products/addbrand.html', title='Update cat',updatecat=updatecat)



@app.route('/deletecat/<int:id>', methods=['GET','POST'])
def deletecat(id):
    if 'email' not in session:
        flash(f'Vui lòng đăng nhập trước','danger')
        return redirect(url_for('login'))
    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        flash(f"Danh mục {category.name} đã được xóa","success")
        db.session.commit()
        return redirect(url_for('categories'))
    flash(f"Danh mục {category.name} không thể xóa","warning")
    return redirect(url_for('admin'))


@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
    if 'email' not in session:
        flash(f'Vui lòng đăng nhập trước','danger')
        return redirect(url_for('login'))
    form = Addproducts(request.form)
    brands = Brand.query.all()
    categories = Category.query.all()
    if request.method=="POST"and 'image_1' in request.files:
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.discription.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        addproduct = Addproduct(name=name,price=price,discount=discount,stock=stock,colors=colors,desc=desc,category_id=category,brand_id=brand,image_1=image_1,image_2=image_2,image_3=image_3)
        db.session.add(addproduct)
        flash(f'Sản phẩm {name} đã được thêm','success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', form=form, title='Add a Product', brands=brands,categories=categories)




@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updateproduct(id):
    if 'email' not in session:
        flash(f'Vui lòng đăng nhập trước','danger')
        return redirect(url_for('login'))
    form = Addproducts(request.form)
    product = Addproduct.query.get_or_404(id)
    brands = Brand.query.all()
    categories = Category.query.all()
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method =="POST":
        product.name = form.name.data 
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data 
        product.colors = form.colors.data
        product.desc = form.discription.data
        product.category_id = category
        product.brand_id = brand
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        flash('Cập nhật sản phẩm thành công','success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.discription.data = product.desc
    brand = product.brand.name
    category = product.category.name
    return render_template('products/addproduct.html', form=form, title='Update Product',getproduct=product, brands=brands,categories=categories)


# @app.route('/deleteproduct/<int:id>', methods=['POST'])
# def deleteproduct(id):
#     product = Addproduct.query.get_or_404(id)
#     if request.method =="POST":
#         try:
#             os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
#             os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
#             os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
#         except Exception as e:
#             print(e)
#         db.session.delete(product)
#         db.session.commit()
#         flash(f'The product {product.name} was delete from your record','success')
#         return redirect(url_for('admin'))
#     flash(f'Can not delete the product','success')
#     return redirect(url_for('admin'))

#DELETE PRODUCT
@app.route('/deleteproduct/<int:id>', methods=['GET','POST'])
def deleteproduct(id):
    if 'email' not in session:
        flash(f'Vui lòng đăng nhập trước','danger')
        return redirect(url_for('login'))
    product = Addproduct.query.get_or_404(id)
    if request.method=="POST":
        #Unlink old image before update
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))               
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))              
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))               
        except Exception as e:
            print(e)
                
        db.session.delete(product)
        db.session.commit()
        flash(f"Sản phẩm {product.name} đã được xóa","success")
        return redirect(url_for('admin'))
    flash(f"Sản phẩm {product.name} không thể xóa","warning")
    return redirect(url_for('admin'))