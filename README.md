# Book Microservice

Une simple architecture de microservice avec FastAPI


## Prérequis:

- Python 3.8+
- pipenv ou pip
- Docker && Docker Compose

##  Cloner le projet

```
git clone https://github.com/flavienn-hugs/fastapi-book-microservice.git
```

## Tester le projet en local

### Installer les dépendances

```Utilisateur de pipenv
pipenv install
```
ou
```Utilisateur de pip
pip install -r requirements.txt
```

### Construire le container avec docker

```
make docker-compose-up
```

## Documentation sur l'API

- Endpoint authors
``` 
http://localhost:8080/api/v1/authors/docs
```
- Endpoint books
```
http://localhost:8080/api/v1/books/docs
```


# if running in local without docker 


run commands in two terminal for book service and author service

book service -    1. set env variables in .env file
                  2. source .env
                  3. uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

open another terminal and run this commands

author service -  1. set env variable in .env file
                  2. source .env
                  3. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

                  