# -*- encoding: utf-8 -*-
"""
MediaWiki-style markup

Copyright (C) 2008 David Cramer <dcramer@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import unicode_literals
from __future__ import absolute_import
from collections import OrderedDict
import re, random, locale
from base64 import b64encode, b64decode
import six
from six.moves import range
from six.moves import zip
try:
	from cgi import escape
except ImportError:
	from html import escape

# a few patterns we use later

MW_COLON_STATE_TEXT = 0
MW_COLON_STATE_TAG = 1
MW_COLON_STATE_TAGSTART = 2
MW_COLON_STATE_CLOSETAG = 3
MW_COLON_STATE_TAGSLASH = 4
MW_COLON_STATE_COMMENT = 5
MW_COLON_STATE_COMMENTDASH = 6
MW_COLON_STATE_COMMENTDASHDASH = 7

_attributePat = re.compile(r'''(?:^|\s)([A-Za-z0-9]+)(?:\s*=\s*(?:"([^<"]*)"|'([^<']*)'|([a-zA-Z0-9!#$%&()*,\-./:;<>?@[\]^_`{|}~]+)|#([0-9a-fA-F]+)))''', re.UNICODE)
_space = re.compile(r'\s+', re.UNICODE)
_closePrePat = re.compile("</pre", re.UNICODE | re.IGNORECASE)
_openPrePat = re.compile("<pre", re.UNICODE | re.IGNORECASE)
_openMatchPat = re.compile("(<table|<blockquote|<h1|<h2|<h3|<h4|<h5|<h6|<pre|<tr|<p|<ul|<ol|<li|</center|</tr|</td|</th)", re.UNICODE | re.IGNORECASE)
_tagPattern = re.compile(r'^(/?)(\w+)([^>]*?)(/?>)([^<]*)$', re.UNICODE)

_htmlpairs = ( # Tags that must be closed
	'b', 'del', 'i', 'ins', 'u', 'font', 'big', 'small', 'sub', 'sup', 'h1',
	'h2', 'h3', 'h4', 'h5', 'h6', 'cite', 'code', 'em', 's',
	'strike', 'strong', 'tt', 'var', 'div', 'center',
	'blockquote', 'ol', 'ul', 'dl', 'table', 'caption', 'pre',
	'ruby', 'rt' , 'rb' , 'rp', 'p', 'span', 'u',
)
_htmlsingle = (
	'br', 'hr', 'li', 'dt', 'dd', 'img',
)
_htmlsingleonly = ( # Elements that cannot have close tags
	'br', 'hr', 'img',
)
_htmlnest = ( # Tags that can be nested--??
	'table', 'tr', 'td', 'th', 'div', 'blockquote', 'ol', 'ul',
	'dl', 'font', 'big', 'small', 'sub', 'sup', 'span', 'img',
)
_tabletags = ( # Can only appear inside table
	'td', 'th', 'tr',
)
_htmllist = ( # Tags used by list
	'ul', 'ol',
)
_listtags = ( # Tags that can appear in a list
	'li',
)
_htmlsingleallowed = _htmlsingle + _tabletags
_htmlelements = _htmlsingle + _htmlpairs + _htmlnest

_htmlEntities = {
	'Aacute': 193,	'aacute': 225, 'Acirc': 194, 'acirc': 226, 'acute': 180,
	'AElig': 198, 'aelig': 230, 'Agrave': 192, 'agrave': 224, 'alefsym': 8501,
	'Alpha': 913, 'alpha': 945, 'amp': 38, 'and': 8743, 'ang': 8736, 'Aring': 197,
	'aring':	  229,
	'asymp':	  8776,
	'Atilde':	 195,
	'atilde':	 227,
	'Auml':	   196,
	'auml':	   228,
	'bdquo':	  8222,
	'Beta':	   914,
	'beta':	   946,
	'brvbar':	 166,
	'bull':	   8226,
	'cap':		8745,
	'Ccedil':	 199,
	'ccedil':	 231,
	'cedil':	  184,
	'cent':	   162,
	'Chi':		935,
	'chi':		967,
	'circ':	   710,
	'clubs':	  9827,
	'cong':	   8773,
	'copy':	   169,
	'crarr':	  8629,
	'cup':		8746,
	'curren':	 164,
	'dagger':	 8224,
	'Dagger':	 8225,
	'darr':	   8595,
	'dArr':	   8659,
	'deg':		176,
	'Delta':	  916,
	'delta':	  948,
	'diams':	  9830,
	'divide':	 247,
	'Eacute':	 201,
	'eacute':	 233,
	'Ecirc':	  202,
	'ecirc':	  234,
	'Egrave':	 200,
	'egrave':	 232,
	'empty':	  8709,
	'emsp':	   8195,
	'ensp':	   8194,
	'Epsilon':	917,
	'epsilon':	949,
	'equiv':	  8801,
	'Eta':		919,
	'eta':		951,
	'ETH':		208,
	'eth':		240,
	'Euml':	   203,
	'euml':	   235,
	'euro':	   8364,
	'exist':	  8707,
	'fnof':	   402,
	'forall':	 8704,
	'frac12':	 189,
	'frac14':	 188,
	'frac34':	 190,
	'frasl':	  8260,
	'Gamma':	  915,
	'gamma':	  947,
	'ge':		 8805,
	'gt':		 62,
	'harr':	   8596,
	'hArr':	   8660,
	'hearts':	 9829,
	'hellip':	 8230,
	'Iacute':	 205,
	'iacute':	 237,
	'Icirc':	  206,
	'icirc':	  238,
	'iexcl':	  161,
	'Igrave':	 204,
	'igrave':	 236,
	'image':	  8465,
	'infin':	  8734,
	'int':		8747,
	'Iota':	   921,
	'iota':	   953,
	'iquest':	 191,
	'isin':	   8712,
	'Iuml':	   207,
	'iuml':	   239,
	'Kappa':	  922,
	'kappa':	  954,
	'Lambda':	 923,
	'lambda':	 955,
	'lang':	   9001,
	'laquo':	  171,
	'larr':	   8592,
	'lArr':	   8656,
	'lceil':	  8968,
	'ldquo':	  8220,
	'le':		 8804,
	'lfloor':	 8970,
	'lowast':	 8727,
	'loz':		9674,
	'lrm':		8206,
	'lsaquo':	 8249,
	'lsquo':	  8216,
	'lt':		 60,
	'macr':	   175,
	'mdash':	  8212,
	'micro':	  181,
	'middot':	 183,
	'minus':	  8722,
	'Mu':		 924,
	'mu':		 956,
	'nabla':	  8711,
	'nbsp':	   160,
	'ndash':	  8211,
	'ne':		 8800,
	'ni':		 8715,
	'not':		172,
	'notin':	  8713,
	'nsub':	   8836,
	'Ntilde':	 209,
	'ntilde':	 241,
	'Nu':		 925,
	'nu':		 957,
	'Oacute':	 211,
	'oacute':	 243,
	'Ocirc':	  212,
	'ocirc':	  244,
	'OElig':	  338,
	'oelig':	  339,
	'Ograve':	 210,
	'ograve':	 242,
	'oline':	  8254,
	'Omega':	  937,
	'omega':	  969,
	'Omicron':	927,
	'omicron':	959,
	'oplus':	  8853,
	'or':		 8744,
	'ordf':	   170,
	'ordm':	   186,
	'Oslash':	 216,
	'oslash':	 248,
	'Otilde':	 213,
	'otilde':	 245,
	'otimes':	 8855,
	'Ouml':	   214,
	'ouml':	   246,
	'para':	   182,
	'part':	   8706,
	'permil':	 8240,
	'perp':	   8869,
	'Phi':		934,
	'phi':		966,
	'Pi':		 928,
	'pi':		 960,
	'piv':		982,
	'plusmn':	 177,
	'pound':	  163,
	'prime':	  8242,
	'Prime':	  8243,
	'prod':	   8719,
	'prop':	   8733,
	'Psi':		936,
	'psi':		968,
	'quot':	   34,
	'radic':	  8730,
	'rang':	   9002,
	'raquo':	  187,
	'rarr':	   8594,
	'rArr':	   8658,
	'rceil':	  8969,
	'rdquo':	  8221,
	'real':	   8476,
	'reg':		174,
	'rfloor':	 8971,
	'Rho':		929,
	'rho':		961,
	'rlm':		8207,
	'rsaquo':	 8250,
	'rsquo':	  8217,
	'sbquo':	  8218,
	'Scaron':	 352,
	'scaron':	 353,
	'sdot':	   8901,
	'sect':	   167,
	'shy':		173,
	'Sigma':	  931,
	'sigma':	  963,
	'sigmaf':	 962,
	'sim':		8764,
	'spades':	 9824,
	'sub':		8834,
	'sube':	   8838,
	'sum':		8721,
	'sup':		8835,
	'sup1':	   185,
	'sup2':	   178,
	'sup3':	   179,
	'supe':	   8839,
	'szlig':	  223,
	'Tau':		932,
	'tau':		964,
	'there4':	 8756,
	'Theta':	  920,
	'theta':	  952,
	'thetasym':   977,
	'thinsp':	 8201,
	'THORN':	  222,
	'thorn':	  254,
	'tilde':	  732,
	'times':	  215,
	'trade':	  8482,
	'Uacute':	 218,
	'uacute':	 250,
	'uarr':	   8593,
	'uArr':	   8657,
	'Ucirc':	  219,
	'ucirc':	  251,
	'Ugrave':	 217,
	'ugrave':	 249,
	'uml':		168,
	'upsih':	  978,
	'Upsilon':	933,
	'upsilon':	965,
	'Uuml':	   220,
	'uuml':	   252,
	'weierp':	 8472,
	'Xi':		 926,
	'xi':		 958,
	'Yacute':	 221,
	'yacute':	 253,
	'yen':		165,
	'Yuml':	   376,
	'yuml':	   255,
	'Zeta':	   918,
	'zeta':	   950,
	'zwj':		8205,
	'zwnj':	   8204
}

_charRefsPat = re.compile(r'''(&([A-Za-z0-9]+);|&#([0-9]+);|&#[xX]([0-9A-Za-z]+);|(&))''', re.UNICODE)
_cssCommentPat = re.compile(r'''\*.*?\*''', re.UNICODE)
_toUTFPat = re.compile(r'''\\([0-9A-Fa-f]{1,6})[\s]?''', re.UNICODE)
_hackPat = re.compile(r'''(expression|tps*://|url\s*\().*''', re.UNICODE | re.IGNORECASE)
_hrPat = re.compile('''^-----*''', re.UNICODE | re.MULTILINE)
_h1Pat = re.compile('^=(.+)=\s*$', re.UNICODE | re.MULTILINE)
_h2Pat = re.compile('^==(.+)==\s*$', re.UNICODE | re.MULTILINE)
_h3Pat = re.compile('^===(.+)===\s*$', re.UNICODE | re.MULTILINE)
_h4Pat = re.compile('^====(.+)====\s*$', re.UNICODE | re.MULTILINE)
_h5Pat = re.compile('^=====(.+)=====\s*$', re.UNICODE | re.MULTILINE)
_h6Pat = re.compile('^======(.+)======\s*$', re.UNICODE | re.MULTILINE)
_quotePat = re.compile("""(''+)""", re.UNICODE)
_removePat = re.compile(r'\b(' + r'|'.join(("a", "an", "as", "at", "before", "but", "by", "for", "from",
							"is", "in", "into", "like", "of", "off", "on", "onto", "per",
							"since", "than", "the", "this", "that", "to", "up", "via",
							"with")) + r')\b', re.UNICODE | re.IGNORECASE)
_nonWordSpaceDashPat = re.compile(r'[^\w\s\-\./]', re.UNICODE)
_multiSpacePat = re.compile(r'[\s\-_\./]+', re.UNICODE)
_spacePat = re.compile(r' ', re.UNICODE)
_linkPat = re.compile(r'^(?:([A-Za-z0-9]+):)?([^\|]+)(?:\|([^\n]+?))?\]\](.*)$', re.UNICODE | re.DOTALL)
_bracketedLinkPat = re.compile(r'(?:\[((?:mailto:|irc://|https?://|ftp://|/)[^<>\]\[' + "\x00-\x20\x7f" + r']*)\s*(.*?)\])', re.UNICODE)
_protocolPat = re.compile(r'(\b(?:mailto:|irc://|https?://|ftp://))', re.UNICODE)
_specialUrlPat = re.compile(r'^([^<>\]\[' + "\x00-\x20\x7f" + r']+)(.*)$', re.UNICODE)
_protocolsPat = re.compile(r'^(mailto:|irc://|https?://|ftp://)$', re.UNICODE)
_controlCharsPat = re.compile(r'[\]\[<>"' + "\\x00-\\x20\\x7F" + r']]', re.UNICODE)
_hostnamePat = re.compile(r'^([^:]+:)(//[^/]+)?(.*)$', re.UNICODE)
_stripPat = re.compile('\\s|\u00ad|\u1806|\u200b|\u2060|\ufeff|\u03f4|\u034f|\u180b|\u180c|\u180d|\u200c|\u200d|[\ufe00-\ufe0f]', re.UNICODE)
_zomgPat = re.compile(r'^(:*)\{\|(.*)$', re.UNICODE)
_headerPat = re.compile(r"<[Hh]([1-6])(.*?)>(.*?)</[Hh][1-6] *>", re.UNICODE)
_templateSectionPat = re.compile(r"<!--MWTEMPLATESECTION=([^&]+)&([^_]+)-->", re.UNICODE)
_tagPat = re.compile(r"<.*?>", re.UNICODE)
_startRegexHash = {}
_endRegexHash = {}
_endCommentPat = re.compile(r'(-->)', re.UNICODE)
_extractTagsAndParams_n = 1
_guillemetLeftPat = re.compile(r'(.) (\?|:|;|!|\302\273)', re.UNICODE)
_guillemetRightPat = re.compile(r'(\302\253) ', re.UNICODE)

def setupAttributeWhitelist():
	common = ( 'id', 'class', 'lang', 'dir', 'title', 'style' )
	block = common + ('align',)
	tablealign = ( 'align', 'char', 'charoff', 'valign' )
	tablecell = ( 'abbr',
					'axis',
					'headers',
					'scope',
					'rowspan',
					'colspan',
					'nowrap', # deprecated
					'width',  # deprecated
					'height', # deprecated
					'bgcolor' # deprecated
					)
	return {
		'div':			block,
		'center':		common, # deprecated
		'span':		block, # ??
		'h1':			block,
		'h2':			block,
		'h3':			block,
		'h4':			block,
		'h5':			block,
		'h6':			block,
		'em':			common,
		'strong':		common,
		'cite':		common,
		'code':		common,
		'var':			common,
		'img':			common + ('src', 'alt', 'width', 'height',),
		'blockquote':	common + ('cite',),
		'sub':			common,
		'sup':			common,
		'p':			block,
		'br':			('id', 'class', 'title', 'style', 'clear',),
		'pre':			common + ('width',),
		'ins':			common + ('cite', 'datetime'),
		'del':			common + ('cite', 'datetime'),
		'ul':			common + ('type',),
		'ol':			common + ('type', 'start'),
		'li':			common + ('type', 'value'),
		'dl':			common,
		'dd':			common,
		'dt':			common,
		'table':		common + ( 'summary', 'width', 'border', 'frame',
									'rules', 'cellspacing', 'cellpadding',
									'align', 'bgcolor',
							),
		'caption':		common + ('align',),
		'thead':		common + tablealign,
		'tfoot':		common + tablealign,
		'tbody':		common + tablealign,
		'colgroup':	common + ( 'span', 'width' ) + tablealign,
		'col':			common + ( 'span', 'width' ) + tablealign,
		'tr':			common + ( 'bgcolor', ) + tablealign,
		'td':			common + tablecell + tablealign,
		'th':			common + tablecell + tablealign,
		'tt':			common,
		'b':			common,
		'i':			common,
		'big':			common,
		'small':		common,
		'strike':		common,
		's':			common,
		'u':			common,
		'font':		common + ( 'size', 'color', 'face' ),
		'hr':			common + ( 'noshade', 'size', 'width' ),
		'ruby':		common,
		'rb':			common,
		'rt':			common, #array_merge( $common, array( 'rbspan' ) ),
		'rp':			common,
	}
_whitelist = setupAttributeWhitelist()
_page_cache = {}
env = {}

def registerTagHook(tag, function):
	mTagHooks[tag] = function

class BaseParser(object):
	def __init__(self):
		self.uniq_prefix = "\x07UNIQ" + six.text_type(random.randint(1, 1000000000))
		self.strip_state = {}
		self.arg_stack = []
		self.env = env
		self.keep_env = (env != {})

	def __del__(self):
		if not self.keep_env:
			global env
			env = {}

	''' Used to store objects in the environment
		used to prevent recursive imports '''
	def store_object(self, namespace, key, value=True):
		# Store the item to not reprocess it
		if namespace not in self.env:
			self.env[namespace] = {}
		self.env[namespace][key] = value

	def has_object(self, namespace, key):
		if namespace not in self.env:
			self.env[namespace] = {}
		if hasattr(self, 'count'):
			data = self.env[namespace]
			test = key in data
			self.count = True
		return key in self.env[namespace]

	def retrieve_object(self, namespace, key, default=None):
		if not self.env.get(namespace):
			self.env[namespace] = {}
		return self.env[namespace].get(key, default)

	def parse(self, text):
		utf8 = isinstance(text, str)
		text = to_unicode(text)
		if text[-1:] != '\n':
			text = text + '\n'
			taggedNewline = True
		else:
			taggedNewline = False

		text = self.strip(text)
		text = self.removeHtmlTags(text)
		text = self.parseHorizontalRule(text)
		text = self.parseAllQuotes(text)
		text = self.replaceExternalLinks(text)
		text = self.unstrip(text)
		text = self.fixtags(text)
		text = self.doBlockLevels(text, True)
		text = self.unstripNoWiki(text)
		text = text.split('\n')
		text = '\n'.join(text)
		if taggedNewline and text[-1:] == '\n':
			text = text[:-1]
		if utf8:
			return text.encode("utf-8")
		return text

	def strip(self, text, stripcomments=False, dontstrip=[]):
		render = True

		commentState = {}

		elements = ['nowiki',]  + list(mTagHooks.keys())
		if True: #wgRawHtml
			elements.append('html')

		# Removing $dontstrip tags from $elements list (currently only 'gallery', fixing bug 2700)
		for k in dontstrip:
			if k in elements:
				del elements[k]

		matches = {}
		text = self.extractTagsAndParams(elements, text, matches)

		for marker in matches:
			element, content, params, tag = matches[marker]
			if render:
				tagName = element.lower()
				if tagName == '!--':
					# comment
					output = tag
					if tag[-3:] != '-->':
						output += "-->"
				elif tagName == 'html':
					output = content
				elif tagName == 'nowiki':
					output = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
				else:
					if tagName in mTagHooks:
						output = mTagHooks[tagName](self, content, params)
					else:
						output = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
			else:
				# Just stripping tags; keep the source
				output = tag

			# Unstrip the output, because unstrip() is no longer recursive so
			# it won't do it itself
			output = self.unstrip(output)

			if not stripcomments and element == '!--':
				commentState[marker] = output
			elif element == 'html' or element == 'nowiki':
				if 'nowiki' not in self.strip_state:
					self.strip_state['nowiki'] = {}
				self.strip_state['nowiki'][marker] = output
			else:
				if 'general' not in self.strip_state:
					self.strip_state['general'] = {}
				self.strip_state['general'][marker] = output

		# Unstrip comments unless explicitly told otherwise.
		# (The comments are always stripped prior to this point, so as to
		# not invoke any extension tags / parser hooks contained within
		# a comment.)
		if not stripcomments:
			# Put them all back and forget them
			for k in commentState:
				v = commentState[k]
				text = text.replace(k, v)

		return text

	def removeHtmlTags(self, text):
		"""convert bad tags into HTML identities"""
		sb = []
		text = self.removeHtmlComments(text)
		bits = text.split('<')
		sb.append(bits.pop(0))
		tagstack = []
		tablestack = tagstack
		for x in bits:
			m = _tagPattern.match(x)
			if not m:
				continue
			slash, t, params, brace, rest = m.groups()
			t = t.lower()
			badtag = False
			if t in _htmlelements:
				# Check our stack
				if slash:
					# Closing a tag...
					if t in _htmlsingleonly or len(tagstack) == 0:
						badtag = True
					else:
						ot = tagstack.pop()
						if ot != t:
							if ot in _htmlsingleallowed:
								# Pop all elements with an optional close tag
								# and see if we find a match below them
								optstack = []
								optstack.append(ot)
								while True:
									if len(tagstack) == 0:
										break
									ot = tagstack.pop()
									if ot == t or ot not in _htmlsingleallowed:
										break
									optstack.append(ot)
								if t != ot:
									# No match. Push the optinal elements back again
									badtag = True
									tagstack += reversed(optstack)
							else:
								tagstack.append(ot)
								# <li> can be nested in <ul> or <ol>, skip those cases:
								if ot not in _htmllist and t in _listtags:
									badtag = True
						elif t == 'table':
							if len(tablestack) == 0:
								bagtag = True
							else:
								tagstack = tablestack.pop()
					newparams = ''
				else:
					# Keep track for later
					if t in _tabletags and 'table' not in tagstack:
						badtag = True
					elif t in tagstack and t not in _htmlnest:
						badtag = True
					# Is it a self-closed htmlpair? (bug 5487)
					elif brace == '/>' and t in _htmlpairs:
						badTag = True
					elif t in _htmlsingleonly:
						# Hack to force empty tag for uncloseable elements
						brace = '/>'
					elif t in _htmlsingle:
						# Hack to not close $htmlsingle tags
						brace = None
					else:
						if t == 'table':
							tablestack.append(tagstack)
							tagstack = []
						tagstack.append(t)
					newparams = self.fixTagAttributes(params, t)
				if not badtag:
					rest = rest.replace('>', '&gt;')
					if brace == '/>':
						close = ' /'
					else:
						close = ''
					sb.append('<')
					sb.append(slash)
					sb.append(t)
					sb.append(newparams)
					sb.append(close)
					sb.append('>')
					sb.append(rest)
					continue
			sb.append('&lt;')
			sb.append(x.replace('>', '&gt;'))

		# Close off any remaining tags
		while tagstack:
			t = tagstack.pop()
			sb.append('</')
			sb.append(t)
			sb.append('>\n')
			if t == 'table':
				if not tablestack:
					break
				tagstack = tablestack.pop()

		return ''.join(sb)

	def removeHtmlComments(self, text):
		"""remove <!-- text --> comments from given text"""
		sb = []
		start = text.find('<!--')
		last = 0
		while start != -1:
			end = text.find('-->', start)
			if end == -1:
				break
			end += 3

			spaceStart = max(0, start-1)
			spaceEnd = end
			while text[spaceStart] == ' ' and spaceStart > 0:
				spaceStart -= 1
			while text[spaceEnd] == ' ':
				spaceEnd += 1

			if text[spaceStart] == '\n' and text[spaceEnd] == '\n':
				sb.append(text[last:spaceStart])
				sb.append('\n')
				last = spaceEnd+1
			else:
				sb.append(text[last:spaceStart+1])
				last = spaceEnd

			start = text.find('<!--', end)
		sb.append(text[last:])
		return ''.join(sb)

	def decodeTagAttributes(self, text):
		"""docstring for decodeTagAttributes"""
		attribs = OrderedDict()
		if text.strip() == '':
			return attribs
		scanner = _attributePat.scanner(text)
		match = scanner.search()
		while match:
			key, val1, val2, val3, val4 = match.groups()
			value = val1 or val2 or val3 or val4
			if value:
				value = _space.sub(' ', value).strip()
			else:
				value = ''
			attribs[key] = self.decodeCharReferences(value)

			match = scanner.search()
		return attribs

	def validateTagAttributes(self, attribs, element):
		"""docstring for validateTagAttributes"""
		out = OrderedDict()
		if element not in _whitelist:
			return out
		whitelist = _whitelist[element]
		for attribute in attribs:
			value = attribs[attribute]
			if attribute not in whitelist:
				continue
			# Strip javascript "expression" from stylesheets.
			# http://msdn.microsoft.com/workshop/author/dhtml/overview/recalc.asp
			if attribute == 'style':
				value = self.checkCss(value)
				if value == False:
					continue
			elif attribute == 'id':
				value = self.escapeId(value)
			# If this attribute was previously set, override it.
			# Output should only have one attribute of each name.
			out[attribute] = value
		return out

	def safeEncodeAttribute(self, encValue):
		"""docstring for safeEncodeAttribute"""
		encValue = encValue.replace('&', '&amp;')
		encValue = encValue.replace('<', '&lt;')
		encValue = encValue.replace('>', '&gt;')
		encValue = encValue.replace('"', '&quot;')
		encValue = encValue.replace('{', '&#123;')
		encValue = encValue.replace('[', '&#91;')
		encValue = encValue.replace("''", '&#39;&#39;')
		encValue = encValue.replace('ISBN', '&#73;SBN')
		encValue = encValue.replace('RFC', '&#82;FC')
		encValue = encValue.replace('PMID', '&#80;MID')
		encValue = encValue.replace('|', '&#124;')
		encValue = encValue.replace('__', '&#95;_')
		encValue = encValue.replace('\n', '&#10;')
		encValue = encValue.replace('\r', '&#13;')
		encValue = encValue.replace('\t', '&#9;')
		return encValue

	def fixTagAttributes(self, text, element):
		if text.strip() == '':
			return ''

		stripped = self.validateTagAttributes(self.decodeTagAttributes(text), element)

		sb = []

		for attribute in stripped:
			value = stripped[attribute]
			encAttribute = attribute.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
			encValue = self.safeEncodeAttribute(value)

			sb.append(' ')
			sb.append(encAttribute)
			sb.append('="')
			sb.append(encValue)
			sb.append('"')

		return ''.join(sb)

	def validateCodepoint(self, codepoint):
		return codepoint ==	0x09 \
			or codepoint ==	0x0a \
			or codepoint ==	0x0d \
			or (codepoint >=	0x20 and codepoint <=   0xd7ff) \
			or (codepoint >=  0xe000 and codepoint <=   0xfffd) \
			or (codepoint >= 0x10000 and codepoint <= 0x10ffff)

	def _normalizeCallback(self, match):
		text, norm, dec, hexval, _ = match.groups()
		if norm:
			sb = []
			sb.append('&')
			if norm not in _htmlEntities:
				sb.append('amp;')
			sb.append(norm)
			sb.append(';')
			return ''.join(sb)
		elif dec:
			dec = int(dec)
			if self.validateCodepoint(dec):
				sb = []
				sb.append('&#')
				sb.append(dec)
				sb.append(';')
				return ''.join(sb)
		elif hexval:
			hexval = int(hexval, 16)
			if self.validateCodepoint(hexval):
				sb = []
				sb.append('&#x')
				sb.append(hex(hexval))
				sb.append(';')
				return ''.join(sb)
		return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

	def normalizeCharReferences(self, text):
		"""docstring for normalizeCharReferences"""
		return _charRefsPat.sub(self._normalizeCallback, text)

	def _decodeCallback(self, match):
		text, norm, dec, hexval, _ = match.groups()
		if norm:
			if norm in _htmlEntities:
				return chr(_htmlEntities[norm])
			else:
				sb = []
				sb.append('&')
				sb.append(norm)
				sb.append(';')
				return ''.join(sb)
		elif dec:
			dec = int(dec)
			if self.validateCodepoint(dec):
				return chr(dec)
			return '?'
		elif hexval:
			hexval = int(hexval, 16)
			if self.validateCodepoint(dec):
				return chr(dec)
			return '?'
		return text

	def decodeCharReferences(self, text):
		"""docstring for decodeCharReferences"""
		if text:
			return _charRefsPat.sub(self._decodeCallback, text)
		return ''

	def _convertToUtf8(self, s):
		return chr(int(s.group(1), 16))

	def checkCss(self, value):
		"""docstring for checkCss"""
		stripped = self.decodeCharReferences(value)

		stripped = _cssCommentPat.sub('', stripped)
		value = stripped

		stripped = _toUTFPat.sub(self._convertToUtf8, stripped)
		stripped.replace('\\', '')
		if _hackPat.search(stripped):
			# someone is haxx0ring
			return False

		return value

	def escapeId(self, value):
		"""docstring for escapeId"""
		# TODO
		return safe_name(value)

	def parseHorizontalRule(self, text):
		return _hrPat.sub(r'<hr />', text)

	def parseHeaders(self, text):
		text = _h6Pat.sub(r'<h6>\1</h6>', text)
		text = _h5Pat.sub(r'<h5>\1</h5>', text)
		text = _h4Pat.sub(r'<h4>\1</h4>', text)
		text = _h3Pat.sub(r'<h3>\1</h3>', text)
		text = _h2Pat.sub(r'<h2>\1</h2>', text)
		text = _h1Pat.sub(r'<h1>\1</h1>', text)
		return text

	def parseQuotes(self, text):
		arr = _quotePat.split(text)
		if len(arr) == 1:
			return text
		# First, do some preliminary work. This may shift some apostrophes from
		# being mark-up to being text. It also counts the number of occurrences
		# of bold and italics mark-ups.
		numBold = 0
		numItalics = 0
		for i,r in zip(list(range(len(arr))), arr):
			if i%2 == 1:
				l = len(r)
				if l == 4:
					arr[i-1] += "'"
					arr[i] = "'''"
				elif l > 5:
					arr[i-1] += "'" * (len(arr[i]) - 5)
					arr[i] = "'''''"
				if l == 2:
					numItalics += 1
				elif l >= 5:
					numItalics += 1
					numBold += 1
				else:
					numBold += 1

		# If there is an odd number of both bold and italics, it is likely
		# that one of the bold ones was meant to be an apostrophe followed
		# by italics. Which one we cannot know for certain, but it is more
		# likely to be one that has a single-letter word before it.
		if numBold%2 == 1 and numItalics%2 == 1:
			firstSingleLetterWord = -1
			firstMultiLetterWord = -1
			firstSpace = -1
			for i,r in zip(list(range(len(arr))), arr):
				if i%2 == 1 and len(r) == 3:
					x1 = arr[i-1][-1:]
					x2 = arr[i-1][-2:-1]
					if x1 == ' ':
						if firstSpace == -1:
							firstSpace = i
					elif x2 == ' ':
						if firstSingleLetterWord == -1:
							firstSingleLetterWord = i
					else:
						if firstMultiLetterWord == -1:
							firstMultiLetterWord = i

			# If there is a single-letter word, use it!
			if firstSingleLetterWord > -1:
				arr[firstSingleLetterWord] = "''"
				arr[firstSingleLetterWord-1] += "'"
			# If not, but there's a multi-letter word, use that one.
			elif firstMultiLetterWord > -1:
				arr[firstMultiLetterWord] = "''"
				arr[firstMultiLetterWord-1] += "'"
			# ... otherwise use the first one that has neither.
			# (notice that it is possible for all three to be -1 if, for example,
			# there is only one pentuple-apostrophe in the line)
			elif firstSpace > -1:
				arr[firstSpace] = "''"
				arr[firstSpace-1] += "'"

		# Now let's actually convert our apostrophic mush to HTML!
		output = []
		buffer = None
		state = ''
		for i,r in zip(list(range(len(arr))), arr):
			if i%2 == 0:
				if state == 'both':
					buffer.append(r)
				else:
					output.append(r)
			else:
				if len(r) == 2:
					if state == 'i':
						output.append("</i>")
						state = ''
					elif state == 'bi':
						output.append("</i>")
						state = 'b'
					elif state == 'ib':
						output.append("</b></i><b>")
						state = 'b'
					elif state == 'both':
						output.append("<b><i>")
						output.append(''.join(buffer))
						buffer = None
						output.append("</i>")
						state = 'b'
					elif state == 'b':
						output.append("<i>")
						state = 'bi'
					else: # ''
						output.append("<i>")
						state = 'i'
				elif len(r) == 3:
					if state == 'b':
						output.append("</b>")
						state = ''
					elif state == 'bi':
						output.append("</i></b><i>")
						state = 'i'
					elif state == 'ib':
						output.append("</b>")
						state = 'i'
					elif state == 'both':
						output.append("<i><b>")
						output.append(''.join(buffer))
						buffer = None
						output.append("</b>")
						state = 'i'
					elif state == 'i':
						output.append("<b>")
						state = 'ib'
					else: # ''
						output.append("<b>")
						state = 'b'
				elif len(r) == 5:
					if state == 'b':
						output.append("</b><i>")
						state = 'i'
					elif state == 'i':
						output.append("</i><b>")
						state = 'b'
					elif state == 'bi':
						output.append("</i></b>")
						state = ''
					elif state == 'ib':
						output.append("</b></i>")
						state = ''
					elif state == 'both':
						output.append("<i><b>")
						output.append(''.join(buffer))
						buffer = None
						output.append("</b></i>")
						state = ''
					else: # ''
						buffer = []
						state = 'both'

		if state == 'both':
			output.append("<i><b>")
			output.append(''.join(buffer))
			buffer = None
			output.append("</b></i>")
		elif state != '':
			if state == 'b' or state == 'ib':
				output.append("</b>")
			if state == 'i' or state == 'bi' or state == 'ib':
				output.append("</i>")
			if state == 'bi':
				output.append("</b>")
		return ''.join(output)

	def parseAllQuotes(self, text):
		sb = []
		lines = text.split('\n')
		first = True
		for line in lines:
			if not first:
				sb.append('\n')
			else:
				first = False
			sb.append(self.parseQuotes(line))
		return ''.join(sb)

	def replaceExternalLinks(self, text):
		sb = []
		bits = _bracketedLinkPat.split(text)
		l = len(bits)
		i = 0
		num_links = 0
		while i < l:
			if i%3 == 0:
				#sb.append(self.replaceFreeExternalLinks(bits[i]))
				sb.append(bits[i])
				i += 1
			else:
				sb.append('<a href="')
				sb.append(bits[i])
				sb.append('" alt="')
				sb.append(bits[i+1])
				sb.append('">')
				if not bits[i+1]:
					num_links += 1
					sb.append(to_unicode(truncate_url(bits[i])))
				else:
					sb.append(bits[i+1])
				sb.append('</a>')
				i += 2
		return ''.join(sb)

	# TODO: fix this so it actually works
	def replaceFreeExternalLinks(self, text):
		bits = _protocolPat.split(text)
		sb = [bits.pop(0)]
		i = 0
		l = len(bits)
		while i < l:
			protocol = bits[i]
			remainder = bits[i+1]
			i += 2
			match = _specialUrlPat.match(remainder)
			if match:
				# Found some characters after the protocol that look promising
				url = protocol + match.group(1)
				trail = match.group(2)

				# special case: handle urls as url args:
				# http://www.example.com/foo?=http://www.example.com/bar
				if len(trail) == 0 and len(bits) > i and _protocolsPat.match(bits[i]):
					match = _specialUrlPat.match(remainder)
					if match:
						url += bits[i] + match.group(1)
						i += 2
						trail = match.group(2)

				# The characters '<' and '>' (which were escaped by
				# removeHTMLtags()) should not be included in
				# URLs, per RFC 2396.
				pos = max(url.find('&lt;'), url.find('&gt;'))
				if pos != -1:
					trail = url[pos:] + trail
					url = url[0:pos]

				sep = ',;.:!?'
				if '(' not in url:
					sep += ')'

				i = len(url)-1
				while i >= 0:
					char = url[i]
					if char not in sep:
						break
					i -= 1
				i += 1

				if i != len(url):
					trail = url[i:] + trail
					url = url[0:i]

				url = self.cleanURL(url)

				sb.append('<a href="')
				sb.append(url)
				sb.append('">')
				sb.append(truncate_url(url))
				sb.append('</a>')
				#sb.append(text)
				sb.append(trail)
			else:
				sb.append(protocol)
				sb.append(remainder)
		return ''.join(sb)

	def urlencode(self, char):
		num = ord(char)
		if num == 32:
			return '+'
		return "%%%02x" % num

	def cleanURL(self, url):
		# Normalize any HTML entities in input. They will be
		# re-escaped by makeExternalLink().
		url = self.decodeCharReferences(url)

		# Escape any control characters introduced by the above step
		url = _controlCharsPat.sub(self.urlencode, url)

		# Validate hostname portion
		match = _hostnamePat.match(url)
		if match:
			protocol, host, rest = match.groups()

			# Characters that will be ignored in IDNs.
			# http://tools.ietf.org/html/3454#section-3.1
			# Strip them before further processing so blacklists and such work.

			_stripPat.sub('', host)

			# @fixme: validate hostnames here

			return protocol + host + rest
		else:
			return url

	def unstripForHTML(self, text):
		text = self.unstrip(text)
		text = self.unstripNoWiki(text)
		return text

	def unstrip(self, text):
		if 'general' not in self.strip_state:
			return text

		general = self.strip_state['general']
		for k in general:
			v = general[k]
			text = text.replace(k, v)
		return text

	def unstripNoWiki(self, text):
		if 'nowiki' not in self.strip_state:
			return text
		nowiki = self.strip_state['nowiki']
		for k in nowiki:
			v = nowiki[k]
			text = text.replace(k, v)
		return text

	def extractTagsAndParams(self, elements, text, matches):
		"""
		Replaces all occurrences of HTML-style comments and the given tags
		in the text with a random marker and returns teh next text. The output
		parameter $matches will be an associative array filled with data in
		the form:
		  'UNIQ-xxxxx' => array(
		  'element',
		  'tag content',
		  array( 'param' => 'x' ),
		  '<element param="x">tag content</element>' ) )
		"""
		stripped = ''

		taglist = '|'.join(elements)
		if taglist not in _startRegexHash:
			_startRegexHash[taglist] = re.compile(r"<(" + taglist + r")(\s+[^>]*?|\s*?)(/?>)|<(!--)", re.UNICODE | re.IGNORECASE)
		start = _startRegexHash[taglist]

		while text != '':
			p = start.split(text, 1)
			stripped += p[0]
			if len(p) == 1:
				break
			elif p[4]:
				# comment
				element = p[4]
				attributes = ''
				close = ''
			else:
				element = p[1]
				attributes = p[2]
				close = p[3]
			inside = p[5]

			global _extractTagsAndParams_n
			marker = self.uniq_prefix + '-' + element + '-' + ("%08X" % _extractTagsAndParams_n) + '-QINU'
			_extractTagsAndParams_n += 1
			stripped += marker

			if close == '/>':
				# empty element tag, <tag />
				content = None
				text = inside
				tail = None
			else:
				if element == '!--':
					end = _endCommentPat
				else:
					if element not in _endRegexHash:
						_endRegexHash[element] = re.compile(r'(</' + element + r'\s*>)', re.UNICODE | re.IGNORECASE)
					end = _endRegexHash[element]
				q = end.split(inside, 1)
				content = q[0]
				if len(q) < 3:
					# no end tag
					tail = ''
					text = ''
				else:
					tail = q[1]
					text = q[2]

			matches[marker] = (
				element,
				content,
				self.decodeTagAttributes(attributes),
				"<" + element + attributes + close + content + tail
			)
		return stripped

	def fixtags(self, text):
		"""Clean up special characters, only run once, next-to-last before doBlockLevels"""
		# french spaces, last one Guillemet-left
		# only if there is something before the space
		text = _guillemetLeftPat.sub(r'\1&nbsp;\2', text)
		# french spaces, Guillemet-right
		text = _guillemetRightPat.sub(r'\1&nbsp;', text)
		return text

	def closeParagraph(self, mLastSection):
		"""Used by doBlockLevels()"""
		result = ''
		if mLastSection != '':
			result = '</' + mLastSection + '>\n'

		return result

	def getCommon(self, st1, st2):
		"""
		getCommon() returns the length of the longest common substring
		of both arguments, starting at the beginning of both.
		"""
		fl = len(st1)
		shorter = len(st2)
		if fl < shorter:
			shorter = fl

		i = 0
		while i < shorter:
			if st1[i] != st2[i]:
				break
			i += 1
		return i

	def openList(self, char, mLastSection):
		"""
		These next three functions open, continue, and close the list
		element appropriate to the prefix character passed into them.
		"""
		result = self.closeParagraph(mLastSection)

		mDTopen = False
		if char == '*':
			result += '<ul><li>'
		elif char == '#':
			result += '<ol><li>'
		elif char == ':':
			result += '<dl><dd>'
		elif char == ';':
			result += '<dl><dt>'
			mDTopen = True
		else:
			result += '<!-- ERR 1 -->'

		return result, mDTopen

	def nextItem(self, char, mDTopen):
		if char == '*' or char == '#':
			return '</li><li>', None
		elif char == ':' or char == ';':
			close = '</dd>'
			if mDTopen:
				close = '</dt>'
			if char == ';':
				return close + '<dt>', True
			else:
				return close + '<dd>', False
		return '<!-- ERR 2 -->'

	def closeList(self, char, mDTopen):
		if char == '*':
			return '</li></ul>\n'
		elif char == '#':
			return '</li></ol>\n'
		elif char == ':':
			if mDTopen:
				return '</dt></dl>\n'
			else:
				return '</dd></dl>\n'
		else:
			return '<!-- ERR 3 -->'

	def findColonNoLinks(self, text, before, after):
		try:
			pos = text.search(':')
		except:
			return False

		lt = text.find('<')
		if lt == -1 or lt > pos:
			# Easy; no tag nesting to worry about
			before = text[0:pos]
			after = text[0:pos+1]
			return before, after, pos

		# Ugly state machine to walk through avoiding tags.
		state = MW_COLON_STATE_TEXT;
		stack = 0;
		i = 0
		while i < len(text):
			c = text[i];

			if state == 0: # MW_COLON_STATE_TEXT:
				if text[i] == '<':
					# Could be either a <start> tag or an </end> tag
					state = MW_COLON_STATE_TAGSTART
				elif text[i] == ':':
					if stack == 0:
						# we found it
						return text[0:i], text[i+1], i
				else:
					# Skip ahead looking for something interesting
					try:
						colon = text.search(':', i)
					except:
						return False
					lt = text.find('<', i)
					if stack == 0:
						if lt == -1 or colon < lt:
							# we found it
							return text[0:colon], text[colon+1], i
					if lt == -1:
						break
					# Skip ahead to next tag start
					i = lt
					state = MW_COLON_STATE_TAGSTART
			elif state == 1: # MW_COLON_STATE_TAG:
				# In a <tag>
				if text[i] == '>':
					stack += 1
					state = MW_COLON_STATE_TEXT
				elif text[i] == '/':
					state = MW_COLON_STATE_TAGSLASH
			elif state == 2: # MW_COLON_STATE_TAGSTART:
				if text[i] == '/':
					state = MW_COLON_STATE_CLOSETAG
				elif text[i] == '!':
					state = MW_COLON_STATE_COMMENT
				elif text[i] == '>':
					# Illegal early close? This shouldn't happen D:
					state = MW_COLON_STATE_TEXT
				else:
					state = MW_COLON_STATE_TAG
			elif state == 3: # MW_COLON_STATE_CLOSETAG:
				# In a </tag>
				if text[i] == '>':
					stack -= 1
					if stack < 0:
						return False
					state = MW_COLON_STATE_TEXT
			elif state == MW_COLON_STATE_TAGSLASH:
				if text[i] == '>':
					# Yes, a self-closed tag <blah/>
					state = MW_COLON_STATE_TEXT
				else:
					# Probably we're jumping the gun, and this is an attribute
					state = MW_COLON_STATE_TAG
			elif state == 5: # MW_COLON_STATE_COMMENT:
				if text[i] == '-':
					state = MW_COLON_STATE_COMMENTDASH
			elif state == MW_COLON_STATE_COMMENTDASH:
				if text[i] == '-':
					state = MW_COLON_STATE_COMMENTDASHDASH
				else:
					state = MW_COLON_STATE_COMMENT
			elif state == MW_COLON_STATE_COMMENTDASHDASH:
				if text[i] == '>':
					state = MW_COLON_STATE_TEXT
				else:
					state = MW_COLON_STATE_COMMENT
			else:
				raise
		if stack > 0:
			return False
		return False

	def doBlockLevels(self, text, linestart):
		# Parsing through the text line by line.  The main thing
		# happening here is handling of block-level elements p, pre,
		# and making lists from lines starting with * # : etc.
		lastPrefix = ''
		mDTopen = inBlockElem = False
		prefixLength = 0
		paragraphStack = False
		_closeMatchPat = re.compile(r"(</table|</blockquote|</h1|</h2|</h3|</h4|</h5|</h6|<td|<th|<div|</div|<hr|</pre|</p|" +  self.uniq_prefix + r"-pre|</li|</ul|</ol|<center)", re.UNICODE | re.IGNORECASE)
		mInPre = False
		mLastSection = ''
		mDTopen = False
		output = []
		for oLine in text.split('\n')[not linestart and 1 or 0:]:
			lastPrefixLength = len(lastPrefix)
			preCloseMatch = _closePrePat.search(oLine)
			preOpenMatch = _openPrePat.search(oLine)
			if not mInPre:
				chars = '*#:;'
				prefixLength = 0
				for c in oLine:
					if c in chars:
						prefixLength += 1
					else:
						break
				pref = oLine[0:prefixLength]

				# eh?
				pref2 = pref.replace(';', ':')
				t = oLine[prefixLength:]
				mInPre = bool(preOpenMatch)
			else:
				# Don't interpret any other prefixes in preformatted text
				prefixLength = 0
				pref = pref2 = ''
				t = oLine

			# List generation
			if prefixLength and lastPrefix == pref2:
				# Same as the last item, so no need to deal with nesting or opening stuff
				tmpOutput, tmpMDTopen = self.nextItem(pref[-1:], mDTopen)
				output.append(tmpOutput)
				if tmpMDTopen is not None:
					mDTopen = tmpMDTopen
				paragraphStack = False

				if pref[-1:] == ';':
					# The one nasty exception: definition lists work like this:
					# ; title : definition text
					# So we check for : in the remainder text to split up the
					# title and definition, without b0rking links.
					term = t2 = ''
					z = self.findColonNoLinks(t, term, t2)
					if z != False:
						term, t2 = z[1:2]
						t = t2
						output.append(term)
						tmpOutput, tmpMDTopen = self.nextItem(':', mDTopen)
						output.append(tmpOutput)
						if tmpMDTopen is not None:
							mDTopen = tmpMDTopen

			elif prefixLength or lastPrefixLength:
				# Either open or close a level...
				commonPrefixLength = self.getCommon(pref, lastPrefix)
				paragraphStack = False
				while commonPrefixLength < lastPrefixLength:
					tmp = self.closeList(lastPrefix[lastPrefixLength-1], mDTopen)
					output.append(tmp)
					mDTopen = False
					lastPrefixLength -= 1
				if prefixLength <= commonPrefixLength and commonPrefixLength > 0:
					tmpOutput, tmpMDTopen = self.nextItem(pref[commonPrefixLength-1], mDTopen)
					output.append(tmpOutput)
					if tmpMDTopen is not None:
						mDTopen = tmpMDTopen

				while prefixLength > commonPrefixLength:
					char = pref[commonPrefixLength:commonPrefixLength+1]
					tmpOutput, tmpMDTOpen = self.openList(char, mLastSection)
					if tmpMDTOpen:
						mDTopen = True
					output.append(tmpOutput)
					mLastSection = ''
					mInPre = False

					if char == ';':
						# FIXME: This is dupe of code above
						term = t2 = ''
						z = self.findColonNoLinks(t, term, t2)
						if z != False:
							term, t2 = z[1:2]
							t = t2
							output.append(term)
							tmpOutput, tmpMDTopen = self.nextItem(':', mDTopen)
							output.append(tmpOutput)
							if tmpMDTopen is not None:
								mDTopen = tmpMDTopen

					commonPrefixLength += 1

				lastPrefix = pref2

			if prefixLength == 0:
				# No prefix (not in list)--go to paragraph mode
				# XXX: use a stack for nestable elements like span, table and div
				openmatch = _openMatchPat.search(t)
				closematch = _closeMatchPat.search(t)
				if openmatch or closematch:
					paragraphStack = False
					output.append(self.closeParagraph(mLastSection))
					mLastSection = ''
					if preCloseMatch:
						mInPre = False
					if preOpenMatch:
						mInPre = True
					inBlockElem = bool(not closematch)
				elif not inBlockElem and not mInPre:
					if t[0:1] == ' ' and (mLastSection ==  'pre' or t.strip() != ''):
						# pre
						if mLastSection != 'pre':
							paragraphStack = False
							output.append(self.closeParagraph('') + '<pre>')
							mInPre = False
							mLastSection = 'pre'
						t = t[1:]
					else:
						# paragraph
						if t.strip() == '':
							if paragraphStack:
								output.append(paragraphStack + '<br />')
								paragraphStack = False
								mLastSection = 'p'
							else:
								if mLastSection != 'p':
									output.append(self.closeParagraph(mLastSection))
									mLastSection = ''
									mInPre = False
									paragraphStack = '<p>'
								else:
									paragraphStack = '</p><p>'
						else:
							if paragraphStack:
								output.append(paragraphStack)
								paragraphStack = False
								mLastSection = 'p'
							elif mLastSection != 'p':
								output.append(self.closeParagraph(mLastSection) + '<p>')
								mLastSection = 'p'
								mInPre = False

			# somewhere above we forget to get out of pre block (bug 785)
			if preCloseMatch and mInPre:
				mInPre = False

			if paragraphStack == False:
				output.append(t + "\n")

		while prefixLength:
			output.append(self.closeList(pref2[prefixLength-1], mDTopen))
			mDTopen = False
			prefixLength -= 1

		if mLastSection != '':
			output.append('</' + mLastSection + '>')
			mLastSection = ''

		return ''.join(output)

class Parser(BaseParser):
	def __init__(self, show_toc=True):
		super(Parser, self).__init__()
		self.show_toc = show_toc

	def parse(self, text):
		utf8 = isinstance(text, six.binary_type)
		text = to_unicode(text)
		if text[-1:] != '\n':
			text = text + '\n'
			taggedNewline = True
		else:
			taggedNewline = False

		text = self.strip(text)
		text = self.removeHtmlTags(text)
		text = self.doTableStuff(text)
		text = self.parseHorizontalRule(text)
		text = self.checkTOC(text)
		text = self.parseHeaders(text)
		text = self.parseAllQuotes(text)
		text = self.replaceExternalLinks(text)
		if not self.show_toc and text.find("<!--MWTOC-->") == -1:
			self.show_toc = False
		text = self.formatHeadings(text, True)
		text = self.unstrip(text)
		text = self.fixtags(text)
		text = self.doBlockLevels(text, True)
		text = self.unstripNoWiki(text)
		text = text.split('\n')
		text = '\n'.join(text)
		if taggedNewline and text[-1:] == '\n':
			text = text[:-1]
		if utf8:
			return text.encode("utf-8")
		return text

	def checkTOC(self, text):
		if text.find("__NOTOC__") != -1:
			text = text.replace("__NOTOC__", "")
			self.show_toc = False
		if text.find("__TOC__") != -1:
			text = text.replace("__TOC__", "<!--MWTOC-->")
			self.show_toc = True
		return text

	def doTableStuff(self, text):
		t = text.split("\n")
		td = [] # Is currently a td tag open?
		ltd = [] # Was it TD or TH?
		tr = [] # Is currently a tr tag open?
		ltr = [] # tr attributes
		has_opened_tr = [] # Did this table open a <tr> element?
		indent_level = 0 # indent level of the table

		for k, x in zip(list(range(len(t))), t):
			x = x.strip()
			fc = x[0:1]
			matches = _zomgPat.match(x)
			if matches:
				indent_level = len(matches.group(1))

				attributes = self.unstripForHTML(matches.group(2))

				t[k] = '<dl><dd>'*indent_level + '<table' + self.fixTagAttributes(attributes, 'table') + '>'
				td.append(False)
				ltd.append('')
				tr.append(False)
				ltr.append('')
				has_opened_tr.append(False)
			elif len(td) == 0:
				pass
			elif '|}' == x[0:2]:
				z = "</table>" + x[2:]
				l = ltd.pop()
				if not has_opened_tr.pop():
					z = "<tr><td></td><tr>" + z
				if tr.pop():
					z = "</tr>" + z
				if td.pop():
					z = '</' + l + '>' + z
				ltr.pop()
				t[k] = z + '</dd></dl>'*indent_level
			elif '|-' == x[0:2]: # Allows for |-------------
				x = x[1:]
				while x != '' and x[0:1] == '-':
					x = x[1:]
				z = ''
				l = ltd.pop()
				has_opened_tr.pop()
				has_opened_tr.append(True)
				if tr.pop():
					z = '</tr>' + z
				if td.pop():
					z = '</' + l + '>' + z
				ltr.pop()
				t[k] = z
				tr.append(False)
				td.append(False)
				ltd.append('')
				attributes = self.unstripForHTML(x)
				ltr.append(self.fixTagAttributes(attributes, 'tr'))
			elif '|' == fc or '!' == fc or '|+' == x[0:2]: # Caption
				# x is a table row
				if '|+' == x[0:2]:
					fc = '+'
					x = x[1:]
				x = x[1:]
				if fc == '!':
					x = x.replace('!!', '||')
				# Split up multiple cells on the same line.
				# FIXME: This can result in improper nesting of tags processed
				# by earlier parser steps, but should avoid splitting up eg
				# attribute values containing literal "||".
				x = x.split('||')

				t[k] = ''

				# Loop through each table cell
				for theline in x:
					z = ''
					if fc != '+':
						tra = ltr.pop()
						if not tr.pop():
							z = '<tr' + tra + '>\n'
						tr.append(True)
						ltr.append('')
						has_opened_tr.pop()
						has_opened_tr.append(True)
					l = ltd.pop()
					if td.pop():
						z = '</' + l + '>' + z
					if fc == '|':
						l = 'td'
					elif fc == '!':
						l = 'th'
					elif fc == '+':
						l = 'caption'
					else:
						l = ''
					ltd.append(l)

					#Cell parameters
					y = theline.split('|', 1)
					# Note that a '|' inside an invalid link should not
					# be mistaken as delimiting cell parameters
					if y[0].find('[[') != -1:
						y = [theline]

					if len(y) == 1:
						y = z + "<" + l + ">" + y[0]
					else:
						attributes = self.unstripForHTML(y[0])
						y = z + "<" + l + self.fixTagAttributes(attributes, l) + ">" + y[1]

					t[k] += y
					td.append(True)

		while len(td) > 0:
			l = ltd.pop()
			if td.pop():
				t.append('</td>')
			if tr.pop():
				t.append('</tr>')
			if not has_opened_tr.pop():
				t.append('<tr><td></td></tr>')
			t.append('</table>')

		text = '\n'.join(t)
		# special case: don't return empty table
		if text == "<table>\n<tr><td></td></tr>\n</table>":
			text = ''

		return text

	def formatHeadings(self, text, isMain):
		"""
		This function accomplishes several tasks:
		1) Auto-number headings if that option is enabled
		2) Add an [edit] link to sections for logged in users who have enabled the option
		3) Add a Table of contents on the top for users who have enabled the option
		4) Auto-anchor headings

		It loops through all headlines, collects the necessary data, then splits up the
		string and re-inserts the newly formatted headlines.
		"""
		doNumberHeadings = False
		showEditLink = True # Can User Edit

		if text.find("__NOEDITSECTION__") != -1:
			showEditLink = False
			text = text.replace("__NOEDITSECTION__", "")

		# Get all headlines for numbering them and adding funky stuff like [edit]
		# links - this is for later, but we need the number of headlines right now
		matches = _headerPat.findall(text)
		numMatches = len(matches)

		# if there are fewer than 4 headlines in the article, do not show TOC
		# unless it's been explicitly enabled.
		enoughToc = self.show_toc and (numMatches >= 4 or text.find("<!--MWTOC-->") != -1)

		# Allow user to stipulate that a page should have a "new section"
		# link added via __NEWSECTIONLINK__
		showNewSection = False
		if text.find("__NEWSECTIONLINK__") != -1:
			showNewSection = True
			text = text.replace("__NEWSECTIONLINK__", "")
		# if the string __FORCETOC__ (not case-sensitive) occurs in the HTML,
		# override above conditions and always show TOC above first header
		if text.find("__FORCETOC__") != -1:
			self.show_toc = True
			enoughToc = True
			text = text.replace("__FORCETOC__", "")
		# Never ever show TOC if no headers
		if numMatches < 1:
			enoughToc = False

		# headline counter
		headlineCount = 0
		sectionCount = 0 # headlineCount excluding template sections

		# Ugh .. the TOC should have neat indentation levels which can be
		# passed to the skin functions. These are determined here
		toc = []
		head = {}
		sublevelCount = {}
		levelCount = {}
		toclevel = 0
		level = 0
		prevlevel = 0
		toclevel = 0
		prevtoclevel = 0
		refers = {}
		refcount = {}
		wgMaxTocLevel = 5

		for match in matches:
			headline = match[2]
			istemplate = False
			templatetitle = ''
			templatesection = 0
			numbering = []

			m = _templateSectionPat.search(headline)
			if m:
				istemplate = True
				templatetitle = b64decode(m[0])
				templatesection = 1 + int(b64decode(m[1]))
				headline = _templateSectionPat.sub('', headline)

			if toclevel:
				prevlevel = level
				prevtoclevel = toclevel

			level = int(matches[headlineCount][0])

			if doNumberHeadings or enoughToc:
				if level > prevlevel:
					toclevel += 1
					sublevelCount[toclevel] = 0
					if toclevel < wgMaxTocLevel:
						toc.append('\n<ul>')
				elif level < prevlevel and toclevel > 1:
					# Decrease TOC level, find level to jump to

					if toclevel == 2 and level < levelCount[1]:
						toclevel = 1
					else:
						for i in range(toclevel, 0, -1):
							if levelCount[i] == level:
								# Found last matching level
								toclevel = i
								break
							elif levelCount[i] < level:
								toclevel = i + 1
								break
					if toclevel < wgMaxTocLevel:
						toc.append("</li>\n")
						toc.append("</ul>\n</li>\n" * max(prevtoclevel - toclevel, 0))
				else:
					if toclevel < wgMaxTocLevel:
						toc.append("</li>\n")

				levelCount[toclevel] = level

				# count number of headlines for each level
				sublevelCount[toclevel] += 1
				for i in range(1, toclevel+1):
					if sublevelCount[i]:
						numbering.append(to_unicode(sublevelCount[i]))

			# The canonized header is a version of the header text safe to use for links
			# Avoid insertion of weird stuff like <math> by expanding the relevant sections
			canonized_headline = self.unstrip(headline)
			canonized_headline = self.unstripNoWiki(canonized_headline)

			# -- don't know what to do with this yet.
			# Remove link placeholders by the link text.
			#	 <!--LINK number-->
			# turns into
			#	 link text with suffix
	#		$canonized_headline = preg_replace( '/<!--LINK ([0-9]*)-->/e',
	#							"\$this->mLinkHolders['texts'][\$1]",
	#							$canonized_headline );
	#		$canonized_headline = preg_replace( '/<!--IWLINK ([0-9]*)-->/e',
	#							"\$this->mInterwikiLinkHolders['texts'][\$1]",
	#							$canonized_headline );

			# strip out HTML
			canonized_headline = _tagPat.sub('', canonized_headline)
			tocline = canonized_headline.strip()
			# Save headline for section edit hint before it's escaped
			headline_hint = tocline
			canonized_headline = self.escapeId(tocline)
			refers[headlineCount] = canonized_headline

			# count how many in assoc. array so we can track dupes in anchors
			if canonized_headline not in refers:
				refers[canonized_headline] = 1
			else:
				refers[canonized_headline] += 1
			refcount[headlineCount] = refers[canonized_headline]

			numbering = '.'.join(numbering)

			# Don't number the heading if it is the only one (looks silly)
			if doNumberHeadings and numMatches > 1:
				# the two are different if the line contains a link
				headline = numbering + ' ' + headline

			# Create the anchor for linking from the TOC to the section
			anchor = canonized_headline;
			if refcount[headlineCount] > 1:
				anchor += '_' + six.text_type(refcount[headlineCount])

			if enoughToc:
				toc.append('\n<li class="toclevel-')
				toc.append(to_unicode(toclevel))
				toc.append('"><a href="#w_')
				toc.append(anchor)
				toc.append('"><span class="tocnumber">')
				toc.append(numbering)
				toc.append('</span> <span class="toctext">')
				toc.append(tocline)
				toc.append('</span></a>')

	#		if showEditLink and (not istemplate or templatetitle != u""):
	#			if not head[headlineCount]:
	#				head[headlineCount] = u''
	#
	#			if istemplate:
	#				head[headlineCount] += sk.editSectionLinkForOther(templatetile, templatesection)
	#			else:
	#				head[headlineCount] += sk.editSectionLink(mTitle, sectionCount+1, headline_hint)

			# give headline the correct <h#> tag
			if headlineCount not in head:
				head[headlineCount] = []
			h = head[headlineCount]
			h.append('<h')
			h.append(to_unicode(level))
			h.append(' id="w_')
			h.append(anchor)
			h.append('">')
			h.append(matches[headlineCount][1].strip())
			h.append(headline.strip())
			h.append('</h')
			h.append(to_unicode(level))
			h.append('>')

			headlineCount += 1

			if not istemplate:
				sectionCount += 1

		if enoughToc:
			if toclevel < wgMaxTocLevel:
				toc.append("</li>\n")
				toc.append("</ul>\n</li>\n" * max(0, toclevel - 1))
			#TODO: use gettext
			#toc.insert(0, u'<div id="toc"><h2>' + _('Table of Contents') + '</h2>')
			toc.insert(0, '<div id="toc"><h2>Table of Contents</h2>')
			toc.append('</ul>\n</div>')

		# split up and insert constructed headlines

		blocks = _headerPat.split(text)

		i = 0
		len_blocks = len(blocks)
		forceTocPosition = text.find("<!--MWTOC-->")
		full = []
		while i < len_blocks:
			j = i/4
			full.append(blocks[i])
			if enoughToc and not i and isMain and forceTocPosition == -1:
				full += toc
				toc = None
			if j in head and head[j]:
				full += head[j]
				head[j] = None
			i += 4
		full = ''.join(full)
		if forceTocPosition != -1:
			return full.replace("<!--MWTOC-->", ''.join(toc), 1)
		else:
			return full

def parse(text, showToc=True):
	"""Returns HTML from MediaWiki markup"""
	p = Parser(show_toc=showToc)
	return p.parse(text)

def parselite(text):
	"""Returns HTML from MediaWiki markup ignoring
	without headings"""
	p = BaseParser()
	return p.parse(text)

def truncate_url(url, length=40):
	if len(url) <= length:
		return url
	import re
	pattern = r'(/[^/]+/?)$'
	match = re.search(pattern, url)
	if not match:
		return url
	l = len(match.group(1))
	domain = url.replace(match.group(1), '')
	firstpart = url[0:len(url)-l]
	secondpart = match.group(1)
	if firstpart == firstpart[0:length-3]:
		secondpart = secondpart[0:length-3] + '...'
	else:
		firstpart = firstpart[0:length-3]
		secondpart = '...' + secondpart
	t_url = firstpart+secondpart
	return t_url

def to_unicode(text, charset=None):
	"""Convert a `str` object to an `unicode` object.

	If `charset` is given, we simply assume that encoding for the text,
	but we'll use the "replace" mode so that the decoding will always
	succeed.
	If `charset` is ''not'' specified, we'll make some guesses, first
	trying the UTF-8 encoding, then trying the locale preferred encoding,
	in "replace" mode. This differs from the `unicode` builtin, which
	by default uses the locale preferred encoding, in 'strict' mode,
	and is therefore prompt to raise `UnicodeDecodeError`s.

	Because of the "replace" mode, the original content might be altered.
	If this is not what is wanted, one could map the original byte content
	by using an encoding which maps each byte of the input to an unicode
	character, e.g. by doing `unicode(text, 'iso-8859-1')`.
	"""
	if not isinstance(text, str):
		if isinstance(text, Exception):
			# two possibilities for storing unicode strings in exception data:
			try:
				# custom __str__ method on the exception (e.g. PermissionError)
				return six.text_type(text)
			except UnicodeError:
				# unicode arguments given to the exception (e.g. parse_date)
				return ' '.join([to_unicode(arg) for arg in text.args])
		return six.text_type(text)
	if charset:
		return six.ensure_text(text, charset, 'replace')
	else:
		try:
			return six.ensure_text(text, 'utf-8')
		except UnicodeError:
			return six.ensure_text(text, locale.getpreferredencoding(), 'replace')

# tag hooks
mTagHooks = {}

## IMPORTANT
## Make sure all hooks output CLEAN html. Escape any user input BEFORE it's returned

# Arguments passed:
# - wiki environment instance
# - tag content
# - dictionary of attributes

# quote example:
# <quote cite="person">quote</quote>

def hook_quote(env, body, attributes={}):
	text = ['<div class="blockquote">']
	if 'cite' in attributes:
		text.append("<strong class=\"cite\">%s wrote:</strong>\n" % escape(attributes['cite'], quote=False))
	text.append(body.strip())
	text.append('</div>')
	return '\n'.join(text)
registerTagHook('quote', hook_quote)

def safe_name(name=None, remove_slashes=True):
	if name is None:
		return None
	name = str2url(name)
	if remove_slashes:
		name = re.sub(r"[^a-zA-Z0-9\-_\s\.]", "", name)
	else:
		name = re.sub(r"[^a-zA-Z0-9\-_\s\.\/]", "", name)
	name = re.sub(r"[\s\._]", "-", name)
	name = re.sub(r"[-]+", "-", name)
	return name.strip("-").lower()

def str2url(str):
	"""
	Takes a UTF-8 string and replaces all characters with the equivalent in 7-bit
	ASCII. It returns a plain ASCII string usable in URLs.
	"""
	mfrom	= "ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝßàáâãäåæçèéêëìíîï"
	to		= "AAAAAAECEEEEIIIIDNOOOOOOUUUUYSaaaaaaaceeeeiiii"
	mfrom	+= "ñòóôõöøùúûüýÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģ"
	to		+= "noooooouuuuyyaaaaaaccccccccddddeeeeeeeeeegggggggg"
	mfrom	+= "ĤĥĦħĨĩĪīĬĭĮįİıĴĵĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŒœŔŕŖŗŘř"
	to		+= "hhhhiiiiiiiiiijjkkkllllllllllnnnnnnnnnoooooooorrrrrr"
	mfrom	+= "ŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽžſƀƂƃƄƅƇƈƉƊƐƑƒƓƔ"
	to		+= "ssssssssttttttuuuuuuuuuuuuwwyyyzzzzzzfbbbbbccddeffgv"
	mfrom	+= "ƖƗƘƙƚƝƞƟƠƤƦƫƬƭƮƯưƱƲƳƴƵƶǍǎǏǐǑǒǓǔǕǖǗǘǙǚǛǜǝǞǟǠǡǢǣǤǥǦǧǨǩ"
	to		+= "likklnnoopettttuuuuyyzzaaiioouuuuuuuuuueaaaaeeggggkk"
	mfrom	+= "ǪǫǬǭǰǴǵǷǸǹǺǻǼǽǾǿȀȁȂȃȄȅȆȇȈȉȊȋȌȍȎȏȐȑȒȓȔȕȖȗȘșȚțȞȟȤȥȦȧȨȩ"
	to		+= "oooojggpnnaaeeooaaaaeeeeiiiioooorrrruuuusstthhzzaaee"
	mfrom	+= "ȪȫȬȭȮȯȰȱȲȳḀḁḂḃḄḅḆḇḈḉḊḋḌḍḎḏḐḑḒḓḔḕḖḗḘḙḚḛḜḝḞḟḠḡḢḣḤḥḦḧḨḩḪḫ"
	to		+= "ooooooooyyaabbbbbbccddddddddddeeeeeeeeeeffgghhhhhhhhhh"
	mfrom	+= "ḬḭḮḯḰḱḲḳḴḵḶḷḸḹḺḻḼḽḾḿṀṁṂṃṄṅṆṇṈṉṊṋṌṍṎṏṐṑṒṓṔṕṖṗṘṙṚṛṜṝṞṟ"
	to		+= "iiiikkkkkkllllllllmmmmmmnnnnnnnnoooooooopppprrrrrrrr"
	mfrom	+= "ṠṡṢṣṤṥṦṧṨṩṪṫṬṭṮṯṰṱṲṳṴṵṶṷṸṹṺṻṼṽṾṿẀẁẂẃẄẅẆẇẈẉẊẋẌẍẎẏẐẑẒẓẔẕ"
	to		+= "ssssssssssttttttttuuuuuuuuuuvvvvwwwwwwwwwwxxxxxyzzzzzz"
	mfrom	+= "ẖẗẘẙẚẛẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊị"
	to		+= "htwyafaaaaaaaaaaaaaaaaaaaaaaaaeeeeeeeeeeeeeeeeiiii"
	mfrom	+= "ỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ"
	to		+= "oooooooooooooooooooooooouuuuuuuuuuuuuuyyyyyyyy"
	for i in zip(mfrom, to):
		str = str.replace(*i)
	return str
