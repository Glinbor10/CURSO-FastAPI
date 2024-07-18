from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
#Boy: To use the body of request
#Path: to use validations of path parameters
#Query: to use validations of query parameters
from fastapi.responses import HTMLResponse, JSONResponse
#Para responder en ditintos formatos, json, html...
#Data scheme, Field for validation scheme
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Coroutine, Optional, List
#Token
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
#Database
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

#FastAPI instance
app = FastAPI()
app.title = 'FastApi'
app.version = '0.1.1'

#To create the database
Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(status_code=403, detail= 'Invalid credentials')
            #Lanzo excepción

class User(BaseModel):
    email: str
    password: str


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


# To Log In
@app.post('/login', tags=['auth']) #authorization
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump()) #instead of .dict()
        return JSONResponse(status_code= 200, content= token)
#http://127.0.0.1:5000/login

#Endpoint
@app.get('/', tags=['home'])  #To organize the routes
def message():
    return HTMLResponse('<h1>Hello world</h1>')

#To indicate what type of response is
@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)
#http://"ip del PC":5000/movies

@app.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200) #between keys the parameter
def get_movie(id: int = Path(ge= 1, le= 2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

#http://127.0.0.1:5000/movies/1

@app.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length= 5, max_length= 15)) -> List[Movie]: #Parameter query because I dont specify it in the route only the / to use query parameter
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
#http://127.0.0.1:5000/movies/?category=Acci%C3%B3n

#To use the body of request
@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    #Start database
    db = Session()
    new_movie = MovieModel(**movie.model_dump()) #**para que esté como parametro
    db.add(new_movie)
    db.commit()
    #movies.append(movie)
    return JSONResponse(content={"message": "Se ha registrado la película"}, status_code=201)

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie( id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(status_code=200, content={'message': 'Se ha modificado correctamente.'})
#http://127.0.1.0:8000/movies/2
    
@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={'message': 'Se ha eliminado correctamente.'})
        

