# blog

A few of the things you can do with *blog*:

* create, delete, update, bookmark/unbookmark, upvote/downvote posts
* make your profile private

## Built With

- Django REST framework
- Docker
- PostgreSQL
- Nginx
- Redis
- Celery
- Flower

## Installation

1. Clone the repo

```bash
  git clone https://github.com/uQwQu/blog.git
```

2. Create .env file based on .env.example

```bash
  cd blog
  cp .env.example .env
```

3. Run containers

```bash
  docker network create blog-nw
  make build
```

## Usage

Check endpoints with OpenAPI docs:

- http://localhost:8080/api/v1/schema/swagger-ui/
- http://localhost:8080/api/v1/schema/redoc/

