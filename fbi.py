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
        make_option('-a', '--all', action="store_true", help="Find all matches.", dest="all", default=None)
    ])
    def do_find(self, arg, opts=None):
        """Find wiseguy(s) matching query"""
        query = opts.__dict__
        wiseguy = Wiseguy.find_all(**query) if opts.all else Wiseguy.find_one(**query)

        if isinstance(wiseguy, Wiseguy):
            self.print_wiseguy(wiseguy)
        elif isinstance(wiseguy, list):
            for w in wiseguy:
                self.print_wiseguy(w)
            print "Found %d wiseguys" % len(wiseguy)
        else:
            print "No Wiseguy found!"

    @options([
        make_option('-i', '--id', action="store", type="string", help="ID of agent.", dest="id", default=None)
    ])
    def do_followers(self, arg, opts=None):
        """Find the number of followers of a wiseguy"""
        wiseguy = Wiseguy.find_one(id=opts.id)

        if not wiseguy:
            print "No Wiseguy found!"
            return

        followers = wiseguy.followers()

        print followers

        if isinstance(followers, list):
            for f in followers:
                self.print_wiseguy(f)
            print "Found %d wiseguy(s) who are followers of %s %s." % (
                len(followers),
                wiseguy.get('first_name'),
                wiseguy.get('last_name')
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

                print "[%s] %s %s: %s" % (
                    wid,
                    wiseguy.get('first_name'),
                    wiseguy.get('last_name'),
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

    @options([])
    def do_reassign(self, arg, opts=None):
        """Reassign a wiseguy to another boss"""

    @options([])
    def do_decommission(self, arg, opts=None):
        """Remove a wiseguy from active duty and set a status"""

    @options([])
    def do_recommission(self, arg, opts=None):
        """Reinstate a wiseguy to active duty automatically setting status to
        active"""

    @options([])
    def do_heir(self, arg, opts=None):
        """Check who is next in line to a wiseguy to inherit followers"""

    @options([])
    def do_boss(self, arg, opts=None):
        """Check the boss of a given wiseguy"""
        self.stdout.write(self.colorize('booyeah', 'green'))

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
