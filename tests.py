from datetime import datetime
import unittest
from app import create_app, db
from app.models import User
from config import Config

class TestConfig(Config):
  TESTING=True
  SQLALCHEMY_DATABASE_URI = 'sqlite://'

class UserModelCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app(TestConfig)
    self.client = self.app.test_client()
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()
  
  def test_password_hashing(self):
    u = User(first_name="John", last_name="Doe", email="john@tesst.com", password="password")
    self.assertFalse(u.check_password("p@ssword"))
    self.assertTrue(u.check_password("password"))

  def test_user_registration(self):
    response = self.client.post('/register', json={
      "email": "jane@test.com",
      "first_name": "Jane",
      "last_name": "Doe",
      "password": "password",
      "phone_number": "1234567890"
    })
    self.assertEqual(response.status_code, 201)
    self.assertEqual(User.query.count(), 1)
  
  def test_user_login(self):
    self.client.post('/register', json={
      "email": "jane@test.com",
      "first_name": "Jane",
      "last_name": "Doe",
      "password": "password",
      "phone_number": "1234567890"
    })

    response = self.client.post('/login', json={
    "email": "jane@test.com",
    "password": "password"
    })
    self.assertEqual(response.status_code, 200)
    self.assertIn('access_token', response.json)

  def test_user_profile_retrieval(self):
    self.client.post('/register', json={
      "email": "jane@test.com",
      "first_name": "Jane",
      "last_name": "Doe",
      "password": "password",
      "phone_number": "1234567890"
    })

    login_response = self.client.post('/login', json={
    "email": "jane@test.com",
    "password": "password"
    })
        
    access_token = login_response.json['access_token']

    headers = {'Authorization': f'Bearer {access_token}'}
    response = self.client.get('/profile', headers=headers)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['first_name'], 'Jane')

if __name__ == "__main__":
  unittest.main(verbosity=2)