import sys
import os
sys.path.append("/home/albert/pythoneer/absentie") # waar de eigenlijke programmatuur staat
from user_main import check_login
from common import httppad, cgipad, printkop
wwwroot = '/home/albert/www/'
filepad = wwwroot + 'pythoneer/absentie'
cgifilepad = wwwroot + "cgi-bin/absentie"

def check_session(uid, pwd):
    if uid and pwd:
        ok, access = check_login(uid, pwd)
        if ok:
            m = ''
        else:
            m = ("%s, uw login (%s) is klaarblijkelijk verlopen" % (uid, pwd))
    else:
        access, m = 0, "Geen usernaam ({}) en/of sessie-id ({}) meegegeven".format(
            uid, pwd)
    return access , m

class MeldFout(object):
    """Foutmelding opmaken en printen

    Dit is een class omdat de te printen regels als een attribuut (list)
    moeten worden teruggegeven"""
    def __init__(self, kop, melding, login="N"):
        self.regels = []
        with open(os.path.join(filepad, "next.html")) as f:
            for x in f:
                x = x.rstrip()
                if "%s" in x:
                    if "stylesheet"in x:
                        self.regels.append(x % httppad)
                elif "<!-- kop -->" in x:
                    for y in printkop(kop):                  # gedefinieerd in school_globals
                        self.regels.append(y)
                elif "<!-- data -->" in x:
                    self.regels.append('<br /><div>%s</div>' % melding)
                elif x.startswith("input"):
                    if login == "N":
                        self.regels.append('<input type="button" value="Terug" '
                            'onclick="history.go(-1)"/>')
                    else:
                        hgoto = ("document.location='%sschool_login.py'" % cgipad)
                        self.regels.append('<input type="button" value="Login" '
                            'onclick="%s"/>' % hgoto)
                else:
                    self.regels.append(x)
