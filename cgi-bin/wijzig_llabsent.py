#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import shared
from absentie_main import ToonAbsentie, WijzigAbsentie

def main():
    form = cgi.FieldStorage()
    form_ok = False
    ## shared.showkeys(form)
    ## return
    u = s = ''
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
            enddag = form.getfirst("eindDag", "")
            endmnd = form.getfirst("eindMnd", "")
            endjaar = form.getfirst("eindJaar", "")
            if enddag == '0' or endmnd == '0' or endjaar == '0':
                enddat = ''
            else:
                if len(enddag) == 1:
                    enddag = "0" + enddag
                if len(endmnd) == 1:
                    endmnd = "0" + endmnd
                enddat = endjaar + endmnd + enddag

            h = WijzigAbsentie(sel_id, newstat, reden, komtvan, u, s,
                kwamvan, newdat, enddat)
    print("Content-Type: text/html\n")     # HTML is following
    for x in h.regels:
        print(x)

if __name__ == '__main__':
    main()

