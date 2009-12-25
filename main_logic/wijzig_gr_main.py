# naar het voorbeeld van adres_wijzig_main.py in c:/c van papa/Mijn projecten/adressen

from school_globals import *
from Edex_objects import lijstGR
from Edex_objects import GRgeg

class wijzig_gr_main:
    def __init__(self,id,nm,jr,lk):
        # hA is een GRgeg object
        self.ok = False
        f = ""
        gr = GRgeg(id)
        gr.read()
        if not gr.found:
            h = lijstGR()
            id = ("%05i" % (int(h.laatste) + 1))        # bepaal laatste groepsid
            gr = GRgeg(id)
        w = False
        if nm != gr.naam:
            gr.setAttr("naam",nm)
            w = True
        if jr != gr.jaar:
            gr.setAttr("jaar",jr)
            w = True
        if lk != gr.lkid:
            gr.setAttr("leerkracht",lk)
            w = True
        if w:
            self.ok = gr.write()
        else:
            self.ok = True

if __name__ == '__main__':
    id = "00048"
    nm = "Ahum"
    jr = "2"
    lk = "00014"
    h = wijzig_gr_main(id,nm,jr,lk)
    print h.ok
