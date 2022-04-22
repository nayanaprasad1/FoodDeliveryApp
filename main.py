from cs50 import SQL
import sqlite3
from flask_session import Session
from flask import Flask, render_template, redirect, request, session, jsonify
from datetime import datetime
from instamojo_wrapper import Instamojo
# # Instantiate Flask object named app
app = Flask(__name__, static_url_path='/static')

# # Configure sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Creates a connection to the database
db = SQL ( "sqlite:///projectDB.db" )


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/userhome")
def home1():
    return render_template("userhome.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/adminlogin")
def adminlogin():
    return render_template("adminlogin.html")

@app.route("/adminhome")
def adminhome():
    return render_template("adminhome.html")

@app.route('/checkadmin',methods=["POST"])
def checkadmin():
    name=request.form["aname"]
    password=request.form["apwd"]

    if name=="admin" and password=="12345":
        return render_template("adminhome.html")
    else:
        return "Invalid Credentials"

@app.route("/add", methods=["POST"])
def add():
    t=""
    if request.method=="POST":
        try:
            a = request.form["username"]
            b = request.form["gender"]
            c = request.form["email"]
            d = request.form["mobile"]
            e = request.form["password"]
            with sqlite3.connect("projectDB.db") as con:
                cur = con.cursor()
                cur.execute("insert into users (name,gender,email,phone,password) values (?,?,?,?,?)", (a, b, c, d, e))
                con.commit()
            session["uname"] = request.form.get("username")
        except Exception as err:
            con.rollback()
            t="Can't be registered {}".format(err)
        finally:
            return render_template("home.html")

@app.route("/verify",methods=["POST"])
def verify():
    email=request.form["uemail"]
    password=request.form["pwd"]
    p=""
    try:
        with sqlite3.connect("projectDB.db") as con:
            cur=con.cursor()
            s="Select password from users where email==?"
            result=cur.execute(s,(email,))
            for row in result:
                p=row[0]
    except Exception as err:
        con.rollback()
        return "{}".format(err)
    finally:
        if p==password:
            query = "SELECT * FROM users WHERE email = :email AND password = :password"
            rows = db.execute(query, email=email, password=password)

            # If username and password match a record in database, set session variables
            if len(rows) == 1:
                session['email'] = email
                session['time'] = datetime.now( )
                session['uid'] = rows[0]["user_id"]
            return render_template("userhome.html")
        else:
            return "Invalid Credentials"


@app.route("/index")
def index():
    products = db.execute("SELECT * FROM products ORDER BY id ASC")
    productsLen = len(products)
    # Initialize variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    if 'user' in session:
        shoppingCart = db.execute("SELECT name, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY name")
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        products = db.execute("SELECT * FROM products ORDER BY name ASC")
        productsLen = len(products)
        return render_template("index.html", shoppingCart=shoppingCart, products=products, shopLen=shopLen,
                               productsLen=productsLen, total=total, totItems=totItems, display=display, session=session)

    return render_template("index.html", products=products, shoppingCart=shoppingCart, productsLen=productsLen, shopLen=shopLen, total=total, totItems=totItems, display=display)

@app.route("/cart/")
def cart():
        # Clear shopping cart variables
    totItems, total, display = 0, 0, 0
        # Grab info currently in database
    shoppingCart = db.execute("SELECT name, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY name")
        # Get variable values
    shopLen = len(shoppingCart)
    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
    # Render shopping cart
    return render_template("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session)

@app.route("/filter/")
def filter():
    if request.args.get('kind'):
        query = request.args.get('kind')
        products = db.execute("SELECT * FROM products WHERE kind = :query ORDER BY id ASC", query=query )
    productsLen = len(products)
    # Initialize shopping cart variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    if 'user' in session:
        # Rebuild shopping cart
        shoppingCart = db.execute("SELECT name, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY kind")
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        # Render filtered view
        return render_template ("index.html", shoppingCart=shoppingCart, products=products, shopLen=shopLen, productsLen=productsLen, total=total, totItems=totItems, display=display, session=session )
    # Render filtered view
    return render_template ( "index.html", products=products, shoppingCart=shoppingCart, productsLen=productsLen, shopLen=shopLen, total=total, totItems=totItems, display=display)


@app.route("/buy/")
def buy():
    # Initialize shopping cart variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    qty = int(request.args.get('quantity'))

        # Store id of the selected shirt
    id = int(request.args.get('id'))
        # Select info of selected shirt from database
    goods = db.execute("SELECT * FROM products WHERE id = :id", id=id)
        # Extract values from selected shirt record
        # Check if shirt is on sale to determine price
    if(goods[0]["onSale"] == 1):
        price = goods[0]["onSalePrice"]
    else:
        price = goods[0]["price"]
    name = goods[0]["name"]
    image = goods[0]["image"]
    subTotal = qty * price
        # Insert selected shirt into shopping cart
    db.execute("INSERT INTO cart (id, qty, name, image, price, subTotal) VALUES (:id, :qty, :name, :image, :price, :subTotal)", id=id, qty=qty, name=name, image=image, price=price, subTotal=subTotal)
    shoppingCart = db.execute("SELECT name, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY name")
    shopLen = len(shoppingCart)
        # Rebuild shopping cart
    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
        # Select all shirts for home page view
    products = db.execute("SELECT * FROM products ORDER BY id ASC")
    productsLen = len(products)
        # Go back to home page
    return render_template ("index.html", shoppingCart=shoppingCart, products=products, shopLen=shopLen, productsLen=productsLen, total=total, totItems=totItems, display=display, session=session)

@app.route("/update/")
def update():
    # Initialize shopping cart variables
    shoppingCart = []
    totItems, total, display = 0, 0, 0
    qty = int(request.args.get('quantity'))

        # Store id of the selected shirt
    id = int(request.args.get('id'))
    db.execute("DELETE FROM cart WHERE id = :id", id=id)
        # Select info of selected shirt from database
    goods = db.execute("SELECT * FROM products WHERE id = :id", id=id)
        # Extract values from selected shirt record
        # Check if shirt is on sale to determine price
    price = goods[0]["onSalePrice"]
    name = goods[0]["name"]
    image = goods[0]["image"]
    subTotal = qty * price
        # Insert selected shirt into shopping cart
    db.execute("INSERT INTO cart (id, qty, name, image, price, subTotal) VALUES (:id, :qty, :name, :image, :price, :subTotal)", id=id, qty=qty, name=name, image=image, price=price, subTotal=subTotal)
    shoppingCart = db.execute("SELECT name, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY name")
    shopLen = len(shoppingCart)
        # Rebuild shopping cart
    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
        # Go back to cart page
    return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session )

@app.route("/remove/", methods=["GET"])
def remove():
    # Get the id of shirt selected to be removed
    out = int(request.args.get("id"))
    # Remove shirt from shopping cart
    db.execute("DELETE from cart WHERE id=:id", id=out)
    # Initialize shopping cart variables
    totItems, total, display = 0, 0, 0
    # Rebuild shopping cart
    shoppingCart = db.execute("SELECT name, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY name")
    shopLen = len(shoppingCart)
    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
    # Turn on "remove success" flag
    display = 1
    # Render shopping cart
    return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session )


@app.route("/placeOrder",methods=["POST"])
def placeOrder():
    a = request.form["q8_fullName"]
    b = request.form["q11_contactNumber"]
    c = request.form["q12_selectDelivery"]
    d = request.form["q7_email"]
    e = request.form['q10_paymentMethod']
    f = request.form["q4_message4"]
    db.execute(
        "INSERT INTO deliveryDetails (uid,name,mobile,ddate,mail,method,address) VALUES(:uid, :a, :b, :c, :d, :e, :f)",
        uid=session["uid"], a=a, b=b,c=c,d=d,e=e,f=f)
    totItems, total, display = 0, 0, 0
    # Grab info currently in database
    shoppingCart = db.execute("SELECT name, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY name")
    # Get variable values
    shopLen = len(shoppingCart)
    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
    # Render shopping cart
    db.execute("DELETE from cart")
    return render_template("success.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems,
                           display=display, session=session)


@app.route("/checkout/")
def checkout():
    order = db.execute("SELECT * from cart")
    # Update purchase history of current customer
    for item in order:
        db.execute("INSERT INTO purchases (uid, id, name, image, quantity, date) VALUES(:uid, :id, :name, :image, :quantity, :date)", uid=session["uid"], id=item["id"], name=item["name"], image=item["image"], quantity=item["qty"] , date=session['time'])
    # Clear shopping cart
    # db.execute("DELETE from cart")
    # shoppingCart = []
    # shopLen = len(shoppingCart)
    # totItems, total, display = 0, 0, 0
    # Redirect to home page
    return render_template("checkout.html")






@app.route("/history/")
def history():
    # Initialize shopping cart variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    # Retrieve all shirts ever bought by current user
    myProucts = db.execute("SELECT * FROM purchases WHERE uid=:uid", uid=session["uid"])
    myProuctsLen = len(myProucts)
    # Render table with shopping history of current user
    return render_template("history.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session, myProucts=myProucts, myProuctsLen=myProuctsLen)



@app.route("/viewhistory")
def viewhistory():
    con = sqlite3.connect("projectDB.db")
    con.row_factory = sqlite3.Row  # Converts the records in Dictionary format, it ain't in just object form anymore
    c = con.cursor()
    c.execute("select * from purchases")
    rows = c.fetchall()
    return render_template("viewhistory.html", rows=rows)


@app.route("/viewdelivery")
def viewdelivery():
    con = sqlite3.connect("projectDB.db")
    con.row_factory = sqlite3.Row  # Converts the records in Dictionary format, it ain't in just object form anymore
    c = con.cursor()
    c.execute("select * from deliveryDetails")
    rows = c.fetchall()
    return render_template("viewdelivery.html", rows=rows)



@app.route("/view")
def view():
    con = sqlite3.connect("projectDB.db")
    con.row_factory=sqlite3.Row #Converts the records in Dictionary format, it ain't in just object form anymore
    c = con.cursor()
    c.execute("select * from users")
    rows = c.fetchall()
    return render_template("view.html", rows=rows)

@app.route("/viewProd")
def viewProd():
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    # Retrieve all shirts ever bought by current user
    myProucts = db.execute("SELECT * FROM products")
    myProuctsLen = len(myProucts)
    # Render table with shopping history of current user
    return render_template("viewProd.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems,
                           display=display, session=session, myProucts=myProucts, myProuctsLen=myProuctsLen)

    # myProducts=db.execute("select * from products")
    # myProuctsLen = len(myProducts)
    # rows = myProducts.fetchall()
    # return render_template("viewProd.html", rows=rows, myProuctsLen=myProuctsLen )

@app.route('/jobSeeker')
def job_seeker():
    return render_template('jobseeker.html')


@app.route("/addjobs",methods=["POST"])
def job():
    t=""
    if request.method=="POST":
        try:
            a = request.form["name"]
            b = request.form["number"]
            c = request.form["description"]

            with sqlite3.connect("projectDB.db") as con:
                cur=con.cursor()
                cur.execute("insert into jobs (name,number,description) values (?,?,?)",(a,b,c))
                con.commit()
        except Exception as err:
            con.rollback()
            t="Can't be registered {}".format(err)
        finally:
            return render_template("userhome.html")


@app.route("/viewseekers")
def view2():
    con = sqlite3.connect("projectDB.db")
    con.row_factory=sqlite3.Row #Converts the records in Dictionary format, it ain't in just object form anymore
    c = con.cursor()
    c.execute("select * from jobs")
    rows = c.fetchall()
    return render_template("viewseekers.html", rows=rows)



@app.route('/support')
def support_page():
    return render_template('support.html')

@app.route("/addsupport",methods=["POST"])
def support():
    t=""
    if request.method=="POST":
        try:
            a = request.form["name"]
            b = request.form["number"]
            c = request.form["city"]
            d = request.form["email"]
            e = request.form["query"]

            with sqlite3.connect("projectDB.db") as con:
                cur=con.cursor()
                cur.execute("insert into contact (name,number,city,email,query) values (?,?,?,?,?)",(a,b,c,d,e))
                con.commit()
        except Exception as err:
            con.rollback()
            t="Can't be registered {}".format(err)
        finally:
            return render_template("userhome.html")


@app.route("/viewsupport")
def view3():
    con = sqlite3.connect("projectDB.db")
    con.row_factory=sqlite3.Row #Converts the records in Dictionary format, it ain't in just object form anymore
    c = con.cursor()
    c.execute("select * from contact")
    rows = c.fetchall()
    return render_template("viewsupport.html", rows=rows)





@app.route("/delPro/")
def delPro():
    query = request.args.get('id')
    db.execute("delete FROM products WHERE id = :query ", query=query )
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    # Retrieve all shirts ever bought by current user
    myProucts = db.execute("SELECT * FROM products")
    myProuctsLen = len(myProucts)
    return render_template("viewProd.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems,
                           display=display, session=session, myProucts=myProucts, myProuctsLen=myProuctsLen)

@app.route("/updatePro/")
def updatePro():
    return render_template("update.html")

@app.route("/updateProDetails/", methods=["POST"])
def updateProDetails():
    id = request.form["id"]
    name = request.form["name"]
    price = request.form["price"]
    category = request.form["category"]
    db.execute("update products set name=:name, onSalePrice=:price, type=:category WHERE id = :id ", name=name, price=price, category=category, id=id )
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    # Retrieve all shirts ever bought by current user
    myProucts = db.execute("SELECT * FROM products")
    myProuctsLen = len(myProucts)
    return render_template("viewProd.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems,
                           display=display, session=session, myProucts=myProucts, myProuctsLen=myProuctsLen)

@app.errorhandler(404)
def pageNotFound( e ):
    if 'user' in session:
        return render_template ( "404.html", session=session )
    return render_template ( "404.html" ), 404

if __name__=='__main__':
    app.run(debug=True)