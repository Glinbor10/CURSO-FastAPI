from fastapi import FastAPI
from fastapi.responses import HTMLResponse

#FastAPI instance
app = FastAPI()
app.title = 'Mi aplicación con FastApi'
app.version = '0.1.1'

movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "Gru",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    }
]

#Endpoint
@app.get('/', tags=['home'])  #To organize the routes
def message():
    return HTMLResponse('<h1>Hello world</h1>')

@app.get('/movies', tags=['movies'])
def get_movies():
    return movies
#http://"ip del PC":5000/movies

@app.get('/movies/{id}', tags=['movies']) #between keys the parameter
def get_movie(id: int):
    return list(filter(lambda movie: movie['id'] == id, movies))
#http://127.0.0.1:5000/movies/1

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str): #Parameter query because I dont specify it in the route only the / to use query parameter
    list(filter(lambda movie: movie['category'] == category, movies))
#http://127.0.0.1:5000/movies/?category=Acci%C3%B3n