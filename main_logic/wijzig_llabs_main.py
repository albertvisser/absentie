from school_globals import *
from Edex_objects import LLgeg
from time import localtime

class wijzig_llabs_main:
  def __init__(self,selId,newstat,reden,komtvan,u,s,kwamvan,newdat=""):
    f = ""
    if selId == "0":
      f = "U moet wel een sleutelwaarde opgeven"
    elif newstat == "":
      f = "U moet wel een status opgeven"
    elif reden == "" and newstat == "2":
      f = "U moet wel een reden opgeven"

    selVan = ''
    if komtvan != "":
        h = komtvan.split("-")
        if len(h) > 0:
            komtvan = h[0]
            if len(h) > 1:
                selKlas = h[1]
                if len(h) > 2:
                    kwamvan = h[2]
                    if len(h) > 3:
                        selVan = h[3]
    else:
        komtvan = "toon_leerling"
    if kwamvan != "":
        h = kwamvan.split("-")
        if len(h) > 1:
            selVan = h[1]
    else:
        kwamvan = "toon_leerling"
    if selVan != '':
        kwamvan = kwamvan + '.' + selVan

    if f == "":
        ll = LLgeg(selId)
        h = localtime()
        if newdat != "":
            dt = ("%s-%s-%s;%02i:%02i:%02i"  % (newdat[6:],newdat[4:6],newdat[:4],h[3],h[4],h[5]))
        else:
            dt = ("%02i-%02i-%02i;%02i:%02i:%02i"  % (h[2],h[1],h[0],h[3],h[4],h[5]))
        ll.update(newstat,reden,dt)
        self.m = "OK"
    else:
        self.m = f

    self.regels = []
    hh = "'fThis'"
    self.regels.append('<html><head></head><body onload="document.getElementById(%s).submit()">' % hh)
    #~ self.regels.append('<form id="fThis" action="%s%s.py" method="post">' % (cgipad,'hallo'))
    self.regels.append('<form id="fThis" action="%s%s.py" method="post">' % (cgipad,komtvan))
    if komtvan == "toon_llabsent":
        #~ self.retadr = ('Location: %s%s.py?hId=%s&txtMeld=%s&tla1=%s&tla2=%s' % (cgipad,komtvan,selId,self.m,u,s))
        self.regels.append('<input type="hidden" id="hId" name="hId" value="%s"></input>' % selId)
        self.regels.append('<input type="hidden" id="txtMeld" name="txtMeld" value="%s"></input>' % self.m)
        self.regels.append('<input type="hidden" id="hVan" name="hVan" value="%s"></input>' % kwamvan)
        self.regels.append('<input type="hidden" id="tla1" name="tla1" value="%s"></input>' % u)
        self.regels.append('<input type="hidden" id="tla2" name="tla2" value="%s"></input>' % s)
    elif komtvan == "toon_klas":
        #~ self.retadr = ('Location: %s%s.py?selKlas=%s&tk1=%s&tk2=%s' % (cgipad,komtvan,selKlas,u,s))
        self.regels.append('<input type="hidden" id="selKlas" name="selKlas" value="%s"></input>' % selKlas)
        self.regels.append('<input type="hidden" id="tk1" name="tk1" value="%s"></input>' % u)
        self.regels.append('<input type="hidden" id="tk2" name="tk2" value="%s"></input>' % s)
    elif komtvan == "toon_absent":
        #~ self.retadr = ('Location: %s%s.py?ta1=%s&ta2=%s' % (cgipad,komtvan,u,s))
        self.regels.append('<input type="hidden" id="ta1" name="ta1" value="%s"></input>' % u)
        self.regels.append('<input type="hidden" id="ta2" name="ta2" value="%s"></input>' % s)
    elif komtvan == "sel_leerling":
        #~ self.retadr = ('Location: %s%s.py?txtZoek=%s&sl1=%s&sl2=%s' % (cgipad,komtvan,selKlas,u,s))
        self.regels.append('<input type="hidden" id="hVan" name="hVan" value="%s"></input>' % kwamvan)
        self.regels.append('<input type="hidden" id="txtZoek" name="txtZoek" value="%s"></input>' % selKlas)
        self.regels.append('<input type="hidden" id="sl1" name="sl1" value="%s"></input>' % u)
        self.regels.append('<input type="hidden" id="sl2" name="sl2" value="%s"></input>' % s)
    self.regels.append('</form></body></html>')

if __name__ == '__main__':
    h = wijzig_llabs_main("00003",'2','x','toon_klas-00005','leerkracht','begin')
    print h.m
    for x in h.regels:
        print x


