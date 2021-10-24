import json

from django.views import View
from django.http  import JsonResponse
from json.decoder import JSONDecodeError

from posts.models import Post
from users.utils  import login_decorator

class PostView(View):
    @login_decorator
    def post(self, request):
        try :
            data    = json.loads(request.body)
            user    = request.user
            title   = data['title'] 
            content = data['content']
    
            Post.objects.create(
                user    = user,
                title   = title,
                content = content,         
            )
        
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError :
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except JSONDecodeError :
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
    
    def get(self, request):
        offset = int(request.GET.get("offset",0))
        limit  = int(request.GET.get("limit",100))
        sort   = request.GET.get('sort')   
        
        limit     = offset + limit
        sort_by   = {
            'recent' : '-created_at',
            'old'    : 'created_at'
        }
        
        posts  = Post.objects.select_related('user').all().order_by(sort_by.get(sort, '-created_at'))[offset : limit]

        post_list = [{
            'post_id'    : post.id,
            'author'     : post.user.name,
            'title'      : post.title,
            'content'    : post.content,
            'created_at' : post.created_at.strftime("%Y/%m/%d %H:%M")
        } for post in posts]

        return JsonResponse({'post_list' : post_list}, status=200)

class PostDetailView(View):
    def get(self, request, post_id):
        try:
            if not Post.objects.filter(id = post_id).exists():
                return JsonResponse({'message' : 'POST_DOES_NOT_EXIST'}, status=404)
        
            post = Post.objects.select_related('user').get(id = post_id)     

            post_info = {
                'post_id'    : post.id,
                'author'     : post.user.name,
                'title'      : post.title,
                'content'    : post.content,
                'created_at' : post.created_at.strftime("%Y/%m/%d %H:%M")
            }
        
            return JsonResponse({'post_info': post_info,} ,status=200)
        
        except Post.DoesNotExist:
            return JsonResponse({'message' : 'POST_DOES_NOT_EXIST'}, status=404)
        
        except Post.MultipleObjectsReturned:
            return JsonResponse({'message' : 'POST_MULTIPE_ERROR'}, status = 400)

    @login_decorator
    def delete(self, request, post_id):
        try:
            user = request.user
            if not Post.objects.filter(id = post_id).exists():
                return JsonResponse({'message' : 'POST_DOES_NOT_EXIST'}, status=404)
        
            post = Post.objects.get(id = post_id)
        
            if user != post.user:
                return JsonResponse({'message' : 'INVALID_USER'}, status=401)
        
            post.delete()
            
            return JsonResponse({'message' : 'SUCCESS'}, status=200)

        except Post.DoesNotExist:
            return JsonResponse({'message' : 'POST_DOES_NOT_EXIST'}, status=404)
        
        except Post.MultipleObjectsReturned:
            return JsonResponse({'message' : 'POST_MULTIPE_ERROR'}, status = 400)
        
    @login_decorator
    def patch(self, request, post_id) :
        try: 
            user = request.user
            data = json.loads(request.body)

            if not Post.objects.filter(id=post_id).exists():
                return JsonResponse({'message' : 'POST_DOES_NOT_EXIST'}, status=404)
            
            post = Post.objects.get(id=post_id)
            
            if user != post.user :
                return JsonResponse({'message' : 'INVALID_USER'}, status=401)
            
            post.title   = data.get('title', post.title)
            post.content = data.get('content', post.content)
            post.save()

            return JsonResponse({'message' : 'SUCCESS'}, status=201)

        except JSONDecodeError :
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except Post.DoesNotExist:
            return JsonResponse({'message' : 'POST_DOES_NOT_EXIST'}, status=404)
        
        except Post.MultipleObjectsReturned:
            return JsonResponse({'message' : 'POST_MULTIPE_ERROR'}, status = 400)


    