from flask import Blueprint, request, render_template
import backend

frontend_api = Blueprint('frontend_api', __name__)


@frontend_api.route('/', methods=['GET'])
def s1_login_front():
    return render_template("s1_login.html")


@frontend_api.route('/s2_register', methods=['GET'])
def s2_register_front():
    return render_template("s2_register.html")


# S3
@frontend_api.route('/s3_home_admin', methods=['GET'])
def s3_home_admin_front():
    return render_template("s3_home_admin.html")


@frontend_api.route('/s3_home_tech', methods=['GET'])
def s3_home_tech_front():
    return render_template("s3_home_tech.html")


@frontend_api.route('/s3_home_manager', methods=['GET'])
def s3_home_manager_front():
    return render_template("s3_home_manager.html")


@frontend_api.route('/s3_home_customer', methods=['GET'])
def s3_home_customer_front():
    return render_template("s3_home_customer.html")


# S4
@frontend_api.route('/s4_create_chain', methods=['GET'])
def s4_create_chain_front():
    return render_template("s4_create_chain.html")


# S5
@frontend_api.route('/s5_create_store', methods=['GET'])
def s5_create_store_front():
    chains = backend.s5_front_helper()
    # print(chains)
    return render_template("s5_create_store.html", data=chains)


# S6

@frontend_api.route('/s6_create_drone', methods=['GET'])
def s6_create_drone_front():
    id, ziplist = backend.s6_front_helper1()
    print(id)
    return render_template("s6_create_drone.html", id=id, ziplist=ziplist)


# S7
@frontend_api.route('/s7_create_item', methods=['GET'])
def s7_create_item_front():
    return render_template("s7_create_item.html")


# S8
@frontend_api.route('/s8_view_customers', methods=['GET'])
def s8_admin_view_customers_view():
    print('in front')
    return render_template("s8_view_customers.html")


# S9
@frontend_api.route('/s9_create_chainitem', methods=['GET'])
def s9_create_chainitem():
    chain_name, item_list, new_PLU = backend.s9_front_helper()
    return render_template("s9_create_chainitem.html", chain_name=chain_name, item_list=item_list, new_PLU=new_PLU)
