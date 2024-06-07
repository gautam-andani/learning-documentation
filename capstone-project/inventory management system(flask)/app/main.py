from flask import Flask, request, jsonify, render_template, session, redirect, url_for, make_response
# from functools import wraps
from . import app
from .models import User, Item, db
from .auth import admin_required, login_required
import logging
from .items import *

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    session.clear()
    logger.warning("Login page has arrived")
    return render_template('login.html'),200

@app.route('/register')
def register():
    error = request.args.get('error')
    if error and int(error) == 500:
        return render_template('register.html', message="Some error has occured please try something else")
    return render_template("register.html")


@app.route('/dashboard')
def dashboard():
    logger.info(f"{session.get('username')} accessed the dashboard")
    return redirect('/admin_dashboard' if session.get('is_admin') else '/employee_dashboard')

@app.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    logger.info(f'Admin {session.get("username")} accessed admin dashboard')
    return render_template('admin_dashboard.html', users_route=url_for('admin_users'), items_route=url_for('admin_items'))

@app.route('/admin/items')
def admin_items():
    return render_template('admin_items.html')

    
@app.route('/employee_dashboard')
@login_required
def employee_dashboard():
    logger.info(f"Employee {session.get('username')} accessed employee dashboard")
    return render_template('employee_dashboard.html')


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    try:
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = user.username
            session['is_admin'] =  is_admin(user.is_admin)
            if int(user.first_login)==1:
                user.first_login = False
                db.session.commit()
                logger.info(f"User {username} logged in for the first time")
                return jsonify({"success": True, "is_admin": is_admin(user.is_admin), "first_login": True}), 200
            else:
                logger.info(f"User {username} logged in")
                return jsonify({"success": True, "is_admin": is_admin(user.is_admin), "first_login": False}), 200
        else:
            logger.warning(f"Failed login attempt for username: {username}")
            return jsonify({"success": False, "error": "Invalid credentials"}), 401
    except Exception as e:
        logger.exception(f'Exception {str(e)} occurred during login for username: {username}')
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/logout", methods=['POST'])
def logout():
    logger.info(f"User {session.get('username')} logged out")
    session.clear()
    return jsonify({"success": True, "message": "LOGGED OUT"}), 200



@app.route('/change_password')
def password_form():
    logger.info(f"User {session.get('username')} accessed password change form")
    return render_template('password_change_form.html')

@app.route('/api/change_password', methods=['POST'])
def change_password():
    data = request.form
    username = session.get('username')
    new_password = data.get('new_password')

    if not username:
        logger.warning("Password change attempt without login")
        return jsonify(success=False, message="User not logged in"), 401

    try:
        user = User.query.filter_by(username=username).first()
        if user is None:
            logger.warning(f"User {username} not found")
            return jsonify(success=False, message="User not found"), 404
        
        user.password = new_password
        db.session.commit()
        logger.info(f"Password changed for user: {username}")
        return jsonify(success=True, message=f"Password changed successfully for user: {username}"), 200
    except Exception as e:
        logger.exception(f'Exception {str(e)} occurred during password change for user: {username}')
        return jsonify(success=False, message="An error occurred while changing the password"), 500
   

def add_user_func(username, password, email, is_admin):
    try:
        new_user = User(username=username, password=password, email=email, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding user: {e}")
        return False

@app.route('/api/register', methods=['POST'])
def add_user():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    is_admin = bool(data.get('is_admin'))
    
    if add_user_func(username, password, email, is_admin):
        session_user = session.get('username', 'self')
        logger.info(f"User {username} added by {session_user}")
        return redirect(url_for('index')), 200
    else:
        logger.exception(f"Exception occurred while adding user {username}")
        if session.get('is_admin'):
            return render_template('admin_dashboard.html', message="Error occurred while adding user"), 500
        return make_response(redirect(url_for('register', error=500)), 302)

@app.route('/api/admin/register', methods=['POST'])
@admin_required
def admin_add_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    is_admin = bool(data.get('is_admin'))
    try:
        new_user = User(username=username, password=password, email=email, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()
        logger.info(f"User {username} added by admin {session.get('username')}")
        return jsonify({"success": True, "message": "User added successfully!"}), 200
    except Exception as e:
        logger.exception(f'Exception {str(e)} occurred while adding user {username}')
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/user/delete', methods=['POST'])
@admin_required
def del_user():
    data = request.get_json()  # Use request.get_json() for JSON data
    username = data.get('username')
    email = data.get('email')

    try:
        user = User.query.filter_by(username=username, email=email).first()
        if user is None:
            return jsonify({"success": False, "error": "User not found"}), 404
        if user.username == 'admin':
            return jsonify({"success": False, "error": "Cannot delete main admin user"}), 400
        db.session.delete(user)
        db.session.commit()
        logger.info(f"User {username} deleted by admin {session.get('username')}")
        return jsonify({"success": True, "message": "User deleted successfully!"}), 200
    except Exception as e:
        logger.exception(f'Exception {str(e)} occurred while deleting user {username}')
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/admin/users')
@admin_required
def admin_users():
    return render_template('admin_users.html')

@app.route('/api/get_users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            "username": user.username,
            "email": user.email
        }
        user_list.append(user_data)
    return jsonify({"users": user_list})
        

@app.route('/api/emp_and_item_list', methods=['GET'])
@admin_required
def emp_and_item_list():
    try:
        items = Item.query.with_entities(Item.item_id, Item.serial_number, Item.assigned_to).all()
        users = User.query.with_entities(User.username).filter_by(is_admin=False).all()
        result = {
            "items": [{"item_id": item.item_id, "serial_number": item.serial_number, "assigned_to": item.assigned_to} for item in items],
            "users": [user.username for user in users]
        }
        logger.info("Fetched employee and item list")
        return jsonify(result), 200
    except Exception as e:
        logger.exception(f'Exception {str(e)} occurred while fetching employee and item list')
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/users/non_admins', methods=['GET'])
@admin_required
def get_non_admin_users():
    try:
        users = User.query.filter_by(is_admin=False).all()
        non_admin_users = [user.username for user in users]
        return jsonify({"success": True, "non_admin_users": non_admin_users}), 200
    except Exception as e:
        logger.exception(f'Exception {str(e)} occurred while fetching non-admin users')
        return jsonify({"success": False, "error": str(e)}), 500

def is_admin(db_object):
    if int(db_object) == 0:
        return False
    return True

if __name__ == '__main__':
    app.run(debug=True)
