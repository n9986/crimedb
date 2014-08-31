from core.criminal import Criminal
from core.mafia.mafia import Mafia


class Wiseguy(Criminal):
    def __init__(self):
        super(Wiseguy, self).__init__()

        self.add_attribute('boss_path')
        self.add_attribute('boss_id')
        self.add_attribute('boss_history')

    @classmethod
    def find_all(cls, *args, **kwargs):
        """Find a wiseguy
        """
        # Since rows are dicts anyway, I will just use this shortcut
        return Mafia.find(Wiseguy.from_dict(kwargs), find_all=True)

    @classmethod
    def find_one(cls, *args, **kwargs):
        """Find a wiseguy
        """
        # Since rows are dicts anyway, I will just use this shortcut
        return Mafia.find(Wiseguy.from_dict(kwargs), find_all=False)


    @classmethod
    def from_dict(cls, data):
        """Create a wiseguy from a dictionary
        """
        wiseguy = cls()
        wiseguy.from_row(data)
        return wiseguy


    def reassign(self, boss):
        """Reassign this guy to a new boss. Will need to manipulate every child
        to have a new tree from this point on.
        """

    def followers(self):
        """Find all the followers of this guy
        """
        ww = Wiseguy()
        ww.set('bossPath', "%s%s/" % (self.get('bossPath'), '[0-9]+'))
        return Mafia.find(ww, find_all=True)

