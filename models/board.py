from models import Model


class Board(Model):
    """
    Board 保存论坛板块信息
    """

    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('title', str, ''),
        ]
        return names
