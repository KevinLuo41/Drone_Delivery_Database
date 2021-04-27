from flask import Blueprint, request, Response, redirect, jsonify, url_for
from flaskext.mysql import MySQL
import frontend

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

    return redirect(url_for('frontend_api.index'))


@backend_api.route('/create_chain_back', methods=["POST"])
def create_chain_back():
    chain_name = request.form['chain-name']
    conn = db.connect()
    cur = conn.cursor()
    try:
        cur.callproc('admin_create_grocery_chain', [chain_name])
        conn.commit()
    except Exception as e:
        print(e)
        return Response(status=500)
    finally:
        cur.execute('select * from chain')
        data = cur.fetchall()
        print(data)
        conn.close()
        return redirect(url_for('frontend_api.create_chain_front'))

    # return redirect(url_for('frontend_api.create_chain_front'))
