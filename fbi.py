from asciitree import draw_tree
from cmd2 import Cmd, make_option, options, Cmd2TestCase
import unittest, optparse, sys
from core.mafia.mafia import Mafia
from core.mafia.wiseguy import Wiseguy


class FBIApp(Cmd):
    prompt = '$FBI> '
    colors = True
    
    def __init__(self, *args, **kwargs):
        Cmd.__init__(self, *args, **kwargs)
        # del self.do_load
        pass

    @options([])
    def do_create(self, arg, opts=None):
        """Create a mafia agent"""

    def print_wiseguy(self, wiseguy):
        for key in wiseguy.data:
            self.stdout.write(
                self.colorize('%s: %s\n' % (key, wiseguy.data[key]), 'green'))
        self.stdout.write('\n')

    @options([
        make_option('-f', '--first-name', type="string", help="Full name of agent.", dest="first_name", default=None),
        make_option('-i', '--id', action="store", type="string", help="ID of agent.", dest="id", default=None),
        make_option('-a', '--all', action="store_true", help="Find all matches.", dest="all", default=None),
        make_option('-d', '--detail', action="store_true", help="Show full detail.", dest="detail", default=False)
    ])
    def do_find(self, arg, opts=None):
        """Find wiseguy(s) matching query"""
        query = opts.__dict__
        wiseguy = Wiseguy.find_all(**query) if opts.all else Wiseguy.find_one(**query)

        if isinstance(wiseguy, Wiseguy):
            print "%s" % wiseguy
            if opts.detail:
                self.print_wiseguy(wiseguy)
        elif isinstance(wiseguy, list):
            for w in wiseguy:
                print "%s" % w
                if opts.detail:
                    self.print_wiseguy(w)
            print "Found %d wiseguys" % len(wiseguy)
        else:
            print "No Wiseguy found!"

    @options([
        make_option('-i', '--id', action="store", type="string", help="ID of agent.", dest="id", default=None),
        make_option('-l', '--level', action="store", type="string", help="Level up to which followers are needed.", dest="level", default=-1)
    ])
    def do_followers(self, arg, opts=None):
        """Find the number of followers of a wiseguy"""
        wiseguy = Wiseguy.find_one(id=opts.id)

        if not wiseguy:
            print "No Wiseguy found!"
            return

        followers = wiseguy.followers(level=opts.level)

        if isinstance(followers, list):
            print "Followers of %s:\n" % wiseguy
            for f in followers:
                print f
            print "\nFound %d wiseguy(s) who are followers of %s.\n" % (
                len(followers),
                wiseguy
            )
        else:
            print "No followers found!"


    def do_compare(self, arg, opts=None):
        """Compare N wiseguys in terms of followers. Accepts N arguments, ID of
        each mafia you want to compare.
        """
        wid_list = arg.split(" ")
        followers = {}
        invalid = []

        print "Follower counts: %s" % (",".join(invalid))

        for wid in wid_list:
            wiseguy = Wiseguy.find_one(id=wid)

            if wiseguy:
                followers[wiseguy] = len(wiseguy.followers())

                print "%s: %s" % (
                    wiseguy,
                    str(followers[wiseguy])
                )
            else:
                invalid.append(wid)

        if len(invalid):
            print "Invalid IDs: %s" % (",".join(invalid))


    @options([])
    def do_hotlist(self, arg, opts=None):
        """Find agents above the danger threshold"""

    @options([])
    def do_remove(self, arg, opts=None):
        """Remove a wiseguy"""

    @options([
        make_option('-i', '--id', action="store", type="string", help="ID of agent.", dest="id", default=None),
        make_option('-b', '--boss', action="store", type="string", help="New boss ID of agent.", dest="boss", default=None)
    ])
    def do_reassign(self, arg, opts=None):
        """Reassign a wiseguy to another boss"""
        if not opts.boss:
            print "Must provide a status!"
            return

        if not opts.id:
            print "Must provide an ID!"
            return

        # Locate the wiseguy
        wiseguy = Wiseguy.find_one(id=opts.id)

        if not wiseguy:
            print "No Wiseguy found!"
            return

        # Locate the boss
        boss = Wiseguy.find_one(id=opts.boss)

        if not boss:
            print "No Boss found!"
            return

        wiseguy.reassign_to(boss)

        print "Done. %s has been reassigned to %s" % (wiseguy, boss)


    @options([
        make_option('-i', '--id', action="store", type="string", help="ID of agent.", dest="id", default=None),
        make_option('-s', '--status', action="store", type="string", help="New status of agent.", dest="status", default=None)
    ])
    def do_decommission(self, arg, opts=None):
        """Remove a wiseguy from active duty and set a status
        """
        if not opts.status:
            print "Must provide a status!"
            return

        if not opts.id:
            print "Must provide an ID!"
            return

        # Locate the wiseguy
        wiseguy = Wiseguy.find_one(id=opts.id)

        if not wiseguy:
            print "No Wiseguy found!"
            return

        # Find the heir
        heir = wiseguy.heir()

        if not heir:
            print "No Heir found!"
            return

        # Reassign all the children to the heir
        # Set boss history for all the children
        followers = wiseguy.followers()

        for follower in followers:
            followers.reassign_to(heir)

        # Deactivate the wiseguy
        wiseguy.deactivate(status=opts.status)

        print "Done!"

    @options([
        make_option('-i', '--id', action="store", type="string", help="ID of agent.", dest="id", default=None),
        make_option('-s', '--status', action="store", type="string", help="New status of agent.", dest="status", default=None)
    ])
    def do_recommission(self, arg, opts=None):
        """Reinstate a wiseguy to active duty automatically setting status to
        active.
        """
        if not opts.status:
            print "Must provide a status!"
            return

        if not opts.id:
            print "Must provide an ID!"
            return

        # Locate the wiseguy
        wiseguy = Wiseguy.find_one(id=opts.id)

        if not wiseguy:
            print "No Wiseguy found!"
            return

        # Reactivate the wiseguy
        wiseguy.reactivate(status=opts.status)

        ex_followers = wiseguy.ex_followers()
        for follower in ex_followers:
            follower.reassign_to(wiseguy)

        print "Done!"

    @options([
        make_option('-i', '--id', action="store", type="string", help="ID of agent.", dest="id", default=None),
    ])
    def do_tree(self, arg, opts=None):
        """Draw an ASCII chart
        """
        wiseguy = Wiseguy.find_one(id=opts.id)

        if not wiseguy:
            print "No Wiseguy found!"
            return

        print draw_tree(wiseguy.tree())


    @options([
        make_option('-i', '--id', action="store", type="string", help="ID of agent.", dest="id", default=None),
    ])
    def do_heir(self, arg, opts=None):
        """Check who is next in line to a wiseguy to inherit followers
        """
        wiseguy = Wiseguy.find_one(id=opts.id)

        if not wiseguy:
            print "No Wiseguy found!"
            return

        heir = wiseguy.heir()

        if not heir:
            print "No heir found!"
            return

        print "Heir to %s is:\n\t %s" % (wiseguy, heir)


    @options([
        make_option('-i', '--id', action="store", type="string", help="ID of agent.", dest="id", default=None),
    ])
    def do_boss(self, arg, opts=None):
        """Check the boss of a given wiseguy
        """
        wiseguy = Wiseguy.find_one(id=opts.id)

        if not wiseguy:
            print "No Wiseguy found!"
            return

        print "Boss of ", wiseguy.to_string(), ":\n"

        boss = Wiseguy.find_one(id=wiseguy.get('boss_id'))

        if not boss:
            print "No boss found! Might be a godfather or decommissioned wiseguy. :)"
            return

        self.print_wiseguy(boss)



    # do__load = None
    # do_load = None
    # do__relative_load = None
    # do_cmdenvironment = None
    # do_ed = None
    # do_edit = None
    # do_l = None
    # do_li = None
    # do_list = None
    # do_set = None
    # do_show = None
    # do_shell = None
    # do_shortcuts = None

class TestMyAppCase(Cmd2TestCase):
    CmdApp = FBIApp
    transcriptFileName = 'testSession.txt'

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-t', '--test', dest='unittests', action='store_true', default=False, help='Run unit test suite')
    (callopts, callargs) = parser.parse_args()
    if callopts.unittests:
        sys.argv = [sys.argv[0]]  # the --test argument upsets unittest.main()
        unittest.main()
    else:
        app = FBIApp()
        app.cmdloop()
