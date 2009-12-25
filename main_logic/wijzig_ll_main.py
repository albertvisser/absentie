# naar het voorbeeld van adres_wijzig_main.py in c:/c van papa/Mijn projecten/adressen

from school_globals import *
from Edex_objects import LLgeg
from Edex_objects import lijstLL

class wijzig_ll_main:
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
        elif naam == "dd":
          self.dd = waarde
        elif naam == "mm":
          self.mm = waarde
        elif naam == "jr":
          self.jr = waarde
        elif naam == "gesl":
          self.gesl = waarde
        elif naam == "aut":
          self.aut = waarde
        elif naam == "grp":
          self.grp = waarde

    def doe(self):
        f = ""
        ll = LLgeg(self.id)
        ll.read()
        if not ll.found:
            h = lijstLL()
            id = ("%05i" % (int(h.laatste) + 1))            # bepaal laatste leerlingid
            ll = LLgeg(id)
        w = False
        if self.vn != ll.naam.vn:
            ll.setAttr("vn",self.vn)
            w = True
        if self.vv != ll.naam.vv:
            ll.setAttr("vv",self.vv)
            w = True
        if self.an != ll.naam.an:
            ll.setAttr("an",self.an)
            w = True
        datum = self.dd + self.mm + self.jr
        datum2 = ll.geboren.getOut("dmj")
        if datum != datum2:
            ll.setAttr("geb",datum)
            w = True
        if self.gesl != ll.gesl:
            ll.setAttr("gesl",self.gesl)
            w = True
        #~ if self.aut != ll.auto:
            #~ ll.setAttr("auto",self.aut)
            #~ w = True
        if self.grp != ll.groep:
            ll.setAttr("groep",self.grp)
            w = True
        if w:
            self.ok = ll.write()
        else:
            self.ok = True

def test():
    ll = wijzig_ll_main("0")
    ll.addArg("vn","Hendrik")
    ll.addArg("vv","de")
    ll.addArg("an","Haan")
    ll.addArg("dd","01")
    ll.addArg("mm","04")
    ll.addArg("jr","2004")
    ll.addArg("gesl","J")
    ll.addArg("aut","0")
    ll.addArg("grp","00083")
    ln = ll.doe()

if __name__ == '__main__':
    test()
