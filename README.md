# Scopic
Scopic test task

### Run task
```shell
~$ docker-compose build
~$ docker-compose up -d
~$ docker-compose logs -f
```

### Users:
```
logins: user1; user2
pass: scopic_user
```

Hello!
Since I used Django, I used its built-in templating language as the basis for the fronted. It's easy and convenient.
Also, I have implemented several Api using DRF and output information via Ajax requests in a static file.
To help user see current products bid - there is autoupdate function.
I used Celery + Redis for task queues. Celery Flower was used to keep track of the Celery states.
I found Sqlite3 as a lightweight database to be a good option for this test task. But it will be better to use PostgreSQL.
Wrapped everything in Docker for a convenient start

Once again I want to note that I will also be glad to consider the positions of Junior Web Developer in your company if i do not qualify for Midlee position. Since at the moment my knowledge in the front may not correspond to Midlle's position


Thank you!
