from flask import Blueprint, redirect, flash,url_for, render_template
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


@frontend_api.route('/s10_view_tech', methods=['GET'])
def s10_view_tech():
    chain_name = backend.get_chain_name()
    locations = backend.get_store_name(chain_name)
    users = backend.get_tech_and_store(chain_name)
    return render_template("s10_view_tech.html", chain_name=chain_name, locations=locations, users=users)


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
    fname, lname = backend.get_flname(username)
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


@frontend_api.route('/s16_review_order', methods=['GET'])
def s16_review_order_front():
    username = config.USERNAME
    result = backend.s16_check_creating(username)
    if not result:
        flash("No creating order is found!")
        return render_template("s3_home_customer.html")
    else:
        chain,store = result[0]

    return backend.s16_review_order_back(chain,store)

@frontend_api.route('/s17_tech_vieworders', methods=['GET'])
def s17_tech_vieworders_front():
    return render_template("s17_tech_vieworders.html")

@frontend_api.route('/s18_tech_orderdetails', methods=['GET'])
def s18_tech_orderdetails_front():
    return render_template("s18_tech_orderdetails.html")

@frontend_api.route('/s19_track_drone', methods=['GET'])
def s19_track_drone_front():
    return render_template("s19_track_drone.html")
