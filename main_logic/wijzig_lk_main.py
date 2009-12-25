# naar het voorbeeld van adres_wijzig_main.py in c:/c van papa/Mijn projecten/adressen

from school_globals import *
from Edex_objects import LKgeg
from Edex_objects import lijstLK

class wijzig_lk_main:
    def __init__(self,id):
        self.ok = False
        self.id = id

    def addArg(self,naam,waarde):
        if naam == "vn":
          self.vn = waarde
        elif naam == "vv":
          self.vv = waarde
        elif naam == "an":
          self.an = waarde

    def doe(self):
        f = ""
        lk = LKgeg(self.id)
        lk.read()
        if not lk.found:
            h = lijstLK()
            id = ("%05i" % (int(h.laatste) + 1))            # bepaal laatste leerkrachtid
            lk = LKgeg(id)
        w = False
        if self.vn != lk.naam.vn:
            lk.setAttr("vn",self.vn)
            w = True
        if self.vv != lk.naam.vv:
            lk.setAttr("vv",self.vv)
            w = True
        if self.an != lk.naam.an:
            lk.setAttr("an",self.an)
            w = True
        if w:
            self.ok = lk.write()
        else:
            self.ok = True

if __name__ == '__main__':
    lk = wijzig_lk_main("0")
    lk.addArg("vn","Willem")
    lk.addArg("vv","van")
    lk.addArg("an","Oranje")
    lk.doe()
    if lk.ok:
        print "gelukt"
    else:
        print "Wijzigen is niet gelukt"
