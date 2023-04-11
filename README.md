# FastAPI Redis Chat  

## Технологии проекта:

1. Web-framework: [FastAPI](https://fastapi.tiangolo.com/)
2. Database: [Redis](https://redis.io/)

## Установка и использование  

### При помощи [Docker](https://docs.docker.com/)
1. Необходимо скачать проект  
   ```git clone https://github.com/Cthupby/fastapi-redis-chat.git```  
   ```cd fastapi-redis-chat```  
2. Создать образ проекта  
   ```docker build -t fastapi_redis_chat .```  
3. Создать и активировать контейнер проекта  
   ```docker-compose up -d --build```
