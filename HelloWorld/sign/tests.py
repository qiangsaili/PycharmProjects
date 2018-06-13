from django.test import TestCase
from sign.models import Event, Guest
from django.contrib.auth.models import User

# Create your tests here.
class ModelTest(TestCase):
	def setUp(self):
		Event.objects.create(id=1, name='oneplus 3 event', status=True, limite=2000, address=u'深圳', start_time=
		'2018-05-31 02:18:22')
		Guest.objects.create(id=1, event_id=1,realname='Alen', phone='18791010100', email='alen@mail.com',sign=False)

	def test_event_models(self):
		result = Event.objects.get(name='oneplus 3 event')
		self.assertEqual(result.address, u'深圳')
		self.assertTrue(result.status)

	def test_guest_models(self):
		result = Guest.objects.get(phone='18791010100')
		self.assertEqual(result.realname, 'Alen')
		self.assertFalse(result.sign)
		
class IndexPageTest(TestCase):
	'''测试index视图'''
	def test_index_page_renders_index_template(self):
		'''测试index视图'''
		response =self.client.get('/index/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'index.html')
		
class LoginActionTest(TestCase):
	'''测试登录动作'''
	def setUp(self):
		User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
		
	def test_add_admin(self):
		'''测试添加用户'''
		user = User.objects.get(username='admin')
		self.assertEqual(user.username, 'admin')
		self.assertEqual(user.email, 'admin@mail.com')
		
	def test_login_action_username_password_null(self):
		'''用户名密码为空'''
		test_data = {'username':'', 'password': ''}
		response = self.client.post('/login_action/', data=test_data)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"username or password error!", response.content)
		
	def test_login_action_username_password_error(self):
		'''用户名密码错误'''
		test_data = {'username':'abc', 'password': '123'}
		response = self.client.post('/login_action/', data=test_data)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"username or password error!", response.content)
		
	def test_login_action_username_password_success(self):
		'''登录成功'''
		test_data = {'username':'admin', 'password': 'admin123456'}
		response = self.client.post('/login_action/', data=test_data)
		self.assertEqual(response.status_code, 302)
		
class EventManageTest(TestCase):
	'''发布会管理'''
	def setUp(self):
		User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
		Event.objects.create(id=1, name='xiaomi5', status=True, limite=2000, address='beijing', start_time=
		'2018-05-31 02:18:22')
		self.login_user = {'username': 'admin', 'password': 'admin123456'}
		
	def test_event_manage_success(self):
		'''测试发布会：xiaomi5'''
		response = self.client.post('/login_action/', data=self.login_user)
		response = self.client.post('/event_manage/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"xiaomi5", response.content)
		self.assertIn(b"beijing", response.content)
	
	def test_event_manage_search_success(self):
		'''测试发布会搜索'''
		response = self.client.post('/login_action/', data=self.login_user)
		response = self.client.post('/search_name/', {"name": "xiaomi5"})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"xiaomi5", response.content)
		self.assertIn(b"beijing", response.content)

class GuestManageTest(TestCase):
	'''嘉宾管理'''
	def setUp(self):
		User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
		Event.objects.create(id=1, name='xiaomi5', status=1, limite=2000, address='beijing', start_time=
		'2018-05-31 02:18:22')
		Guest.objects.create(id=1, event_id=1, realname='Alen', phone='18791010100', email='alen@mail.com', sign=0)
		self.login_user = {'username': 'admin', 'password': 'admin123456'}
		
	def test_guest_manage_success(self):
		'''测试嘉宾信息：Alen'''
		response = self.client.post('/login_action/', data=self.login_user)
		response = self.client.post('/guest_manage/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"Alen", response.content)
		self.assertIn(b"18791010100", response.content)
		
	def test_guest_manage_search_success(self):
		'''测试嘉宾搜索'''
		response = self.client.post('/login_action/', data=self.login_user)
		response = self.client.post('/search_name_guest/', {"name": "Alen"})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"Alen", response.content)
		self.assertIn(b"18791010100", response.content)