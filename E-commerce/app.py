from flask import Flask, request, render_template, redirect, url_for, session
import pymysql



app = Flask(__name__)
app.secret_key = 'Mysecretkey'


@app.route('/')
def index():
    return render_template("index.html")
                          

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
         # Check if passwords match
        if password != confirm_password:
            return render_template('register.html', alert='Passwords do not match')
         
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Ayushayush123',
            database='ayushserver',
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
                cursor.execute(sql, (email, username, password))
                connection.commit()
                return redirect(url_for('index'))  
        finally:
            connection.close()

    return render_template('index.html')  

@app.route('/login', methods=['GET','POST'])
def login():
    username = request.form.get('username')  # Use get() to avoid KeyError
    password = request.form.get('password')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Ayushayush123',
        database='ayushserver',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username=%s AND password=%s"
            # print("SQL Query:", sql)
            cursor.execute(sql, (username, password))
            user = cursor.fetchone()  
            # print("User:", user)
            if user:
                session['user_id'] = user['id']
                return render_template('home.html')
            else:
                
                return render_template('register.html')
    finally:
        connection.close()
        
@app.route('/clothes', methods=['GET','POST'])
def clothes():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if user is not logged in
    
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_url = request.form['product_url']
        product_price = request.form['product_price']  # Get the product price from the form
        user_id = session['user_id']
        
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Ayushayush123',
            database='ayushserver',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        try:
            with connection.cursor() as cursor:
                # Check if the product already exists in the cart
                sql_select = "SELECT * FROM clothes WHERE products = %s AND user_id = %s"
                cursor.execute(sql_select, (product_name, user_id))
                product = cursor.fetchone()
                
                if product:
                    # If the product exists, check if add_to_cart is 0
                    if product['add_to_cart'] == 0:
                        # If add_to_cart is 0, update it to 1 and set the URL and price
                        sql_update = "UPDATE clothes SET add_to_cart = 1, url = %s, price = %s WHERE products = %s AND user_id = %s"
                        cursor.execute(sql_update, (product_url, product_price, product_name, user_id))
                    else:
                        # Otherwise, increment the add_to_cart value and update URL and price
                        sql_update = "UPDATE clothes SET add_to_cart = add_to_cart + 1, url = %s, price = %s WHERE products = %s AND user_id = %s"
                        cursor.execute(sql_update, (product_url, product_price, product_name,user_id))
                else:
                    # If the product doesn't exist, insert a new row into the clothes table with URL and price
                    sql_insert = "INSERT INTO clothes (products, add_to_cart, url, price, user_id) VALUES (%s, 1, %s, %s, %s)"
                    cursor.execute(sql_insert, (product_name, product_url, product_price, user_id))
                    
                connection.commit()
                
                # After updating the cart, you can redirect to the same clothes page
                return redirect(url_for('clothes'))
        finally:
            connection.close()
    
    # If it's a GET request, simply render the clothes page
    return render_template('clothes.html')


@app.route('/shoes', methods=['GET','POST'])
def shoes():
    if request.method == 'POST':
        # Handle the form submission for the sports page (similar to clothes route)
        product_name = request.form['product_name']
        product_url = request.form['product_url']
        product_price = request.form['product_price']
        user_id = session['user_id']
        
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Ayushayush123',
            database='ayushserver',
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cursor:
                # Check if the product already exists in the cart
                sql_select = "SELECT * FROM clothes WHERE products = %s AND user_id = %s"
                cursor.execute(sql_select, (product_name,user_id))
                product = cursor.fetchone()
                
                if product:
                    # If the product exists, check if add_to_cart is 0
                    if product['add_to_cart'] == 0:
                        # If add_to_cart is 0, update it to 1 and set the URL and price
                        sql_update = "UPDATE clothes SET add_to_cart = 1, url = %s, price = %s WHERE products = %s AND user_id = %s"
                        cursor.execute(sql_update, (product_url, product_price, product_name , user_id))
                    else:
                        # Otherwise, increment the add_to_cart value and update URL and price
                        sql_update = "UPDATE clothes SET add_to_cart = add_to_cart + 1, url = %s, price = %s WHERE products = %s AND user_id = %s"
                        cursor.execute(sql_update, (product_url, product_price, product_name , user_id))
                else:
                    # If the product doesn't exist, insert a new row into the clothes table with URL and price
                    sql_insert = "INSERT INTO clothes (products, add_to_cart, url, price, user_id) VALUES (%s, 1, %s, %s, %s)"
                    cursor.execute(sql_insert, (product_name, product_url, product_price,user_id))
                 
                connection.commit()    
            return redirect(url_for('shoes'))
                
        finally:
            connection.close()
    return render_template('shoes.html')

@app.route('/home', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        
        product_name = request.form['product_name']
        product_url = request.form['product_url']
        product_price = request.form['product_price']
        user_id = session['user_id']
        
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Ayushayush123',
            database='ayushserver',
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cursor:
                # Check if the product already exists in the cart
                sql_select = "SELECT * FROM clothes WHERE products = %s AND user_id = %s"
                cursor.execute(sql_select, (product_name,user_id))
                product = cursor.fetchone()
                
                if product:
                    # If the product exists, check if add_to_cart is 0
                    if product['add_to_cart'] == 0:
                        # If add_to_cart is 0, update it to 1 and set the URL and price
                        sql_update = "UPDATE clothes SET add_to_cart = 1, url = %s, price = %s WHERE products = %s AND user_id = %s"
                        cursor.execute(sql_update, (product_url, product_price, product_name, user_id))
                    else:
                        # Otherwise, increment the add_to_cart value and update URL and price
                        sql_update = "UPDATE clothes SET add_to_cart = add_to_cart + 1, url = %s, price = %s WHERE products = %s AND user_id = %s"
                        cursor.execute(sql_update, (product_url, product_price, product_name, user_id))
                else:
                    # If the product doesn't exist, insert a new row into the clothes table with URL and price
                    sql_insert = "INSERT INTO clothes (products, add_to_cart, url, price, user_id) VALUES (%s, 1, %s, %s, %s)"
                    cursor.execute(sql_insert, (product_name, product_url, product_price, user_id))
                 
                connection.commit()    
            return redirect(url_for('home'))
                
        finally:
            connection.close()
          # Redirect back to the sports page after adding to cart
    
    return render_template('home.html')
    

@app.route('/sports', methods=['GET', 'POST'])
def sports():
    if request.method == 'POST':
        # Handle the form submission for the sports page (similar to clothes route)
        product_name = request.form['product_name']
        product_url = request.form['product_url']
        product_price = request.form['product_price']
        user_id = session['user_id']
        
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Ayushayush123',
            database='ayushserver',
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cursor:
                # Check if the product already exists in the cart
                sql_select = "SELECT * FROM clothes WHERE products = %s AND user_id = %s"
                cursor.execute(sql_select, (product_name, user_id))
                product = cursor.fetchone()
                
                if product:
                    # If the product exists, check if add_to_cart is 0
                    if product['add_to_cart'] == 0:
                        # If add_to_cart is 0, update it to 1 and set the URL and price
                        sql_update = "UPDATE clothes SET add_to_cart = 1, url = %s, price = %s WHERE products = %s AND user_id = %s"
                        cursor.execute(sql_update, (product_url, product_price, product_name, user_id))
                    else:
                        # Otherwise, increment the add_to_cart value and update URL and price
                        sql_update = "UPDATE clothes SET add_to_cart = add_to_cart + 1, url = %s, price = %s WHERE products = %s AND user_id = %s"
                        cursor.execute(sql_update, (product_url, product_price, product_name, user_id))
                else:
                    # If the product doesn't exist, insert a new row into the clothes table with URL and price
                    sql_insert = "INSERT INTO clothes (products, add_to_cart, url, price, user_id) VALUES (%s, 1, %s, %s, %s)"
                    cursor.execute(sql_insert, (product_name, product_url, product_price, user_id))
                 
                connection.commit()    
            return redirect(url_for('sports'))
                
        finally:
            connection.close()
          # Redirect back to the sports page after adding to cart
    
    return render_template('sports.html')   

@app.route('/electronics', methods=['GET', 'POST'])
def electronics():
    if request.method == 'POST':
        # Handle the form submission for the sports page (similar to clothes route)
        product_name = request.form['product_name']
        product_url = request.form['product_url']
        product_price = request.form['product_price']
        user_id = session['user_id']
        
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Ayushayush123',
            database='ayushserver',
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cursor:
                # Check if the product already exists in the cart
                sql_select = "SELECT * FROM clothes WHERE products = %s AND user_id = %s"
                cursor.execute(sql_select, (product_name,user_id))
                product = cursor.fetchone()
                
                if product:
                    # If the product exists, check if add_to_cart is 0
                    if product['add_to_cart'] == 0:
                        # If add_to_cart is 0, update it to 1 and set the URL and price
                        sql_update = "UPDATE clothes SET add_to_cart = 1, url = %s, price = %s WHERE products = %s AND user_id = %s"
                        cursor.execute(sql_update, (product_url, product_price, product_name, user_id))
                    else:
                        # Otherwise, increment the add_to_cart value and update URL and price
                        sql_update = "UPDATE clothes SET add_to_cart = add_to_cart + 1, url = %s, price = %s WHERE products = %s AND user_id = %s"
                        cursor.execute(sql_update, (product_url, product_price, product_name, user_id))
                else:
                    # If the product doesn't exist, insert a new row into the clothes table with URL and price
                    sql_insert = "INSERT INTO clothes (products, add_to_cart, url, price, user_id) VALUES (%s, 1, %s, %s, %s)"
                    cursor.execute(sql_insert, (product_name, product_url, product_price, user_id))   
                 
                connection.commit()   
                
                 
            return redirect(url_for('electronics'))
                
        finally:
            connection.close()
          # Redirect back to the sports page after adding to cart
    
    return render_template('electronics.html')

@app.route('/cart')
def view_cart():
    user_id = session.get('user_id')  # Get the current user's ID from the session
    if user_id:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Ayushayush123',
            database='ayushserver',
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cursor:
                # Query the cart items for the current user
                sql_select = "SELECT * FROM clothes WHERE user_id = %s AND add_to_cart > 0"
                cursor.execute(sql_select, (user_id,))
                cart_items = cursor.fetchall()
                


            return render_template('cart.html', cart_items=cart_items)
        finally:
            connection.close()
    else:
        # If the user is not logged in, redirect to the login page
        return redirect(url_for('login'))

        
@app.route('/cart/increment/<int:item_id>', methods=['POST'])
def increment_cart_item(item_id):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Ayushayush123',
        database='ayushserver',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            # Update the add_to_cart count in the clothes table
            sql_update = "UPDATE clothes SET add_to_cart = add_to_cart + 1 WHERE id = %s"
            cursor.execute(sql_update, (item_id,))
            connection.commit()

            # Redirect back to the cart page after incrementing
            return redirect(url_for('view_cart'))
    finally:
        connection.close()        

@app.route('/cart/decrement/<int:item_id>', methods=['POST'])
def decrement_cart_item(item_id):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Ayushayush123',
        database='ayushserver',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            # Update the add_to_cart count in the clothes table
            sql_update = "UPDATE clothes SET add_to_cart = add_to_cart - 1 WHERE id = %s AND add_to_cart > 0"
            cursor.execute(sql_update, (item_id,))
            connection.commit()

            # Redirect back to the cart page after decrementing
            return redirect(url_for('view_cart'))
    finally:
        connection.close()
        
@app.route('/logout', methods=['GET','POST'])
def logout():
    
    session.clear()
    
    return render_template("index.html")

@app.route('/signup',methods=['GET','POST'])
def signup():
    return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True)
