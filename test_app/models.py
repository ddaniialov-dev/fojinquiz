from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime, Text, Table, String
from sqlalchemy.orm import relationship


from quiz_project.behaviours import AbstractBaseModel
from quiz_project.utils import get_current_time

class Test(AbstractBaseModel):
    __tablename__ = "tests"
    
    title = Column(String(256))
    holder = Column(Integer, ForeignKey("users.id"))
    published = Column(Boolean)
    published_date = Column(DateTime, default=get_current_time)
    questions = relationship("Question")


class Question(AbstractBaseModel):
    __tablename__ = "questions"
    
    test = Column(Integer, ForeignKey("tests.id"))
    text = Column(Text)
    answers = relationship("Answer")


class Answer(AbstractBaseModel):
    __tablename__ = "answers"
    
    question = Column(Integer, ForeignKey("questions.id"))
    text = Column(Text)
    is_true = Column(Boolean, default=True)
    user_answers = relationship("user_answers.id")


class UserAnswer(AbstractBaseModel):
    __tablename__ = "user_answers"
    
    answer = Column(Integer, ForeignKey("answers.id"))
    session = Column(Integer, ForeignKey("sessions.id"))


class Session(AbstractBaseModel):
    __tablename__ = "sessions"
    
    finished_date = Column(DateTime, nullable=True)
    user = Column(Integer, ForeignKey("users.id"))
    test = Column(Integer, ForeignKey("tests.id"))


association_table = Table('association', AbstractBaseModel.metadata,
    Column('question_id', ForeignKey('questions.id')),
    Column('session_id', ForeignKey('sessions.id'))
)