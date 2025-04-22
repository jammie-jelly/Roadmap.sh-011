from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_admin_user
from app.schemas.user import UserUpdate, UserOut
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_update.role:
        db_user.role = user_update.role
    db.commit()
    db.refresh(db_user)
    return db_user
