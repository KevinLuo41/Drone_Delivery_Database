from flask import Blueprint, request, Response, session, redirect, render_template
import backend



frontend_api = Blueprint('frontend_api', __name__)
@frontend_api.route('/')
def index():
    return render_template("index.html")

@frontend_api.route('/admin_home', methods=['GET','POST'])
def admin_home():
    return render_template("admin_home.html")

@frontend_api.route('/create_chain', methods=['GET','POST'])
def create_chain_front():
    return render_template("create_chain.html")

@frontend_api.route('/create_store', methods=['GET','POST'])
def create_store_front():
    return render_template("create_store.html")