from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime, Text, Table, String
from sqlalchemy.orm import relationship

from quiz_project.behaviours.base_model import AbstractBaseModel

session_question = Table('session_question', AbstractBaseModel.metadata,
    Column('session_id', ForeignKey('sessions.id'), primary_key=True),
    Column('question_id', ForeignKey('questions.id'), primary_key=True)
)

class Test(AbstractBaseModel):
    __tablename__ = "tests"

    title = Column(String(256))
    holder = Column(Integer, ForeignKey("users.id"))
    published = Column(Boolean)
    questions = relationship("Question")
    sessions = relationship("Session")


class Question(AbstractBaseModel):
    __tablename__ = "questions"

    test = Column(Integer, ForeignKey("tests.id"))
    text = Column(Text)
    answers = relationship("Answer")
    images = relationship("Image")
    sessions = relationship("Session", secondary=session_question, back_populates='questions')


class Answer(AbstractBaseModel):
    __tablename__ = "answers"

    question = Column(Integer, ForeignKey("questions.id"))
    text = Column(Text)
    is_true = Column(Boolean, default=True)
    user_answers = relationship("UserAnswer")


class UserAnswer(AbstractBaseModel):
    __tablename__ = "user_answers"

    answer = Column(Integer, ForeignKey("answers.id"))
    session = Column(Integer, ForeignKey("sessions.id"))


class Session(AbstractBaseModel):
    __tablename__ = "sessions"

    finished_date = Column(DateTime(timezone=True), nullable=True)
    user = Column(Integer, ForeignKey("users.id"))
    test = Column(Integer, ForeignKey("tests.id"))
    questions = relationship("Question", secondary=session_question, back_populates='sessions')


class Image(AbstractBaseModel):
    __tablename__ = 'images'

    path = Column(Text)
    content_type = Column(Text)
    question = Column(Integer, ForeignKey("questions.id"))

