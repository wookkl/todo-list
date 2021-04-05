# todo-list

- 유데미에서 배운 것들을 토대로 제작한 API입니다.
- 장고 REST 프레임워크를 사용하면 제작한 투두 리스트 API입니다.
- JWT를 사용하여 사용자 인증을 했습니다.

## 사용한 기술

- DRF
- Travis CI
- Docker, docker-compose

## 엔드포인트

- 회원가입: /api/users/join/
- 내정보: /api/users/me/
- JWT
  - 토큰 생성: /api/token/
  - 토큰 재생성: /api/token/refresh/
  - 토큰 검증: /api/token/verify/
- 할일 CRUD: /api/works/

### 실행방법

- `docker-compose up`
- http://127.0.0.1:8000/api/users/join/
