import os
import common
from Edex_objects import leerlingenlijst, absentenlijst

row, endrow = '    <tr>', '    </tr>'
col, endcol = '<td valign="top">', '</td>'
coltext = '     {}%s{}'.format(col, endcol)
form_wijzig = '      <form id="wla-%s" action="%swijzig_llabsent.py" method="post">'
form_toon = '    <form action="%stoon_llabsent.py" method="post">'
hidden_inputs = """\
       <input type="hidden" name="hVan" id="hVan" value="toon_klas-{0}" />
       <input type="hidden" name="hId" id="hId" value="{1}" />
       <input type="hidden" name="{2}la1-{1}" id = "{2}la1-{1}"/>
       <input type="hidden" name="{2}la2-{1}" id = "{2}la2-{1}"/>
"""
select = '  	  <select name="selStat" id="selStat" onchange="%s" >'
optiontext = '	    <option %svalue="%i">%s</option>'
selected_text = 'selected="selected" '
endselect = '	  </select>'
endform = '     </form>'
submit_button = '        <input type="submit" value="Details" onclick="%s"/>'
button_disabled = '<input type="button" value="Details" disabled="disabled"/>'
notfound ='<tr><td colspan="3">Geen leerlingen gevonden bij %s</td></tr>'

class ToonKlas:
  def __init__(self, sel_id, u, xslevel):
    self.regels = []
    klas, _, leerk = leerlingenlijst(leerkracht=sel_id) # of juist groep=sel_id?
    abs = absentenlijst()
    with open(os.path.join(common.filepad, "toon_klas.html")) as fh:
        for x in fh:
            x = x.rstrip()
            if "%s" in x:
                if "stylesheet" in x:
                    self.regels.append(x % (common.httppad))
                elif "<script" in x:
                    self.regels.extend(common.get_script())
                elif "action" in x:
                    self.regels.append(x % common.cgipad)
                elif "hVan" in x:
                    self.regels.append(x % ('toon_klas-' + str(sel_id)))
                elif 'chkAbs' in x:
                    self.regels.append(x)
                elif "option" in x:
                    for g in groep:
                        self.regels.append(x % (g, g))
            elif "<!-- kop -->" in x:
                self.regels.extend(common.printkop("Gezocht op: groep van %s" % u, u))
            elif "<!-- contents -->" in x:
                lknm = leerk.naam.voornaam     # voornaam van de leerkracht bij de gevraagde klas/groep
                for key, data in klas.items():
                    leerl = data[0]
                    self.regels.append(row)
                    self.regels.append(coltext % leerl)
                    self.regels.append(coltext % lknm)
                    if key in abs:
                        h = int(abs[key][0])
                        absdat = abs[key][2]
                        hh = absdat[:10]
                    else:
                        h = 0
                        absdat = hh = "&nbsp;"
                    if xslevel > 2: # wijzigen niet toegestaan
                        self.regels.append(coltext % common.afwstat[h])
                    else:
                        self.regels.append(col)
                        self.regels.append(form_wijzig % (key, common.cgipad))
                        self.regels.append(hidden_inputs.format(sel_id, key, "w"))
                        hh = "doit_sub('wla-{0}','wla1-{0}','wla2-{0}')".format(key)
                        self.regels.append(select % hh)
                        for ix, z in enumerate(common.afwstat):
                            hs = selected_text if ix == h else ''
                            self.regels.append(optiontext % (hs, ix, z))
                        self.regels.append(endselect)
                        self.regels.append(endform)
                        self.regels.append(endcol)
                    self.regels.append(coltext % absdat)
                    if xslevel > 2: # wijzigen niet toegestaan
                        self.regels.append(coltext % button_disabled)
                    else:
                        self.regels.append(col)
                        self.regels.append(form_toon % common.cgipad)
                        ## self.regels.append(vanregel % sel_id)
                        self.regels.append(hidden_inputs.format(sel_id, key, "t"))
                        hh = "doit('tla1-{0}','tla2-{0}')".format(key)
                        self.regels.append(submit_button % hh)
                        self.regels.append(endform)
                        self.regels.append(endcol)
                    self.regels.append(endrow)
                if len(klas) == 0:
                    self.regels.append(notfound % lknm)
            else:
                self.regels.append(x)
