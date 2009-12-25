import cgi
import school_progpad
from toon_kl_main import toon_kl_main
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
    sZoek = ""
    # op basis van de inhoud van de velden tk1 en tk2 de login checken
    # aan de login database
    if form.has_key("tk1") and form.has_key("tk2"):
        u = form["tk1"].value
        s = form["tk2"].value
        h = check_login(u,s)
        if h.SessionOk:
            if form.has_key("selKlas"):
                form_ok = True
                selId = form["selKlas"].value
                xslevel = h.xslevel
            else:
                m = "Geen klas-id opgegeven"
        else:
            m = ("%s, uw login (%s) is klaarblijkelijk verlopen" % (u,s))
    else:
        m = "Geen usernaam en/of sessie-id meegegeven"
    if form_ok:
        h = toon_kl_main(selId,u,xslevel)
    else:
        h = meld_fout("Er is iets misgegaan",m)
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
    for x in h.regels:
      print x

if __name__ == '__main__':
    main()

