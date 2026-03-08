from fastapi import FastAPI, HTTPException

from app.schemas import PostCreate, PostResponse
app = FastAPI()

text_post = {
	1: {"title": "New Title", "content": "New Content"},
	2: {"title": "Morning Thoughts", "content": "Starting the day with fresh ideas and coffee."},
	3: {"title": "Learning FastAPI", "content": "Today I explored how to build APIs using FastAPI."},
	4: {"title": "Python Tips", "content": "Remember to keep your code clean and readable."},
	5: {"title": "Daily Journal", "content": "It was a productive day working on my project."},
	6: {"title": "Tech News", "content": "New frameworks are constantly improving developer productivity."},
	7: {"title": "Weekend Plans", "content": "Planning to relax and write some code experiments."},
	8: {"title": "Debugging Story", "content": "Spent two hours debugging a missing comma."},
	9: {"title": "Database Notes", "content": "Understanding how SQLAlchemy manages sessions."},
	10: {"title": "Project Update", "content": "Added authentication and improved API responses."}
}

@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_post.values())[:limit]
    return text_post


@app.get("/posts/{id}")
def get_post(id: int) -> PostResponse:
    if id not in text_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_post.get(id)

@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"title": post.title, "content": post.content}
    text_post[max(text_post.keys()) + 1] = new_post
    return new_post