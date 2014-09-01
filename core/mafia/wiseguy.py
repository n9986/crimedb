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
        followers = self.followers(level=1)

        # This is a bit tricky. Tracking the last boss.
        # - If the new boss is the same as the old boss then no need to recompute
        # boss history.
        # - If the new boss exists in the boss history, then it is some old ex
        # boss. Move whole tree there and erase boss history to that point.
        # - If the new boss does not exist in the boss history, then add him to
        # it.
        boss_history = self.get('boss_history')
        if boss.get('id') != self.get('boss_id'):
            boss_history = self.get('boss_history')

            try:
                idx = boss_history.index(boss.get('id'))
                boss_history = boss_history.replace(boss_history[idx+2:], "")
            except:
                boss_history += boss.get('id') + "/"

        # Reset boss data.
        self.set('boss_path', "%s%s/" % (boss.get('boss_path'), self.get('id')))
        self.set('boss_history', boss_history)
        self.set('boss_id', boss.get('id'))

        # Save
        self.save()

        for follower in followers:
            follower.reassign_to(self)


    def deactivate(self, status):
        # Reassign all the children to the heir
        # Set boss history for all the children
        followers = self.followers(level=1)

        # Find the heir
        heir = self.heir()

        self.set('boss_path', '/%s/' % self.get('id'))
        self.set('boss_id', "-1")
        self.set('status', status)
        self.set('active', "0")

        self.save()

        # If no heir and no followers, then no need to assign
        if not heir or len(followers) == 0:
            return

        for follower in followers:
            follower.reassign_to(heir)


    def reactivate(self, status):
        ex_followers = Wiseguy.find_all(boss_history=self.get('id'))

        for ex_follower in ex_followers:
            ex_follower.reassign_to(self)


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
                if wiseguy.get('active') == "1":
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

    def save(self):
        Mafia.update(self)
