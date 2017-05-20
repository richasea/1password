"""
Author: Sean Richardson
Email: richasea<at>gmail.com
Description: Class to encapsulate the user interface.
"""

#pylint: disable=no-member

import curses

class Gui(object):
    """
    A class to encapsule the user interface using ncurses.
    """

    def __init__(self):
        """
        Intialise gui variables.
        """
        self._screen = None
        self._index = 0
        self._vault = None

    def setup(self, vault):
        """
        Setup ncurses and render to the screen.
        """
        self._screen = curses.initscr()
        curses.start_color()
        curses.noecho()
        self._screen.keypad(1)
        curses.curs_set(0)
        self._vault = vault

    def render_headers(self):
        """
        Renders the columns for the UI.
        """
        self._screen.addstr(0, 0, "Account")
        (_, width) = self._screen.getmaxyx()
        self._screen.hline(1, 0, curses.ACS_HLINE, width)

    def render_accounts(self):
        """
        Renders account information.
        """
        index = 2
        #self._screen.bkgd(' ', curses.color_pair(1))
        accounts = list(self._vault.accounts)
        accounts.sort()
        (height, _) = self._screen.getmaxyx()
        for account in accounts:
            if index - 2 == self._index:
                self._screen.addstr(index, 0, account, curses.A_BOLD)
            else:
                self._screen.addstr(index, 0, account)
            index = index + 1
            if index == height:
                break
        self._screen.refresh()

    def main_loop(self):
        """
        Main processing loop for the program.
        """
        while True:
            key = self._screen.getch()
            if key == ord('q') or key == ord('Q'):
                break
            elif key == curses.KEY_DOWN:
                self._index += 1
                self.render_accounts()
            elif key == curses.KEY_UP:
                if self._index == 0:
                    continue
                else:
                    self._index -= 1
                    self.render_accounts()

    @staticmethod
    def teardown():
        """
        Cleanup ncurses
        """
        curses.endwin()

# vim: et ai ts=4
