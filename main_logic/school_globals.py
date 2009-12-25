import sys
sys.path.append("f:/pythoneer/absentie/data")
httppad = "http://school.pythoneer.nl/"
cgipad = httppad + "cgi-bin/"
filepad = "F:/www/pythoneer/school/"
afwstat = ["aanwezig","afwezig, reden onbekend","afwezig met reden","ziek","bijzonder verlof"]
gsltab = {"J": "jongen","M": "meisje"}
auttab = {"0": "autochtoon", "1": "niet autochtoon","9":"onbekend"}
grptab = ["1","2","3","4","5","6","7","8","S","H"]
from time import localtime
dag = ["maandag","dinsdag","woensdag","donderdag","vrijdag","zaterdag","zondag"]
maand = ["","januari","februari","maart","april","mei","juni","juli","augustus","september",
           "oktober","november","december",]
xtypes = {'adm': 'Beheer','usr': 'Gewoon'}
# xtypes = {'adm': 'Beheer','usr': 'Gewoon','prt': 'Beperkt','vwr': 'Alleen-lezen'}
btypes = {'J': 'ja','N': 'nee'}
snames = ['start','toon_klas','sel_leerling','toon_absent']

def dattijd():
    h = localtime()
    return ("het is nu %s %i %s %i, %02i:%02i" % (dag[h[6]],h[2],maand[h[1]],h[0],h[3],h[4]))

def printkop(t,u="",vandaan=""): # u is user voor in melding
    l = []
    if u != '':
        u = u + ', '
    f = open(filepad + "kop.html","r")
    for x in f.readlines():
        y = x[:-1]
        if x.find('src="%s') > -1:
            l.append(y % httppad)
        elif x.find("%s") > -1:
            l.append(y % t)
        elif x[:-1] == "<!-- datum/tijd -->":
            #~ l.append(dattijd())
            l.append('<div><span class="half" style="text-align: left"><span class="uname">%s</span>%s</span>' % (u,dattijd()))
            if t != "Login fout" and t != "Login" and t != 'Er is iets misgegaan' and t != 'Uitloggen':
                #~ l.append('<span class="mid" style="text-align: right"><a href="%sschool_start.py">Terug naar beginscherm</a></span>' % cgipad) -- oorspronkelijk
                l.append('<span class="half" style="text-align: right">')
                if t == "Details van leerling":
                    vs = vandaan.split("-")
                    if vs[0] == 'toon_klas':
                        h = "doit('tk1','tk2')"
                        l.append('<form action="%stoon_klas.py" method="post"><input type="hidden" name="tk1" id="tk1" /><input type="hidden" name="tk2" id="tk2" /><input type="hidden" name="selKlas" id="selKlas" value="%s"/><input type="submit" value="Terug naar selectiescherm" onclick="%s" /></form>' % (cgipad,vs[1],h))
                    elif vs[0] == 'sel_leerling':
                        h = "doit('sl1','sl2')"
                        if len(vs) > 2:
                            vann = vs[2]
                            if len(vs) > 3:
                                vann = vann + "-" + vs[3]
                            l.append('<form action="%ssel_leerling.py" method="post"><input type="hidden" name="sl1" id="sl1" /><input type="hidden" name="sl2" id="sl2" /><input type="hidden" name="txtZoek" id="txtZoek" value="%s"/><input type="hidden" name="hVan" id="hVan" value="%s"/><input type="submit" value="Terug naar selectiescherm" onclick="%s" /></form>' % (cgipad,vs[1],vann,h))
                        # nog toevoegen: eerdere herkomst (hVan)
                    elif vs[0] == 'toon_absent':
                        h = "doit('ta1','ta2')"
                        l.append('<form action="%stoon_absent.py" method="post"><input type="hidden" name="ta1" id="ta1" /><input type="hidden" name="ta2" id="ta2" /><input type="submit" value="Terug naar selectiescherm" onclick="%s" /></form>' % (cgipad,h))
                elif t == 'Gezocht op: naam(deel)':
                    vs = vandaan.split("-")
                    if vs[0] == 'toon_klas':
                        h = "doit('tk1','tk2')"
                        l.append('<form action="%stoon_klas.py" method="post"><input type="hidden" name="tk1" id="tk1" /><input type="hidden" name="tk2" id="tk2" /><input type="hidden" name="selKlas" id="selKlas" value="%s"/><input type="submit" value="Terug naar selectiescherm" onclick="%s" /></form>' % (cgipad,vs[1],h))
                if t != "Startscherm":
                    h = "doit('tb1','tb2')"
                    l.append('<form action="%sschool_start.py" method="post"><input type="hidden" name="tb1" id="tb1" /><input type="hidden" name="tb2" id="tb2" /><input type="submit" value="Terug naar beginscherm" onclick="%s" /></form>' % (cgipad,h))
                h = "doit('lu1','lu2')"
                l.append('<form action="%sschool_logout.py" method="post"><input type="hidden" name="lu1" id="lu1" /><input type="hidden" name="lu2" id="lu2" /><input type="submit" value="Log Uit" onclick="%s" /></form>' % (cgipad,h))
                l.append('</span>')
            l.append('</div><br />')
        else:
            l.append(y)
    f.close()
    return l

def test():
    for x in printkop("hallo"):
      print x

if __name__ == '__main__':
	test()
