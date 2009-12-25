import cgi
import school_progpad
from wijzig_gr_main import wijzig_gr_main
from Edex_objects import GRgeg
from check_login import check_login
from check_login import meld_fout

def main():
    form = cgi.FieldStorage()
    #~ print "Content-Type: text/html"     # HTML is following
    #~ print                               # blank line, end of headers
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
    u = ''
    s = ''
    for k in form.keys():
        if k[:4] == 'wgr1':
            u = form[k].value
        elif k[:4] == 'wgr2':
            s = form[k].value
    if u != '' and s != '':
        h = check_login(u,s)
        if h.SessionOk:
            form_ok = True
        else:
            m = ("%s, uw login (%s) is klaarblijkelijk verlopen" % (u,s))
    else:
        m = "Geen usernaam en/of sessie-id meegegeven"

    if form_ok and form.has_key("hId"):
        id = form["hId"].value
    else:
        form_ok = 0
    if form_ok and form.has_key("tnaam"):
        nm = form["tnaam"].value
    if form_ok and form.has_key("selJR"):
        jr = form["selJR"].value
    if form_ok and form.has_key("selLK"):
        lk = form["selLK"].value
    if not form_ok:
        if m == '':
            m = "Alle rubrieken moeten worden ingevuld"
        h = meld_fout("Er is iets misgegaan",m)
        print "Content-Type: text/html"     # HTML is following
        print
        for x in h.regels:
            print x
        return
    ln = wijzig_gr_main(id,nm,jr,lk)
    if ln.ok:
        print "Content-Type: text/html"     # HTML is following
        # doorlinken naar selectiescherm
        print ('Location: http://school.pythoneer.nl/cgi-bin/toon_groepen.py?tgr1=%s&tgr2=%s' % (u,s))
        print
    else:
        print "Content-Type: text/html"     # HTML is following
        print
        print "Wijzigen is niet gelukt"

if __name__ == '__main__':
    main()

