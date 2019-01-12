from models import Model
from models.user import User
from models.topic import Topic


class Reply(Model):
    """
    Reply 保存对应话题和用户的回复
    """

    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('content', str, ''),
            ('topic_id', int, 0),
            ('user_id', int, 0),
        ]
        return names

    def user(self):
        u = User.find_by(id=self.user_id)
        return u

    def topic(self):
        t = Topic.find_by(id=self.topic_id)
        return t

    def update_reply(self, form):
        self.content = form.get('content')
        self.update()
