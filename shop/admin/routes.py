from shop.customers.model import CustomerOrder
from flask import render_template,session, request,redirect,url_for,flash
from flask_login import login_required, current_user, logout_user, login_user
from shop import app,db,bcrypt
from .forms import RegistrationForm,LoginForm
from .models import User
from shop.products.models import Addproduct,Category,Brand
from shop.customers.model import CustomerOrder, Register

#ADMIN
@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Vui lòng đăng nhập trước','danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title='Admin page',products=products)

#REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'email' not in session:
        flash(f'Vui lòng đăng nhập trước','danger')
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        flash(f'Đăng ký tài khoản admin {form.name.data} thành công','success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('admin/register.html',title='Register user', form=form)

#LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Tài khoản admin {form.email.data} đăng được sử dụng','success')
            return redirect(url_for('admin'))
        else:
            flash(f'Sai Email hoặc mật khẩu', 'success')
            return redirect(url_for('login'))
    return render_template('admin/login.html',title='Login page',form=form)

#BRAND
@app.route('/brands')
def brands():
    if 'email' not in session:
        flash(f'Vui lòng đăng nhập trước','danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title='brands',brands=brands)

#CATEGORY
@app.route('/categories')
def categories():
    if 'email' not in session:
        flash(f'Vui lòng đăng nhập trước','danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title='categories',categories=categories)

#ORDER
@app.route('/showorders')
def showorders():
    if 'email' not in session:
        flash(f'Vui lòng đăng nhập trước','danger')
        return redirect(url_for('login'))
    orders = CustomerOrder.query.order_by(CustomerOrder.id.desc()).all()
    return render_template('admin/showorder.html', title='orders',orders=orders)


# @app.route('/orderdetail/<int:id>/<string:invoice>')
# def orderdetail(id, invoice):
#     if 'email' not in session:
#         flash(f'Vui lòng đăng nhập trước','danger')
#         return redirect(url_for('login'))
#     order_id = CustomerOrder.query.get_or_404(id)
#     invoice = CustomerOrder.query.get_or_404(invoice)
#     orders = CustomerOrder.query.filter_by(id = order_id, invoice = invoice).order_by(CustomerOrder.id.desc()).all()
#     return render_template('admin/orderdetail.html', title='orderdetail', orders = orders, order_id = order_id, invoice = invoice)

#ORDER DETAILS
@app.route('/orderdetail/<invoice>')
def orderdetail(invoice):
    grandTotal = 0
    subTotal = 0   
    orders = CustomerOrder.query.filter_by(invoice=invoice).order_by(CustomerOrder.id.desc()).first()
    customer = Register.query.filter_by(id=orders.customer_id).first()
    
    for _key, product in orders.orders.items():
        discount = (product['discount']/100) * float(product['price'])
        subTotal += float(product['price']) * int(product['quantity'])
        subTotal -= discount
        tax = ("%.2f" % (.06 * float(subTotal)))
        grandTotal = ("%.2f" % (1.06 * float(subTotal)))

    return render_template('admin/orderdetail.html', invoice=invoice, tax=tax,subTotal=subTotal,grandTotal=grandTotal,orders=orders, customer = customer)

#DELETE ORDER
@app.route('/deleteorder/<int:id>', methods=['GET','POST'])
def deleteorder(id):
    if 'email' not in session:
        flash(f'Vui lòng đăng nhập trước','danger')
        return redirect(url_for('login'))
    order = CustomerOrder.query.get_or_404(id)
    if request.method=="POST":         
        db.session.delete(order)
        db.session.commit()
        flash(f"Hóa đơn {order.invoice} đã được xóa","success")
        return redirect(url_for('showorders'))
    flash(f"Sản phẩm {order.invoice} không thể xóa","warning")
    return redirect(url_for('showorders'))



#LOGOUT ADMIN
@app.route('/adminlogout')
def adminlogout():
    session.clear()
    return redirect('admin')

