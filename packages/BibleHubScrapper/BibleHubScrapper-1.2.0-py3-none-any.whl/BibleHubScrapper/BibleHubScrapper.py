#!/usr/bin/python3.8
import requests
from bs4 import BeautifulSoup

header = "\033[4m"
red = "\033[31m"
green = "\033[32m"
blue = "\033[34m"
normal = "\033[0m"


class BibleHubQuery:
    """A Biblehub.com query, contains a passage with the text and the version.
    Can optionally contain Treasury of Scriptures(tsks), cross references(crfs) and lexicons
    Use the \"query\" function to create these objects. """

    def __init__(self, passage, text, version, crfs=None, tsks=None, lexicons=None):
        if lexicons is None:
            lexicons = []
        if tsks is None:
            tsks = []
        if crfs is None:
            crfs = []
        assert isinstance(text, str)
        assert isinstance(crfs, list)
        assert isinstance(tsks, list)
        assert isinstance(lexicons, list)
        assert isinstance(version, str)
        self.passage = passage
        self.text = text
        self.version = version
        self.crfs = crfs
        self.tsks = tsks
        self.lexicons = lexicons

    def __str__(self) -> str:
        response = self.format_verse()
        if self.crfs:
            response += "\n\n{header}Cross References{normal}\n{crfs}".format(header=header, normal=normal,
                                                                              crfs=self.format_crfs())
        if self.tsks:
            response += "\n\n{header}Treasury Of Scripture{normal}\n{tsks}".format(header=header, normal=normal,
                                                                                   tsks=self.format_tsks())
        if self.lexicons:
            response += "\n\n{header}Lexicon{normal}\n{lexicon}".format(header=header, normal=normal,
                                                                        lexicon=self.format_lexicons())
        return response

    def format_crfs(self) -> str:
        response = ''
        for crf in self.crfs:
            response += crf + '\n'
        return response

    def format_tsks(self) -> str:
        response = []
        for tsk in self.tsks:
            response.append(tsk)
        return '\n'.join(response)

    def format_verse(self) -> str:
        return "{blue}{reference} ({version}) - {normal}{verse}".format(
            blue=blue, reference=self.passage, version=self.version.upper(),
            normal=normal, verse=self.text
        )

    def format_lexicons(self) -> str:
        response = []
        for lexicon in self.lexicons:
            response.append(lexicon.__str__())
        return '\n\n'.join(response)


class _Lexicon:
    def __init__(self, text, lang, translit, parse, strong, definition):
        self.text = text
        self.lang = lang
        self.translit = translit
        self.parse = parse
        self.strong = strong
        self.definition = definition

    def __str__(self):
        return """\
%s
%s %s
%s
%s %s """ % (self.text, self.lang, self.translit, self.parse, self.strong, self.definition)


def _query_site(url) -> BeautifulSoup.find:
    result = requests.get(url)
    return BeautifulSoup(result.content, "lxml")


def _format_query(text) -> str:
    if isinstance(text, str):
        arr = text.split(sep=" ")
    else:
        arr = text
    if len(arr) == 3:
        book = arr[0].lower() + "_" + arr[1].lower()
        index = 2
    elif len(arr) == 2:
        book = arr[0].lower()
        index = 1
    else:
        raise ValueError("Invalid Query")
    verses = arr[index].split(sep=":")
    return "https://biblehub.com/%s/%s-%s.htm" % (book, verses[0], verses[1])


def _get_crfs(whole) -> list:
    crfs_list = whole.find("div", {"id": "crf"}).find_all("span", {"class": "crossverse"})
    crfs = []
    for crf in crfs_list:
        crfs.append(crf.get_text())
    return crfs


def _get_lexicon(page) -> list:
    lexicon = page.find("div", {"id": "combox"}).find("div")
    words = lexicon.find_all("span", {"class": "word"})
    lexicons = []
    for word in words:
        lexicons.append(_Lexicon(word.get_text().strip(),
                                 word.find_next("span", class_=['heb', 'grk']).get_text().strip("\n"),
                                 word.find_next("span", {"class": "translit"}).get_text().strip("\n"),
                                 word.find_next("span", {"class": "parse"}).get_text().strip("\n"),
                                 word.find_next("span", {"class": "str"}).get_text().strip("\n"),
                                 word.find_next("span", {"class": "str2"}).get_text().strip("\n")
                                 ))
    return lexicons


def _get_tsks(page) -> list:
    tsks_list = page.find_all("p", {"class": "tskverse"})
    tsks = []
    for tsk in tsks_list:
        tsks.append(tsk.get_text())
    return tsks


def _find_version(whole, ver) -> BeautifulSoup:
    versions = whole.find_all_next("span", "versiontext")
    for version in versions:
        if version.a.attrs['href'].startswith(ver):
            return version
    return versions[0]


def _get_passage(whole, version) -> str:
    version_formatted = "/%s/" % version.lower()
    first = _find_version(whole, version_formatted)
    second = first.find_next_sibling("span", {"class": "versiontext"})
    beg = first.get_text()
    block = whole.get_text()
    if second is None:
        verse = block[str.find(block, beg) + len(beg):]
    else:
        end = second.get_text()
        verse = block[str.find(block, beg) + len(beg): str.find(block, end)]
    return verse


def query(reference, version="niv", get_tsks=True, get_crfs=True, get_lexicons=True) -> BibleHubQuery:
    """Returns up to **one** verse along with the information provided by Biblehub

    :param reference: The reference to be parsed (i.e Genesis 1:1)
    :param version: The abbreviation of the version to be parsed (i.e esv or niv), defaults to niv
    :param get_tsks: Whether to fetch the Treasury of Scripture(tsk) (Contains references and texts), defaults to True
    :param get_crfs: Whether to fetch cross references (Only contains reference), defaults to True
    :param get_lexicons: Whether to fetch the lexicons, defaults to True

    :return: A BibleHubQuery
    :rtype: BibleHubScrapper.BibleHubQuery
    """
    url = _format_query(reference)
    page = _query_site(url)
    whole = page.find("div", {"id": "par"})
    verse = _get_passage(whole, version)
    lexicons = None
    if get_lexicons:
        lexicons = _get_lexicon(page)
    tsks = None
    if get_tsks:
        tsks = _get_tsks(page)
    crfs = None
    if get_crfs:
        crfs = _get_crfs(page)
    hub_query = BibleHubQuery(reference.title(), verse, version, crfs, tsks, lexicons)
    return hub_query
