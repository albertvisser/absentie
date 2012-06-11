#! /usr/bin/env python
import cgi
import cgitb
cgitb.enable()
import shared
from absentie_main import ToonAbsentie, WijzigAbsentie

def main():
    form = cgi.FieldStorage()
    form_ok = False
    u = ''
    s = ''
    for k in form.keys():
        if k.startswith('wla1'):
            u = form.getvalue(k)
        elif k.startswith('wla2'):
            s = form.getvalue(k)
    xslevel, meld = shared.check_session(u, s)
    if meld:
        h = shared.MeldFout("Er is iets misgegaan", meld)
    else:
        sel_id = form.getfirst("hId", "0")
        newstat = form.getfirst("selStat", "")
        reden = form.getfirst("txtReden", "")
        komtvan = form.getfirst("hVan", "")
        kwamvan = form.getfirst("hTerug", "")
        if newstat == "2" and reden == "":
            meld = "Geef een reden op"
            h = toon_llabs_main(u, sel_id, meld, komtvan, newstat)
        else:
            newdag = form.getfirst("selDag", "")
            newmnd = form.getfirst("selMnd", "")
            newjaar = form.getfirst("selJaar", "")
            if len(newdag) == 1:
                newdag = "0" + newdag
            if len(newmnd) == 1:
                newmnd = "0" + newmnd
            newdat = newjaar + newmnd + newdag
            h = WijzigAbsentie(sel_id, newstat, reden, komtvan, u, s,
                kwamvan, newdat)
    print "Content-Type: text/html"     # HTML is following
    print
    for x in h.regels:
        print x

if __name__ == '__main__':
    main()

