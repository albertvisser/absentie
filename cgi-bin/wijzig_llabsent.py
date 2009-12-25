import cgi
import school_progpad
from toon_llabs_main import toon_llabs_main
from wijzig_llabs_main import wijzig_llabs_main
from check_login import check_login
from check_login import meld_fout

def main():
    form = cgi.FieldStorage()
    form_ok = False
    #~ print "Content-Type: text/html"     # HTML is following
    #~ print
    #~ print "<html>"
    #~ print "<head></head>"
    #~ print "<body>"
    #~ keys = form.keys()
    #~ keys.sort()
    #~ print
    #~ print "<H3>Form Contents:</H3>"
    #~ if not keys:
        #~ print "<P>No form fields."
    #~ print "<DL>"
    #~ for key in keys:
        #~ print "<DT>" + cgi.escape(key) + ":",
        #~ value = form[key]
        #~ print "<i>" + cgi.escape(`type(value)`) + "</i>"
        #~ print "<DD>" + cgi.escape(`value`)
    #~ print "</DL>"
    #~ print
    #~ print "</body></html>"
    #~ return
    # op basis van de inhoud van de velden tk1 en tk2 de login checken
    # aan de login database
    u = ''
    s = ''
    for k in form.keys():
        if k[:4] == 'wla1':
            u = form[k].value
        elif k[:4] == 'wla2':
            s = form[k].value
    if u != '' and s != '':
        h = check_login(u,s)
        if h.SessionOk:
            form_ok = True
        else:
            m = ("%s, uw login (%s) is klaarblijkelijk verlopen" % (u,s))
    else:
        m = "Geen usernaam en/of sessie-id meegegeven"
    if form_ok:
        if form.has_key("hId"):
            selId = form["hId"].value
        else:
            selId = "0"
        if form.has_key("selStat"):
            newstat = form["selStat"].value
        else:
            newstat = ""
        if form.has_key("txtReden"):
            reden = form["txtReden"].value
        else:
            reden = ""
        if form.has_key("hVan"):
            komtvan = form["hVan"].value
        else:
            komtvan = ""
        if form.has_key("hTerug"):
            kwamvan = form["hTerug"].value
        else:
            kwamvan = ""

        if newstat == "2" and reden == "":
            meld = "Geef een reden op"
            h = toon_llabs_main(u, selId, meld, komtvan, newstat)
        else:
            if form.has_key("selDag"):
                newdag = form["selDag"].value
            else:
                newdag = ""
            if form.has_key("selMnd"):
                newmnd = form["selMnd"].value
            else:
                newmnd = ""
            if form.has_key("selJaar"):
                newjaar = form["selJaar"].value
            else:
                newjaar = ""
            if len(newdag) == 1: newdag = "0" + newdag
            if len(newmnd) == 1: newmnd = "0" + newmnd
            newdat = newjaar + newmnd + newdag
            h = wijzig_llabs_main(selId,newstat,reden,komtvan,u,s,kwamvan,newdat)

        print "Content-Type: text/html"     # HTML is following
        #~ print h.retadr
        print
        for x in h.regels:
            print x
    else:
        h = meld_fout("Er is iets misgegaan",m)
        print "Content-Type: text/html"     # HTML is following
        print
        for x in h.regels:
            print x

if __name__ == '__main__':
    main()

