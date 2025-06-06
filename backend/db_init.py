from database import Base, engine, SessionLocal
from models import User
from auth import get_password_hash, ROLES


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if not db.query(User).first():
        admin = User(username='admin', password_hash=get_password_hash('admin'), role='NOC')
        db.add(admin)
        db.commit()
    db.close()

if __name__ == '__main__':
    init_db()
