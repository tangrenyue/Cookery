import time
from models import Model
from models.board import Board
from models.user import User


class Topic(Model):
    """
    Topic 保存用户发的话题
    """

    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('title', str, ''),
            ('content', str, ''),
            ('user_id', int, 0),
            ('board_id', int, 0),
            ('views', int, 0),
            ('edited_time', int, 0),
        ]
        return names

    @classmethod
    def get(cls, t_id):
        """
        点击数+1
        """
        t = cls.find_by(id=t_id)
        if t is not None:
            t.views += 1
            t.save()
        return t

    def board(self):
        b = Board.find_by(id=self.board_id)
        return b

    def user(self):
        u = User.find_by(id=self.user_id)
        return u

    def replies(self):
        from models.reply import Reply
        rs = Reply.find_all(topic_id=self.id)
        return rs

    def num_of_replies(self):
        from models.reply import Reply
        num = Reply.count(topic_id=self.id)
        return num

    @classmethod
    def replied(cls, r):
        """
        回复时更新updated_time
        """
        t = cls.find_by(id=r.topic_id)
        t.update()

    def last_reply(self):
        from models.reply import Reply
        r = Reply.find_by(topic_id=self.id, __sort=('created_time', -1))
        return r

    def board_title(self):
        b = self.board()
        return b.title

    def update_topic(self, form):
        self.title = form.get('title')
        self.board_id = int(form.get('board_id'))
        self.content = form.get('content')
        self.edited_time = int(time.time())
        self.update()
