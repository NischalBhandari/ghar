from app import app
import unittest
class FlaskTestCase(unittest.TestCase):
	# test the status code returned by the page
	def test_home(self):
		tester=app.test_client(self)
		response=tester.get('/',content_type='html/text')
		self.assertEqual(response.status_code,200)
#test wether the page returns an actual page returns an string

	def test_home_string(self):
		tester=app.test_client(self)
		response=tester.get('/')
		self.assertIn(b'Welcome to Ghar Khoj',response.data)
	def test_login_success(self):
		tester=app.test_client(self)
		response=tester.post('/login',data=dict(username="admin",password="admin"),follow_redirects=True)
		self.assertIn(b'Hello test',response.data)
	def test_login_failure(self):
		tester=app.test_client(self)
		response=tester.post('/login',data=dict(username="admin",password="what"),follow_redirects=True)
		self.assertIn(b'Invalid credentials, Please try again',response.data)
	def test_logout(self):
		tester=app.test_client(self)
		tester.post('/login',data=dict(username="admin",password="admin"),follow_redirects=True)
		response=tester.get('/logout',follow_redirects=True)
		self.assertIn(b'you were just logged out',response.data)
	def test_ghar_requires_login(self):
		tester=app.test_client(self)
		response=tester.get('/ghar/nischal',follow_redirects=True)
		self.assertTrue(b'You need to Login First' in response.data)

if __name__=='__main__':
	unittest.main()