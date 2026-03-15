from contextlib import asynccontextmanager
from http.client import HTTPException

from fastapi import FastAPI, File, UploadFile, Form, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Post, create_db_and_tables, get_async_session

from app.images import imagekit
import shutil
import os
import uuid
import tempfile


@asynccontextmanager
async def lifespan(app: FastAPI):
	await create_db_and_tables()
	yield
app = FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_file(
		file: UploadFile = File(...),
		caption: str = Form(""),
		session: AsyncSession = Depends(get_async_session),#dependency injection
):
	temp_file_path = None

	try:
		with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
			temp_file_path = tmp_file.name
			shutil.copyfileobj(file.file, tmp_file)

		upload_result = imagekit.files.upload(
			file=open(temp_file_path, "rb"),
			file_name=file.filename,
			use_unique_file_name=True,
			tags=["backend-upload"]
		)

		if upload_result.response.http_sstatus == 200:
			post = Post(
				caption=caption,
				url="dummyurl",
				file_type="photo",
				file_name="dummyname"
			)
			session.add(post)
			await session.commit()
			await session.refresh(post)
			return post

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
	finally:
		if temp_file_path and os.path.exists(temp_file_path):
			os.unlink(temp_file_path)
			file.file.close()

@app.get("/feed")
async def get_feed(
		session: AsyncSession = Depends(get_async_session)
):
	result = await session.execute(select(Post).order_by(Post.created_at.desc()))
	posts = [row[0] for row in result.all()]
	posts_data = []
	for post in posts:
		posts_data.append({
			"id": str(post.id),
			"caption": post.caption,
			"url": post.url,
			"file_name": post.file_name,
			"file_type": post.file_type,
			"created_at": post.created_at.isoformat()
		})
		return {"posts": posts_data}
