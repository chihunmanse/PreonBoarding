import json
import jwt

from django.test  import TestCase, Client
from django.conf  import settings

from users.models import User
from posts.models import Post

class PostTest(TestCase):
    def setUp(self):
        user1 = User.objects.create(id = 1, email = 'user1@gmail.com', password = 'abc1234!', name = '박유저')
        user2 = User.objects.create(id = 2, email = 'user2@gmail.com', password = 'abc1234!', name = '김유저')

        global post1, post2
        post1 = Post.objects.create(id = 1, user = user1, title = '제목1', content = '내용1')
        post2 = Post.objects.create(id = 2, user = user2, title = '제목2', content = '내용2')

        global headers
        access_token = jwt.encode({'user_id':1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {'HTTP_AUTHORIZATION': access_token}
    
    def tearDown(self):
        User.objects.all().delete()
        Post.objects.all().delete()
    
    def test_postview_post_success(self):
        client = Client()

        post = {
            'title'   : '제목',
            'content' : '내용' 
        }

        response = client.post('/posts', json.dumps(post), content_type = 'application/json', **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
            {
                'message' : 'SUCCESS'
            }
        )
    
    def test_postview_post_key_error_title(self):
        client = Client()

        post = {
            'content' : '내용' 
        }

        response = client.post('/posts', json.dumps(post), content_type = 'application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR'
            }
        )

    def test_postview_post_key_error_content(self):
        client = Client()

        post = {
            'title' : '제목' 
        }

        response = client.post('/posts', json.dumps(post), content_type = 'application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR'
            }
        )

    def test_postview_post_unauthorized(self):
        client = Client()

        post = {
            'title'   : '제목',
            'content' : '내용' 
        }

        response = client.post('/posts', json.dumps(post), content_type = 'application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
            {
                'message' : 'UNAUTHORIZED'
            }
        )
    
    def test_postview_post_jsondecode_error(self):
        client = Client()

        response = client.post('/posts', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'JSON_DECODE_ERROR'
            }
        )
    
    def test_postview_get_success(self):
        client = Client()

        post_list = [
            {
                'post_id' : 2,
                'author'  : '김유저',
                'title'   : '제목2',
                'content' : '내용2',
                'created_at' : post2.created_at.strftime("%Y/%m/%d %H:%M")
            },
            {
                'post_id' : 1,
                'author'  : '박유저',
                'title'   : '제목1',
                'content' : '내용1',
                'created_at' : post1.created_at.strftime("%Y/%m/%d %H:%M")
            },
        ]  

        response = client.get('/posts')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'post_list' : post_list})
    
    def test_postview_get_sort_old(self):
        client = Client()

        post_list = [
            {
                'post_id' : 1,
                'author'  : '박유저',
                'title'   : '제목1',
                'content' : '내용1',
                'created_at' : post1.created_at.strftime("%Y/%m/%d %H:%M")
            },
            {
                'post_id' : 2,
                'author'  : '김유저',
                'title'   : '제목2',
                'content' : '내용2',
                'created_at' : post2.created_at.strftime("%Y/%m/%d %H:%M")
            },
        ]  

        response = client.get('/posts?sort=old')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'post_list' : post_list})
    
    def test_postdetailview_get_success(self):
        client = Client()

        post_info = {
            'post_id' : 1,
            'author'  : '박유저',
            'title'   : '제목1',
            'content' : '내용1',
            'created_at' : post1.created_at.strftime("%Y/%m/%d %H:%M")
            }
        
        response = client.get('/posts/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'post_info' : post_info})
    
    def test_postdetailview_get_post_does_not_exist(self):
        client = Client()

        response = client.get('/posts/3')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message' : 'POST_DOES_NOT_EXIST'})

    def test_postdetailview_delete_success(self):
        client = Client()

        response = client.delete('/posts/1', **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SUCCESS'})

    def test_postdetailview_delete_post_does_not_exist(self):
        client = Client()

        response = client.delete('/posts/3', **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message' : 'POST_DOES_NOT_EXIST'})
    
    def test_postdetailview_delete_invalid_user(self):
        client = Client()

        response = client.delete('/posts/2', **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message' : 'INVALID_USER'})
    
    def test_postdetailview_delete_unauthorized(self):
        client = Client()

        response = client.delete('/posts/1')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
            {
                'message' : 'UNAUTHORIZED'
            }
        )

    def test_postdetailview_patch_success(self):
        client = Client()

        post = {
            'title'   : '제목 수정',
            'content' : '내용 수정' 
        }

        response = client.patch('/posts/1', json.dumps(post), content_type = 'application/json', **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
            {
                'message' : 'SUCCESS'
            }
        )

    def test_postdetailview_patch_post_does_not_exist(self):
        client = Client()

        post = {
            'title'   : '제목 수정',
            'content' : '내용 수정' 
        }

        response = client.patch('/posts/3', json.dumps(post), content_type = 'application/json', **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
            {
                'message' : 'POST_DOES_NOT_EXIST'
            }
        )

    def test_postdetailview_patch_post_invalid_user(self):
        client = Client()

        post = {
            'title'   : '제목 수정',
            'content' : '내용 수정' 
        }

        response = client.patch('/posts/2', json.dumps(post), content_type = 'application/json', **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
            {
                'message' : 'INVALID_USER'
            }
        )

    def test_postdetailview_patch_post_jsondecode_error(self):
        client = Client()

        response = client.patch('/posts/1', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'JSON_DECODE_ERROR'
            }
        )

        
