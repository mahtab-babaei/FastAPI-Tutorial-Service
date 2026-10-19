from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create base class for declaring tables
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(30))
    last_name = Column(String(30), nullable=True)
    age = Column(Integer)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    def __repr__(self):
        return f"User(id={self.id}, first_name={self.first_name}, last_name={self.last_name})"


# to create tables and database
Base.metadata.create_all(engine)

session = SessionLocal()

# insert data
# ali = User(first_name="Ali", age=25)
# session.add(ali)
# session.commit()

# bulk insert
# mia = User(first_name="Mia", age=31)
# maya = User(first_name="Maya", age=6)
# session.add_all([mia, maya])
# session.commit()

# retrieve all data
# users = session.query(User).all()
# print(users)

# retrieve filtered data
# user = session.query(User).filter_by(first_name="Ali").all()
# print(user)

# update data
# user = session.query(User).filter_by(first_name="Ali").first()
# user.last_name = "Modiri"
# session.commit()

# delete data
user = session.query(User).filter_by(first_name="Ali").first()
if user:
    session.delete(user)
    session.commit()
