from globals import xmlpad
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape

class FindUser(ContentHandler):
    "bevat de gegevens van een bepaalde user"
    def __init__(self, username):
        self.search_username = username
        self.userfound = False
        self.founduser = False

    def startElement(self, name, attrs):
        if name == 'user':
            user = attrs.get('id', None)
            if user == self.search_username:
                self.founduser = True
                self.username = user
            if self.founduser:
                self.password = attrs.get('paswd', None)
                self.login = attrs.get('login', None)
                self.utype = attrs.get('type', None)
                self.blck = attrs.get('blok', None)
                self.start = attrs.get('start', None)

    def endElement(self, name):
        if name == 'user':
            if self.founduser:
                self.userfound = True
                self.founduser = False

class UpdateUser(XMLGenerator):
    "schrijf nieuwe gegevens weg in XML-document"
    def __init__(self, user):
        self.uh = user
        self.search_item = self.uh.userid
        self.fh = open(self.uh.fn,'w')
        self.founditem = False
        self.itemfound = False
        XMLGenerator.__init__(self,self.fh)
        self.utype = 'usr'
        self.blck = 'N'
        self.start = 'start'

    def startElement(self, name, attrs):
        "nog een attribuut erbij: login error (init op 0)"
    #-- kijk of we met de te wijzigen user bezig zijn
        if name == 'user':
            item = attrs.get('id', None)
            if item == str(self.search_item):
                self.founditem = True
                self.itemfound = True
                if self.uh.paswd == "":
                    self.password = attrs.get('paswd',None)
                else:
                    self.password = self.uh.paswd
                if self.uh.utype == "":
                    self.utype = attrs.get('type',None)
                else:
                    self.utype = self.uh.utype
                if self.uh.login == "":
                    self.login = attrs.get('login',None)
                else:
                    self.login = self.uh.login
                if self.uh.blck == "":
                    self.blck = attrs.get('blok',None)
                else:
                    self.blck = self.uh.blck
                if self.uh.start == "":
                    self.start = attrs.get('start',None)
                else:
                    self.start = self.uh.start
    #-- xml element (door)schrijven
        if self.founditem :
            if name == 'user':
                self._out.write('<' + name)
                self.username = self.uh.userid
                self.login = self.uh.login
                for (name,value) in attrs.items():
                    h = value
                    if name == 'id':
                        if value != self.username:
                            h = self.username
                    if name == 'type':
                        if value != self.utype:
                            h = self.utype
                    if name == 'paswd':
                        if value != self.password:
                            h = self.password
                    if name == 'login':
                        if value != self.login:
                            h = self.login
                    if name == 'blok':
                        if value != self.blck:
                            h = self.blck
                    if name == 'start':
                        if value != self.start:
                            h = self.start
                    self._out.write(' %s="%s"' % (name,escape(h)))
        else:
            XMLGenerator.startElement(self, name, attrs)

    def characters(self,content):
##        newcontent = content.encode("iso-8859-1")
##        XMLGenerator.characters(self,newcontent)
        pass

    def endElement(self, name):
        if self.founditem:
            if name == 'user':
                self.founditem = False
                self._out.write('></%s>' % name)
        else:
            if name == 'users':
                if not self.itemfound:
                    self._out.write('<user')
                    self._out.write(' id="%s"' % escape(self.uh.userid))
                    self._out.write(' type="%s"' % escape(self.uh.utype))
                    self._out.write(' paswd="%s"' % escape(self.uh.paswd))
                    self._out.write(' login="%s"' % escape(self.uh.login))
                    self._out.write(' blok="%s"' % escape(self.uh.blck))
                    self._out.write(' start="%s"' % escape(self.uh.start))
                    self._out.write('></user>')
            XMLGenerator.endElement(self, name)

    def endDocument(self):
##        XMLGenerator.endDocument(self)
        self.fh.close()


class ListUsers(ContentHandler):
    def __init__(self):
        self.Items = []

    def startElement(self, name, attrs):
        if name == 'user':
            user = attrs.get('id', '')
            login = attrs.get('login', '')
            utype = attrs.get('type', '')
            blck = attrs.get('blok', '')
            start = attrs.get('start', '')
            self.Items.append([user,login,utype,blck,start])

class UserLijst:
    "lijst met gegevens van alle users:"
    "resp. naam, login, autorisatieniveau, blokkade"
    def __init__(self):
        self.fn = xmlpad + 'users.xml'
        self.fno = xmlpad + 'users_oud.xml'
        self.Items = []
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = ListUsers()
        parser.setContentHandler(dh)
        parser.parse(self.fn)
        for x in dh.Items:
            h = []
            for y in x:
                h.append(y.encode('ISO-8859-1'))
            self.Items.append(h)

class User:
    "gegevens van een bepaalde user"
    "a. alleen usernaam gegeven: read-opdracht moet expliciet volgen"
    "b. usernaam en password: doe een logon met een impliciete read"
    "   als het password ok is overige gegevens ophalen"
    "c. usernaam en sessie: doe een read en controleer de sessie"
    "   als het ok is de overige gegevens ophalen"
    def __init__(self,userid,paswd="",isSesId=False): # user aanmaken
        self.fn = xmlpad + 'users.xml'
        self.fno = xmlpad + 'users_oud.xml'
        self.userid = userid
        self.paswd = ''
        self.paswdok = False
        self.SessionOk = False
        self.login = ""
        self.utype = ''
        self.geblokkeerd = False
        self.blck = 'N'
        self.start = 'start'
#        self.xtypes = ['adm','usr','prt','vwr']
        self.xtypes = ['adm','usr']
        self.btypes = ['J','N']
        self.snames = ['start','toon_klas','sel_leerling','toon_absent']

        if paswd != '':
            if isSesId:
                dh = self.read()
                if self.found:
                    self.SessionOk = self.checkSession(paswd,dh.login)
            else:
                dh = self.logon(paswd)
            if self.SessionOk or self.paswdok:
                self.login = dh.login
                self.utype = dh.utype
                self.blck = dh.blck
                self.start = dh.start
            dh = ''

    def read(self):
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = FindUser(str(self.userid))
        parser.setContentHandler(dh)
        parser.parse(self.fn)
        self.found = dh.userfound
        return dh

    def logon(self,value):
        dh = self.read()
        if self.found:
            if value == dh.password:
                self.paswdok = True
            else:
                self.loginerr += 1
                if self.loginerr > 3:
                    self.setBlok("J")
        return dh

    def setPass(self,value):
        "wijzigen van het wachtwoord"
        self.paswd = value
        self.write()
        self.paswd = ''

    def getPass(self):
        dh = self.read()
        if self.found:
            self.paswd = dh.password

    def setType(self,value):
        try:
            h = self.xtypes.index(value)
        except:
            return False
        else:
            self.utype = value
            self.write()
            return True

    def setStart(self,value):
        try:
            h = self.snames.index(value)
        except:
            return False
        else:
            self.start = value.upper()
            self.write()
            return True

    def setBlok(self,value):
        try:
            h = self.btypes.index(value)
        except:
            return False
        else:
            self.blck = value.upper()
            self.write()
            return True

    def getAttr(self,name):
        if name == 'type':
            return self.utype
        elif name == 'start':
            return self.start
        elif name == 'blok':
            return self.blck
        else:
            return False

    def getLevel(self):
        "vertaal access-level in een volgnummer"
        try:
            h = self.xtypes.index(self.utype)
        except:
            return 0
        else:
            return h + 1

    def startSession(self):
        "aangeven dat de gebruiker aangelogd is"
        from time import gmtime, strftime
        i = strftime("%Y/%m/%d-%H:%M:%S")
        self.login = i
        sessionid = i[0] + i[2] + i[5] + i[9] + i[15] + i[18]+ i[17] + i[14] + i[11] + i[6] + i[1] + i[3] + i[8] + i[12]
        self.write()
        return sessionid

    def checkSession(self,sessionid,login):
        "sessionid controleren"
        i = sessionid
        if len(i) == 14:
            dts = i[0] + i[10] + i[1] + i[11] + "/" + i[2] + i[9] + "/" + i[12] + i[3] + "-" + i[8] + i[13] + ":" + i[7] + i[4] + ":" + i[6] + i[5]
            try:
                if dts == login:
                    return True
            except:
                pass
        return False

    def endSession(self):
        "aangeven dat de gebruiker niet (meer) aangelogd is"
        self.login = ""
        try:
            self.write()
        except:
            return False
        return True

    def write(self):
        retval = 0
        #~ if self.userid == '':
            #~ retval = 1
        #~ elif self.utype == '':
            #~ retval = 2
        #~ elif self.paswd == '':
            #~ retval = 4
        if retval == 0:
            from shutil import copyfile
            from os import remove
            copyfile(self.fn,self.fno)
            remove(self.fn)
            parser = make_parser()
            parser.setFeature(feature_namespaces, 0)
            dh = UpdateUser(self)
            parser.setContentHandler(dh)
            parser.parse(self.fno)
        return retval

def test():
    #~ dh = User('woefdram')
    #~ dh.read()
    #~ if dh.found:
        #~ print dh.__dict__
    #~ else:
        #~ print "user not found"
    #~ dh = User('vader',"begin")
    #~ if dh.paswdok:
        #~ print dh.__dict__
    #~ else:
        #~ print "password not ok"
    #~ return
    #~ dh = User('vader',"20015533280430",True)
    #~ print dh.SessionOk
    #~ print dh.blck
    #~ print dh.xtypes
    #~ print dh.getLevel()
    #~ return
    #~ dh = User('woefdram','magiokis')
    #~ s = dh.startSession()
    #~ xslevel = dh.getLevel
    # defining a user, starting out with username only
    #~ dh = User('Brian')
    #~ dh.read()
    #~ if dh.found:
        #~ dh.setPass('life')
        #~ if not dh.setType('user'):
            #~ print "type moet 'adm' of 'usr' zijn"
        #~ dh.logon('life')
        #~ if dh.paswdok:
            #~ print "found user, password ok"
        #~ else:
            #~ print "found user, password wrong"
    #~ else:
        #~ print "user not found, adding new one (I hope)"
        #~ dh.utype = '1'
        #~ dh.blck = 'N'
        #~ dh.start = 'toon_klas:Brian'
        #~ h = dh.write()
    #~ return
    # defining a user from userid and password
    #~ dh = User('Brian','life')
    #~ if dh.found:
        #~ if dh.paswdok:
            #~ print "found user, password ok"
        #~ else:
            #~ print "found user, password wrong"
    #~ else:
        #~ print "user not found, adding new one (I hope)"
    dh = UserLijst()
    for x in dh.Items:
        print x
    #~ return
    #-- testen password aanpassen
    #~ if dh.paswdok:
        #~ print dh.userid,dh.paswd,dh.login
        #~ print "password ophalen"
        #~ dh.getPass()
        #~ print dh.userid,dh.paswd,dh.login
        #~ print "password wijzigen"
        #~ dh.setPass("magiokis")
    #--- testen start / check / end Session
    #~ s = dh.startSession()
    #~ print "sessie gestart met id:", s
    #~ dh = User('Brian', 'life')
    #~ print dh.__dict__
    #~ dh = User('Brian','20062043280412',True)
    #~ print dh.__dict__
    #~ s = '20032123280410'
    #~ h = dh.checkSession(s)
    #~ if h:
        #~ print "...en de sessie loopt"
    #~ else:
        #~ print "sessie-id",s,"klopt niet"
    #~ dh = User('woefdram','20032123280410',True)
    #~ if dh.SessionOk:
        #~ print "...en de sessie loopt"
    #~ else:
        #~ print "sessie-id",s,"klopt niet"
    #~ s = "hallo hallo hallo hallo"
    #~ h = dh.checkSession(s)
    #~ if h:
        #~ print "...en de sessie loopt"
    #~ else:
        #~ print "sessie-id",s,"klopt niet"
    #~ dh = User('woefdram', 'magiokis')
    #~ if dh.endSession():
        #~ print "sessie succesvol afgesloten"
    #~ dh = User('woefdram', 'magiokis')
    #~ print dh.userid,dh.paswd,dh.login

if __name__ == '__main__':
	test()
