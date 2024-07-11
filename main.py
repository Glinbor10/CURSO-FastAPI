from fastapi import FastAPI, Body, Path, Query 
#Boy: To use the body of request
#Path: to use validations of path parameters
#Query: to use validations of query parameters
from fastapi.responses import HTMLResponse, JSONResponse
#Para responder en ditintos formatos, json, html...
#Data scheme, Field for validation scheme
from pydantic import BaseModel, Field
from typing import Optional, List

#FastAPI instance
app = FastAPI()
app.title = 'Mi aplicación con FastApi'
app.version = '0.1.1'


#Data scheme(Like java, using classes of objects)
class Movie(BaseModel):
    id: Optional[int] = None
    #Validations using Field of the library pydantic used in Python usually when we use FastAPI
    '''title: str = Field(default= 'Mi película', min_length= 5, max_length= 15)'''
    title: str = Field(min_length= 5, max_length= 15)
    overview: str = Field(min_length= 15, max_length= 50)
    year: int = Field(le= 2022) #lower or equal
    rating: float = Field(ge= 1, le= 10)
    category: str = Field(min_length= 5, max_length= 15)

    #To use defaults values
    model_config = {
        "json_schema_extra": {
            "examples": [
               {
                'id': 1,
                'title' : 'Crepusculo',
                'overview' : 'The twilight is almost better than sunday',
                'year' : 2022,
                'rating' : 9.5,
                'category' : 'Phantasy'
            }
            ]
        }
    }

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

#To indicate what type of response is
@app.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies)
#http://"ip del PC":5000/movies

@app.get('/movies/{id}', tags=['movies'], response_model=Movie) #between keys the parameter
def get_movie(id: int = Path(ge= 1, le= 2000)) -> Movie:
    for item in movies:
            if item['id']==id:
                return JSONResponse(content=item)
    return JSONResponse(content=[])

#http://127.0.0.1:5000/movies/1

@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length= 5, max_length= 15)) -> List[Movie]: #Parameter query because I dont specify it in the route only the / to use query parameter
    data = [item for item in movies if item['category']== category]
    return JSONResponse(content=data)
    #list(filter(lambda movie: movie['category'] == category, movies))
    #[ item for item in movies if item['category']==category]
#http://127.0.0.1:5000/movies/?category=Acci%C3%B3n

#To use the body of request
@app.post('/movies', tags=['movies'], response_model=dict)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(content={"message": "Se ha registrado la película"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict)
def update_movie( id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(content={"message": "Se ha modificado la película"})
#http://127.0.1.0:8000/movies/2
    
@app.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(content={"message": "Se ha eliminado la película"})

