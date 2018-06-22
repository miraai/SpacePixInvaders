from spacepixinvaders.models import HighScore

from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError, OperationalError

class DatabaseGateway(object):
    def __init__(self, session):
        self.session = session

    def insert_player(self, username):
        try:
            # Try to find a player
            player = self.session.query(HighScore).filter_by(username=username).first()

            # If there is none, insert a new player into the database
            if not player:
                player = HighScore(username=username, score=0)
                self.session.add(player)
                self.session.commit()
        except (IntegrityError, OperationalError) as e:
            self.session.rollback()

    def update_score(self, username, score):
        try:
            player = self.session.query(HighScore).filter_by(username=username).first()

            player.score = score
            self.session.commit()
        except (IntegrityError, OperationalError) as e:
            self.session.rollback()
        
    def show_highscores(self):
        try:
            scores = self.session.query(HighScore).order_by(HighScore.score.desc()).all()
            result = []
            for score in scores:
                result.append(score.username)
        
            return result
            
        except (IntegrityError, OperationalError) as e:
            self.session.rollback()
