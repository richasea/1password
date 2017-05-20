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
        self._tab = 0

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
        pos = 0
        index = 0
        for header in self._vault.headers:
            if index == self._tab:
                attribute = curses.A_BOLD
            else:
                attribute = curses.A_NORMAL

            self._screen.addstr(0, pos, header, attribute)
            index += 1
            pos += len(header) + 1

        (_, width) = self._screen.getmaxyx()
        self._screen.hline(1, 0, curses.ACS_HLINE, width)

    def render_items(self):
        """
        Renders account information.
        """
        index = 2
        headers = self._vault.headers
        curtab = headers[self._tab]
        items = self._vault[curtab]
        (height, _) = self._screen.getmaxyx()
        for (name, _) in items:
            self._screen.addstr(index, 0, name)
            index += 1
            if index == height:
                break
        self._screen.refresh()

    def _on_tab_changed(self):
        self._screen.erase()
        self.render_headers()
        self._index = 0
        self.render_items()
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
                self.render_items()
            elif key == curses.KEY_UP:
                if self._index == 0:
                    continue
                else:
                    self._index -= 1
                    self.render_items()
            elif key == curses.KEY_LEFT:
                if self._tab > 0:
                    self._tab -= 1
                    self._on_tab_changed()
            elif key == curses.KEY_RIGHT:
                if self._tab < len(self._vault.headers) - 1:
                    self._tab += 1
                    self._on_tab_changed()

    @staticmethod
    def teardown():
        """
        Cleanup ncurses
        """
        curses.endwin()

# vim: et ai ts=4
