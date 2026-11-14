from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

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
    username = Column(String(30))
    email = Column(String())
    password = Column(String())
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    addresses = relationship("Address", backref="user")
    profile = relationship("Profile", backref="user",uselist=False)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    first_name = Column(String())
    last_name = Column(String())
    bio = Column(Text(), nullable=True)

    def __repr__(self):
        return f"Profiles(id={self.id},first_name={self.first_name},last_name={self.last_name})"


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    city = Column(String())
    state = Column(String())
    zip_code = Column(String())

    def __repr__(self):
        return f"Address(id={self.id}, user_id={self.user_id}, city={self.city})"


# to create tables and database
Base.metadata.create_all(engine)

session = SessionLocal()

# session.add(User(username="mahtabbabaei",email="mahtab@babaei.com", password="123"))
user = session.query(User).filter_by(username="mahtabbabaei").one_or_none()
# session.add(Profile(user_id=user.id, first_name="Mahtab", last_name="Babaei"))
# session.commit()
print(user.profile.first_name)

# session.add(User(username="mahtabbabaei",email="mahtab@babaei.com", password="123"))
# session.commit()

# user = session.query(User).filter_by(username="mahtabbabaei").one_or_none()
# print(user.addresses)

# addresses = [
#     Address(user_id=user.id, city="abarkouh", state="yazd", zip_code="123"),
#     Address(user_id=user.id, city="torbate heydariyeh",
#             state="khorasan razavi", zip_code="123")
# ]

# session.add_all(addresses)
# session.commit()

# address = session.query(Address).filter_by(
#     user_id=user.id, city="abarkouh").one_or_none()

# print(address.user.username)
