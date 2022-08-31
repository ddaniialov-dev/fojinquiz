from sqlalchemy import (Boolean, CheckConstraint, Column, DateTime, ForeignKey,
                        Integer, String, Table, Text)
from sqlalchemy.orm import backref, relationship

from quiz_project.behaviours.base_model import AbstractBaseModel

session_question = Table(
    "session_question",
    AbstractBaseModel.metadata,
    Column(
        "session_id", ForeignKey("sessions.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "question_id", ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True
    ),
)


class Test(AbstractBaseModel):
    __tablename__ = "tests"

    title = Column(String(256))
    holder_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    published = Column(Boolean)
    duration = Column(Integer)
    questions = relationship(
        "Question",
        backref=backref("test", lazy="selectin"),
        lazy="selectin",
        cascade="all, delete",
    )
    sessions = relationship(
        "Session",
        backref=backref("test", lazy="selectin"),
        lazy="selectin",
        cascade="all, delete",
    )


class Question(AbstractBaseModel):
    __tablename__ = "questions"

    test_id = Column(Integer, ForeignKey("tests.id", ondelete="CASCADE"))
    text = Column(Text)
    answers = relationship(
        "Answer",
        backref=backref("question", lazy="selectin"),
        lazy="selectin",
    )
    user_answers = relationship(
        "UserAnswer",
        backref=backref("question", lazy="selectin"),
        lazy="selectin",)
    images = relationship(
        "Image",
        lazy="selectin",
    )
    ordering = Column(Integer, CheckConstraint("ordering>0"))


class Answer(AbstractBaseModel):
    __tablename__ = "answers"

    question_id = Column(Integer, ForeignKey(
        "questions.id", ondelete="CASCADE"))
    text = Column(Text)
    is_true = Column(Boolean, default=True)
    user_answers = relationship(
        "UserAnswer",
        backref=backref("answer", lazy="selectin"),
        lazy="selectin",
        cascade="all, delete",
    )


class UserAnswer(AbstractBaseModel):
    __tablename__ = "user_answers"

    answer_id = Column(Integer, ForeignKey("answers.id", ondelete="CASCADE"))
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))


class Session(AbstractBaseModel):
    __tablename__ = "sessions"

    finished_date = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    test_id = Column(Integer, ForeignKey("tests.id", ondelete="CASCADE"))
    questions = relationship(
        "Question", secondary=session_question, lazy="selectin", cascade="all, delete"
    )


class Image(AbstractBaseModel):
    __tablename__ = "images"

    path = Column(Text)
    content_type = Column(Text)
    question = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))
