from school_globals import *
from Edex_objects import LLgeg
from Edex_objects import AbsentHist

class today: # pre-2.3 support
    def __init__(self):
        from time import gmtime
        t = gmtime()
        self.day = t[2]
        self.month = t[1]
        self.year = t[0]

class toon_llabs_main:
  def __init__(self,u,selId,meld,vandaan,selopt=""):
    self.regels = []
    ll = LLgeg(selId)
    #~ from datetime import date
    #~ dmy = date.today()
    dmy = today()
    fh = open(filepad + "toon_leerling.html")
    for x in fh.readlines():
        h = x.find("%s")
        if h > -1:
            xx = x[:-1]
            hs = xx.split("%s")
            if x.find("stylesheet") > -1:
                self.regels.append("%s%s%s" % (hs[0],httppad,hs[1]))
            elif x.find("<script") > -1:
                self.regels.append(hs[0])
                f2 = file(filepad + 'check.js')
                for x in f2.readlines():
                    self.regels.append(x[:-1])
                f2.close()
                self.regels.append(hs[1])
            elif x.find("form action") > -1:
                self.regels.append("%s%s%s" % (hs[0],cgipad,hs[1]))
            elif x.find("Naam") > -1:
                self.regels.append("%s%s%s" % (hs[0],ll.naam.naam,hs[1]))
            elif x.find("hTerug") > -1:
                self.regels.append("%s%s%s" % (hs[0],vandaan,hs[1]))
            elif x.find("option") > -1:
                for s in range(len(afwstat)):
                    sh = ""
                    if selopt != "":
                        if s == int(selopt): sh = 'selected="selected"'
                    else:
                        if s == int(ll.code): sh = 'selected="selected"'
                    self.regels.append('         <option %s value="%i">%s</option>'% (sh,s,afwstat[s]))
            elif x.find("textarea") > -1:
                sh = ll.reden
                self.regels.append("%s%s%s" % (hs[0],sh,hs[1]))
            elif x.find("hId") > -1:
                self.regels.append("%s%s%s" % (hs[0],selId,hs[1]))
            elif x.find("colspan") > -1:
                if meld != "":
                    self.regels.append("%s%s%s" % (hs[0],meld,hs[1]))
        else:
            if x == "<!-- kop -->\n":
                for y in printkop("Details van leerling",u,vandaan):                  # gedefinieerd in school_globals
                  self.regels.append(y)
            elif x.find("selDag") >= 0:
                self.regels.append(x[:-1])
                for i in range(1,32):
                    y = ''
                    if i == dmy.day: y = 'selected="selected"'
                    self.regels.append('         <option value="%i"%s>%2i</option>' % (i,y,i))
            elif x.find("selMnd") >= 0:
                self.regels.append(x[:-1])
                for i in range(1,13):
                    y = ''
                    if i == dmy.month: y = 'selected="selected"'
                    self.regels.append('         <option value="%i"%s>%2i</option>' % (i,y,i))
            elif x.find("selJaar") >= 0:
                self.regels.append(x[:-1])
                for i in range(2004,2007):
                    y = ''
                    if i == dmy.year: y = 'selected="selected"'
                    self.regels.append('         <option value="%i"%s>%2i</option>' % (i,y,i))
            elif x == "<!-- AbsentHist -->\n":
                la = AbsentHist(selId)
                self.regels.append("<br />Geschiedenis:")
                self.regels.append('<table>')
                self.regels.append("<tr><th>datum/tijd</th><th>&nbsp;</th><th>status</th><th>&nbsp;</th><th>evt. reden</th></tr>")
                for x in la.lijst:
                    h1 = afwstat[int(x[1])]
                    if x[2] != "":
                        h2 = x[2]
                    else:
                        h2 = "&nbsp;"
                    self.regels.append('<tr><td>%s</td><td>&nbsp;</td><td>%s</td><td>&nbsp;</td><td>%s</td></tr>' % (x[0],h1,h2))
                self.regels.append("</table>"  )
            else:
                self.regels.append(x[:-1])

if __name__ == '__main__':
    selId = "00198"
    meld = "Hallo"
    h = toon_llabs_main(selId, meld)
    f = file("test.html","w")
    for x in h.regels:
      f.write("%s\n" % x)
    f.close()

