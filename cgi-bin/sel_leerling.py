import cgi
import school_progpad
from sel_ll_main import sel_ll_main
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
    form_ok = 0
    zoek = ""
    # op basis van de inhoud van de velden tk1 en tk2 de login checken
    # aan de login database
    if form.has_key("sl1") and form.has_key("sl2"):
        u = form["sl1"].value
        s = form["sl2"].value
        h = check_login(u,s)
        if h.SessionOk:
            if form.has_key("txtZoek"):
                form_ok = 1
                zoek = form["txtZoek"].value
                xslevel = h.xslevel
                if form.has_key("hVan"):
                    vandaan = form["hVan"].value
                else:
                    vandaan = "start"
            else:
                m = "Geen zoekstring opgegeven"
        else:
            m = ("%s, uw login (%s) is klaarblijkelijk verlopen" % (u,s))
    else:
        m = "Geen usernaam en/of sessie-id meegegeven"
    if form_ok:
        h = sel_ll_main(zoek,vandaan,u,s,xslevel)
    else:
        h = meld_fout("Er is iets misgegaan",m)
    print "Content-Type: text/html"     # HTML is following
    print
    for x in h.regels:
        print x

if __name__ == '__main__':
    main()

