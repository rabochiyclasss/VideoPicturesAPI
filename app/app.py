from fastapi import FastAPI, HTTPException

app = FastAPI()

text_post = {1: {"title": "New Title", "content": "New Content"}}

@app.get("/posts")
def get_all_posts():
    return text_post


@app.get("/posts/{id}")
def get_post(id: int):
    if id not in text_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_post.get(id)