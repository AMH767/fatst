from typing import Dict
from fastapi import Depends, status, HTTPException, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session


router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, str])
def vote(user_vote: schemas.VoteCreate, db: Session = Depends(database.get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    # since we are expecting a post_id from the body, we must check if that post exists in the database
    # in order to associate a vote with it or dissassociate a vote from it [ either ways, the post must first exist in the db]
    post = db.query(models.Post).filter(models.Post.id == user_vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {user_vote.post_id} was not found.")
    vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == user_vote.post_id)
    found_vote = vote_query.first()
    if user_vote.vote_direction == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with id {current_user.id} has already voted for post with id {user_vote.post_id}")
        new_vote = models.Vote(user_id=current_user.id, post_id=user_vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist.")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}

