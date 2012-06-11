import os
import shutil
from globals import xmlpad
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape
userfile = os.path.join(xmlpad, 'users.xml')
backup = '_oud'.join(os.path.splitext(userfile))

def _mangle(timestamp):
    i = timestamp
    retval = i[0] + i[2] + i[5] + i[9] + i[15] + i[18]+ i[17] + i[14]
    retval = retval + i[11] + i[6] + i[1] + i[3] + i[8] + i[12]
    return retval

def _unmangle(sessionid):
    i = sessionid
    retval = i[0] + i[10] + i[1] + i[11] + "/" + i[2] + i[9] + "/" + i[12] + i[3]
    retval = retval + "-" + i[8] + i[13] + ":" + i[7] + i[4] + ":" + i[6] + i[5]
    return retval

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
        XMLGenerator.__init__(self, self.fh)
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
                if self.uh.usertype == "":
                    self.utype = attrs.get('type',None)
                else:
                    self.utype = self.uh.usertype
                if self.uh.login == "":
                    self.login = attrs.get('login',None)
                else:
                    self.login = self.uh.login
                if self.uh.blocked == "":
                    self.blck = attrs.get('blok',None)
                else:
                    self.blck = 'J' if self.uh.blocked else 'N'
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
                for (name, value) in attrs.items():
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
                    self._out.write(' type="%s"' % escape(self.uh.usertype))
                    self._out.write(' paswd="%s"' % escape(self.uh.paswd))
                    self._out.write(' login="%s"' % escape(self.uh.login))
                    blck = 'J' if self.uh.blocked else 'N'
                    self._out.write(' blok="%s"' % blck)
                    self._out.write(' start="%s"' % escape(self.uh.start))
                    self._out.write('></user>')
            XMLGenerator.endElement(self, name)

    def endDocument(self):
##        XMLGenerator.endDocument(self)
        self.fh.close()


class ListUsers(ContentHandler):
    def __init__(self):
        self.items = []

    def startElement(self, name, attrs):
        if name == 'user':
            user = attrs.get('id', '')
            login = attrs.get('login', '')
            utype = attrs.get('type', '')
            blck = attrs.get('blok', '')
            start = attrs.get('start', '')
            self.items.append((user, login, utype, blck, start))

def userlijst():
    "lijst met gegevens van alle users:"
    "resp. naam, login, autorisatieniveau, blokkade"
    items = []
    parser = make_parser()
    parser.setFeature(feature_namespaces, 0)
    dh = ListUsers()
    parser.setContentHandler(dh)
    parser.parse(userfile)
    for x in dh.items:
        items.append([y.encode('ISO-8859-1') for y in x])
    return items

class User:
    """gegevens van een bepaalde user

    a. alleen usernaam gegeven: read-opdracht moet expliciet volgen
    b. usernaam en password: doe een logon met een impliciete read
       als het password ok is overige gegevens ophalen
    c. usernaam en sessie: doe een read en controleer de sessie
       als het ok is de overige gegevens ophalen
    """
    def __init__(self, userid, paswd="",is_sessionid=False): # user aanmaken
        self.fn = userfile
        self.fno = backup
        self.userid = userid
        self.paswd = ''
        self.paswdok = False
        self.session_ok = False
        self.login = ""
        self.usertype = ''
        self.geblokkeerd = False
        self.blocked = False
        self.start = 'start'
        self.access_types = ('adm', 'usr') # ,'prt, 'vwr')
        self.start_names = ('start', 'toon_klas', 'sel_leerling', 'toon_absent')

        if paswd != '':
            if is_sessionid:
                self.read()
                if self.found:
                    self.session_ok = self.check_session(paswd, self.login)
            else:
                self.logon(paswd)

    def read(self):
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = FindUser(str(self.userid))
        parser.setContentHandler(dh)
        parser.parse(self.fn)
        self.found = dh.userfound
        if self.found:
            self.login = dh.login
            self.usertype = dh.utype
            self.blocked = True if dh.blck == 'J' else False
            self.start = dh.start
        return dh

    def logon(self, value):
        dh = self.read()
        if self.found:
            if value == dh.password:
                self.paswdok = True
            else:
                self.loginerr += 1
                if self.loginerr > 3:
                    self.blocked = True

    def set_pass(self,value):
        "wijzigen van het wachtwoord"
        self.paswd = value
        self.write()
        self.paswd = ''

    def get_pass(self):
        dh = self.read()
        if self.found:
            self.paswd = dh.password

    def set_type(self,value):
        try:
            h = self.access_types.index(value)
        except:
            return False
        else:
            self.usertype = value
            self.write()
            return True

    def set_start(self,value):
        if value not in self.start_names.index(value):
            return False
        self.start = value.lower()
        self.write()
        return True

    def block(self, value=True):
        if value not in self.blocked_types:
            return False
        self.blocked = value
        self.write()
        return True

    def get_attr(self,name):
        if name == 'type':
            return self.usertype
        elif name == 'start':
            return self.start
        elif name == 'blok':
            return self.blocked

    def get_level(self):
        "vertaal access-level in een volgnummer"
        try:
            h = self.access_types.index(self.usertype)
        except ValueError:
            return 0
        else:
            return h + 1

    def start_session(self):
        "aangeven dat de gebruiker aangelogd is"
        from time import gmtime, strftime
        self.login = strftime("%Y/%m/%d-%H:%M:%S")
        sessionid = _mangle(self.login)
        self.write()
        return sessionid

    def check_session(self, sessionid, login):
        "sessionid controleren"
        if len(sessionid) == 14:
            dts = _unmangle(sessionid)
            if dts == login:
                return True
        return False

    def end_session(self):
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
            shutil.copyfile(self.fn, self.fno)
            os.remove(self.fn)
            parser = make_parser()
            parser.setFeature(feature_namespaces, 0)
            dh = UpdateUser(self)
            parser.setContentHandler(dh)
            parser.parse(self.fno)
        return retval
