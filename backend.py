from flask import Blueprint, request, Response, session, redirect
from flaskext.mysql import MySQL
import json
import datetime

db = MySQL()
backend_api = Blueprint('backend_api', __name__)