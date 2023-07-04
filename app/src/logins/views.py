from flask import Blueprint, render_template, request, redirect, url_for, flash

from app import app

logins = Blueprint("logins", __name__)

@logins.route("/",methods=['GET'])
def index_get():
    return render_template('index.html')