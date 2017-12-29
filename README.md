# WebTuff
WebTuff is a testing utility that verifies whether your IIS server is vulnerable to 
Microsoft IIS 6.0 WebDAV Remote Authentication Bypass.
In a successful breach, WebTuff saves the remote resource locally under the same name.

Usage: 

WebTuff.py  <url to web directory>

For example: WebTuff.py http://www.victim.com/path/to/file.txt
