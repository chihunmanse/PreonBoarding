import json
import re
import bcrypt
import jwt

from django.http            import JsonResponse
from django.views           import View
from json.decoder           import JSONDecodeError
from django.conf            import settings

from users.models           import User

class SignUpView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data['email']
            password     = data['password']
            name         = data['name']
            phone_number = data.get('phone_number')

            REGEX_EMAIL    = "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            REGEX_PASSWORD = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"

            if not re.match(re.compile(REGEX_EMAIL), email):
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)

            if not re.match(re.compile(REGEX_PASSWORD), password):
                return JsonResponse({'message' : 'INVAILD_PASSWORD'}, status = 400)

            if User.objects.filter(email = email).exists():
                return JsonResponse({'message' : 'ALREADY_EXISTS_EMAIL'}, status = 409)

            hashed_password         = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_password = hashed_password.decode('utf-8')

            User.objects.create(
                email        = email,
                name         = name,
                password     = decoded_hashed_password,
                phone_number = phone_number,
            )

            return JsonResponse({'message' : 'SUCCESS'}, status = 201)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        except JSONDecodeError:
            return  JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)

class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if not User.objects.filter(email= email).exists():
                return JsonResponse({'message': 'INVALID_USER_EMAIL'}, status = 401)

            user = User.objects.get(email = email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_USER_PASSWORD'}, status = 401)
            
            access_token = jwt.encode({'user_id' : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

            return JsonResponse({'access_token': access_token}, status = 200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)
        
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status = 401)
        
        except User.MultipleObjectsReturned:
            return JsonResponse({'message' : 'USER_MULTIPLE_RETURN_ERROR'}, status = 400)