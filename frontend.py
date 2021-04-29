from flask import Blueprint, request, Response, session, flash, render_template
import backend


frontend_api = Blueprint('frontend_api', __name__)

@frontend_api.route('/', methods=['GET','POST'])
def s1_login_front():
    return render_template("s1_login.html")

@frontend_api.route('/s2_register', methods=['GET','POST'])
def s2_register_front():
    return render_template("s2_register.html")

# S3
@frontend_api.route('/s3_home_admin', methods=['GET','POST'])
def s3_home_admin_front():
    return render_template("s3_home_admin.html")

@frontend_api.route('/s3_home_tech', methods=['GET','POST'])
def s3_home_tech_front():
    return render_template("s3_home_tech.html")

@frontend_api.route('/s3_home_manager', methods=['GET','POST'])
def s3_home_manager_front():
    return render_template("s3_home_manager.html")

@frontend_api.route('/s3_home_customer', methods=['GET','POST'])
def s3_home_customer_front():
    return render_template("s3_home_customer.html")

# S4
@frontend_api.route('/s4_create_chain', methods=['GET','POST'])
def s4_create_chain_front():
    return render_template("s4_create_chain.html")

# S5
@frontend_api.route('/s5_create_store', methods=['GET','POST'])
def s5_create_store_front():
    chains = backend.s5_front_helper()
    # print(chains)
    return render_template("s5_create_store.html",data=chains)

# S6

@frontend_api.route('/s6_create_drone', methods=['GET','POST'])
def s6_create_drone_front():
    id,ziplist = backend.s6_front_helper1()
    print(id)
    return render_template("s6_create_drone.html",id = id, ziplist=ziplist)