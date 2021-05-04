from flask import Blueprint, request, Response, redirect, jsonify, url_for, flash, render_template
from flaskext.mysql import MySQL
import config
import json
from datetime import datetime

db = MySQL()
backend_api = Blueprint('backend_api', __name__)


@backend_api.route("/initial", methods=["POST"])
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
            except Exception as e:
                print(command)
                print("!!!!@#@#!---", e)

    # cur.execute('select * from chain')
    # data = cur.fetchall()
    # conn.commit()
    # print(data)
    cur.close()
    conn.close()
    print("initialized")

    return redirect(url_for('frontend_api.s1_login_front'))


@backend_api.route('/s1_login', methods=["POST"])
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
                    [username, password, password])
        conn.commit()
        result = cur.fetchall()
        if not result:
            flash('Incorrect username or password')
            return redirect(url_for('frontend_api.s1_login_front'))
        # print(result)

        type = None
        cur.execute('select * from admin where username = %s', [username])
        if cur.fetchall(): type = "admin"

        cur.execute('select * from customer where username = %s', [username])
        if cur.fetchall(): type = "customer"

        cur.execute('select * from manager where username = %s', [username])
        if cur.fetchall(): type = "manager"

        cur.execute('select * from drone_tech where username = %s', [username])
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


@backend_api.route('/s2_register', methods=["POST"])
def s2_register_back():
    print(request.form)
    lname = request.form['lname']
    fname = request.form['fname']
    username = request.form['username']
    password = request.form['password']
    confirm = request.form['confirm']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    zipcode = request.form['zipcode']

    card1 = request.form['card1']
    card2 = request.form['card2']
    card3 = request.form['card3']
    card4 = request.form['card4']
    cvv = request.form['cvv']
    month = request.form['month']
    year = request.form['year']

    chain = request.form['chain']
    store = request.form['store']

    if len(password) < 8:
        flash("Password must contain at least 8 characters!!")
        return redirect(url_for("frontend_api.s2_register_front"))
    if password != confirm:
        flash("Password and confirm password should be same!!")
        return redirect(url_for("frontend_api.s2_register_front"))

    conn = db.connect()
    cur = conn.cursor()
    try:
        if card1:
            card = card1 + " " + card2 + " " + card3 + " " + card4
            exp = year + "-" + month + "-01"
            cur.callproc('register_customer',
                         [username, password, fname, lname, street, city, state, zipcode, card, cvv, exp])
            conn.commit()
            flash("Registration Succeed! Welcome Customer!")
            # conn.close()
            return redirect(url_for("frontend_api.s1_login_front"))

        if chain:
            if store:
                result = cur.execute("select * from store where chainname = %s and storename =%s", [chain, store])
                if not result:
                    flash("incorrect chain-store combination")
                    return redirect(url_for("frontend_api.s2_register_front"))
                else:
                    cur.callproc('register_employee', [username, password, fname, lname, street, city, state, zipcode])
                    cur.execute("insert into drone_tech values(%s,%s,%s)", [username, store, chain])
                    conn.commit()
                    flash("Registration Succeed! Welcome drone tech!")
                    # conn.close()
                    return redirect(url_for("frontend_api.s1_login_front"))
            else:
                result = cur.execute(
                    "select * from chain natural left join manager where chainname = %s and  username is null", [chain])
                if not result:
                    flash("incorrect chain name or already has a manager!!")
                    return redirect(url_for("frontend_api.s2_register_front"))
                else:
                    cur.callproc('register_employee', [username, password, fname, lname, street, city, state, zipcode])
                    cur.execute("insert into manager values(%s,%s)", [username, chain])
                    conn.commit()
                    flash("Registration Succeed! Welcome Manager!")
                    # conn.close()
                    return redirect(url_for("frontend_api.s1_login_front"))

    except Exception as e:
        print(e)
        return redirect(url_for("frontend_api.s2_register_front"))
    finally:
        conn.close()
        # return redirect(url_for("frontend_api.s2_register_front"))


@backend_api.route('/s4_create_chain', methods=["POST"])
def s4_create_chain_back():
    chain_name = request.form['chain-name']
    conn = db.connect()
    cur = conn.cursor()
    try:
        cur.callproc('admin_create_grocery_chain', [chain_name])
        conn.commit()
        flash("Chain Creation Succeed!!")
    except Exception as e:
        flash("Incorrect chain name or chain name already exists!")
        return Response(status=500)
    finally:
        data = s5_front_helper()
        print(data)
        conn.close()
        # return render_template("admin_home.html")
        return redirect(url_for('frontend_api.s3_home_admin_front'))


@backend_api.route('/s5_create_store', methods=["POST"])
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
        cur.callproc('admin_create_new_store', [store_name, chain_name, street, city, state, zipcode])
        conn.commit()
        flash("Store Creation Succeed!")
    except Exception as e:
        flash(str(e))
        print(e)
        return Response(status=500)
    finally:
        cur.execute('select * from store')
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


@backend_api.route('/s6_create_drone', methods=["POST"])
def s6_create_drone_back():
    print(request.form)
    try:
        id = request.form['drone-id']
        zipcode = request.form['zipcode']
        radius = request.form['radius']
        tech = request.form['tech']
    except Exception as e:
        flash("All fields are required")
        return redirect(url_for('frontend_api.s6_create_drone_front'))

    conn = db.connect()
    cur = conn.cursor()
    try:
        cur.callproc('admin_create_drone', [id, zipcode, radius, tech])
        conn.commit()
        flash("Drone Creation Succeed!")
    except Exception as e:
        flash(str(e))
        print(e)
        return redirect(url_for('frontend_api.s6_create_drone_front'))
    finally:
        cur.execute('select * from drone')
        conn.commit()
        result = cur.fetchall()
        print(result)
        conn.close()
        return redirect(url_for('frontend_api.s3_home_admin_front'))


def s6_front_helper1():
    conn = db.connect()
    cur = conn.cursor()
    cur.execute('select max(id) from drone')
    conn.commit()

    result = cur.fetchall()
    new_id = result[0][0] + 1

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
    cur.execute('select distinct(username) from drone_tech natural join users where zipcode = %s', [zipcode])
    conn.commit()

    result = cur.fetchall()
    data = [{"username": x[0]} for x in result]
    print(data)
    return jsonify(data)


@backend_api.route('/s7_create_item', methods=["POST"])
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
        return redirect(url_for('frontend_api.s3_home_admin_front'))
    except Exception as e:
        print(e)
        flash(str(e))
        return redirect(url_for('frontend_api.s7_create_item_front'))
    finally:
        conn.close()


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
        cur.callproc('admin_view_customers', [firstname, lastname])  # 8a
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
    new_PLU = result[0][0] + 1

    conn.close()
    return ChainName, itemlist, new_PLU


@backend_api.route('/s9_create_chainitem', methods=["POST"])
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
        return redirect(url_for('frontend_api.s3_home_manager_front'))
    except Exception as e:
        print(e)
        flash(str(e))
        return redirect(url_for('frontend_api.s9_create_chainitem'))

    finally:
        conn.close()



@backend_api.route('/s10_view_tech/filter', methods=["POST"])
def s10_view_tech_filter():
    chain_name = get_chain_name()
    locations = get_store_name(chain_name)
    users = get_tech_and_store(chain_name)

    print(request.form)
    tech_name = request.form['Username']
    location = request.form['location']
    if tech_name == '': tech_name = None
    if location == 'NULL': location = None
    users = get_tech_and_store(chain_name, tech_name, location)
    return render_template("s10_view_tech.html", chain_name=chain_name, tech_name=tech_name, location=location,
                           locations=locations, users=users)


@backend_api.route('/s10_view_tech/assign', methods=["POST"])
def s10_view_tech_assign():
    chain_name = get_chain_name()
    store_name = get_store_name(chain_name)
    users = get_tech_and_store(chain_name)

    print(request.form)
    for user, _, curr_loc in users:
        re_loc = request.form[user]
        print(re_loc)
        if re_loc != curr_loc:
            store_zip = get_zip(chain_name, re_loc)
            set_tech_store(user, re_loc)
            set_drone_zip(user, store_zip)

    # return render_template("s10_view_tech.html")
    return redirect(url_for('frontend_api.s10_view_tech'))


def get_tech_and_store(chain_name, tech_name=None, store_name=None):
    conn = db.connect()
    cur = conn.cursor()
    result_list = []
    try:
        cur.callproc('manager_view_drone_technicians', [chain_name, tech_name, store_name])  # 10a
        conn.commit()
    except Exception as e:
        print(e)
        return Response(status=500)
    finally:
        cur.execute('select * from manager_view_drone_technicians_result')
        conn.commit()
        result = cur.fetchall()
        result_list = list(result)
        print(result_list)
        conn.close()
    return result_list


def get_zip(chain_name, store_name):
    conn = db.connect()
    cur = conn.cursor()
    result_list = []
    cur.execute('SELECT Zipcode FROM grocery_drone_delivery.STORE where ChainName = %s AND StoreName = %s',
                [chain_name, store_name])
    conn.commit()
    result = cur.fetchall()
    zipcode = result[0][0]
    return zipcode


def set_drone_zip(tech, zipcode):
    conn = db.connect()
    cur = conn.cursor()
    result_list = []
    cur.execute('UPDATE grocery_drone_delivery.DRONE SET Zip = %s WHERE DroneTech = %s', [zipcode, tech])
    conn.commit()
    conn.close()


def set_tech_store(tech, store):
    conn = db.connect()
    cur = conn.cursor()
    result_list = []
    cur.execute('UPDATE grocery_drone_delivery.DRONE_TECH SET StoreName = %s WHERE Username = %s', [store, tech])
    conn.commit()
    conn.close()


@backend_api.route('/s11_view_drone', methods=["POST"])
def s11_view_drone():
    print(request.form)
    print("in filter")
    drone_id = request.form['drone_id']
    radius = request.form['radius']
    drone_id = None if drone_id == '' else int(drone_id)
    radius = None if radius == '' else int(radius)
    mgr_username = config.USERNAME  # current user
    conn = db.connect()
    cur = conn.cursor()
    result_list = []
    try:
        cur.callproc('manager_view_drones', [mgr_username, drone_id, radius])  # 11a
        conn.commit()
        # flash("Customers Filter Succeed!")
    except Exception as e:
        # flash(e)
        print(e)
        return Response(status=500)
    finally:
        cur.execute('select * from manager_view_drones_result')
        conn.commit()
        result = cur.fetchall()
        result_list = list(result)
        print(result_list)
        conn.close()
    return render_template("s11_view_drone.html", result=result_list, id=drone_id, r=radius)


@backend_api.route('/s12_manage_store', methods=["POST"])
def s12_manage_store():
    username = config.USERNAME  # current user
    chain_name = get_chain_name()
    store_name = get_store_name(chain_name)

    print(request.form)
    range_min = request.form['min']
    range_max = request.form['max']
    range_min = None if range_min == '' else int(range_min)
    range_max = None if range_max == '' else int(range_max)
    select_store = request.form['store_name']
    if select_store == 'NULL': select_store = None
    print(username)
    print(select_store)
    print(range_min)
    print(range_max)
    stores = get_stores(username, select_store, range_min, range_max)
    return render_template("s12_manage_store.html", min=range_min, max=range_max, sstore=select_store,
                           chain_name=chain_name, store_name=store_name, stores=stores)


def get_chain_name():
    mgr_username = config.USERNAME  # current user
    conn = db.connect()
    cur = conn.cursor()
    result_list = []
    cur.execute('SELECT ChainName FROM grocery_drone_delivery.MANAGER where Username = %s', [mgr_username])
    conn.commit()
    result = cur.fetchall()
    chain_name = result[0][0]
    print(chain_name)
    return chain_name


def get_store_name(chain_name):
    mgr_username = config.USERNAME  # current user
    conn = db.connect()
    cur = conn.cursor()
    result_list = []
    cur.execute('SELECT StoreName FROM grocery_drone_delivery.STORE where ChainName = %s', [chain_name])
    conn.commit()
    result = cur.fetchall()
    result_list = [item[0] for item in result]
    print(result_list)
    return result_list


def get_stores(manager, store_name, _min=None, _max=None):
    conn = db.connect()
    cur = conn.cursor()
    result_list = []
    try:
        cur.callproc('manager_manage_stores', [manager, store_name, _min, _max])  # 12a
        conn.commit()
    except Exception as e:
        print(e)
        return Response(status=500)
    finally:
        cur.execute('select * from manager_manage_stores_result')
        conn.commit()
        result = cur.fetchall()
        result_list = list(result)
        print(result_list)
        conn.close()
    return result_list


@backend_api.route('/s13_change_card', methods=["POST"])
def s13_change_card():
    username = config.USERNAME  # current user
    print(request.form)
    card_number = request.form['card_number']
    cvv = int(request.form['cvv'])
    year = request.form['year']
    month = request.form['month']
    conn = db.connect()
    cur = conn.cursor()
    date = year + '-' + month + '-' + '01'
    try:
        cur.callproc('customer_change_credit_card_information', [username, card_number, cvv, date])  # 13a
        conn.commit()
    except Exception as e:
        print(e)
        return Response(status=500)
    finally:
        conn.close()
    return redirect(url_for('frontend_api.s13_change_card'))


def get_flname(username):
    conn = db.connect()
    cur = conn.cursor()
    try:
        cur.execute('SELECT FirstName, LastName FROM grocery_drone_delivery.USERS where Username = %s', [username])
        conn.commit()
    except Exception as e:
        print(e)
        return Response(status=500)
    finally:
        result = cur.fetchall()
        print(result)
        conn.close()
    return result[0][0], result[0][1]


@backend_api.route('/s14_view_orderhistory', methods=['POST'])
def s14_view_orderhistory():
    username = config.USERNAME  # current user
    id = request.form["id"]
    ids = get_order_id(username)
    print(username, id)

    conn = db.connect()
    cur = conn.cursor()
    try:
        print("!23")
        cur.callproc('customer_view_order_history', [username, id])
        conn.commit()
    except Exception as e:
        print(e)
        return Response(status=500)
    finally:
        cur.execute("select * from customer_view_order_history_result")
        row_headers = [x[0] for x in cur.description]
        result = cur.fetchall()
        print(result)
        dict_data = dict(zip(row_headers, list(map(str, result[0]))))
        # return redirect(url_for('frontend_api.s3_home_admin_front'))
        print(dict_data)
    # print(ids, id)
    return render_template("s14_view_orderhistory.html", username=username, ids=ids, id=id, data=dict_data)


def get_order_id(username):
    conn = db.connect()
    cur = conn.cursor()
    try:
        cur.execute('select id from orders where customerusername = %s', [username])
        conn.commit()
        result = cur.fetchall()
        list_data = []
        for row in result:
            list_data.append(row[0])
        conn.close()
    except Exception as e:
        print(e)
        return []

    return list_data


def s15_get_chain():
    conn = db.connect()
    cur = conn.cursor()
    cur.execute(
        'select ChainName, StoreName from store where Zipcode = (select Zipcode from users where Username = %s)',
        [config.USERNAME])
    conn.commit()

    result = cur.fetchall()
    chainlist = {}
    for row in result:
        if row[0] not in chainlist.keys():
            chainlist[str(row[0])] = []
        chainlist[row[0]].append(str(row[1]))

    conn.close()
    return json.dumps(chainlist)


@backend_api.route('/s15_get_category', methods=["POST"])
def s15_get_category():
    chain = request.form["chain"]
    conn = db.connect()
    cur = conn.cursor()
    cur.execute(
        'select distinct(itemtype) from  (select * from chain_item as ci, item as i where ci.chainitemname = i.itemname and chainname = %s) as t order by itemtype; ',
        [chain])
    conn.commit()

    result = cur.fetchall()
    data = [{"itemtype": x[0]} for x in result]
    print(data)
    return jsonify(data)


@backend_api.route('/s15_get_items', methods=["POST"])
def s15_get_items():
    chain = request.form["chain"]
    category = request.form["category"]
    conn = db.connect()
    cur = conn.cursor()
    if category == "":
        cur.execute('select ChainItemName, Orderlimit from chain_item as ci where ci.ChainName = %s', [chain])
    else:
        cur.execute(
            'select ChainItemName, Orderlimit from chain_item as ci, item as i where ci.chainitemname = i.itemname and ci.ChainName = %s and i.itemtype = %s',
            [chain, category])
    conn.commit()

    result = cur.fetchall()
    data = [{"name": x[0], "quantity": x[1]} for x in result]
    print(data)
    return jsonify(data)


@backend_api.route('/s15_place_order', methods=["POST"])
def s15_place_order():
    username = config.USERNAME
    print((request.form.to_dict()))
    chain = request.form["Chain"]
    store = request.form["Store"]
    orders = request.form.to_dict()
    correct_order =False
    for item, quant in orders.items():
        if item == "Chain" or item == "Store" or item == "Category" or quant == "0":
            continue
        else:
            correct_order=True
            print(item, ":", quant)
            conn = db.connect()
            cur = conn.cursor()
            try:
                cur.callproc('customer_select_items', [username, chain, store, item, int(quant)])
                conn.commit()

            except Exception as e:
                print(e)
                redirect(url_for("frontend_api.s3_home_customer_front"))
            finally:
                conn.close()

    if not correct_order:
        flash("No order placed")
        return redirect(url_for("frontend_api.s3_home_customer_front"))

    return s16_review_order_back(chain, store)


@backend_api.route('/s16_review_order', methods=['POST'])
def s16_review_order_back(chain,store):
    username = config.USERNAME
    conn = db.connect()
    cur = conn.cursor()
    items=[]
    try:
        cur.callproc('customer_review_order', [username])
        cur.execute('select * from customer_review_order_result')
        conn.commit()
        result = cur.fetchall()
        for re in result:
            # print(re)
            list_data = list(map(str, re))
            items.append(list_data)
        # print(list_data)

    except Exception as e:
        print(e)
        redirect(url_for("frontend_api.s3_home_customer_front"))
    finally:
        conn.close()
    return render_template("s16_review_order.html", chain =chain,store =store, items = items)

def s16_check_creating(username):

    conn = db.connect()
    cur = conn.cursor()
    result =[]
    try:
        cur.execute("SELECT storename, chainname FROM store "
                    "WHERE (chainname , zipcode) = "
                    "(SELECT chainname, zipcode FROM orders "
                    "JOIN contains ON id = orderid JOIN users "
                    "ON customerusername = username "
                    "WHERE orderstatus = 'Creating' "
                    "and username = %s "
                    "GROUP BY chainname , zipcode)",[username])
        conn.commit()
        result = cur.fetchall()
        print(result)
    except Exception as e:
        print(e)

    return result

@backend_api.route('/s16_place_order', methods=['POST'])
def s16_place_order():
    username = config.USERNAME
    orders = request.form.to_dict(flat=False)
    updates = dict(zip(orders["item"],orders['update']))
    print(updates)

    exp = s16_get_exp(username)
    curdate = datetime.today().date()
    if exp<curdate:
        flash("card expired, change a card to continue")
        return redirect(url_for("frontend_api.s3_home_customer_front"))
    else:
        conn = db.connect()
        cur = conn.cursor()
        for item, quant in updates.items():
            print(item, ":", quant)
            try:
                cur.callproc('customer_update_order', [username, item, int(quant)])
                conn.commit()

            except Exception as e:
                print(e)
                return redirect(url_for("frontend_api.s3_home_customer_front"))

        cur.execute("UPDATE orders SET OrderStatus = 'Pending' "
                    "WHERE OrderStatus = 'Creating' AND CustomerUsername = %s",[username])
        conn.commit()
        conn.close()

    flash("Your order has been received!")
    return  redirect(url_for("frontend_api.s3_home_customer_front"))

def s16_get_exp(username):
    conn = db.connect()
    cur = conn.cursor()
    cur.execute("select exp_date from customer where username =%s",[username])
    exp = cur.fetchall()[0][0]
    print(exp)
    return exp

@backend_api.route('/s17_tech_vieworders', methods=['POST'])
def s17_tech_vieworders_back():
    username = config.USERNAME
    # print(username)
    syear = request.form["syear"]
    smonth = request.form["smonth"]
    sday = request.form["sday"]

    eyear = request.form["eyear"]
    emonth = request.form["emonth"]
    eday = request.form["eday"]
    print(request.form)


    if syear and smonth and sday:
        sdate = syear + "-" + smonth + "-" + sday
    elif (not syear) and (not smonth) and (not sday):
        sdate = None
    else:
        flash("Incorrect date format")
        return redirect(url_for("frontend_api.s17_tech_vieworders_front"))

    if eyear and emonth and eday:
        edate = eyear + "-" + emonth + "-" + eday
    elif (not eyear) and (not emonth) and (not eday):
        edate = None
    else:
        flash("Incorrect date format")
        return redirect(url_for("frontend_api.s17_tech_vieworders_front"))

    conn = db.connect()
    cur = conn.cursor()
    orders = []
    name = "None"
    drones = []
    try:
        name = get_name(username)
        drones = get_drone(username)

        cur.callproc('drone_technician_view_order_history', [username, sdate, edate])
        cur.execute('select * from drone_technician_view_order_history_result')
        conn.commit()
        result = cur.fetchall()
        # print(result)
        for re in result:
            # print(re)
            list_data = list(map(str, re))
            orders.append(list_data)
        # print(orders)
    except Exception as e:
        print(e)
    finally:
        conn.close()

    return render_template("s17_tech_vieworders.html", name=name, drones=drones, orders=orders)


def get_name(username):
    conn = db.connect()
    cur = conn.cursor()
    cur.execute('select concat(firstname," ",lastname) from users where username =%s', [username])
    name = cur.fetchall()[0][0]
    conn.commit()
    conn.close()
    return name


def get_drone(username):
    conn = db.connect()
    cur = conn.cursor()
    cur.execute('select id from drone where dronetech =%s and dronestatus ="Available"', [username])
    result = cur.fetchall()
    conn.commit()
    # print(result)
    drones = []
    for d in result:
        drones.append(d[0])
    conn.close()
    return drones


@backend_api.route('/s17_assgin_drone', methods=['POST'])
def s17_assgin_drone_back():
    username = config.USERNAME
    try:
        oid = request.form["oid"]
        operator = request.form["operator"]
        did = request.form["did"]
    except:
        return redirect(url_for("frontend_api.s17_tech_vieworders_front"))

    # print(request.form)

    if operator == "None" and did == "None":
        return redirect(url_for("frontend_api.s17_tech_vieworders_front"))
    if (operator != "None" and did == "None") or (operator == "None" and did != "None"):
        flash("operator and drone must be assigned together")
        return redirect(url_for("frontend_api.s17_tech_vieworders_front"))
    try:
        status = request.form["status"]
    except:
        flash("Pending status is not allowed")
        return redirect(url_for("frontend_api.s17_tech_vieworders_front"))

    conn = db.connect()
    cur = conn.cursor()

    try:
        cur.callproc('dronetech_assign_order', [username, did, status, oid])
        conn.commit()
        flash("Update Succeed!")
    except Exception as e:
        print(e)
    finally:
        conn.close()
    return redirect(url_for("frontend_api.s17_tech_vieworders_front"))


@backend_api.route('/s18_tech_orderdetails', methods=['POST'])
def s18_tech_orderdetails_back():
    username = config.USERNAME
    # print(request.form)
    try:
        oid = request.form["selected"]
        print(username, oid)
    except Exception as e:
        print(e)
        return redirect(url_for("frontend_api.s17_tech_vieworders_front"))

    conn = db.connect()
    cur = conn.cursor()
    detail = None
    items = []
    try:
        cur.callproc('dronetech_order_details', [username, oid])
        cur.execute('select * from dronetech_order_details_result')
        conn.commit()
        row_headers = [x[0] for x in cur.description]
        result = cur.fetchall()

        detail = dict(zip(row_headers, list(map(str, result[0]))))

        cur.callproc('dronetech_order_items', [username, oid])
        cur.execute('select * from dronetech_order_items_result')
        conn.commit()
        row_headers = [x[0] for x in cur.description]
        result = cur.fetchall()

        print(result)
        items = {}
        for row in result:
            items[row[0]] = row[1]
    except Exception as e:
        print(e)
    finally:
        conn.close()
    return render_template("s18_tech_orderdetails.html", detail=detail, items=items)


@backend_api.route('/s19_track_drone', methods=['POST'])
def s19_track_drone_back():
    username = config.USERNAME  # current user
    did = request.form["id"]
    if did:
        did = int(did)
    else:
        did = None
    status = request.form["status"]
    print(username, did, status)

    conn = db.connect()
    cur = conn.cursor()
    drones = []
    try:
        cur.callproc('dronetech_assigned_drones', [username, did, status])
        cur.execute('select * from dronetech_assigned_drones_result')
        conn.commit()
        result = cur.fetchall()
        print(result)

        for re in result:
            drones.append(re)
        print(drones)
    except Exception as e:
        print(e)
    finally:
        conn.close()

    return render_template("s19_track_drone.html", drones=drones, status=status)
