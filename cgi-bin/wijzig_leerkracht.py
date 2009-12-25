import cgi
import school_progpad
from wijzig_lk_main import wijzig_lk_main
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
    m = ''
    u = ''
    s = ''
    for k in form.keys():
        if k[:4] == 'wlk1':
            u = form[k].value
        elif k[:4] == 'wlk2':
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
        lk = wijzig_lk_main(form["hId"].value)
    else:
        form_ok = 0
    if form_ok and form.has_key("tvnaam"):
        lk.addArg("vn",form["tvnaam"].value)
    if form_ok:
       if form.has_key("ttus"):
          lk.addArg("vv",form["ttus"].value)
       else:
          lk.addArg("vv","")
    if form_ok and form.has_key("tanaam"):
        lk.addArg("an",form["tanaam"].value)
    if not form_ok:
        if m == '':
            m = "Alle rubrieken moeten worden ingevuld"
        h = meld_fout("Er is iets misgegaan",m)
        print "Content-Type: text/html"     # HTML is following
        print
        for x in h.regels:
            print x
        return
    lk.doe()
    if lk.ok:
        print "Content-Type: text/html"     # HTML is following
        # doorlinken naar selectiescherm
        print ('Location: http://school.pythoneer.nl/cgi-bin/toon_leerkrachten.py?tlk1=%s&tlk2=%s' % (u,s))
        print
    else:
        print "Content-Type: text/html"     # HTML is following
        print
        print "Wijzigen is niet gelukt"

if __name__ == '__main__':
    main()

