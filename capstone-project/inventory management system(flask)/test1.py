import os
os.environ['DATABASE_URL'] = 'sqlite:///test.db'
os.environ['SECRET_KEY'] = 'test_secret_key'

import unittest
from datetime import date
from flask import session
from app import app, db
from app.models import User, Item

class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
        app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self):
        with app.app_context():
            db.create_all()
            admin_user = User(username='admins', password='adminpass', email='admins@nucleusteq.com', is_admin='1')
            db.session.add(admin_user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

        response_with_error = self.client.get('/register?error=500')
        self.assertEqual(response_with_error.status_code, 200)

    def test_dashboard(self):
        with self.client.session_transaction() as sess:
            sess['username'] = 'testuser'
            sess['is_admin'] = False

        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)

    def test_admin_dashboard(self):
        with self.client.session_transaction() as sess:
            sess['username'] = 'admins'
            sess['is_admin'] = True

        response = self.client.get('/admin_dashboard')
        self.assertEqual(response.status_code, 200)

    def test_admin_items(self):
        with self.client.session_transaction() as sess:
            sess['username'] = 'admins'
            sess['is_admin'] = True

        response = self.client.get('/admin/items')
        self.assertEqual(response.status_code, 200)

    def test_employee_dashboard(self):
        with self.client.session_transaction() as sess:
            sess['username'] = 'testuser'
            sess['is_admin'] = False

        response = self.client.get('/employee_dashboard')
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        with app.app_context():
            user = User(username='testuser', password='testpass', email='test@nucleusteq.com')
            db.session.add(user)
            db.session.commit()

        response = self.client.post('/api/login', json={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)

    def test_login_failure(self):
        response = self.client.post('/api/login', json={'username': 'wronguser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 401)

    def test_logout(self):
        with self.client.session_transaction() as sess:
            sess['username'] = 'testuser'

        response = self.client.post('/api/logout')
        self.assertEqual(response.status_code, 200)

    def test_change_password(self):
        with app.app_context():
            user = User(username='testuser', password='testpass', email='test@nucleusteq.com')
            db.session.add(user)
            db.session.commit()
            
        with self.client.session_transaction() as sess:
            sess['username'] = 'testuser'

        response = self.client.post('/api/change_password', data={'new_password': 'newpass'})
        self.assertEqual(response.status_code, 200)

    def test_add_user(self):
        response = self.client.post('/api/register', data={
            'username': 'newuser',
            'password': 'newpass',
            'email': 'newuser@nucleusteq.com',
            'is_admin': False
        })
        self.assertEqual(response.status_code, 200)

    def test_admin_add_user(self):
        with self.client.session_transaction() as sess:
            sess['username'] = 'admins'
            sess['is_admin'] = True

        response = self.client.post('/api/admin/register', json={
            'username': 'newadminuser',
            'password': 'newpass',
            'email': 'newadminuser@nucleusteq.com',
            'is_admin': '1'
        })
        self.assertEqual(response.status_code, 200)

    def test_del_user(self):
        with app.app_context():
            user = User(username='deluser', password='delpass', email='deluser@nucleusteq.com')
            db.session.add(user)
            db.session.commit()

        with self.client.session_transaction() as sess:
            sess['username'] = 'admins'
            sess['is_admin'] = True

        response = self.client.post('/user/delete', json={'username': 'deluser', 'email': 'deluser@nucleusteq.com'})
        self.assertEqual(response.status_code, 200)

    def test_get_users(self):
        with self.client.session_transaction() as sess:
            sess['username'] = 'admins'
            sess['is_admin'] = True

        response = self.client.get('/api/get_users')
        self.assertEqual(response.status_code, 200)

    def test_get_non_admin_users(self):
        with self.client.session_transaction() as sess:
            sess['username'] = 'admins'
            sess['is_admin'] = True

        response = self.client.get('/users/non_admins')
        self.assertEqual(response.status_code, 200)

    def test_get_items_unauthorized(self):
        with self.client.session_transaction() as sess:
            sess.clear()
        response = self.client.get('/api/items')
        self.assertEqual(response.status_code, 401)

    def test_get_items_authorized(self):
        with self.client.session_transaction() as sess:
            sess['username'] = 'testuser'

        response = self.client.get('/api/items')
        self.assertEqual(response.status_code, 200)

    def test_add_item(self):
        with self.client.session_transaction() as sess:
            sess['username'] = 'admins'
            sess['is_admin'] = True

        response = self.client.post('/item/add', json={
            'item_name': 'item1',
            'serial_number': 12345,
            'bill_no': 67890,
            'date_of_purchase': date(2024,1,1),
            'warranty': date(2025,1,1)
        })
        self.assertEqual(response.status_code, 200)

    def test_update_item(self):
        with app.app_context():
            item = Item(item_name='item2', serial_number=12356, bill_no=67895, date_of_purchase=date(2023, 1, 1), warranty=date(2024, 1, 1))
            db.session.add(item)
            db.session.commit()
            item_id = item.item_id

        with self.client.session_transaction() as sess:
            sess['username'] = 'admins'
            sess['is_admin'] = True

        response = self.client.post('/item/update', json={
            'item_id': item_id,
            'serial_number': 12346,
            'bill_no': 67891,
            'date_of_purchase': date(2024,2,1),
            'warranty': date(2026,2,1),
            'assigned_to': None
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        with app.app_context():
            item = Item(item_name='item1', serial_number=12345, bill_no=67890, date_of_purchase=date(2024, 1, 1), warranty=date(2025, 1, 1))
            db.session.add(item)
            db.session.commit()
            item_id = item.item_id

        with self.client.session_transaction() as sess:
            sess['username'] = 'admins'
            sess['is_admin'] = True

        response = self.client.post('/item/delete', json={'item_id': item_id})
        self.assertEqual(response.status_code, 200)

    def test_get_unassigned_items(self):
        with self.client.session_transaction() as sess:
            sess['username'] = 'admins'
            sess['is_admin'] = True

        response = self.client.get('/item/unassigned')
        self.assertEqual(response.status_code, 200)

    def test_item_assignment(self):
        with app.app_context():
            item = Item(item_name='item1', serial_number=12345, bill_no=67890, date_of_purchase=date(2024, 1, 1), warranty=date(2025, 1, 1))
            user = User(username='testuser', password='testuser', email='testuser@nucleusteq.com', is_admin=False, first_login=False)
            db.session.add(item)
            db.session.add(user)
            db.session.commit()
            item_id = item.item_id

        with self.client.session_transaction() as sess:
            sess['username'] = 'admins'
            sess['is_admin'] = True

        response = self.client.post('/item/assignment', json={'item_id': item_id, 'assigned_to': 'testuser'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
