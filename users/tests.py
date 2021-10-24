import json
import bcrypt

from django.test  import TestCase, Client

from users.models import User

class SignUpTest(TestCase):
    def setUp(self):
        User.objects.create(
            id           = 1,
            email        = 'user1@gmail.com',
            password     = 'abc1234!',
            name         = '박유저',
            phone_number = '01012345678'
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signupview_post_success(self):
        client = Client()
        
        user  = {
            'email'        : 'user2@gmail.com',
            'password'     : 'abc1234!',
            'name'         : '김유저',
            'phone_number' : '01000000000'
        }

        response = client.post('/users/signup', json.dumps(user), content_type = 'application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
            {
                'message' : 'SUCCESS'
            }
        )
    
    def test_signupview_post_invalid_email(self):
        client = Client()
        
        user = {
            'email'        : 'user2gmail',
            'password'     : 'abc1234!',
            'name'         : '김유저',
            'phone_number' : '01000000000'
        }

        response = client.post('/users/signup', json.dumps(user), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'INVALID_EMAIL'
            }
        )
    
    def test_signupview_post_invalid_password(self):
        client = Client()
        
        user = {
            'email'        : 'user2@gmail.com',
            'password'     : '1234',
            'name'         : '김유저',
            'phone_number' : '01000000000'
        }

        response = client.post('/users/signup', json.dumps(user), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'INVAILD_PASSWORD'
            }
        )

    def test_signupview_post_duplicated_email(self):
        client = Client()
        
        user = {
            'email'        : 'user1@gmail.com',
            'password'     : 'abc1234!',
            'name'         : '김유저',
            'phone_number' : '01000000000'
        }

        response = client.post('/users/signup', json.dumps(user), content_type = 'application/json')

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(),
            {
                'message' : 'ALREADY_EXISTS_EMAIL'
            }
        )
    
    def test_signupview_post_key_error_email(self):
        client = Client()
        
        user = {
            'password'     : 'abc1234!',
            'name'         : '김유저',
            'phone_number' : '01000000000'
        }

        response = client.post('/users/signup', json.dumps(user), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR'
            }
        )
    
    def test_signupview_post_key_error_password(self):
        client = Client()
        
        user = {
            'email'        : 'user2@gmail.com',
            'name'         : '김유저',
            'phone_number' : '01000000000'
        }

        response = client.post('/users/signup', json.dumps(user), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR'
            }
        )

    def test_signupview_post_key_error_name(self):
        client = Client()
        
        user = {
            'email'        : 'user2@gmail.com',
            'password'     : 'abc1234!',
            'phone_number' : '01000000000'
        }

        response = client.post('/users/signup', json.dumps(user), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR'
            }
        )

    def test_signupview_post_jsondecode_error(self):
        client = Client()
 
        response = client.post('/users/signup')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'JSON_DECODE_ERROR'
            }
        )

class SigninTest(TestCase):
    def setUp(self):
        password = 'abc1234!'
        User.objects.create(
            id           = 1,
            email        = 'user1@gmail.com',
            password     = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            name         = '박유저',
            phone_number = '01012345678' 
        )
    
    def tearDown(self):
        User.objects.all().delete()

    def test_signinview_post_success(self):
        client = Client()
        
        user = {
            'email'    : 'user1@gmail.com',
            'password' : 'abc1234!'
        }
        response     = client.post('/users/signin', json.dumps(user), content_type='application/json')
        access_token = response.json()['access_token']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
                'access_token' : access_token
            }
        )

    def test_signinview_post_invalid_email(self):
        client = Client()
        
        user = {
            'email'    : 'user2@gmail.com',
            'password' : 'abc1234!'
        }
        response     = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 
            {
                'message' : 'INVALID_USER_EMAIL'
            }
        )
    
    def test_signinview_post_invalid_password(self):
        client = Client()
        
        user = {
            'email'    : 'user1@gmail.com',
            'password' : 'abc1234@'
        }
        response     = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 
            {
                'message' : 'INVALID_USER_PASSWORD'
            }
        )

    def test_signinview_post_key_error_email(self):
        client = Client()
        
        user = {
            'password' : 'abc1234!'
        }
        response     = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message' : 'KEY_ERROR'
            }
        )

    def test_signinview_post_key_error_password(self):
        client = Client()
        
        user = {
             'email' : 'user1@gmail.com'
        }
        response     = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message' : 'KEY_ERROR'
            }
        )

    def test_signinview_post_jsondecod_eerror(self):
        client = Client()

        response     = client.post('/users/signin')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message' : 'JSON_DECODE_ERROR'
            }
        )