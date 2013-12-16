#!/usr/bin/env python

import unittest

import asnames

asnames_db_file = 'test/asnames.txt'

class ASNamesTest(unittest.TestCase):
	def setUp(self):#{{{
		self.db = asnames.ASNamesDB(asnames_db_file)
	#}}}

	def testFullToShortName(self):#{{{
		string = 'ISI-AS - University of Southern California'
		short = asnames.full2short(string)
		self.assertEquals(short, 'ISI-AS')

		string = 'LEVEL3 Level 3 Communications'
		short = asnames.full2short(string)
		self.assertEquals(short, string)

		string = 'PUR-PO-SE -NO- PLZ - GO'
		short = asnames.full2short(string)
		self.assertEquals(short, string)

		string = 'Purpose - GO'
		short = asnames.full2short(string)
		self.assertEquals(short, string)

		string = 'PURPOSE - GO'
		short = asnames.full2short(string)
		self.assertEquals(short, 'PURPOSE')

		string = 'PUR-POSE - GO'
		short = asnames.full2short(string)
		self.assertEquals(short, 'PUR-POSE')

		string = 'MULTISPACE   - GO'
		short = asnames.full2short(string)
		self.assertEquals(short, string)

		string = ' MULTISPACE   - GO'
		short = asnames.full2short(string)
		self.assertEquals(short, string)
	#}}}

	def testString2ASN(self):#{{{
		self.assertRaises(ValueError, asnames.str2asn, 'ASN123')
		self.assertRaises(ValueError, asnames.str2asn, '1.2.3')
		self.assertRaises(ValueError, asnames.str2asn, '1.asdf')
		self.assertEquals(asnames.str2asn('12'), 12)
		self.assertEquals(asnames.str2asn(12), 12)
		self.assertRaises(ValueError, asnames.str2asn, '0x10')
		self.assertEquals(asnames.str2asn('1.0'), 1<<16)
		self.assertEquals(asnames.str2asn('2.21'), 131093)
	#}}}

	def testUnknownASN(self):#{{{
		unknown_asn = (1 << 27) + 51
		line = self.db.full(unknown_asn)
		self.assertEquals(line, asnames.UNKNOWN_FULL)
		short = self.db.short(unknown_asn)
		self.assertEquals(short, asnames.UNKNOWN_SHORT)
	#}}}

	def testReadLine(self):#{{{
		line = 'AS5     SYMBOLICS - Symbolics, Inc.'
		asn, full = asnames.readline(line)
		self.assertEquals(asn, 5)
		self.assertEquals(full, 'SYMBOLICS - Symbolics, Inc.')

		line = 'AS6     BULL-NETWORK for further information please visit http://www.bull.com'
		asn, full = asnames.readline(line)
		self.assertEquals(asn, 6)
		self.assertEquals(full, 'BULL-NETWORK for further information please visit http://www.bull.com')

		line = 'AS7     UK Defence Research Agency'
		asn, full = asnames.readline(line)
		self.assertEquals(asn, 7)
		self.assertEquals(full, 'UK Defence Research Agency')

		line = 'AS8     RICE-AS - Rice University'
		asn, full = asnames.readline(line)
		self.assertEquals(asn, 8)
		self.assertEquals(full, 'RICE-AS - Rice University')

		line = 'AS6.10 INTERCONTINENTALEXCHANGE-MULTI_ISP IntercontinentalExchange Inc. remote site multi-isp peering ASN, ARIN assigned'
		asn, full = asnames.readline(line)
		self.assertEquals(asn, asnames.str2asn('6.10'))
		self.assertEquals(full, 'INTERCONTINENTALEXCHANGE-MULTI_ISP IntercontinentalExchange Inc. remote site multi-isp peering ASN, ARIN assigned')

		line = 'ASN44 BROKEN - TEST'
		self.assertRaises(ValueError, asnames.readline, line)

		line = 'AS4.4.4 BROKEN - TEST'
		self.assertRaises(ValueError, asnames.readline, line)

		line = 'GAHOGA - WTF'
		self.assertRaises(ValueError, asnames.readline, line)
	#}}}

	def testShortASN(self):#{{{
		# AS4	  ISI-AS - University of Southern California
		# AS3356  LEVEL3 Level 3 Communications
		isi_full = 'ISI-AS - University of Southern California'
		isi_short = 'ISI-AS'
		lvl3_full = 'LEVEL3 Level 3 Communications'
		lvl3_short = 'LEVEL3 Level 3 Communications'

		line = self.db.full(4)
		self.assertEquals(line, isi_full)
		short = self.db.short(4)
		self.assertEquals(short, isi_short)

		line = self.db.full(3356)
		self.assertEquals(line, lvl3_full)
		short = self.db.short(3356)
		self.assertEquals(short, lvl3_short)
	#}}}

	def testPrivateASN(self):#{{{
		# AS65437 -Private Use AS-
		private_full = '-Private Use AS-'
		private_short = '-Private Use AS-'
		line = self.db.full(65500)
		self.assertEquals(line, private_full)
		short = self.db.short(65500)
		self.assertEquals(short, private_short)
	#}}}


if __name__ == '__main__':
	unittest.main()
