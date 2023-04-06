from html import parser, escape
from typing import Dict, Any, List, Tuple, Set, Optional
import re
import string

from . import abstract

assert Set

# pylint: disable=too-many-instance-attributes

class CSSParser(abstract.AbstractParser):
    """There is no such things as metadata in CSS files,
    only comments of the form `/* … */`, so we're removing the laters."""
    mimetypes = {'text/css', }
    flags = re.MULTILINE | re.DOTALL

    def remove_all(self) -> bool:
        with open(self.filename, encoding='utf-8') as f:
            try:
                content = f.read()
            except UnicodeDecodeError:  # pragma: no cover
                raise ValueError
            cleaned = re.sub(r'/\*.*?\*/', '', content, 0, self.flags)
        with open(self.output_filename, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        return True

    def get_meta(self) -> Dict[str, Any]:
        metadata = {}
        with open(self.filename, encoding='utf-8') as f:
            try:
                content = f.read()
            except UnicodeDecodeError:  # pragma: no cover
                raise ValueError
        cssdoc = re.findall(r'/\*(.*?)\*/', content, self.flags)
        for match in cssdoc:
            for line in match.splitlines():
                try:
                    k, v = line.split(':')
                    metadata[k.strip(string.whitespace + '*')] = v.strip()
                except ValueError:
                    metadata['harmful data'] = line.strip()
        return metadata


class AbstractHTMLParser(abstract.AbstractParser):
    tags_blocklist = set()  # type: Set[str]
    # In some html/xml-based formats some tags are mandatory,
    # so we're keeping them, but are discarding their content
    tags_required_blocklist = set()  # type: Set[str]

    def __init__(self, filename):
        super().__init__(filename)
        self.__parser = _HTMLParser(self.filename, self.tags_blocklist,
                                    self.tags_required_blocklist)
        with open(filename, encoding='utf-8') as f:
            self.__parser.feed(f.read())
        self.__parser.close()

    def get_meta(self) -> Dict[str, Any]:
        return self.__parser.get_meta()

    def remove_all(self) -> bool:
        return self.__parser.remove_all(self.output_filename)


class HTMLParser(AbstractHTMLParser):
    mimetypes = {'text/html', 'application/xhtml+xml'}
    tags_blocklist = {'meta', }
    tags_required_blocklist = {'title', }


class _HTMLParser(parser.HTMLParser):
    """Python doesn't have a validating html parser in its stdlib, so
    we're using an internal queue to track all the opening/closing tags,
    and hoping for the best.

    Moreover, the parser.HTMLParser call doesn't provide a get_endtag_text
    method, so we have to use get_starttag_text instead, put its result in a
    LIFO, and transform it in a closing tag when needed.

    Also, gotcha: the `tag` parameters are always in lowercase.
    """
    def __init__(self, filename, blocklisted_tags, required_blocklisted_tags):
        super().__init__()
        self.filename = filename
        self.__textrepr = ''
        self.__meta = {}
        self.__validation_queue = []  # type: List[str]

        # We're using counters instead of booleans, to handle nested tags
        self.__in_dangerous_but_required_tag = 0
        self.__in_dangerous_tag = 0

        if required_blocklisted_tags & blocklisted_tags:  # pragma: nocover
            raise ValueError("There is an overlap between %s and %s" % (
                required_blocklisted_tags, blocklisted_tags))
        self.tag_required_blocklist = required_blocklisted_tags
        self.tag_blocklist = blocklisted_tags

    def error(self, message):  # pragma: no cover
        """ Amusingly, Python's documentation doesn't mention that this
        function needs to be implemented in subclasses of the parent class
        of parser.HTMLParser. This was found by fuzzing,
        triggering the following exception:
            NotImplementedError: subclasses of ParserBase must override error()
        """
        raise ValueError(message)

    def remove_all(self, output_filename: str) -> bool:
        if self.__validation_queue:
            raise ValueError("Some tags (%s) were left unclosed in %s" % (
                ', '.join(self.__validation_queue),
                self.filename))
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(self.__textrepr)
        return True

    def get_meta(self) -> Dict[str, Any]:
        if self.__validation_queue:
            raise ValueError("Some tags (%s) were left unclosed in %s" % (
                ', '.join(self.__validation_queue),
                self.filename))
        return self.__meta
