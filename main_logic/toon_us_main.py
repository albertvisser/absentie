# naar het voorbeeld van adres_select_main.py in c:/c van papa/Mijn projecten/adressen

from school_globals import *
from school_user import UserLijst
from school_user import User

class toon_us_main:
    def __init__(self,xslevel,u,s,editEntry=False,selId="0"):
        self.regels = []
        self.xslevel = xslevel
        self.ul = UserLijst()
        self.tprog = "toon_users.py"
        self.wprog = "wijzig_user.py"
        fh = open(filepad + "users.html")
        for x in fh.readlines():
            h = x.find("%s")
            if h > -1:
                hs = x[:-1].split("%s")
                if x.find("stylesheet") > -1:
                    self.regels.append(httppad.join(hs))
                elif x.find("<script") > -1:
                    self.regels.append(hs[0])
                    f2 = file(filepad + 'check.js')
                    for x in f2.readlines():
                        self.regels.append(x[:-1])
                    f2.close()
                    self.regels.append(hs[1])
                elif x.find('action=') > -1:
                    if not editEntry:
                        self.regels.append(cgipad.join(hs))
                elif x.find('input type="submit"') > -1:
                    hh = "doit_edit('tu1','tu2','0')"
                    self.regels.append(hh.join(hs))
            else:
                if x[:-1] == "<body>" and editEntry:
                    hh = "window.location='#wijzigdeze'"
                    self.regels.append('<body onload="%s">' % hh)
                elif x[:-1] == "<!-- kop -->":
                    for y in printkop("Lijst gebruikers",u):                  # gedefinieerd in school_globals
                        self.regels.append(y)
                elif x[:-1] == "<!-- contents -->":
                    if editEntry and selId == "0":
                        self.wijzigregel("0",u,s)
                    h = self.ul.Items
                    for y in h:
                        if editEntry:
                            if y[0] == selId:
                                self.wijzigregel(y,u,s)
                            else:
                                self.toonregel(y,True)
                        else:
                            self.toonregel(y,False)
                elif editEntry and x[:-1] == "</form>":
                    pass
                else:
                    self.regels.append(x[:-1])
        fh.close()

      #~ <th width="30%">Naam</th>          x[0]
      #~ <th width="10%">Accesstype</th>    x[2]
      #~ <th width="10%">Geblokkeerd</th>   x[3]
      #~ <th width="20%">Ingelogd</th>      x[1]
      #~ <th width="10%"><input type="submit" value="Nieuw" onclick="%s"></th>

    def toonregel(self,x,editEntry):
        self.regels.append('    <tr>')
        self.regels.append('      <td valign="top">%s</td>' % x[0])
        self.regels.append('      <td valign="top">%s</td>' % xtypes[x[2]])
        h = x[4].split(':')
        if h[0] == '': h[0] = snames[0]
        self.regels.append('      <td valign="top">%s</td>' % h[0])
        hh = '&nbsp;'
        if len(h) > 1: hh = h[1]
        self.regels.append('      <td valign="top">%s</td>' % hh)
        self.regels.append('      <td valign="top">%s</td>' % btypes[x[3]])
        h = x[1]
        if h == '': h = '&nbsp;'
        self.regels.append('      <td valign="top">%s</td>' % h)
        if self.xslevel > 2 or editEntry: # wijzigen niet toegestaan
            self.regels.append('      <td valign="top"><input type="button"  disabled="disabled" value="Wijzigen" >')
        else:
            hh = ("doit_edit('tu1','tu2','%s')" % x[0])
            self.regels.append('      <td valign="top"><input type="submit" value="Wijzigen" onclick="%s">' % hh)
        self.regels.append('    </tr>')

    def wijzigregel(self,x,un,so):
        newuser = False
        if x == "0":
            x = ['','',xtypes.keys()[1],btypes.keys()[1],snames[0]]
            newuser = True
        #-- het navolgende stukje is leuk als je een lijst langer dan een scherm hebt
        self.regels.append('    <tr>')
        self.regels.append('      <td><a name="wijzigdeze"></a>Gebruikersnaam:</td>')
        self.regels.append('      <td>Toegangstype:</td>')
        self.regels.append('      <td>Eerste scherm:</td>')
        self.regels.append('      <td>Zoekargument:</td>')
        self.regels.append('      <td>Geblokkeerd:</td>')
        self.regels.append('      <td>&nbsp;</td>')
        self.regels.append('      <td>&nbsp;</td>')
        self.regels.append('    </tr>')
        self.regels.append('    <tr>')
        self.regels.append('    <form action="%s%s" method="post">' % (cgipad,self.wprog))
        self.regels.append('      <td valign="top">')
        self.regels.append('        <input type="text" name="tNaam" id="tNaam" value="%s"/>' % x[0])
        self.regels.append('      </td>')
        self.regels.append('      <td valign="top">')
        self.regels.append('        <select name="sType" id="sType">')
        for i in xtypes.keys():
            si = ''
            if i == x[2]:
                si = ' selected="selected"'
            self.regels.append('          <option%s value="%s">%s</option>' % (si,i,xtypes[i]))
        self.regels.append('        </select>')
        self.regels.append('      </td>')
        h = x[4].split(':')
        self.regels.append('      <td valign="top">')
        self.regels.append('        <select name="sStart" id="sStart">')
        if h[0] == '':
            h[0] = snames[0]
        for i in range(4):
            si = ''
            if snames[i] == h[0]:
                si = ' selected="selected"'
            self.regels.append('          <option%s value="%s">%s</option>' % (si,snames[i],snames[i]))
        self.regels.append('        </select>')
        self.regels.append('      </td>')
        self.regels.append('      <td valign="top">')
        hh = ''
        if len(h) > 1: hh = h[1]
        self.regels.append('        <input type="text" name="tMet" id="tMet" value="%s"/>' % hh)
        self.regels.append('      </td>')
        self.regels.append('      <td valign="top">')
        self.regels.append('        <select name="sBlok" id="sBlok">')
        for i in btypes.keys():
            si = ''
            if i == x[3]:
                si = ' selected="selected"'
            self.regels.append('          <option%s value="%s">%s</option>' % (si,i,btypes[i]))
        self.regels.append('        </select>')
        self.regels.append('      </td>')
        self.regels.append('      <td valign="top">')
        if newuser:
            self.regels.append('        <input type="hidden" name="hPw" id="hPw" value="0" />')
            self.regels.append('        Voor een nieuwe gebruiker wordt automatisch een standaard wachtwoord opgevoerd')
        else:
            self.regels.append('        <input type="hidden" name="hPw" id="hPw" value="N" />')
            hh = ("doit_wpw('wu1','wu2','J')")
            self.regels.append('        <input type="submit" value="wachtwoord wijzigen" onclick="%s"/>' % hh)
        self.regels.append('      </td>')
        self.regels.append('      <td valign="top">')
        self.regels.append('        <input type="hidden" name="hVan" id="hVan" value="toon_users" />')
        self.regels.append('        <input type="hidden" name="wu1" id="wu1" value="%s" />' % un)
        self.regels.append('        <input type="hidden" name="wu2" id="wu2" value="%s" />' % so)
        hh = ("doit_woord('tNaam','Gebruikersnaam','wu1','wu2');return document.doit_retval")
        self.regels.append('        <input type="submit" value="OK" onclick="%s"/>' % hh)
        self.regels.append('        <input type="button" value="Cancel" onclick="javascript:history.go(-1)" />')
        self.regels.append('      </td>')
        self.regels.append('    </form>')
        self.regels.append('    </tr>')

if __name__ == '__main__':
    f = file("test.html","w")
    l = toon_us_main(1,'woefdram','magiokis',False,"0")
    for x in l.regels:
        f.write("%s\n"% x)
    f.close()
