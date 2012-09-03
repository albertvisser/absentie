#! /usr/bin/env python
import cgi
import cgitb
cgitb.enable()
import shared
from leerling_main import SelectLeerling

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    zoek = ""
    u = form.getfirst("sl1", '')
    s = form.getfirst("sl2", '')
    xslevel, meld = shared.check_session(u, s)
    if not meld:
        zoek = form.getfirst("txtZoek", None)
        absent = form.getfirst('chkAbs', False)
        if zoek is not None or absent:
            vandaan = form.getfirst("hVan", "start")
            h = SelectLeerling(zoek, vandaan, u, s, xslevel, absent)
        else:
            meld = "Geen zoekstring opgegeven"
    if meld:
        h = shared.MeldFout("Er is iets misgegaan", meld)
    print "Content-Type: text/html"     # HTML is following
    print
    for x in h.regels:
        print x

if __name__ == '__main__':
    main()

