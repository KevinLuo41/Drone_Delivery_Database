from flask import Blueprint, request, Response, redirect, jsonify, url_for, flash, render_template
from flaskext.mysql import MySQL
import config

db = MySQL()
backend_api = Blueprint('backend_api', __name__)

@backend_api.route("/initial")
def initial():
    conn = db.connect()
    cur = conn.cursor()
    with open("./sql/grocery_drone_delivery.sql", 'r') as fd:
        sqlFile = fd.read()
        sqlCommands = sqlFile.split(';')
    for command in sqlCommands:
        try:
            if command.strip() != '':
                cur.execute(command)
                conn.commit()
        except Exception as e:
            print(command)
            print(e)

    with open("./sql/cs4400_phase3_shell.sql", 'r') as fd:
        sqlFile = fd.read()
        sqlCommands = sqlFile.split('//')

        for command in sqlCommands:
            try:
                if command.strip() != '':
                    cur.execute(command)
                    conn.commit()
            except Exception as e :
                print(command)
                print("!!!!@#@#!---",e)


    # cur.execute('select * from chain')
    # data = cur.fetchall()
    # conn.commit()
    # print(data)
    cur.close()
    conn.close()
    print("initialized")

    return redirect(url_for('frontend_api.s1_login_front'))

@backend_api.route('/s1_login_back', methods=["POST"])
def s1_login_back():
    # print("asdf")
    global USERNAME, USERTYPE
    username = request.form['username']
    password = request.form['password']

    print(username, password)
    if not password or not username:
        flash("Empty username or password!!")
        return redirect(url_for('frontend_api.s1_login_front'))

    conn = db.connect()
    cur = conn.cursor()

    try:
        cur.execute('SELECT * FROM users where username = %s and (pass = MD5(%s) or pass = %s)',
                    [username,password,password])
        conn.commit()
        result = cur.fetchall()
        if not result:
            flash('incorrect username or password')
            return redirect(url_for('frontend_api.s1_login_front'))
        # print(result)

        type =None
        cur.execute('select * from admin where username = %s',[username])
        if cur.fetchall(): type = "admin"

        cur.execute('select * from customer where username = %s',[username])
        if cur.fetchall(): type = "customer"

        cur.execute('select * from manager where username = %s',[username])
        if cur.fetchall(): type = "manager"

        cur.execute('select * from drone_tech where username = %s',[username])
        if cur.fetchall(): type = "tech"

    except Exception as e:
        print(e)
        return Response(status=500)
    finally:
        conn.close()

    print('type', type)
    config.USERNAME = username
    config.USERTYPE = type

    if type == 'customer':
        return redirect(url_for('frontend_api.s3_home_customer_front'))
    if type == 'tech':
        return redirect(url_for('frontend_api.s3_home_tech_front'))
    if type == 'manager':
        return redirect(url_for('frontend_api.s3_home_manager_front'))
    if type == 'admin':
        return redirect(url_for('frontend_api.s3_home_admin_front'))



@backend_api.route('/s4_create_chain_back', methods=["POST"])
def s4_create_chain_back():
    chain_name = request.form['chain-name']
    conn = db.connect()
    cur = conn.cursor()
    try:
        cur.callproc('admin_create_grocery_chain', [chain_name])
        conn.commit()
        flash("Chain Creation Succeed!!")
    except Exception as e:
        print(e)
        return Response(status=500)
    finally:
        data = s5_front_helper()
        print(data)
        conn.close()
        # return render_template("admin_home.html")
        return redirect(url_for('frontend_api.s3_home_admin_front'))

@backend_api.route('/s5_create_store_back', methods=["POST"])
def s5_create_store_back():
    print(request.form)
    chain_name = request.form['chain-name']
    store_name = request.form['store-name']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    zipcode = request.form['zip']

    conn = db.connect()
    cur = conn.cursor()
    try:
        cur.callproc('admin_create_new_store', [store_name,chain_name,street,city,state,zipcode])
        conn.commit()
        flash("Store Creation Succeed!")
    except Exception as e:
        flash(e)
        print(e)
        return Response(status=500)
    finally:
        cur.execute('select * from store')
        conn.commit()
        result = cur.fetchall()
        print(result)
        conn.close()
        return redirect(url_for('frontend_api.s3_home_admin_front'))

@backend_api.route('/s6_create_drone_back', methods=["POST"])
def s6_create_drone_back():
    print(request.form)
    id = request.form['drone-id']
    zipcode = request.form['zipcode']
    radius = request.form['radius']
    tech = request.form['tech']

    conn = db.connect()
    cur = conn.cursor()
    try:
        cur.callproc('admin_create_drone', [id,zipcode,radius,tech])
        conn.commit()
        flash("Drone Creation Succeed!")
    except Exception as e:
        flash(e)
        print(e)
        return Response(status=500)
    finally:
        cur.execute('select * from drone')
        conn.commit()
        result = cur.fetchall()
        print(result)
        conn.close()
        return redirect(url_for('frontend_api.s3_home_admin_front'))

def s5_front_helper():
    conn = db.connect()
    cur = conn.cursor()
    cur.execute('select * from chain')
    conn.commit()

    result = cur.fetchall()
    list_data = []
    for row in result:
        list_data.append(row[0])
    conn.close()

    return list_data

def s6_front_helper1():
    conn = db.connect()
    cur = conn.cursor()
    cur.execute('select max(id) from drone')
    conn.commit()

    result = cur.fetchall()
    new_id = result[0][0]+1

    cur.execute('select distinct(zipcode) from users natural join drone_tech')
    conn.commit()
    result = cur.fetchall()
    ziplist = []
    for row in result:
        ziplist.append(row[0])
    print(ziplist)
    conn.close()
    return new_id, ziplist

@backend_api.route('/s6_front_helper2', methods=["POST"])
def s6_front_helper2():
    zipcode = request.form["ziplist"]
    conn = db.connect()
    cur = conn.cursor()
    cur.execute('select distinct(username) from drone_tech natural join users where zipcode = %s',[zipcode])
    conn.commit()

    result = cur.fetchall()
    data = [{"username": x[0]} for x in result]
    print(data)
    return jsonify(data)


@backend_api.route('/s8_view_customers', methods=["POST"])
def s8_admin_view_customers():
    print(request.form)
    print("in filter")
    firstname = request.form['customer_firstname']
    lastname = request.form['customer_lastname']
    if firstname == '': firstname = None
    if lastname == '': lastname = None
    conn = db.connect()
    cur = conn.cursor()
    result_list = []
    try:
        cur.callproc('admin_view_customers', [firstname, lastname]) # 8a
        conn.commit()
        # flash("Customers Filter Succeed!")
    except Exception as e:
        # flash(e)
        print(e)
        return Response(status=500)
    finally:
        cur.execute('select * from admin_view_customers_result')
        conn.commit()
        result = cur.fetchall()
        result_list = list(result)
        print(result_list)
        conn.close()
    return render_template("s8_view_customers.html", result=result_list, fname=firstname, lname=lastname)

@backend_api.route('/s7_create_item_back', methods=["POST"])
def s7_create_item_back():
    print(request.form)
    item_name = request.form['Name']
    item_type = request.form['Type']
    item_organic = request.form['Organic']
    item_origin = request.form['Origin']
    conn = db.connect()
    cur = conn.cursor()
    try:
        cur.callproc('admin_create_item', [item_name, item_type, item_organic, item_origin])
        conn.commit()
        flash("Item Creation Succeed!!")
    except Exception as e:
        print(e)
        return Response(status=500)
    finally:
        cur.execute('select * from item')
        conn.commit()
        result = cur.fetchall()
        print(result)
        conn.close()
        return redirect(url_for('frontend_api.s3_home_admin_front'))
    
def s9_front_helper():
    conn = db.connect()
    cur = conn.cursor()
    cur.execute('select ChainName from manager where username = %s', [config.USERNAME])
    conn.commit()

    result = cur.fetchall()
    ChainName = result[0][0]
    
    cur.execute('select * from item')
    conn.commit()
    
    result = cur.fetchall()
    itemlist = []
    for row in result:
        itemlist.append(row[0])
    print(itemlist)
    
    cur.execute('select max(PLUNumber) from chain_item')
    conn.commit()

    result = cur.fetchall()
    new_PLU = result[0][0]+1
    
    conn.close()
    return ChainName,itemlist,new_PLU

@backend_api.route('/s9_create_chainitem_back', methods=["POST"])
def s9_create_chainitem_back():
    print(request.form)
    chain_name = request.form['Chain Name']
    item_name = request.form['Item']
    quantity = request.form['Quantity Available']
    order_limit = request.form['Limit Per Order']
    PLU = request.form['PLU Number']
    price = request.form['Price per Unit']
    conn = db.connect()
    cur = conn.cursor()
    try:
        cur.callproc('manager_create_chain_item', [chain_name, item_name, quantity, order_limit, PLU, price])
        conn.commit()
        flash("Chain Item Creation Succeed!!")
    except Exception as e:
        print(e)
        return Response(status=500)
    finally:
        cur.execute('select * from chain_item')
        conn.commit()
        result = cur.fetchall()
        print(result)
        conn.close()
        return redirect(url_for('frontend_api.s3_home_admin_front'))