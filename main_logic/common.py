import os
import sys
from time import localtime
filepad = '../html' # was '/home/albert/www/lemoncurry/absentie' # waar de html staat
## sys.path.append(os.path.join(os.path.dirname(__file__), "data"))
sys.path.append("../dml")
httppad = "http://absentie.lemoncurry.nl/"
cgipad = httppad + "cgi-bin/"
afwstat = ["aanwezig", "afwezig,  reden onbekend", "afwezig met reden", "ziek",
    "bijzonder verlof"]
gsltab = {"J": "jongen", "M": "meisje"}
auttab = {"0": "autochtoon", "1": "niet autochtoon", "9":"onbekend"}
grptab = ["1", "2", "3", "4", "5", "6", "7", "8", "S", "H"]
dag = ["maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag"]
maand = ["", "januari", "februari", "maart", "april", "mei", "juni", "juli",
    "augustus", "september", "oktober", "november", "december",]
xtypes = {'adm': 'Beheer', 'usr': 'Gewoon'}
# xtypes = {'adm': 'Beheer','usr': 'Gewoon','prt': 'Beperkt','vwr': 'Alleen-lezen'}
btypes = {'J': 'ja', 'N': 'nee'}
start_names = ['start', 'toon_klas', 'sel_leerling', 'toon_absent']
logoutteksten = ("Login fout", "Login", 'Er is iets misgegaan', 'Uitloggen')
script, endscript = '  <script type="text/javascript">', '</script>'

def dattijd():
    h = localtime()
    return ("het is nu %s %i %s %i, %02i:%02i" % (dag[h[6]], h[2], maand[h[1]],
        h[0], h[3], h[4]))

def get_script():
    regels= [script]
    with open(os.path.join(filepad, 'check.js')) as f2:
        regels.extend([x.rstrip() for x in f2])
    regels.append(endscript)
    return regels

halfspantext = '<span class="half" style="text-align: {}">'
klasformtext = """\
<form action="%stoon_klas.py" method="post">
 <input type="hidden" name="tk1" id="tk1" />
 <input type="hidden" name="tk2" id="tk2" />
 <input type="hidden" name="selKlas" id="selKlas" value="%s"/>
 <input type="submit" value="Terug naar selectiescherm" onclick="%s" />
</form>"""
selformtext = """\
<form action="%ssel_leerling.py" method="post">
 <input type="hidden" name="sl1" id="sl1" />
 <input type="hidden" name="sl2" id="sl2" />
 <input type="hidden" name="txtZoek" id="txtZoek" value="%s"/>
 <input type="hidden" name="hVan" id="hVan" value="%s"/>
 <input type="submit" value="Terug naar selectiescherm" onclick="%s" />
</form>"""
absentformtext = """\
<form action="%stoon_absent.py" method="post">
 <input type="hidden" name="ta1" id="ta1" />
 <input type="hidden" name="ta2" id="ta2" />
 <input type="submit" value="Terug naar selectiescherm" onclick="%s" />
</form>"""
startformtext = """\
<form action="%sschool_start.py" method="post">
 <input type="hidden" name="tb1" id="tb1" />
 <input type="hidden" name="tb2" id="tb2" />
 <input type="submit" value="Terug naar beginscherm" onclick="%s" />
</form>"""
logoutformtext = """\
<form action="%sschool_logout.py" method="post">
 <input type="hidden" name="lu1" id="lu1" />
 <input type="hidden" name="lu2" id="lu2" />
 <input type="submit" value="Log Uit" onclick="%s" />
</form>"""

def printkop(t, u="", vandaan=""): # u is user voor in melding
    l = []
    if u != '':
        u = u + ', '
    with open(os.path.join(filepad, "kop.html")) as f:
        for x in f:
            y = x.rstrip()
            if 'src="%s' in y:
                l.append(y % httppad)
            elif "%s" in y:
                l.append(y % t)
            elif "<!-- datum/tijd -->" in y:
                #~ l.append(dattijd())
                l.append('<div>%s<span class="uname">%s</span>%s</span>' % (
                    halfspantext.format('left'), u, dattijd()))
                if t not in logoutteksten:
                    #~ l.append('<span class="mid" style="text-align: right"><a href="%sschool_start.py">Terug naar beginscherm</a></span>' % cgipad) -- oorspronkelijk
                    l.append(halfspantext.format('right'))
                    if t == "Details van leerling":
                        vs = vandaan.split("-")
                        if vs[0] == 'toon_klas':
                            h = "doit('tk1','tk2')"
                            l.append(klasformtext % (cgipad, vs[1], h))
                        elif vs[0] == 'sel_leerling':
                            h = "doit('sl1','sl2')"
                            if len(vs) > 2:
                                vann = vs[2]
                                if len(vs) > 3:
                                    vann = vann + "-" + vs[3]
                                l.append(selformtext % (cgipad, vs[1], vann, h))
                            # nog toevoegen: eerdere herkomst (hVan)
                        elif vs[0] == 'toon_absent':
                            h = "doit('ta1','ta2')"
                            l.append(absentformtext % (cgipad, h))
                    elif t.startswith('Gezocht op: naam(deel)'):
                        vs = vandaan.split("-")
                        if vs[0] == 'toon_klas':
                            h = "doit('tk1','tk2')"
                            l.append(klasformtext % (cgipad, vs[1], h))
                        elif vs[0] == 'toon_absent':
                            h = "doit('ta1','ta2')"
                            l.append(absentformtext % (cgipad, h))
                    if t != "Startscherm":
                        h = "doit('tb1','tb2')"
                        l.append(startformtext % (cgipad, h))
                    h = "doit('lu1','lu2')"
                    l.append(logoutformtext % (cgipad, h))
                    l.append('</span>')
                l.append('</div><br />')
            else:
                l.append(y)
    return l
