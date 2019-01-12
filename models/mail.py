from models import Model
from models.user import User


class Mail(Model):
    """
    Mail 保存私信、通知信息
    """

    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('title', str, ''),
            ('content', str, ''),
            ('sender_id', int, 0),
            ('receiver_id', int, 0),
            ('read', bool, False),
            ('url', bool, False),
        ]
        return names

    def mark_read(self):
        self.read = True
        self.save()

    @classmethod
    def send_mail(cls, form, **kwargs):
        username = form.get('username')
        receiver = User.find_by(username=username)
        if receiver is None or form.get('title') == '':
            return False
        else:
            cls.new(form, receiver_id=receiver.id, **kwargs)
            return True

    def sender(self):
        u = User.find_by(id=self.sender_id)
        return u

    def receiver(self):
        u = User.find_by(id=self.receiver_id)
        return u
