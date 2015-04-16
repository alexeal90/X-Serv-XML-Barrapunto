#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

	Alejandro Valeriano Fernandez - GITT
	BarraPunto

"""
#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                # To avoid Unicode trouble
                self.newsTitle = (self.theContent + ".").encode('utf-8')
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                htmlNewsStart = "            <li>"
                htmlNewsStart += "<a href='" + self.theContent + "' "
                htmlNewsStart += 'target="_blank"> '
                barrapuntoHTML.write(htmlNewsStart)
                htmlNewsEnd = self.newsTitle + "</a></li>\n"
                barrapuntoHTML.write(htmlNewsEnd)
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog

if len(sys.argv)<2:
    print "Usage: python xml-parser-barrapunto.py <document>"
    print
    print " <document>: file name of the document to parse"
    sys.exit(1)

barrapuntoHTML = open("BarrapuntoRSS.html", "w")

bodyTitle = "        <div align=center><h2>Titulares Barrapunto</h2></div>\n"
bodyTitle += '        <HR align="center" size="4" width="300" color="purple">\n'
newsListStart = "        <ul type=number>\n"
htmlBodyStart = "    <body>\n" + bodyTitle + newsListStart

htmlCodeStart = "<html>\n" + htmlBodyStart
barrapuntoHTML.write(htmlCodeStart)

# Load parser and driver

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!

xmlFile = open(sys.argv[1],"r")
theParser.parse(xmlFile)

newsListEnd = "        </ul>\n"
htmlBodyEnd = newsListEnd + "    </body>\n"
htmlCodeEnd = htmlBodyEnd + "</html>"
barrapuntoHTML.write(htmlCodeEnd)
barrapuntoHTML.close()

print "Parse complete"

