from school_globals import *
from Edex_objects import lijstLL
from Edex_objects import lijstGR
from Edex_objects import lijstAbsent

class toon_abs_main:
  def __init__(self,u,xslevel):
    self.regels = []
    sZoek = ""
    abs = lijstAbsent()
    ll = lijstLL()
    gr = lijstGR()
    fh = open(filepad + "toon_absent.html")
    for x in fh.readlines():
        h = x.find("%s")
        if h > -1:
            hs = x.split("%s")
            if x.find("stylesheet") > -1:
                self.regels.append("%s%s%s" % (hs[0],httppad,hs[1]))
            elif x.find("<script") > -1:
                self.regels.append(hs[0])
                f2 = file(filepad + 'check.js')
                for x in f2.readlines():
                    self.regels.append(x[:-1])
                f2.close()
                self.regels.append(hs[1])
            elif x.find("action") > -1:
                self.regels.append("%s%s%s" % (hs[0],cgipad,hs[1]))
            elif x.find("hVan") > -1:
                self.regels.append("%s%s%s" % (hs[0],selId,hs[1]))
            elif x.find("option") > -1:
                for g in groep:
                    self.regels.append("%s%s%s%s%s"% (hs[0],g,hs[1],g,hs[2][:-1]))
        else:
            if x == "<!-- kop -->\n":
                for y in printkop("Lijst absente leerlingen ",u):                  # gedefinieerd in school_globals
                    self.regels.append(y)
            elif x == "    <!-- contents -->\n":
                aantabs = 0
                for y in abs.ll.keys():
                    abstat = abs.ll[y][0]
                    if abstat != "0":
                        aantabs = aantabs + 1
                        absrdn = abs.ll[y][1]
                        absdat = abs.ll[y][2]
                        leerl = ll.ll[y]
                        llnm = leerl[0]
                        llgr = gr.groep[leerl[1]]
                        lknm = llgr.lknm
                        self.regels.append('    <tr>')
                        self.regels.append('     <td valign="top">%s</td>' % llnm.naam)
                        self.regels.append('     <td valign="top">%s</td>' % lknm)
                        if xslevel > 2: # wijzigen niet toegestaan
                            self.regels.append('     <td valign="top">%s</td>' % afwstat[int(abstat)])
                        else:
                            self.regels.append('      <td valign="top">')
                            self.regels.append('      <form id="wla-%s" action="%swijzig_llabsent.py" method="post">' % (y,cgipad))
                            self.regels.append('       <input type="hidden" name="hVan" id="hVan" value="toon_absent" />')
                            self.regels.append('       <input type="hidden" name="hId" id="hId" value="%s" />' % y)
                            self.regels.append('  	  <input type="hidden" name="wla1-%s" id = "wla1-%s"/>' % (y,y))
                            self.regels.append('  	  <input type="hidden" name="wla2-%s" id = "wla2-%s"/>' % (y,y))
                            hh = ("doit_sub('wla-%s','wla1-%s','wla2-%s')" % (y,y,y))
                            self.regels.append('  	  <select name="selStat" id="selStat" onchange="%s" >' % hh)
                            i = 0
                            for z in afwstat:
                                hs = ""
                                if str(i) == abstat: hs = 'selected="selected" '
                                self.regels.append('	    <option %svalue="%i">%s</option>' % (hs,i,z))
                                i = i + 1
                            self.regels.append('	  </select>')
                            self.regels.append('     </form>')
                            #~ if absrdn != '':
                                #~ self.regels.append('     <td valign="top">%s</td>' % absrdn)
                            self.regels.append('     </td>')
                        self.regels.append('     <td valign="top">%s</td>' % absdat[:10])
                        if xslevel > 2: # wijzigen niet toegestaan
                            self.regels.append('     <td valign="top"><input type="button" value="Toon/Wijzig" disabled="disabled"/></td>')
                        else:
                            self.regels.append('      <td valign="top">')
                            self.regels.append('    <form action="%stoon_llabsent.py" method="post">' % cgipad)
                            self.regels.append('       <input type="hidden" name="hVan" id="hVan" value="toon_absent" />')
                            self.regels.append('       <input type="hidden" name="hId" id="hId" value="%s" />' % y)
                            self.regels.append('  	  <input type="hidden" name="tla1-%s" id = "tla1-%s"/>' % (y,y))
                            self.regels.append('  	  <input type="hidden" name="tla2-%s" id = "tla2-%s"/>' % (y,y))
                            hh = ("doit('tla1-%s','tla2-%s')" % (y,y))
                            self.regels.append('        <input type="submit" value="Toon/Wijzig" onclick="%s"/>' % hh)
                            self.regels.append('     </form>')
                            self.regels.append('     </td>')
                        self.regels.append('    </tr>')
                if aantabs == 0:
                    self.regels.append('<tr><td colspan="3">Geen absente leerlingen</td></tr>')
            else:
                self.regels.append(x[:-1])
    fh.close()

if __name__ == '__main__':
    h = toon_abs_main()
    f = file("test.html","w")
    for x in h.regels:
      f.write("%s\n" % x)
    f.close()
