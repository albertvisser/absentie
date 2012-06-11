#! /usr/bin/env python
import cgi
import cgitb
cgitb.enable()
import shared
from absentie_main import ToonAbsenten

def main():
    form = cgi.FieldStorage()
    form_ok = False
    u = form.getfirst("ta1", '')
    s = form.getfirst("ta2", '')
    xslevel, meld = shared.check_session(u, s)
    if meld:
        l = shared.MeldFout("Er is iets misgegaan", meld)
    else:
        l = ToonAbsenten(u, xslevel)
        #~ m = ('gebruiker %s heeft toegangsniveau %s' % (u,xslevel))
        #~ l = meld_fout("Er is iets misgegaan",m)
    print "Content-Type: text/html"     # HTML is following
    print
    for x in l.regels:
      print x

if __name__ == '__main__':
    main()

