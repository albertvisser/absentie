#! /usr/bin/env python3
import cgi
import cgitb
cgitb.enable()
import shared
from absentie_main import ToonAbsentie

def main():
    form = cgi.FieldStorage()
    form_ok = False
    u = s = ''
    for k in form.keys():
        if k.startswith('tla1'):
            u = form.getfirst(k, '')
        elif k.startswith('tla2'):
            s = form.getfirst(k, '')
    xslevel, meld = shared.check_session(u, s)
    if meld:
        h = shared.MeldFout("Er is iets misgegaan", meld)
    else:
        vandaan = form.getfirst("hVan", 'start')
        sel_id = form.getfirst("hId", 0)
        meld = form.getfirst("txtMeld", "")
        h = ToonAbsentie(u, sel_id, meld, vandaan)
    print("Content-Type: text/html\n")     # HTML is following
    for x in h.regels:
      print(x)

if __name__ == '__main__':
    main()

