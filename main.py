from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.params import Body

app = FastAPI()

posts = [{'user': '1', 'day': 'Today', 'content': 'I did a thing'}]


class Post(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    date_published: str
    votes: Optional[int] = None


class idClass(BaseModel):
    id: str


def find_post_by_id(id):
    try:
        return posts[id]

    except IndexError:
        return '404'


def add_post(post):
    posts.append(post)
    print(posts)


def delete_jeet(id):
    try:
        posts[id].pop()

    except IndexError:
        return '404'


def update(id, newmessage):
    try:
        print(posts)
        posts[id] = newmessage
        print(posts)

    except IndexError:
        return '404'


@app.get("/")
def root():
    return {"hello": "test"}


@app.get("/jeet")
def get_posts():
    return posts


@app.get("/jeetbyid")
def get_post_by_id(id: idClass):
    returner = find_post_by_id(int(id.id))

    print(returner)

    if returner == '404':
        raise HTTPException(status_code=404, detail="Item not found")

    else:
        return {'message': returner}


@app.post("/createjeet")
def create_post(post: dict = Body(...)):
    add_post(post)
    return post


@app.delete("/deletejeet")
def delete_post(id: idClass):
    id = int(id.id)
    delete_jeet(id)
    return HTTPException(status_code=201, detail="Deleted successfully")


@app.patch("/updatejeetbyid")
def update_post_by_id(newmessage: Post):
    newmessage = dict(newmessage)
    returner = update(int(newmessage['id']), newmessage)

    if returner == '404':
        raise HTTPException(status_code=404, detail="Item not found")

    else:
        return {'message': f'successfully update to {newmessage}'}
