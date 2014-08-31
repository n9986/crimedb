import operator
from core.criminal import Criminal
from core.mafia.mafia import Mafia


class TreeNode():
    def __init__(self, name, followers):
        self.name = str(name)

        self.children = []
        for follower in followers:
            self.children.append(TreeNode(follower, follower.followers(level=1)))

    def __str__(self):
        return self.name


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

    def reassign_to(self, boss):
        """Reassign this guy to a new boss. Will need to manipulate every child
        to have a new tree from this point on.
        """

    def heir(self):
        """Find the heir of this guy. Calculate according to this formula:

        - Firstly, oldest wiseguy at the same level.
        - Second candidate is immediate and oldest subordinate.
        - Finally, return None if none match (only if no subordinates or if just
        one).
        """
        path = self.get('boss_path')
        depth = path.count('/') - 1

        ww = Wiseguy()

        # Simple regex to find the boss paths of same size. Which also implies
        # they are all at the same level in the tree.
        ww.set('boss_path', "^\/([0-9]+\/){%d}$" % depth)

        # Run the search and viola
        heir_candidates = Mafia.find(ww, find_all=True)

        if len(heir_candidates) == 0:
            heir_candidates = self.followers()

            if len(heir_candidates) == 0:
                return None

        date_sorted_wiseguys = []
        for wiseguy in heir_candidates:
            if wiseguy.get('id') != self.get('id'):
                date_sorted_wiseguys.append((wiseguy, wiseguy.get('date_of_initiation')))

        date_sorted_wiseguys = sorted(
            date_sorted_wiseguys,
            key=operator.itemgetter(1)
        )

        return date_sorted_wiseguys[0][0]


    def followers(self, level=-1):
        """Find all the followers of this guy
        """
        self_depth = self.get('boss_path').count('/') - 1

        ww = Wiseguy()
        ww.set('boss_path', "%s%s/" % (self.get('boss_path'), '[0-9]+'))
        followers = Mafia.find(ww, find_all=True)

        if level > 0:
            followers = filter(
                lambda item: (item.get('boss_path').count('/') - 1) - self_depth <= level,
                followers
            )

        return followers


    def ex_followers(self):
        """Find all ex followers of this guy
        """
        ww = Wiseguy()
        ww.set('boss_history', "/%s/" % (self.get('id')))


    def tree(self):
        root = TreeNode(self, self.followers(level=1))
        return root

    def __str__(self):
        return self.to_string()

    def to_string(self):
        return "%s %s [%s]"% (
            self.get('first_name'),
            self.get('last_name'),
            self.get('id')
        )
