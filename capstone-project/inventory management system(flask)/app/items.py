from .models import Item,  db
from . import app
from .auth import *
from .main import *
from datetime import datetime
from email.utils import parsedate_to_datetime
from flask import request, jsonify, render_template

@app.route('/item/add', methods=['POST'])
@admin_required
def add_item():
    data = request.get_json()
    item_name = data.get('item_name')
    serial_number = int(data.get('serial_number'))
    bill_no = int(data.get('bill_no'))
    date_of_purchase = data.get('date_of_purchase',None) if data.get('date_of_purchase',None) !="" else None
    warranty = data.get('warranty',None) if data.get('warranty',None) != "" else None
    print(date_of_purchase, warranty,'#############################')
    if app.config['TESTING']:
        date_of_purchase = parsedate_to_datetime(date_of_purchase).date()
        warranty = parsedate_to_datetime(warranty).date()
    print(date_of_purchase, warranty,'#############################')

    try:
        new_item = Item(item_name=item_name, serial_number=serial_number, bill_no=bill_no, date_of_purchase=date_of_purchase, warranty=warranty)
        db.session.add(new_item)
        db.session.commit()
        logger.info(f"Item {serial_number} added by admin {session.get('username')}")
        return jsonify({"success": True}), 200
    except Exception as e:
        logger.exception(f'Exception {str(e)} occurred while adding item {serial_number}')
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/item/update', methods=['POST'])
@admin_required
def update_item():
    data = request.get_json()
    item_id = data.get('item_id')
    serial_number = data.get('serial_number')
    bill_no = data.get('bill_no')
    date_of_purchase = data.get('date_of_purchase')
    warranty = data.get('warranty')
    assigned_to = data.get('assigned_to') if data.get('assigned_to')!='null' else None
    if app.config['TESTING']:
        date_of_purchase = parsedate_to_datetime(date_of_purchase).date()
        warranty = parsedate_to_datetime(warranty).date()
    try:
        item = Item.query.filter_by(item_id=item_id).first()
        item.serial_number = serial_number
        item.bill_no = bill_no
        if date_of_purchase!="":
            item.date_of_purchase = date_of_purchase
        item.assigned_to = assigned_to
        db.session.commit()
        logger.info(f"Item {item_id} updated by admin {session.get('username')}")
        return jsonify({"success": True}), 200
    except Exception as e:
        logger.exception(f'Exception {str(e)} occurred while updating item {item_id}')
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/item/delete', methods=['POST'])
@admin_required
def delete_item():
    data = request.get_json()
    item_id = data.get('item_id')

    try:
        item = Item.query.filter_by(item_id=item_id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            logger.info(f"Item {item_id} deleted by admin {session.get('username')}")
            return jsonify({"success": True}), 200
        else:
            logger.warning(f"Failed to delete item {item_id}")
            return jsonify({"success": False, "error": "Item not found"}), 404
    except Exception as e:
        logger.exception(f'Exception {str(e)} occurred while deleting item {item_id}')
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/item/assignment', methods=['POST'])
@admin_required
def item_assignment():
    data = request.get_json()
    item_id = data.get('item_id')
    assigned_to = data.get('assigned_to')

    try:
        item = Item.query.filter_by(item_id=item_id).first()
        item.assigned_to = assigned_to
        db.session.commit()
        logger.info(f"Item {item_id} assigned to {assigned_to} by admin {session.get('username')}")
        return jsonify({"success": True}), 200
    except Exception as e:
        logger.exception(f'Exception {str(e)} occurred while assigning item {item_id}')
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/item/unassigned', methods=['GET'])
@admin_required
def get_unassigned_items():
    try:
        items = Item.query.filter_by(assigned_to=None).all()
        unassigned_items = [{"item_id": item.item_id, "serial_number": item.serial_number} for item in items]
        return jsonify({"success": True, "unassigned_items": unassigned_items}), 200
    except Exception as e:
        logger.exception(f'Exception {str(e)} occurred while fetching unassigned items')
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/item_assignment_page')
@admin_required
def item_assignment_page():
    return render_template('item_assignment.html')

@app.route('/items_page')
@admin_required
def items_page():
    return render_template('admin_items.html')

@app.route('/api/assignment_list', methods=['GET'])
@admin_required
def assignment_list():
    try:
        items = Item.query.with_entities(Item.item_id, Item.assigned_to).all()
        logger.info("Fetched assignment list")
        return jsonify([{"item_id": item.item_id, "assigned_to": item.assigned_to} for item in items]), 200
    except Exception as e:
        logger.exception(f'Exception {str(e)} occurred while fetching assignment list')
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/items", methods=['GET'])
def get_items():
    username = session.get('username')
    if username is None or username == '':
        return jsonify({"success": False, "message": "User not logged in"}), 401
    items = Item.query.all()
    items_list = [{
        "item_id": item.item_id,
        "item_name": item.item_name,
        "serial_number": item.serial_number,
        "bill_no": item.bill_no,
        "date_of_purchase": item.date_of_purchase,
        "assigned_to": item.assigned_to,
        "warranty": item.warranty
    } for item in items]
    return jsonify({"success": True, "items": items_list}), 200