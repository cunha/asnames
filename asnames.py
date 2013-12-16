import re
import logging


_full2short_regexp_string = r'^([-A-Z]+)\s-\s.*$'
_full2short_regexp = re.compile(_full2short_regexp_string)
def full2short(string):
    m = _full2short_regexp.match(string)
    return string if m is None else m.group(1)


UNKNOWN_FULL = 'UNKNOWN-NAMESDB - ASNamesDB unknown AS number'
UNKNOWN_SHORT = full2short(UNKNOWN_FULL)


def str2asn(string):
    if isinstance(string, int):
        return string
    if '.' in string:
        first, second = string.split('.')
        return int(first) * (1<<16) + int(second)
    return int(string)


_readline_regexp_string = r'^AS(\d+|\d+\.\d+)\s+(.*)$'
_readline_regexp = re.compile(_readline_regexp_string)
def readline(line):
    m = _readline_regexp.match(line)
    if m is None: raise ValueError('malformed line %s' % line)
    return str2asn(m.group(1)), m.group(2)


class ASNamesDB(object):
    def __init__(self, fn):
        self.asn2full = dict()
        fd = open(fn, 'r')
        for line in fd:
            line = line.strip()
            try:
                asn, full = readline(line)
                self.asn2full[asn] = full
            except ValueError:
                logging.info('malformed line: %s', line)
        fd.close()
        logging.info('ASNamesDB %d ASes from %s', len(self.asn2full), fn)

    def full(self, asn):
        return self.asn2full.get(int(asn), UNKNOWN_FULL)

    def short(self, asn):
        return full2short(self.full(asn))
