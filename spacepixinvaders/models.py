from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String

Base = declarative_base()

class HighScore(Base):
    __tablename__ = 'highscore'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    score = Column(Integer, default=0, nullable=True)

    def __init__(self, username, score):
        self.username = username
        self.score = score

    def __str__(self):
        return 'id: %s | username: %s | score: %s' %(self.id, self.username, self.score)

    def as_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'score': self.score
        }

def create_database(session, engine):
    session.configure(bind=engine)
    Base.metadata.create_all(engine)