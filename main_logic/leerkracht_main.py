#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import common
from Edex_objects import Leerkracht, leerkrachtenlijst, groepenlijst

row, endrow = '    <tr>', '    </tr>'
col, endcol = '      <td valign="top">', '</td>'
coltext = '{}%s{}'.format(col, endcol)
button_disabled = '<input type="button"  disabled="disabled" value="Wijzigen" >'
button = '<input type="{}" value="{}" onclick="{}">'
header = """\
      <td><a name="wijzigdeze"></a>Voornaam / tussenvoegsel / achternaam:</td>
      <td>Groepen:</td>
      <td>&nbsp;</td>
"""
form, endform = '    <form action="%s%s" method="post">', '    </form>'
select, endselect = '        <select name="{0}" id="{0}">', '        </select>'
selected_text = ' selected="selected"'
option = '          <option%s value="%s">%s</option>'
input_text = '        <input type="{0}" name="{1}" id="{1}" value="{2}"/>'

class ToonLeerkracht(object):
    def __init__(self, xslevel, u, s, edit_entry=False, sel_id="0"):
        self.regels = []
        self.xslevel = xslevel
        self.leerkrachten = leerkrachtenlijst()[0]
        self.toon_prog = "toon_leerkrachten.py"
        self.wijzig_prog = "wijzig_leerkracht.py"
        with open(os.path.join(common.filepad, "leerkrachten.html")) as fh:
            for x in fh.readlines():
                x = x.rstrip()
                if "%s" in x:
                    if "stylesheet" in x:
                        self.regels.append(x % common.httppad)
                    elif "<script" in x:
                        self.regels.extend(common.get_script())
                    elif 'action=' in x:
                        if not edit_entry:
                            self.regels.append(x % common.cgipad)
                    elif 'input type="submit"' in x:
                        self.regels.append(x % "doit_edit('tlk1','tlk2','0')")
                else:
                    if x == "<body>" and edit_entry:
                        hh = "window.location='#wijzigdeze'"
                        self.regels.append('<body onload="%s">' % hh)
                    elif x == "<!-- kop -->":
                        self.regels.extend(common.printkop("Lijst leerkrachten",u))
                    elif x == "<!-- contents -->":
                        if edit_entry and sel_id == "0":
                            self.wijzigregel("0", u, s)
                        for y in self.leerkrachten:
                            if edit_entry and y[1] == sel_id:
                                self.wijzigregel(y, u, s)
                            else:
                                self.toonregel(y, edit_entry)
                    elif edit_entry and x == "</form>":
                        pass
                    else:
                        self.regels.append(x)

#~ lijstLK.lk: [lknm,lkid]
#~ LKgeg.id
        #~ .naam.vn
                #~ .vv
                #~ .an
                #~ .naam
        #~ .groep: [id,id,id]
        #~ .grpnm: [naam,naam,naam]

    def toonregel(self, x, edit_entry):
        y = Leerkracht(x[1])
        self.regels.append(row)
        self.regels.append(coltext % str(y.naam))
        if len(y.groep) == 0:
            s = "&nbsp;"
        else:
            s = ", ".join(sorted(y.groep.values()))
        self.regels.append(coltext % s)
        if self.xslevel > 2 or edit_entry: # wijzigen niet toegestaan
            hh = button_disabled
        else:
            hh = "doit_edit('tlk1','tlk2','%s')" % y.id
            hh = button.format('submit', 'Wijzigen', hh)
        self.regels.append(coltext % hh)
        self.regels.append(endrow)

    def wijzigregel(self, x, un, si):
        lg = groepenlijst()
        if x == "0":
            vn = ""
            vv = ""
            an = ""
            gl = []
        else:
            y = Leerkracht(x[1])
            vn = y.naam.voornaam
            vv = y.naam.voorvoegsel
            an = y.naam.achternaam
            gl = y.groep
        self.regels.append(row)
        self.regels.append(header)
        self.regels.append(endrow)
        self.regels.append(row)
        self.regels.append(form % (common.cgipad, self.wijzig_prog))
        self.regels.append(col)
        self.regels.append(input_text.format('text', 'tvnaam', vn))
        self.regels.append(input_text.format('text" size="5', 'ttus', vv))
        self.regels.append(input_text.format('text', 'tanaam', an))
        self.regels.append(endcol)
        if x == "0" or len(y.groep) == 0:
            s = "&nbsp;"
        else:
            s = ", ".join(sorted(y.groep.values()))
        self.regels.append(coltext % s)
        self.regels.append(col)
        self.regels.append(input_text.format('hidden', 'hId', x))
        self.regels.append(input_text.format('hidden', 'wlk1', un))
        self.regels.append(input_text.format('hidden', 'wlk2', si))
        hh = "doit_naam('tvnaam','tanaam','wlk1','wlk2');return doit_retval"
        self.regels.append(button.format('submit', 'OK', hh))
        self.regels.append(button.format('button', 'Cancel',
            'javascript:history.go(-1)'))
        self.regels.append(endcol)
        self.regels.append(endform)
        self.regels.append(endrow)

def wijzig_leerkracht(id_ , vn='', vv='', an=''):
    wijzigen = ok = False
    lk = Leerkracht(id_)
    lk.read()
    if not lk.found:
        id_ = ("%05i" % (int(leerkrachtenlijst()[1]) + 1))
        lk = LKgeg(id_)
    if vn != lk.naam.vn:
        lk.set_attr("vn", vn)
        wijzigen = True
    if vv != lk.naam.vv:
        lk.set_attr("vv", vv)
        wijzigen = True
    if an != lk.naam.an:
        lk.set_attr("an", an)
        wijzigen = True
    if wijzigen:
        ok = lk.write()
    else:
        ok = True
    return True
