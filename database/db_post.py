from routers.schemas import PostBase
from sqlalchemy.orm.session import Session
import datetime
from database.models import DbPost
from fastapi import HTTPException, status


def create(db: Session, request: PostBase):
    new_post = DbPost(
        image_url=request.image_url,
        title=request.title,
        content=request.content,
        creator=request.creator,
        timestamp=datetime.datetime.now()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_all(db: Session):
    return db.query(DbPost).all()


def delete_post(post_id: int, db: Session):
    post = db.query(DbPost).filter(DbPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with the given id: {post_id} is not '
                                                                          f'present')
    db.delete(post)
    db.commit()
    return f'Post with id: {post_id} is deleted'
