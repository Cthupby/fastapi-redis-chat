# FastAPI Redis Chat  

## Технологии проекта:

1. Web-framework: [FastAPI](https://fastapi.tiangolo.com/);  
2. Database: [Redis](https://redis.io/);  
3. Database-client: [Redis-py](https://redis-py.readthedocs.io/en/stable/);  

## Установка и использование  

### При помощи [Docker](https://docs.docker.com/)
1. Необходимо скачать проект.  
   ```git clone https://github.com/Cthupby/fastapi-redis-chat.git```  
   ```cd fastapi-redis-chat```  
2. Создать образ.  
   ```docker build -t fastapi_redis_chat .```  
3. Создать и активировать контейнеры.  
   ```docker-compose up -d --build```  
4. Перейти на локальный адрес.   
   ```http://0.0.0.0:8000```
