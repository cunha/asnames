'''AS names database

This module parses a file with information about AS names.  The
current parser works with the information at
bgp.potaroo.net/cidr/autnums.html; which looks like

AS2     UDEL-DCN - University of Delaware
AS3     MIT-GATEWAYS - Massachusetts Institute of Technology
AS4     ISI-AS - University of Southern California
AS5     SYMBOLICS - Symbolics, Inc.
AS6     BULL-NETWORK for further information please visit http://www.bull.com
...
AS6.110 HOSTING4BIZ - Hosting4Biz
AS6.111 GWBPC-ASN-BGP - THE GEORGE W. BUSH FOUNDATION
AS6.112 CMG-115-MFR - Comnet Marketing Group, Inc.
AS6.113 ASHLEY-STEWART - New Ashley Stewart Inc.
AS6.114 IRI-BGP - Information Resources Incorporated
AS6.115 APPFOLIO-2 - AppFolio, Inc.

The first token contains the AS number (4-byte AS numbers may be
written in decimal or in dotted format.  The rest of the line is the
AS name.  If the first token of the AS name contains only capital
letters or dashes, and is followed by another dash, then we call
that the "short" name of the AS.

Standard use goes like:

	db = ASNamesDB('path_to_file');
	assert db[2].full() == 'UDEL-DCN - University of Delaware'
	assert db[2].short() == 'UDEL-DCN'

Author: Italo Cunha <cunha@dcc.ufmg.br>
License: Latest version of the GPL.
'''

import re
import logging


_full2short_regexp_string = r'^([-A-Z]+)\s-\s.*$'
_full2short_regexp = re.compile(_full2short_regexp_string)
def _full2short(string):
    m = _full2short_regexp.match(string)
    return string if m is None else m.group(1)


UNKNOWN_FULL = 'UNKNOWN-NAMESDB - ASNamesDB unknown AS number'
UNKNOWN_SHORT = _full2short(UNKNOWN_FULL)


def str2asn(string):
    if isinstance(string, int):
        return string
    if '.' in string:
        first, second = string.split('.')
        return int(first) * (1<<16) + int(second)
    return int(string)


_readline_regexp_string = r'^AS(\d+|\d+\.\d+)\s+(.*)$'
_readline_regexp = re.compile(_readline_regexp_string)
def _readline(line):
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
                asn, full = _readline(line)
                self.asn2full[asn] = full
            except ValueError:
                logging.info('malformed line: %s', line)
        fd.close()
        logging.info('ASNamesDB %d ASes from %s', len(self.asn2full), fn)

    def full(self, asn):
        return self.asn2full.get(int(asn), UNKNOWN_FULL)

    def short(self, asn):
        return _full2short(self.full(asn))
