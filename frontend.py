from flask import Blueprint, request, render_template
import backend, config

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


# S11
@frontend_api.route('/s11_view_drone', methods=['GET'])
def s11_view_drone_view():
    # print('in front')
    return render_template("s11_view_drone.html")


# S12
@frontend_api.route('/s12_manage_store', methods=['GET'])
def s12_manage_store():
    chain_name = backend.get_chain_name()
    store_name = backend.get_store_name(chain_name)
    return render_template("s12_manage_store.html", chain_name=chain_name, store_name=store_name)


# S13
@frontend_api.route('/s13_change_card', methods=['GET'])
def s13_change_card():
    username = config.USERNAME
    print(username)
    fname, lname = backend.get_name(username)
    return render_template("s13_change_card.html", username=username, fname=fname, lname=lname)


@frontend_api.route('/s14_view_orderhistory', methods=['GET'])
def s14_view_orderhistory():
    username = config.USERNAME
    print(username)
    ids = backend.get_order_id(username)
    # print(ids)
    return render_template("s14_view_orderhistory.html", username=username, id=-1, ids=ids, data=None)

@frontend_api.route('/s15_view_storeitems', methods=['GET'])
def s15_view_storeitems():
    username = config.USERNAME
    chainlist = backend.s15_get_chain()
    print(chainlist)
    return render_template("s15_view_storeitems.html",Username = username, chainlist = chainlist)


def s16_review_order():
    return render_template("s16_review_order.html")


def s17_tech_vieworders():
    return render_template("s17_tech_vieworders.html")


def s18_tech_orderdetails():
    return render_template("s18_tech_orderdetails.html")


def s19_track_drone():
    return render_template("s19_track_drone.html")
