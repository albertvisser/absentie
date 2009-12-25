from school_globals import *
from school_user import User

class check_login:
    def __init__(self,usernaam,sessionid):
        h = User(usernaam,sessionid,True)
        self.SessionOk = h.SessionOk
        self.xslevel = h.getLevel()

class meld_fout:
    def __init__(self,kop,melding,login="N"):
        self.regels = []
        f = file(filepad + "next.html","r")
        for x in f.readlines():
            h = x.find("%s")
            if h > -1:
                hs = x[:-1].split("%s")
                if x.find("stylesheet") > -1:
                    self.regels.append(httppad.join(hs))
            elif x[:-1] == "<!-- kop -->":
                for y in printkop(kop):                  # gedefinieerd in school_globals
                    self.regels.append(y)
            elif x[:-1] == "<!-- data -->":
                self.regels.append('<br /><div>%s</div>' % melding)
            elif x[1:6] == "input":
                if login == "N":
                    self.regels.append('<input type="button" value="Terug" onclick="history.go(-1)"/>')
                else:
                    hgoto = ("document.location='%sschool_login.py'" % cgipad)
                    self.regels.append('<input type="button" value="Login" onclick="%s"/>' % hgoto)
            else:
                self.regels.append(x[:-1])

def test():
    s = check_login('vader',"20018405280430")
    print s.__dict__

if __name__ == '__main__':
    test()
