from .. import models, schemas, oauth2
from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List

router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("/", response_model=List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0, search: str = ""):
    # posts = cur.execute("""SELECT * FROM posts""").fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # by default, sqlalchemy will use a 'left inner join'. We can use the isouter keyword argument to apply a 'left outer join' which is equivalent to a 'left join' in SQL
    # don't forget the field in your 'select clause' should appear in your 'group by clause'
    # note: for sqlalchemy joins, if you don't bring the 'label()' method, any aggregate functions you use in your select clause will not appear in the result
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get("/{id}", response_model=schemas.PostVote)
# Using the PostVote schema will not only validate the data coming from the db but will also
# prevent any lazy-loading by accessing all fields (e.g. pydantic will try to access the 'owner' field)
# which will cause sqlalchemy to return the data on the 'owner' field, otherwise sqlalchemy will not even return that field at all
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    # values for the query parameters in an SQL Query, are received into a tuple. Even if there is only one query paramater value, bring a trailing comma
    # post = cur.execute("""SELECT * FROM posts WHERE id = %s """, (id,)).fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist.")      
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error": f"Post with id: {id} does not exist."}
        # note: for sqlalchemy joins, if you don't bring the 'label()' method, any aggregate functions you use in your select clause will not appear in the result
    post_with_vote = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id).first()
    return post_with_vote


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post :schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    # don't forget to bring the 'RETURNING *' for queries that do not return a table record after the operation(delete, insert, update)
    # use query placeholders via '%s' in order to prevent SQL injection attacks, this allows psycopg to sanitize the input data coming from the user
    # cur.execute("""INSERT INTO posts (title, content, published)
    #             VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published,))
    # post = cur.fetchone()
    # conn.commit() will commit the staged changes to the database, call conn.commit() to persist newly created entity/resource to the db
    # conn.commit()
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    # db.refresh() will retrieve the newly created record from the database and store it in the variable new_post
    # this allows us to obtain any new fields added by the database
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    # deleted_post = cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (id,)).fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()      
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist.")
    if current_user.id != post.owner_id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You can only delete posts that belong to you.")
    # conn.commit()
    post_query.delete(synchronize_session=False)
    db.commit()
    # when you have no data to send to the user, you can just set the status code on the response object and send it
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    # cur.execute(""" UPDATE posts SET title = %s, content = %s, published = %s 
    #             WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id,))
    # updated_post = cur.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist.")
    # conn.commit()
    if current_user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You can only delete posts that belong to you.")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    # fetch the query again to return updated post from the db
    return post_query.first()