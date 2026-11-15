from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, DateTime, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, backref
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create base class for declaring tables
Base = declarative_base()

enrollments = Table("enrollments", Base.metadata,
                    Column("id", Integer, primary_key=True, autoincrement=True),
                    Column("user_id", Integer, ForeignKey(
                        "users.id"), unique=True),
                    Column("course_id", Integer, ForeignKey(
                        "courses.id"), unique=True),
                    Column("enrolled_date", DateTime(), default=datetime.now),
                    UniqueConstraint("user_id", "course_id",
                                     name="unique_user_course_inrolled")
                    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30))
    email = Column(String())
    password = Column(String())
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    addresses = relationship("Address", backref="user")
    profile = relationship("Profile", backref="user", uselist=False)
    posts = relationship("Post", backref="user")
    comments = relationship("Comment", backref="user")
    courses = relationship("Course", secondary=enrollments,
                           back_populates="attendees")

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


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String())
    content = Column(Text())

    created_date = Column(DateTime(), default=datetime.now)
    updated_date = Column(
        DateTime(), default=datetime.now, onupdate=datetime.now)

    comments = relationship("Comment", backref="post")

    def __repr__(self):
        return f"post(id={self.id}, title={self.title})"


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)

    content = Column(Text())

    # parent = relationship(
    #     "Comment", back_populates="children", remote_side=[id])
    # children = relationship(
    #     "Comment", back_populates="parent", remote_side=[parent_id])

    # Or instead of two lines above we can use:
    children = relationship(
        "Comment", backref=backref("parent", remote_side=[id]))

    def __repr__(self):
        return f"comment(id={self.id}, user_id={self.user_id}, post_id={self.post_id}, parent_id={self.parent_id})"


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String())

    attendees = relationship(
        "User", secondary=enrollments, back_populates="courses")

    def __repr__(self):
        return f"course(id={self.id}, title={self.title})"


# to create tables and database
Base.metadata.create_all(engine)

session = SessionLocal()

user = session.query(User).filter_by(username="mahtabbabaei").one_or_none()

# session.add(Course(title="Python"))

# session.commit()

course = session.query(Course).filter_by(title="Python").one()

# course.attendees.append(user)

# session.commit()

print(course.attendees)
print(user.courses)