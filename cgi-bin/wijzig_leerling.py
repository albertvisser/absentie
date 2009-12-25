import cgi
import school_progpad
from wijzig_ll_main import wijzig_ll_main
from check_login import check_login
from check_login import meld_fout

def main():
    form = cgi.FieldStorage()
    form_ok = False
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
    u = ''
    s = ''
    for k in form.keys():
        if k[:4] == 'wll1':
            u = form[k].value
        elif k[:4] == 'wll2':
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
        ll = wijzig_ll_main(form["hId"].value)
    else:
        form_ok = 0
    if form_ok and form.has_key("tvnaam"):
        ll.addArg("vn",form["tvnaam"].value)
    if form_ok:
       if form.has_key("ttus"):
          ll.addArg("vv",form["ttus"].value)
       else:
          ll.addArg("vv","")
    if form_ok and form.has_key("tanaam"):
        ll.addArg("an",form["tanaam"].value)
    if form_ok and form.has_key("tdag"):
        ll.addArg("dd",form["tdag"].value)
    if form_ok and form.has_key("tmaand"):
        ll.addArg("mm",form["tmaand"].value)
    if form_ok and form.has_key("tjaar"):
        ll.addArg("jr",form["tjaar"].value)
    if form_ok and form.has_key("selgesl"):
        ll.addArg("gesl",form["selgesl"].value)
    if form_ok and form.has_key("selaut"):
        ll.addArg("aut",form["selaut"].value)
    if form_ok and form.has_key("selgrp"):
        ll.addArg("grp",form["selgrp"].value)
    if not form_ok:
        if m == '':
            m = "Alle rubrieken moeten worden ingevuld"
        h = meld_fout("Er is iets misgegaan",m)
        print "Content-Type: text/html"     # HTML is following
        print
        for x in h.regels:
            print x
        return
    ln = ll.doe()
    if ll.ok:
        print "Content-Type: text/html"     # HTML is following
        # doorlinken naar selectiescherm
        print ('Location: http://school.pythoneer.nl/cgi-bin/toon_leerlingen.py?tll1=%s&tll2=%s' % (u,s))
        print
    else:
        print "Content-Type: text/html"     # HTML is following
        print
        print "Wijzigen is niet gelukt"

if __name__ == '__main__':
    main()

