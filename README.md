# Wanted

### 사용한 기술 스택
- python, django

### 구현 내용
- 사용자 인증, 인가(회원가입, 로그인 기능)
- 게시판 CRUD 기능 API

### 구현 방법

#### 회원가입
- 이름, 이메일, 패스워드, 전화번호를 입력 받아 이메일을 아이디로 사용합니다.
- 비밀번호는 bcrypt를 사용하여 hashing후 저장합니다.

#### 로그인
- 로그인 시 추후 인가를 위한 토큰을 jwt로 발행합니다.

#### 게시판
- 게시글 작성, 수정, 삭제는 jwt를 통해 확인 된 유저만 가능합니다.
- 게시판 글 읽기는 로그인 없이 누구나 가능합니다.

### END POINT
| **METHOD** | **ENDPOINT**                     | **body**                      | **수행 목적**   |
|:-----------|:---------------------------------|:------------------------------|:--------------|
| POST       | /user/signup                     | name, email, password, moible | 회원가입        |
| POST       | /users/signin                    | email, password               | 로그인          |
| POST       | /board/create                    | title, text                   | 게시글 작성      |
| GET        | /board/text?page=<int>           |                               | 게시글 전체목록   |
| GET        | /board/<text_id>                 |                               | 게시글 보기      |
| PATCH      | /board/<text_id>                 | title, text                   | 게시글 수정      |
| DELETE     | /board/<text_id>                 |                               | 게시글 삭제      |
| GET        | /board/user/<user_id>?page=<int> |                               | 유저별 게시글 목록|

### API 명세
#### 1. 회원가입

| Key      | data type | body input                    | request                                        |
|:---------|:----------|:------------------------------|:-----------------------------------------------|
| name     | string    | "name" : "peter"              | 영문/이름 128 글자 이내 값 입력                      |
| email    | string    | "email" : "dissgogo@gmail.com"| "@"와 "."을 기준으로 그 사이 2-3글자 포함             |
| password | string    | "password" : "dlangus123!"    | 영문/한글, 숫자, 특수문자를 각각 하나 이상 포함한 8-16글자 |
| mobile   | string    | "mobile" : "010-1234-5678"    |                                                |

**Success example**
```
  {"message" : "SUCCESS"}
```
**이미 등록된 유저의 경우**
```
  {"message" : "EXIST USER"}
```
**이메일 형태가 올바르지 않을 경우**
```
  {"message" : "INVALID_EMAIL"}
```
**패스워드 형태가 올바르지 않을 경우**
```
  {"message" : "INVALID_PASSWORD"}
```
**키 형태가 올바르지 않을 경우**
```
  {"message" : "KEY_ERROR"}
```

#### 2. 로그인
  
| Key      | data type | body input                    | request                                        |
|:---------|:----------|:------------------------------|:-----------------------------------------------|  
| email    | string    | "email" : "dissgogo@gmail.com"| "@"와 "."을 기준으로 그 사이 2-3글자 포함             |
| password | string    | "password" : "dlangus123!"    | 영문/한글, 숫자, 특수문자를 각각 하나 이상 포함한 8-16글자 |  
**Success example**
```
  {"message": "LOGIN_SUCCESS",
   "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.jyLCgMloNjfH2xze_VleQaqy-9VulZ3jOjc0wNiy9fQ"}
```
**없는 유저일 경우**
```
  {"message" : "INVALID_USER"}
```
**잘못된 비밀번호일 경우**
```
  {"message" : "INVALID_PASSWORD"}
```
**키 형태가 올바르지 않을 경우**
```
  {"message" : "KEY_ERROR"}
```

#### 3. 게시글 작성
| Key      | data type | body input                    | request  |
|:---------|:----------|:------------------------------|:---------|  
| title    | string    | "title" : "처음 뵙겠습니다."      | 공백 불가, 128글자 이내  |
| text     | string    | "text" : "잘 부탁 드립니다."      |          | 
**Success example**
```
  {"message" : "SUCCESS"}
```
**제목이 비어있을 경우**
```
  {"message" : "TITLE EMPTY"}
```
**제목이 너무 길 경우**
```
  {"message" : "TITLE TOO LONG"}
```
**키 형태가 올바르지 않을 경우**
```
  {"message" : "KEY_ERROR"}
```

#### 4. 게시만 전체 목록 조회
- 제목과 작성자만 노출되며, 페이지네이션 기능을 통해 15개씩 페이지에 나타납니다.<br>
**Success example**
```
  {"title_lists": [
        {
            "title": "3",
            "user": "김정수"
        },
        {
            "title": "2",
            "user": "김정수"
        },
        {
            "title": "1",
            "user": "김정수"
        },
        {
            "title": "수원에 사는 공대생입니다.",
            "user": "김정수"
        }
  ]}
```
**텍스트가 하나도 없을 경우**
```
  {'message' : 'TEXT DOES NOT EXISTS'}
```
**쿼리파라미터 페이지 값이 잘못 입력된 경우**
```
  {"message" : "WRONG REQUEST"}
```

#### 5. 게시글 읽기

**Success example**
```
   {"title": "수원에 사는 공대생입니다.",
    "text": "잘 부탁 드립니다.",
    "created_at": "2021-10-24T11:29:21.918Z",
    "updated_at": "2021-10-24T11:29:21.918Z",
    "user": "김정수"}
```
**패스 파라미터 값이 잘못 입력된 경우**
```
  {'MESSAGE' : 'NOT FOUND'}
```

#### 6. 게시글 수정
| Key      | data type | body input                    | request  |
|:---------|:----------|:------------------------------|:---------|  
| title    | string    | "title" : "수정 시도"           | 공백 불가, 128글자 이내  |
| text     | string    | "text" : "수정 성공하였습니다."    |          |

**Success example**
```
  "message": "UPDATE SUCCESS"
```
**키 형태가 올바르지 않을 경우**
```
  {"message" : "KEY_ERROR"}
```

#### 7. 게시글 삭제

**Success example**
```
  {"message" : "DELETE COMPLETE"}
```

#### 8. 유저별 게시글 리스트 조회
- 제목과 작성자만 노출되며, 페이지네이션 기능을 통해 15개씩 페이지에 나타납니다.<br>
**Success example**
```
  {"title_lists" : [
  
      {"title": "수원에 사는 공대생입니다.",
      "user": "김정수"
            },
      {"title": "하위.",
      "user": "김정수"
            },
      {"title": "또 뵙네요",
      "user": "김정수"
           }]
  }
```
**패스 파라미터 값이 잘못 입력된 경우**
```
  {'MESSAGE' : 'NOT FOUND'}
```
**쿼리파라미터 페이지 값이 잘못 입력된 경우**
```
  {"message" : "WRONG REQUEST"}
```
