# preonboarding

**회원가입**

- 정규표현식을 통해 이메일, 비밀번호 유효성 검사를 하고 유효한 값일 때만 유저가 생성되게 했습니다.

  (비밀번호 조건 : 8자 이상, 최소 하나의 문자, 숫자, 특수 문자)

- bcrypt를 사용하여 비밀번호를 암호화하여 저장되게 했습니다.

- Unit Test

**로그인**

- 로그인시 jwt 토큰이 발행됩니다.
- Unit Test

**게시물 작성**

- 로그인 유저만 가능합니다.
- Unit Test

**게시물 조회**

- querystring 으로 limit, offset 값을 받아 pagination을 구현했습니다.
- querystring 으로 sort 값을 받아 오래된순, 최신순으로 sorting이 가능하게 했습니다.
- Unit Test

**특정 게시물 조회**

- Path Variable로 post_id 식별, 특정 게시물을 조회합니다.
- Unit Test

**게시물 삭제**

- Path Variable로 post_id 식별, 특정 게시물을 삭제합니다.

- 게시물을 작성한 유저만 가능합니다.
- Unit Test

**게시물 수정**

- Path Variable로 post_id 식별, 특정 게시물을 수정합니다.

- 게시물을 작성한 유저만 가능합니다.
- Unit Test



# EndPoint

### **회원가입**

### **POST /users/signup**

**body key list**

- email(필수 사항)

- password(필수 사항)

- name(필수 사항)

- phone_number

email과 password, name은 필수 입력 사항이기 때문에 요청의 body에 해당 key가 없을 때 KeyError를 반환합니다.

email과 password 값이 유효한 형식이 아닐 때 status 400 코드를 반환합니다.

email이 기존 유저의 email과 중복될 때 status 409 코드를 반환합니다. 이 경우 400, 403, 409 코드 중에 어떤 코드를 반환하는게 맞는지 고민하였는데, 400 코드는 일반적으로 요청의 문법이 틀려서 서버가 요청을 제대로 수행하지 못 하는 경우에 사용하는데 이 경우 요청은 정상적이고, 클라이언트 입장에서 이메일이 중복될지 안 될지 요청을 보내기 전에 알 수 있는 상황도 아니기 때문에 완전히 적합한 코드 아니라고 생각했습니다. 403 코드는 인가(Authorization) 실패 상태 코드로 유효성 검사와 관련된 경우에 많이 사용되는데 이메일 중복은 데이터의 유효성이나 인가와는 다른 맥락이기 때문에 사용하지 않았습니다. 409 코드는 리소스가 충돌하여 요청을 처리할 수 없을 때 사용되는 코드인데 기존의 이메일 리소스와 요청에서의 이메일 리소스가 충돌하여 요청을 처리할 수 없는 상황이기 때문에 가장 적합한 코드라고 생각했습니다.

요청에 body가 없다면 json 데이터를 python으로 읽어오는 과정에서 에러가 발생되기 때문에 JSONDecodeError를 except로 처리해주었습니다.

### **로그인**

### **POST /users/signin**

**body key list**

- email(필수 사항)

- password(필수 사항)

email과 password는 필수 입력 사항이기 때문에 요청의 body에 해당 key가 없을 때 KeyError를 반환합니다.

요청의 email과 동일한 email을 가진 유저가 존재하지 않는다면 401 코드를 반환합니다.

bcrypt를 통해 db에 저장돼있는 해당 유저의 비밀번호와 요청에서 입력된 비밀번호를 비교해주고 맞지 않을시 401 코드를 반환합니다.

앞의 과정들을 전부 거쳤다면 이메일과 비밀번호 모두 맞기 때문에 payload에 로그인 유저의 id를 넣어 jwt 토큰을 발행합니다.

SECRET_KEY와 ALGORITHM 값은 gitignore 파일로 지정된 파일에 따로 선언하여 관리했습니다. 

요청에 body가 없다면 json 데이터를 python으로 읽어오는 과정에서 에러가 발생되기 때문에 JSONDecodeError를 except로 처리해주었습니다.

### **게시물 생성**

### **POST /posts**

로그인 유저만 가능

**headers / Authorization : token (필수사항)**

**body key list**

- title (필수 사항)

- content (필수 사항)

게시물 생성은 로그인 유저만 가능하기 때문에 post 함수가 실행되기 전에 로그인 데코레이터를 거쳐 인가 작업이 진행됩니다.

요청의 headers에 Authorization 키가 존재하지 않는다면 401 코드가 반환됩니다.

jwt로 토큰을 decode 해주는 과정에서 DecodeError가 발생한다면 적절한 토큰값이 아닌 것이기 때문에 401 코드가 반환됩니다.

payload에 저장돼있는 user_id를 통해 유저 정보를 얻은 다음, 데코레이터 다음에 실행되는 함수들에서 유저 정보에 바로 접근할 수 있도록 request.user에 담아줍니다.

title과 content key가 존재하지 않으면 keyError를 반환합니다.

로그인 인가 과정을 거치고 body에 적절한 데이터가 들어왔다면 토큰에서 얻은 유저 정보를 통해 해당 유저의 게시물을 생성합니다.

요청에 body가 없다면 json 데이터를 python으로 읽어오는 과정에서 에러가 발생되기 때문에 JSONDecodeError를 except로 처리해주었습니다.

### **게시물 조회**

### **GET /posts**

**query parameter list**

- limit (요청에 없을 때 기본 100으로 지정)

- offset (요청에 없을 때 기본 0으로 지정)

- sort = recent(최신순 정렬), old(오래된순 정렬), 요청에 없을 때 기본 정렬은 최신순 

limit과 offset을 query string으로 받아 pagination이 가능하도록 했습니다. limit key값이 들어오지 않았을 때 모든 게시물의 데이터가 가는 것을 방지하기 위해 get 메서드를 통해 limit key가 존재하지 않으면 100이 되도록 했습니다.

limit 변수에 요청에서 얻은 limit과 offset을 더해주고 모든 게시물의 쿼리셋을 offset과 limit으로 슬라이싱합니다. 이때 ORM의 lazy loading 특성으로 인해 모든 게시물을 가져오는 쿼리를 날린 후에 다시 슬라이싱 되는게 아니라 슬라이싱 되는 시점 (쿼리셋이 평가되는 시점)에 쿼리를 날리기 때문에 limit 값만큼만 게시물을 가져오는 쿼리가 한 번 날라가게 됩니다.

/posts?limit=4 요청시

```sql
DEBUG (0.001) SELECT "posts"."id", "posts"."created_at", "posts"."updated_at", "posts"."user_id", "posts"."title", "posts"."content", "users"."id", "users"."created_at", "users"."updated_at", "users"."email", "users"."password", "users"."name", "users"."phone_number" FROM "posts" INNER JOIN "users" ON ("posts"."user_id" = "users"."id") ORDER BY "posts"."created_at" DESC LIMIT 4; args=()
```

sorting은 sort_by 딕셔너리를 만들어서 sort parameter에 딕셔너리에 지정된 key가 들어왔을 때 order_by()에서 해당 key의 값으로 정렬되도록 했습니다. 만약 요청에 sort parameter가 없거나 잘못된 key로 들어왔을 때는 최신순으로 정렬되도록 했습니다. 

### **특정 게시물 조회**

### **GET /posts/{int:post_id}**

Path Variable로 post_id 식별, 특정 게시물을 조회합니다. 해당 post_id의 게시물이 없을 때 404 코드를 반환합니다.

### 특정 게시물 삭제

### DELETE /posts/{int:post_id}

로그인 유저만 가능

**headers / Authorization : token (필수사항)**

게시물 삭제는 로그인 유저만 가능하기 때문에 delete 함수가 실행되기 전에 로그인 데코레이터를 거쳐 인가 작업이 진행됩니다.

해당 post_id의 게시물이 없을 때 404 코드를 반환합니다.

로그인 후 요청을 보낸 유저가 삭제하려는 게시물의 작성 유저인지 확인하고 다르다면 401 코드를 반환합니다.

같은 유저가 맞다면 게시물을 삭제합니다.

### 특정 게시물 수정

### PATCH /posts/{int:post_id}

로그인 유저만 가능

**headers / Authorization : token (필수사항)**

**body key list**

- title

- content 

게시물 수정은 로그인 유저만 가능하기 때문에 patch 함수가 실행되기 전에 로그인 데코레이터를 거쳐 인가 작업이 진행됩니다.

해당 post_id의 게시물이 없을 때 404 코드를 반환합니다.

로그인 후 요청을 보낸 유저가 수정하려는 게시물의 작성 유저인지 확인하고 다르다면 401 코드를 반환합니다.

같은 유저가 맞다면 게시물을 수정합니다.

title이나 content key가 요청의 body에 존재하지 않으면 기존 게시물의 title과 content 값을 불러옵니다.

요청에 body가 없다면 json 데이터를 python으로 읽어오는 과정에서 에러가 발생되기 때문에 JSONDecodeError를 except로 처리해주었습니다.

## API 명세

**request :**

**POST /users/signup**

body :

```json
{

    "email" : "user3@gmail.com",

    "password" : "abc1234!",

    "name"  : "박치훈"

}
```

response :

```json
{

    "message": "SUCCESS"

}
```

**request :**

**POST /users/signin**

body :

```json
{
    "email" : "user3@gmail.com",
    "password" : "abc1234!"
}
```

response :

```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyfQ.XrXZe_o5spy-4tZVPD_Dk8NPyJQyGRy7t01Kbik_DZg"
}
```

**request :**

**POST /posts**

headers : 'Authorization' :  'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyfQ.XrXZe_o5spy-4tZVPD_Dk8NPyJQyGRy7t01Kbik_DZg'

body :

```json
{
    "title" : "제목3",
    "content" : "내용3"
}
```

response :

```json
{
    "message": "SUCCESS"
}
```

**request :**

**GET /posts**

response:

```json
{
    "post_list": [
        {
            "post_id": 5,
            "author": "박치훈",
            "title": "제목4",
            "content": "내용4",
            "created_at": "2021/10/24 09:19"
        },
        {
            "post_id": 4,
            "author": "박치훈",
            "title": "제목3",
            "content": "내용3",
            "created_at": "2021/10/24 09:18"
        },
        {
            "post_id": 3,
            "author": "김유저",
            "title": "제목2",
            "content": "내용2",
            "created_at": "2021/10/23 13:45"
        },
        {
            "post_id": 2,
            "author": "김유저",
            "title": "제목입니다",
            "content": "내용입니다",
            "created_at": "2021/10/23 13:20"
        }
    ]
}
```

**GET /posts?limit=3**

response :

```json
{
    "post_list": [
        {
            "post_id": 5,
            "author": "박치훈",
            "title": "제목4",
            "content": "내용4",
            "created_at": "2021/10/24 09:19"
        },
        {
            "post_id": 4,
            "author": "박치훈",
            "title": "제목3",
            "content": "내용3",
            "created_at": "2021/10/24 09:18"
        },
        {
            "post_id": 3,
            "author": "김유저",
            "title": "제목2",
            "content": "내용2",
            "created_at": "2021/10/23 13:45"
        }
    ]
}
```

**GET /posts?limit=3&sort=old**

response :

```json
{
    "post_list": [
        {
            "post_id": 2,
            "author": "김유저",
            "title": "제목입니다",
            "content": "내용입니다",
            "created_at": "2021/10/23 13:20"
        },
        {
            "post_id": 3,
            "author": "김유저",
            "title": "제목2",
            "content": "내용2",
            "created_at": "2021/10/23 13:45"
        },
        {
            "post_id": 4,
            "author": "박치훈",
            "title": "제목3",
            "content": "내용3",
            "created_at": "2021/10/24 09:18"
        }
    ]
}
```

**request :**

**GET /posts/2**

response :

```json
{
    "post_info": {
        "post_id": 2,
        "author": "김유저",
        "title": "제목입니다",
        "content": "내용입니다",
        "created_at": "2021/10/23 13:20"
    }
}
```

**request :**

**DELETE /posts/5**

headers : 'Authorization' :  'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyfQ.XrXZe_o5spy-4tZVPD_Dk8NPyJQyGRy7t01Kbik_DZg'

response :

```json
{
    "message": "SUCCESS"
}
```

**request :**

**PATCH /posts/4**

headers : 'Authorization' :  'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyfQ.XrXZe_o5spy-4tZVPD_Dk8NPyJQyGRy7t01Kbik_DZg'

body :

```json
{
    "title" : "제목 수정",
    "content" : "내용 수정"
}
```

response :

```json
{
    "message": "SUCCESS"
}
```
