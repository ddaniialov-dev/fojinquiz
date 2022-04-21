from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime, Text, Table, String
from sqlalchemy.orm import relationship, backref
from quiz_project.behaviours.base_model import AbstractBaseModel

session_question = Table('session_question', AbstractBaseModel.metadata,
    Column('session_id', ForeignKey('sessions.id'), primary_key=True),
    Column('question_id', ForeignKey('questions.id'), primary_key=True)
)


class Test(AbstractBaseModel):
    __tablename__ = "tests"

    title = Column(String(256))
    holder_id = Column(Integer, ForeignKey("users.id"))
    published = Column(Boolean)
    questions = relationship("Question", backref=backref("test", lazy="joined"))
    sessions = relationship("Session", backref=backref("test", lazy="joined"))


class Question(AbstractBaseModel):
    __tablename__ = "questions"

    test_id = Column(Integer, ForeignKey("tests.id"))
    text = Column(Text)
    answers = relationship("Answer", backref=backref("question", lazy="joined"))
    images = relationship("Image")


class Answer(AbstractBaseModel):
    __tablename__ = "answers"

    question_id = Column(Integer, ForeignKey("questions.id"))
    text = Column(Text)
    is_true = Column(Boolean, default=True)
    user_answers = relationship("UserAnswer", backref=backref("answer", lazy="joined"))


class UserAnswer(AbstractBaseModel):
    __tablename__ = "user_answers"

    answer_id = Column(Integer, ForeignKey("answers.id"))
    session_id = Column(Integer, ForeignKey("sessions.id"))


class Session(AbstractBaseModel):
    __tablename__ = "sessions"

    finished_date = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    test_id = Column(Integer, ForeignKey("tests.id"))
    questions = relationship("Question", secondary=session_question, backref=backref("sessions", lazy="joined"))


class Image(AbstractBaseModel):
    __tablename__ = 'images'

    path = Column(Text)
    content_type = Column(Text)
    question = Column(Integer, ForeignKey("questions.id"))

