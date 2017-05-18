"""
Author: Sean Richardson
Email: richasea<at>gmail.com
Description: A parser for Apple property lists.
"""

from xml.etree import ElementTree

class PropertyList(object):
    """
    A property list container class.
    """
    def __init__(self):
        self._data = None

    def load(self, filename):
        """
        Loads the property list from `filename`
        """
        nodes = ElementTree.parse(filename)
        root = nodes.getroot()
        self._data = self._parse_xml(root)

    def _parse_xml(self, node):
        """
        Parse the XML into a data structure.
        """
        for child in node:
            if child.tag == "dict":
                return self._parse_dict(child)
            else:
                raise RuntimeError("Unsupported tag: " + child.tag)

    def _parse_dict(self, node):
        """
        Load dictionary elements.
        """
        result = dict()
        key = None
        for child in node:
            if child.tag == "key":
                key = child.text
                continue
            elif child.tag == "string" and key != None:
                result[key] = child.text
                key = None
                continue
            elif child.tag == "integer" and key != None:
                result[key] = int(child.text)
                key = None
                continue
            elif child.tag == "array" and key != None:
                result[key] = self._parse_array(child)
            else:
                raise RuntimeError("Unsupported Tag: " + child.tag)
        return result

    def _parse_array(self, node):
        """
        Parse arrays
        """
        result = list()
        for child in node:
            if child.tag == "dict":
                result.append(self._parse_dict(child))
            else:
                raise RuntimeError("unsupported tag: " + child.tag)
        return result

    @property
    def data(self):
        "Get the parsed data"
        return self._data
