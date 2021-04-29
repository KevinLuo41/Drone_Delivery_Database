from flask import Blueprint, request, Response, redirect, jsonify, url_for, flash
from flaskext.mysql import MySQL
import json

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
        data = select_chain()
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
    zip = request.form['zip']

    conn = db.connect()
    cur = conn.cursor()
    try:
        cur.callproc('admin_create_new_store', [store_name,chain_name,street,city,state,zip])
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

@backend_api.route('/s6_front_helper2')
def s6_front_helper2():
    zipcode = request.args.get("ziplist")
    conn = db.connect()
    cur = conn.cursor()
    cur.execute('select distinct(username) from drone_tech natural join users where zipcode = %s',[zipcode])
    conn.commit()

    result = cur.fetchall()
    data = [{"username": x[0]} for x in result]
    print(data)
    return jsonify(data)