import cgi
import school_progpad
from toon_llabs_main import toon_llabs_main
from check_login import check_login
from check_login import meld_fout

def main():
    form = cgi.FieldStorage()
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
    form_ok = False
    # op basis van de inhoud van de velden tk1 en tk2 de login checken
    # aan de login database
    u = ''
    s = ''
    for k in form.keys():
        if k[:4] == 'tla1':
            u = form[k].value
        elif k[:4] == 'tla2':
            s = form[k].value
    if u != '' and s != '':
        h = check_login(u,s)
        if h.SessionOk:
            form_ok = True
            xslevel = h.xslevel
            if form.has_key("hVan"):
                vandaan = form["hVan"].value
            else:
                vandaan = "start"
        else:
            m = ("%s, uw login (%s) is klaarblijkelijk verlopen" % (u,s))
    else:
        m = "Geen usernaam en/of sessie-id meegegeven"
    if form_ok:
        if form.has_key("hId"):
            selId = form["hId"].value
        else:
            form_ok = 0
        if form.has_key("txtMeld"):
            meld = form["txtMeld"].value
        else:
            meld = ""
    if form_ok:
        h = toon_llabs_main(u, selId, meld, vandaan)
    else:
        h = meld_fout("Er is iets misgegaan",m)
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
    for x in h.regels:
      print x

if __name__ == '__main__':
    main()

