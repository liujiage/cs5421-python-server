
_syntax_next = "."
_syntax_slice_left = "["
_syntax_slice_right = "]"
_syntax_query_left = "{"
_syntax_query_right = "}"
_syntax = {_syntax_next, _syntax_slice_left, _syntax_slice_right, _syntax_query_left, _syntax_query_right}

''' element:movies,slice:[0],query:{parent.cast[:] =~ 'De Niro',element:title,... '''
_syntax_element = "element"
_syntax_slice = "slice"
_syntax_query = "query"

_syntax_split = ":"

"""
parse keyword
input:  movies[0].parent.{cast[:] =~ 'De Niro'}.title[:]...
output: ['element:movies', 'slice:[0]', 'element:parent', "query:{cast[:] =~ 'De Niro'}", 'element:title', 'slice:[:]']...
_syntax_next = "."
_syntax_slice_left = "["
_syntax_slice_right = "]"
_syntax_query_left = "{"
_syntax_query_right = "}"
"""


class Parser:
    def __init__(self):
        self.res = []
        self._element = ""
        self._slice = ""
        self._query = ""

    def parse(self, keyword):
        for key in keyword:
            if key == _syntax_next and not self._query:
                print("_syntax_next {}".format(key))
                self.add_element()
            elif key == _syntax_slice_left and not self._query:
                print("_syntax_slice_left {}".format(key))
                self._slice = self._slice + key
                self.add_element()
            elif key == _syntax_slice_right and not self._query:
                print("_syntax_slice_right {}".format(key))
                self._slice = self._slice + key
                self.add_slice()
            elif key == _syntax_query_left and not self._query:
                print("_syntax_query_left {}".format(key))
                self.add_element()
                self._query = self._query + key
            elif key == _syntax_query_right:
                print("_syntax_query_right {}".format(key))
                self._query = self._query + key
                self.add_query()
            elif self._query:
                self._query = self._query + key
            elif self._slice and not self._query:
                self._slice = self._slice + key
            else:
                print("element {}".format(key))
                self._element = self._element + key
        self.add_element()
        return self.res

    def add_element(self):
        if self._element:
            self.res.append(_syntax_element + _syntax_split + self._element)
            self._element = ""

    def add_slice(self):
        if self._slice:
            self.res.append(_syntax_slice + _syntax_split + self._slice)
            self._slice = ""

    def add_query(self):
        if self._query:
            self.res.append(_syntax_query + _syntax_split + self._query)
            self._query = ""
