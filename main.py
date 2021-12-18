from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.params import Body

from databaseConnector import *

app = FastAPI()

posts = [{'user': '1', 'day': 'Today', 'content': 'I did a thing'}]

class Post(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    date_published: str
    votes: Optional[int] = None

class UpdatePost(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    date_published: Optional[str] = None
    votes: Optional[int] = None

class idClass(BaseModel):
    idOfPost: str


@app.get("/")
def root():
    return {"Message": "Welcome to the Jitter API - Hope you enjoy!"}


@app.get("/posts")
def get_posts():
    return getValues()


@app.get("/postbyid")
def get_post_by_id(id: idClass):
    returner = find_post_by_id(int(id.idOfPost))

    if returner == '404':
        raise HTTPException(status_code=404, detail="Item not found")

    else:
        return {'message': returner}


@app.post("/createpost")
def create_post(post: Post):

    add_post(post)
    return ({'message': post})


@app.delete("/deletepost")
def delete_post(id: idClass):


    returner = delete_post_by_id(id.idOfPost)

    if returner == 0:
        return HTTPException(status_code=201, detail="Deleted successfully")

    else:
        raise HTTPException(status_code=404, detail="Item not found")
        


@app.patch("/updatepost")
def update_post_by_id(newmessage: UpdatePost):

    returner = update(int(newmessage.id), newmessage)

    if returner == '404':
        raise HTTPException(status_code=404, detail="Item not found")

    else:
        return {'message': f'successfully update to {newmessage}'}
