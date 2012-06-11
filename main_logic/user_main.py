#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import common
from school_user import userlijst, User

row, endrow = '    <tr>', '    </tr>'
col, endcol = '      <td valign="top">', '</td>'
coltext = '{}%s{}'.format(col, endcol)
disabled_button = '<input type="button"  disabled="disabled" value="Wijzigen" >'
button = '<input type="%s" value="%s" onclick="%s">'
header = """\
      <th><a name="wijzigdeze"></a>Gebruikersnaam:</th>
      <th>Toegangstype:</th>
      <th>Eerste scherm:</th>
      <th>Zoekargument:</th>
      <th>Geblokkeerd:</th>
      <th>&nbsp;</th>
      <th>&nbsp;</th>
"""
form, endform = '    <form action="%s%s" method="post">', '    </form>'
select, endselect = '        <select name="{0}" id="{0}">', '        </select>'
selected_text = ' selected="selected"'
option = '          <option%s value="%s">%s</option>'
input_text = '        <input type="{0}" name="{1}" id="{1}" value="{2}"/>'
toelichting = '        Voor een nieuwe gebruiker wordt automatisch ' \
                'een standaard wachtwoord opgevoerd'

def check_login(usernaam, sessionid):
    h = User(usernaam, sessionid, True)
    return h.session_ok, h.get_level()

class ToonUser(object):
    def __init__(self, access_level, u, s, edit_entry=False, sel_id="0"):
        self.regels = []
        self.access_level = access_level
        self.toon_prog = "toon_users.py"
        self.wijzig_prog = "wijzig_user.py"
        with open(os.path.join(common.filepad, "users.html")) as fh:
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
                        self.regels.append(x % "doit_edit('tu1','tu2','0')")
                else:
                    if x == "<body>" and edit_entry:
                        hh = "window.location='#wijzigdeze'"
                        self.regels.append('<body onload="%s">' % hh)
                    elif x == "<!-- kop -->":
                        self.regels.extend(common.printkop("Lijst gebruikers", u))
                    elif x == "<!-- contents -->":
                        if edit_entry and sel_id == "0":
                            x = ('', '', common.xtypes.keys()[1],
                                common.btypes.keys()[1], snames[0])
                            self.wijzigregel("0", u, s)
                        for y in userlijst():
                            if edit_entry and y[0] == sel_id:
                                self.wijzigregel(y, u, s)
                            else:
                                self.toonregel(y, edit_entry)
                    elif edit_entry and x == "</form>":
                        pass
                    else:
                        self.regels.append(x)

    def toonregel(self,x,edit_entry):
        self.regels.append(row)
        self.regels.append(coltext % x[0])
        self.regels.append(coltext % common.xtypes[x[2]])
        h = snames[0] if x[4].startswith(':') else x[4].split(':')
        self.regels.append(coltext % h[0])
        hh = h[1] if len(h) > 1 else '&nbsp;'
        self.regels.append(coltext % hh)
        self.regels.append(coltext % common.btypes[x[3]])
        h = x[1] if x[1] != '' else '&nbsp;'
        self.regels.append(coltext % h)
        if self.access_level > 2 or edit_entry: # wijzigen niet toegestaan
            hh = disabled_button
        else:
            hh = ("doit_edit('tu1','tu2','%s')" % x[0])
            hh = button % ('submit', 'Wijzigen', hh)
        self.regels.append(coltext % hh)
        self.regels.append(endrow)

    def wijzigregel(self, x, un, so):
        newuser = False if x != "" else True
        #-- het navolgende stukje is leuk als je een lijst langer dan een scherm hebt
        self.regels.append(row)
        self.regels.append(header)
        self.regels.append(endrow)
        self.regels.append(row)
        self.regels.append(form % (common.cgipad,self.wijzig_prog))
        self.regels.append(col)
        self.regels.append(input_text.format('text', 'tNaam', x[0]))
        self.regels.append(endcol)
        self.regels.append(col)
        self.regels.append(select.format('sType'))
        for i in common.xtypes.keys():
            si = selected_text if i == x[2] else ''
            self.regels.append(option % (si, i, common.xtypes[i]))
        self.regels.append(endselect)
        self.regels.append(endcol)
        h = x[4].split(':')
        self.regels.append(col)
        self.regels.append(select.format('sStart'))
        if h[0] == '':
            h[0] = common.start_names[0]
        for i in range(4):
            si = selected_text if common.start_names[i] == h[0] else ''
            self.regels.append(option % (si, common.start_names[i],
                common.start_names[i]))
        self.regels.append(endselect)
        self.regels.append(endcol)
        self.regels.append(col)
        hh = h[1] if len(h) > 1 else ''
        self.regels.append(input_text.format('text', 'tMet', hh))
        self.regels.append(endcol)
        self.regels.append(col)
        self.regels.append(select.format('sBlok'))
        for i in common.btypes.keys():
            si = selected_text if i == x[3] else ''
            self.regels.append(option % (si, i, common.btypes[i]))
        self.regels.append(endselect)
        self.regels.append(endcol)
        self.regels.append(col)
        if newuser:
            self.regels.append(input_text.format('hidden', 'hPw', '0'))
            self.regels.append(toelichting)
        else:
            self.regels.append(input_text.format('hidden', 'hPw', 'N'))
            self.regels.append('        ' + button % ('submit', "wachtwoord wijzigen",
                "doit_wpw('wu1','wu2','J')"))
        self.regels.append(endcol)
        self.regels.append(col)
        self.regels.append(input_text.format('hidden', 'hVan', 'toon_users'))
        self.regels.append(input_text.format('hidden', 'wu1', un))
        self.regels.append(input_text.format('hidden', 'wu2', so))
        self.regels.append('        ' + button % ('submit', "OK", "doit_woord("
            "'tNaam','Gebruikersnaam','wu1','wu2');return document.doit_retval"))
        self.regels.append('        ' + button % ('button', 'Cancel',
            'javascript:history.go(-1)'))
        self.regels.append(endcol)
        self.regels.append(endform)
        self.regels.append(endrow)

def wijzig_user(id_, nieuw=False, utype=None, blocked= None, start=None, arg=None):
    ok = False
    meld = ''
    if start is not None:
        try:
            start, arg = start.split(':')
        except valueError:
            pass
    ok = False
    u = User(id_)
    u.read()
    if nieuw:
        if u.found:
            ok = False
            meld = "user bestaat al"
        else:
            ok = true
            u.setPass('begin') # user wordt hierbij initieel opgevoerd
            meld = 'user is opgevoerd'
    else:
        if not u.found:
            ok = False
            meld = "user bestaat niet"
        else:
            wijzig = False
            if utype is not None and utype != u.utype:
                u.utype = utype
                wijzig = True
            if blocked is not None and blocked != u.blocked:
                u.blocked = blocked
                wijzig = True
            if start is not None and start != u.start:
                u.start = start
                wijzig = True
            if wijzig:
                u.write()
            meld = 'user is aangepast'
            ok = True
    return ok, meld

class VraagPassword(object): # opbouwen scherm om wachtwoord te wijzigen
    def __init__(self, uid, van):
        self.regels = []
        with open(os.path.join(common.filepad, "newpw.html")) as fh:
            for x in fh:
                if "%s" in x:
                    x = x.rstrip()
                    if "stylesheet"in x:
                        self.regels.append(x % common.httppad)
                    elif "<script"in x:
                        self.regels.extend(common.get_script())
                    elif 'action='in x:
                        self.regels.append(x % common.cgipad)
                    elif 'id="tNaam"'in x:
                        self.regels.append(x % uid)
                    elif 'id="hVan"'in x:
                        self.regels.append(x % van)
                    elif 'input type="submit"' in x:
                        self.regels.append(x % "doit('wu1','wu2','0')")
                else:
                    if "<!-- kop -->" in x:
                        self.regels.extend(common.printkop("Wachtwoord wijzigen"))
                    #~ elif x[:-1] == "<body>" and editEntry:
                        #~ hh = "window.location='#wijzigdeze'"
                        #~ self.regels.append('<body onload="%s">' % hh)
                    else:
                        self.regels.append(x)

def wijzig_password(self, uid, oldpw, newpw):
    # maak user
    u = User(uid,oldpw)
    if u.paswdok:
        # wijzig wachtwoord
        u.set_pass(newpw)
    # klaar
    self.ok = u.paswdok
