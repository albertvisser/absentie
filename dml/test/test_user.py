# -*- coding: utf-8 -*-
import sys
import os
from logbook import Logger, FileHandler
logger = Logger('Test_Edex')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from school_user import userlijst, User

def test_userlijst():
    logger.info('test userlijst')
    for item in userlijst():
        logger.info('    {}'.format(item))

def test_user(usernaam, password=None, flag=None):
    if password is None:
        logger.info('test user voor usernaam {}'.format(usernaam))
        dh = User(usernaam)
        dh.read()
        if dh.found:
            logger.info('    {}'.format(dh.__dict__))
        else:
            logger.info("    user not found")
        return
    elif flag is None:
        logger.info('test user voor usernaam {} password {}'.format(usernaam,
            password))
        dh = User(usernaam, password)
        if dh.paswdok:
            logger.info('    {}'.format(dh.__dict__))
        else:
            logger.info("    password not ok")
        return
    logger.info('test user voor usernaam {} password {} is_sessionid {}'.format(
        usernaam, password, flag))
    dh = User(usernaam, password, flag)
    if not flag:
        if dh.paswdok:
            logger.info('    {}'.format(dh.__dict__))
        else:
            logger.info("    password not ok")
    else:
        if dh.session_ok:
            logger.info('    {}'.format(dh.__dict__))
        else:
            logger.info("    session not ok")
    return dh


if __name__ == '__main__':
    log_handler = FileHandler('test_user.log', mode="w")
    with log_handler.applicationbound():
        test_userlijst()
        test_user('woefdram')
        test_user('vader',"begin")
        test_user('vader',"begin", False)
        test_user('vader',"20015533280430",True)

        usernaam, passwd = 'leerkracht', 'begin'
        test_user(usernaam)
        dh = test_user(usernaam, passwd)
        login = dh.login
        test_user(usernaam, passwd, False)
        test_user(usernaam, "20015533280430", True)
        test_user(usernaam, dh.login, True)
        dh = test_user(usernaam, passwd)
        if dh:
            s = dh.startSession()
            xslevel = dh.getLevel
        else:
            logger.info('usernaam of password incorrect')
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
