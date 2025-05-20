from flask import Flask,render_template,url_for,session,redirect,g,request,jsonify
from database import get_db,close_db
from flask_session import Session
from forms import RegistrationForm,LoginForm,ClassCommoditiesForm,AdminRegistrationForm,AdminLoginForm,AddProductForm,BuyForm
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
from datetime import datetime
from random import randint

"""this app of user and admin is free to register. However, there is user account,that bought something. (username:ting password:123)(admin name:admin password:123)"""

app=Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"]="this-is-my-secret-key"
app.config["UPLOAD_FOLDER"]='static/uploads'
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"

Session(app)

def turn_price_to_number(price):
    if price=="0~100":
        min_price=0
        max_price=100
    if price=="100~500":
        min_price=100
        max_price=500
    if price=="over 500":
        min_price=500
        max_price=9999999
    return min_price,max_price

@app.before_request
def load_logged_in_user():
    g.user=session.get("user_id",None)
    g.admin=session.get("admin_id",None)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args,**kwargs):
        if g.user is None:
            return redirect(url_for("login",next=request.url))
        return view(*args,**kwargs)
    return wrapped_view

def login_required2(view):
    @wraps(view)
    def wrapped_view(*args,**kwargs):
        if g.admin is None:
            return redirect(url_for("admin_login",next=request.url))
        return view(*args,**kwargs)
    return wrapped_view

@app.errorhandler(404)
def pag3e_no_found(error):
    return render_template("error.html"),404

@app.route("/admin_index",methods=["POST","GET"])
@login_required2
def admin_index():
    form=ClassCommoditiesForm()
    gender=form.gender.data
    price=form.price.data
    type=form.type.data  
    db=get_db()
    if gender !="all" and price!="all" and type!="all":
        min,max=turn_price_to_number(price)
        jewels=db.execute("""SELECT * FROM jewels
                          WHERE gender=? AND type=? AND price BETWEEN ? AND ?;""",(gender,type,min,max)).fetchall()
        
    elif gender !="all" and price=="all" and type=="all":

        jewels=db.execute("""SELECT * FROM jewels
                          WHERE gender=?;""",(gender,)).fetchall()
    elif type!="all" and gender=="all" and price=="all":

        jewels=db.execute("""SELECT * FROM jewels
                          WHERE type=?;""",(type,)).fetchall()
    elif price!="all" and gender=="all" and type=="all":
        min,max=turn_price_to_number(price)
        jewels=db.execute("""SELECT * FROM jewels
                          WHERE price BETWEEN ? and ?;""",(min,max)).fetchall()
    elif  gender !="all" and type !="all":
        jewels=db.execute("""SELECT * FROM jewels
                          WHERE type=? AND gender=?;""",(type,gender,)).fetchall()
    elif gender !="all" and price !="all":
        min,max=turn_price_to_number(price)
        jewels=db.execute("""SELECT * FROM jewels
                          WHERE gender=? AND price BETWEEN ? AND ?;""",(gender,min,max)).fetchall()
    elif type !="all" and price !="all":
        min,max=turn_price_to_number(price)
        jewels=db.execute("""SELECT * FROM jewels
                          WHERE type=? AND price BETWEEN ? AND ?;""",(type,min,max)).fetchall()
    else:
        jewels=db.execute("""SELECT * FROM jewels;""").fetchall()  
    return render_template("admin_index.html",jewels=jewels,form=form)

@app.route("/",methods=["POST","GET"])
def index():
    form=ClassCommoditiesForm()
    gender=form.gender.data
    price=form.price.data
    type=form.type.data  
    db=get_db()
    if gender !="all" and price!="all" and type!="all":
        min,max=turn_price_to_number(price)
        jewels=db.execute("""SELECT * FROM jewels
                          WHERE gender=? AND type=? AND price BETWEEN ? AND ?;""",(gender,type,min,max)).fetchall()
        
    elif gender !="all" and price=="all" and type=="all":

        jewels=db.execute("""SELECT * FROM jewels
                          WHERE gender=?;""",(gender,)).fetchall()
    elif type!="all" and gender=="all" and price=="all":

        jewels=db.execute("""SELECT * FROM jewels
                          WHERE type=?;""",(type,)).fetchall()
    elif price!="all" and gender=="all" and type=="all":
        min,max=turn_price_to_number(price)
        jewels=db.execute("""SELECT * FROM jewels
                          WHERE price BETWEEN ? and ?;""",(min,max)).fetchall()
    elif  gender !="all" and type !="all":
        jewels=db.execute("""SELECT * FROM jewels
                          WHERE type=? AND gender=?;""",(type,gender,)).fetchall()
    elif gender !="all" and price !="all":
        min,max=turn_price_to_number(price)
        jewels=db.execute("""SELECT * FROM jewels
                          WHERE gender=? AND price BETWEEN ? AND ?;""",(gender,min,max)).fetchall()
    elif type !="all" and price !="all":
        min,max=turn_price_to_number(price)
        jewels=db.execute("""SELECT * FROM jewels
                          WHERE type=? AND price BETWEEN ? AND ?;""",(type,min,max)).fetchall()
    else:
        jewels=db.execute("""SELECT * FROM jewels;""").fetchall()
           
    return render_template("index.html",jewels=jewels,form=form)



@app.route("/register",methods=["GET","POST"])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user_id=form.user_id.data
        password=form.password.data
        password2=form.password2.data
        db=get_db()
        conflict_user=db.execute(
            """SELECT* FROM users
                WHERE user_id=?;""",(user_id,)).fetchone()
        if conflict_user is not None:
            form.user_id.errors.append("Username already taken")
        else:
            db.execute("""INSERT INTO users(user_id,password)
                        VALUES(?,?);""",(user_id,generate_password_hash(password)))
            db.commit()
            return redirect(url_for("login"))
    return render_template("register.html",form=form)

@app.route("/admin_register",methods=["GET","POST"])
def admin_register():
    form=AdminRegistrationForm()
    if form.validate_on_submit():
        admin_id=form.admin_id.data
        password=form.password.data
        password2=form.password2.data
        db=get_db()
        conflict_user=db.execute(
            """SELECT* FROM admins
                WHERE admin_id=?;""",(admin_id,)).fetchone()
        if conflict_user is not None:
            form.admin_id.errors.append("Username already taken")
        else:
            db.execute("""INSERT INTO admins(admin_id,password)
                        VALUES(?,?);""",(admin_id,generate_password_hash(password)))
            db.commit()
            return redirect(url_for("admin_login"))
    return render_template("admin_register.html",form=form)

@app.route("/jewels")
def jewels():   
    db=get_db()
    jewels=db.execute("""SELECT * FROM jewels;""").fetchall()
    return render_template("jewels.html",jewels=jewels)



@app.route("/jewel/<int:jewel_id>")
def jewel(jewel_id):
    db=get_db()
    jewel=db.execute("""SELECT * FROM jewels
                        WHERE jewel_id=?;""",(jewel_id,)).fetchone()
    return render_template("jewel.html",jewel=jewel)

@app.route("/admin_product/<int:jewel_id>")
def admin_product(jewel_id):
    db=get_db()
    jewel=db.execute("""SELECT * FROM jewels
                        WHERE jewel_id=?;""",(jewel_id,)).fetchone()
    return render_template("admin_product.html",jewel=jewel)

@app.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user_id=form.user_id.data
        password=form.password.data
        db=get_db()
        user=db.execute("""SELECT * FROM users
                                WHERE user_id=?""",(user_id,)).fetchone()
        if user is  None:
            form.user_id.errors.append("No such user name!")
        elif not check_password_hash(user["password"],password):
            form.password.errors.append("Incorrect password!")
        else:
            session.clear()
            session["user_id"]=user_id
            next_page=request.args.get("next")
            if not next_page:
                next_page=url_for("index")
            return redirect(next_page)
    return render_template("login.html",form=form)

@app.route("/admin_login",methods=["GET","POST"])
def admin_login():
    form=AdminLoginForm()
    if form.validate_on_submit():
        admin_id=form.admin_id.data
        password=form.password.data
        db=get_db()
        admin=db.execute("""SELECT * FROM admins
                                WHERE admin_id=?""",(admin_id,)).fetchone()
        if admin is  None:
            form.admin_id.errors.append("No such admin name!")
        elif not check_password_hash(admin["password"],password):
            form.password.errors.append("Incorrect password!")
        else:
            session.clear()
            session["admin_id"]=admin_id
            next_page=request.args.get("next")
            if not next_page:
                next_page=url_for("admin_index")
            return redirect(next_page)
    return render_template("admin_login.html",form=form)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/cart",methods=["POST","GET"])
@login_required
def cart():

    if "cart" not in session:
        session["cart"]={}
    names={}
    db=get_db()
    itemNumber=0
    totalPrice=0
    for jewel_id in session["cart"]:
        jewel=db.execute("""SELECT * FROM jewels
                            WHERE jewel_id=?;""",(jewel_id,)).fetchone()
        itemNumber+=session["cart"][jewel_id]
        totalPrice+=jewel["price"]*session["cart"][jewel_id]
        name=jewel["name"]
        names[jewel_id]=name   
    return render_template("cart.html",cart=session["cart"],names=names,itemNumber=itemNumber,totalPrice=totalPrice)
    
@app.route("/add_to_cart/<int:jewel_id>")
@login_required
def add_to_cart(jewel_id):
    if "cart" not in session:
        session["cart"]={}
    if jewel_id not in session["cart"]:
        session["cart"][jewel_id]=1
    else:
        session["cart"][jewel_id] +=1
    session.modified=True
    return redirect(url_for("cart"))

@app.route("/sub_to_cart/<int:jewel_id>")
@login_required
def sub_to_cart(jewel_id):
    if "cart" not in session:
        session["cart"]={}
    elif session["cart"][jewel_id]>1:
        session["cart"][jewel_id] -=1
    else:
        del session["cart"][jewel_id]
    session.modified=True
    return redirect(url_for("cart"))

@app.route("/del_to_cart/<int:jewel_id>")
@login_required
def del_to_cart(jewel_id):   
    del session["cart"][jewel_id]
    session.modified=True
    return redirect(url_for("cart"))

@app.route("/management")
@login_required2
def management():
    form=ClassCommoditiesForm()
    gender=form.gender.data
    price=form.price.data
    type=form.type.data  
    db=get_db()
    if gender !="all" and price!="all" and type!="all":
        min,max=turn_price_to_number(price)
        jewels=db.execute("""SELECT * FROM jewels
                          WHERE gender=? AND type=? AND price BETWEEN ? AND ?;""",(gender,type,min,max)).fetchall()
        
    elif gender !="all" and price=="all" and type=="all":

        jewels=db.execute("""SELECT * FROM jewels
                          WHERE gender=?;""",(gender,)).fetchall()
    elif type!="all" and gender=="all" and price=="all":

        jewels=db.execute("""SELECT * FROM jewels
                          WHERE type=?;""",(type,)).fetchall()
    elif price!="all" and gender=="all" and type=="all":
        min,max=turn_price_to_number(price)
        jewels=db.execute("""SELECT * FROM jewels
                          WHERE price BETWEEN ? and ?;""",(min,max)).fetchall()
    elif  gender !="all" and type !="all":
        jewels=db.execute("""SELECT * FROM jewels
                          WHERE type=? AND gender=?;""",(type,gender,)).fetchall()
    elif gender !="all" and price !="all":
        min,max=turn_price_to_number(price)
        jewels=db.execute("""SELECT * FROM jewels
                          WHERE gender=? AND price BETWEEN ? AND ?;""",(gender,min,max)).fetchall()
    elif type !="all" and price !="all":
        min,max=turn_price_to_number(price)
        jewels=db.execute("""SELECT * FROM jewels
                          WHERE type=? AND price BETWEEN ? AND ?;""",(type,min,max)).fetchall()
    else:
        jewels=db.execute("""SELECT * FROM jewels;""").fetchall()   
    return render_template("management.html",jewels=jewels,form=form)



@app.route("/add_stock/<int:jewel_id>")
def add_stock(jewel_id):
    db=get_db()
    stock=db.execute("""SELECT * FROM jewels
                            WHERE jewel_id=?;""",(jewel_id,)).fetchone()
    stock=stock["stock"]
    add_stock=stock+1
    db=get_db()
    db.execute("""UPDATE jewels
                    SET stock=?
                    WHERE jewel_id=?;""",(add_stock,jewel_id))
    db.commit()
    next_page=request.args.get("next")
    if not next_page:
        next_page=url_for("admin_product",jewel_id=jewel_id)
        return redirect(next_page)
@app.route("/sub_stock/<int:jewel_id>")
def sub_stock(jewel_id):
    message=""
    db=get_db()
    stock=db.execute("""SELECT * FROM jewels
                            WHERE jewel_id=?;""",(jewel_id,)).fetchone()
    stock=stock["stock"]

    if stock>0:
        add_stock=stock-1
        db=get_db()
        db.execute("""UPDATE jewels
                        SET stock=?
                        WHERE jewel_id=?;""",(add_stock,jewel_id))
        db.commit()
    else:
        message="Stock cannot be less than 0"
    next_page=request.args.get("next")
    if not next_page:
        next_page=url_for("admin_product",jewel_id=jewel_id)
        return redirect(next_page)

@app.route("/add_new_product",methods=["POST","GET"])
def add_new_product():
    form=AddProductForm()
    name=form.name.data
    price=form.price.data
    type=form.type.data
    gender=form.gender.data
    description=form.description.data
    stock=form.stock.data
    if price is not None:
        try:           
            price=float(price)
        except ValueError:
            price=None
    if stock is not None:
        try:           
            stock=int(stock)
        except ValueError:
            stock=None
    
    db=get_db()
    name_conflict=db.execute("""SELECT * FROM jewels
                                WHERE name=?;""",(name,)).fetchone()
    if form.validate_on_submit():
        if name_conflict is not None:
            form.name.errors.append("You have owned the same product,please user other product name!")
            return render_template("add_new_product.html",form=form)
        elif price<0:
            form.price.errors.append("please enter a right price!")
            return render_template("add_new_product.html",form=form)
        elif stock<0:
            form.stock.errors.append("please enter a right stock!")
            return render_template("add_new_product.html",form=form)
        else:
            db.execute("""INSERT INTO jewels(name,price,type,gender,description,stock)
                        VALUES(?,?,?,?,?,?);""",(name,price,type,gender,description,stock))
            db.commit()
            return redirect(url_for("admin_index"))
    
    return render_template("add_new_product.html",form=form)

@app.route("/sold_out/<int:jewel_id>")
def sold_out(jewel_id):
    db=get_db()
    db.execute("""DELETE FROM jewels
                WHERE jewel_id=?;""",(jewel_id,))
    db.commit()
    next_page=request.args.get("next")
    if not next_page:
        next_page=url_for("admin_index",jewel_id=jewel_id)
        return redirect(next_page)
    
@app.route("/guest_information",methods=["POST","GET"])
def guest_information():
    form=BuyForm()
    user_id=session["user_id"] 
    time=datetime.now().strftime("%H:%M:%S %d-%m-%y")
    order_id=randint(99000,99999)
    if form.validate_on_submit(): 
        address=form.address.data
        phone=form.phone_number.data
        cart=session["cart"]

        
        for jewel_id,number in cart.items():
            db=get_db()
            jewel=db.execute("""SELECT * FROM jewels
                             WHERE jewel_id=?;""",(jewel_id,)).fetchone()
            jewel_name=jewel["name"]
            jewel_price=jewel["price"]
            order_sum=jewel_price*number
            db.execute("""INSERT INTO orders(order_id,user_id,jewel_id,jewel_name,jewel_price,order_sum,phone,address,number)
                    VALUES(?,?,?,?,?,?,?,?,?);""",(order_id,user_id,jewel_id,jewel_name,jewel_price,order_sum,phone,address,number))
            db.commit()
        session["cart"]={}
        return redirect(url_for("index"))
    return render_template("guest_information.html",form=form)

@app.route("/order")
@login_required
def order():
    big_orders=[]
    db=get_db()
    user_id=session["user_id"]
    order_ids=db.execute("""SELECT DISTINCT(order_id) FROM orders""").fetchall()
    
    for order_id in order_ids:
        db=get_db()
        order=db.execute("""SELECT * FROM orders
                        WHERE user_id=? AND order_id=?;""",(user_id,order_id['order_id'])).fetchall()
        big_orders.append(order)
    return render_template("order.html",big_orders=big_orders,order_ids=order_ids)

@app.route("/admin_order")
@login_required2
def admin_order():
    big_orders=[]
    db=get_db()

    order_ids=db.execute("""SELECT DISTINCT(order_id) FROM orders""").fetchall()
    
    for order_id in order_ids:
        db=get_db()
        order=db.execute("""SELECT * FROM orders
                        WHERE  order_id=?;""",(order_id['order_id'],)).fetchall()
        big_orders.append(order)
    return render_template("admin_order.html",big_orders=big_orders,order_ids=order_ids)

@app.route("/order_detail/<int:order_id>")
def order_detail(order_id):
    db=get_db()
    orders=db.execute("""SELECT * FROM orders
                        WHERE  order_id=?;""",(order_id,)).fetchall()

    return render_template("order_detail.html",orders=orders)



@app.route("/admin_order_detail/<int:order_id>")
def admin_order_detail(order_id):
    db=get_db()
    orders=db.execute("""SELECT * FROM orders
                        WHERE  order_id=?;""",(order_id,)).fetchall()

    return render_template("admin_order_detail.html",orders=orders)




    return render_template("order_detail.html")
