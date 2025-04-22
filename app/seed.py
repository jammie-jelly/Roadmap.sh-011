from app.utils.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.utils.security import hash_password

def seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin:
            admin = User(
                email="admin@example.com",
                hashed_password=hash_password("adminpassword"),
                role=UserRole.admin,
            )
            db.add(admin)
        elif admin.role != UserRole.admin:
            admin.role = UserRole.admin
        db.flush()
        db.commit()
    finally:
        db.close()
if __name__ == "__main__":
    seed_db()
