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
        self._scroll_limit = 0
        self._header = None
        self._body = None

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
        self._header = self._screen.subwin(2, curses.COLS, 0, 0)
        self._body = self._screen.subwin(2, 0)

        self._body.refresh()

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

            self._header.addstr(0, pos, header, attribute)
            index += 1
            pos += len(header) + 1

        self._header.hline(1, 0, curses.ACS_HLINE, curses.COLS)
        self._header.refresh()

    def render_items(self):
        """
        Renders account information.
        """
        index = 0
        headers = self._vault.headers
        curtab = headers[self._tab]
        items = self._vault[curtab]
        self._scroll_limit = len(items)
        for (name, _) in items:
            if index == self._index:
                attributes = curses.A_BOLD
            else:
                attributes = curses.A_NORMAL
            self._body.addstr(index, 0, name, attributes)
            index += 1
        self._body.refresh()

    def _get_tab_height(self):
        tabheader = self._vault.headers[self._tab]
        tab_items = self._vault[tabheader]
        height =len(tab_items)
        if height < 1:
            return 1
        return height

    def _on_tab_changed(self):
        # self._screen.erase()
        self.render_headers()
        self._index = 0
        self._body.erase()
        self._body.refresh()
        self._body.resize(self._get_tab_height(), curses.COLS)
        self.render_items()
        # self._screen.refresh()

    def main_loop(self):
        """
        Main processing loop for the program.
        """
        while True:
            key = self._screen.getch()
            if key == ord('q') or key == ord('Q'):
                break
            elif key == curses.KEY_DOWN:
                if self._index + 1 < self._scroll_limit:
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
            elif key == curses.KEY_ENTER or key == ord('\n'):
                self._display_item()
                # break

    @staticmethod
    def _filter_display_items(items_dict):
        blacklist_keys = ["sections", "URLs", "notesPlain", "passwordHistory"]
        if "fields" in items_dict and isinstance(items_dict["fields"], list):
            index = 0
            for field in items_dict["fields"]:
                for(key, value) in field.items():
                    if isinstance(key, str) and isinstance(value, str):
                        items_dict[key + "_" + str(index)] = value
                        index += 1

        allowed = {k: v for k, v in items_dict.items() if v != "" and k not in blacklist_keys}
        valid_types = {k: v for k, v in allowed.items() if isinstance(v, str)}

        if valid_types.items():
            return valid_types
        return {"Error" : "No items can be displayed"}

    def _construct_window(self, item_dict):
        longest_key = max([len(k) for k in item_dict.keys()])
        longest_value = max([len(str(v)) for v in item_dict.values()])
        new_width = longest_key + 4 + longest_value
        new_height = len(item_dict.items()) + 2
        (screen_height, screen_width) = self._screen.getmaxyx()
        y_pos = int(screen_height / 2 - new_height / 2)
        x_pos = int(screen_width / 2 - new_width / 2)
        new_window = curses.newwin(new_height, new_width, y_pos, x_pos)
        new_window.overlay(self._screen)
        new_window.border()
        return new_window

    def _display_item(self):
        header_item = self._vault.headers[self._tab]
        (_, lookval) = self._vault[header_item][self._index]
        item_dict = self._vault.decrypt_item(lookval)

        item_dict = Gui._filter_display_items(item_dict)

        new_window = self._construct_window(item_dict)
        longest_key = max([len(k) for k in item_dict.keys()])
        index = 1
        for key, value in item_dict.items():
            new_window.addstr(index, 1, key + ":", curses.A_BOLD)
            new_window.addstr(index, longest_key + 2, str(value))
            index += 1
        self._screen.refresh()
        while True:
            key = new_window.getch()
            if key == 27: # ESC OR ALT
                break
        del new_window
        self._screen.touchwin()
        self._screen.refresh()

    @staticmethod
    def teardown():
        """
        Cleanup ncurses
        """
        curses.endwin()

# vim: et ai ts=4
