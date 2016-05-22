# -*- coding: utf-8 -*-
import sys
import os
from logbook import Logger, FileHandler
logger = Logger('Test_Edex')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import Edex_objects as ex

def test_naamobj(naam=None, obj=None):
    if obj is None:
        logger.info('test_naamobj voor naam "{}"'.format(naam))
        if naam is None:
            obj = ex.Naamobj()
        else:
            obj = ex.Naamobj(naam)
    else:
        logger.info('test_naamobj voor object "{}"'.format(str(obj)))
    logger.info('    {}'.format(obj.__dict__))
    logger.info('    {}'.format(str(obj)))
    logger.info('    {}'.format(obj.displaynaam('atv')))
    return obj

def test_wijzig_naamobj(obj, naam, waarde):
    logger.info('test_wijzig_naamobj voor naam "{}" waarde "{}"'.format(naam,
        waarde))
    obj.wijzig(naam, waarde)

def test_datumobj(format=None, data=None, obj = None):
    if obj is None:
        logger.info('test_datumobj voor format {} data {}'.format(format, data))
        if format is None and data is None:
            obj = ex.Datumobj()
        else:
            obj = ex.Datumobj(format, data)
    else:
        logger.info('test_datumobj voor object "{}"'.format(str(obj)))
    logger.info('    {}'.format(obj.__dict__))
    return obj

def test_datumobj_in(obj, format, data):
    logger.info('test_datumobj_in voor format {} data {}'.format(format, data))
    obj.get_in(format, data)

def test_datumobj_out(obj, format):
    logger.info('test_datumobj_uit voor format {}'.format(format))
    data = obj.get_out(format)
    logger.info('   {}'.format(data))

def test_leerkrachtenlijst():
    logger.info('test leerkrachtenlijst')
    lijst, laatste = ex.leerkrachtenlijst()
    logger.info('    laatste: {}'.format(laatste))
    for item in lijst:
        logger.info('    {}'.format(item))

def test_leerkracht(leerk_id):
    logger.info('test leerkracht "{}"'.format(leerk_id))
    obj = ex.Leerkracht(leerk_id)
    logger.info('    {}'.format(obj.__dict__))
    return obj

def test_groepenlijst():
    logger.info('test groepenlijst')
    lijst = ex.groepenlijst()
    for item in lijst:
        logger.info('    {}'.format(item))

def test_groependetailslijst():
    logger.info('test groependetailslijst')
    lijst, laatste = ex.groependetailslijst()
    logger.info('    laatste: {}'.format(laatste))
    for key, data in lijst.items():
        logger.info('    {}: {}'.format(key, data))

def test_groep(groep_id):
    logger.info('test groep "{}"'.format(groep_id))
    obj = ex.Groep(groep_id)
    obj.read()
    logger.info('    {}'.format(obj.__dict__))
    return obj

def test_leerlingenlijst(leerk=None, groep=None):
    logger.info('test leerlingenlijst voor leerk {} groep {}'.format(leerk, groep))
    if leerk is None:
        if groep is None:
            lijst, laatste = ex.leerlingenlijst()
        else:
            lijst, laatste = ex.leerlingenlijst(groep=groep)
    else:
        if groep is None:
            lijst, laatste = ex.leerlingenlijst(leerkracht=leerk)
        else:
            lijst, laatste = ex.leerlingenlijst(leerkracht=leerk, groep=groep)
    logger.info('    laatste: {}'.format(laatste))
    for key, item in lijst.items():
        logger.info('    {}: {}'.format(key, item))

def test_absentenlijst():
    logger.info('test absentenlijst')
    lijst = ex.absentenlijst()
    for key, item in lijst.items():
        logger.info('    {}: {}'.format(key, item))

def test_absenties(leerl=None):
    logger.info('test absentenlijst')
    if leerl is None:
        lijst = ex.absenties()
    else:
        lijst = ex.absenties(leerl)
    for item in lijst:
        logger.info('    {}'.format(item))

def test_zoek_leerl(zoek, van):
    logger.info('test zoek leerling(en): zoek is {}, van is {}'.format(zoek, van))
    for item in ex.zoek_leerlingen(zoek, van):
        logger.info('    {}'.format(item))

def test_leerling(leerl_id):
    logger.info('test leerling "{}"'.format(leerl_id))
    obj = ex.Leerling(leerl_id)
    logger.info('    {}'.format(obj.__dict__))
    logger.info('    laatste absentie: {}'.format(obj.laatste_absentie()))
    return obj

if __name__ == '__main__':
    ## log_handler = FileHandler('test_naamobj.log', mode="w")
    ## with log_handler.applicationbound():
        ## obj = test_naamobj()
        ## obj = test_naamobj("")
        ## obj = test_naamobj(
            ## "Gargelhuil Thoe Sneerensteijn           van       Barend Hertog       ")
        ## obj = test_naamobj(
            ## "Hollandsche-Rading                      van den   Wim-Joost           ")
        ## obj = test_naamobj(
            ## "Krijt                                             Toon                ")
        ## test_wijzig_naamobj(obj, 'vn', 'Willem')
        ## test_naamobj(obj=obj)
        ## test_wijzig_naamobj(obj, 'vv', 'van')
        ## test_naamobj(obj=obj)
        ## test_wijzig_naamobj(obj, 'an', 'Snorkesteijn')
        ## test_naamobj(obj=obj)

    ## log_handler = FileHandler('test_datumobj.log', mode="w")
    ## with log_handler.applicationbound():
        ## obj = test_datumobj()
        ## obj = test_datumobj('dmj')
        ## obj = test_datumobj(format='dmj')
        ## obj = test_datumobj('1234567890')
        ## obj = test_datumobj(data='1234567890')
        ## obj = test_datumobj(format='', data='1234567890')
        ## obj = test_datumobj(format='dmj', data='')
        ## obj = test_datumobj(format='gargl', data='1234567890')
        ## obj = test_datumobj(format='dmj', data='1234567890')
        ## obj = test_datumobj(format='jmd', data='1234567890')
        ## test_datumobj_in(obj, format='dmj', data='1234567890')
        ## test_datumobj(obj)
        ## test_datumobj_in(obj, format='dmj', data='1234567890')
        ## test_datumobj(obj)
        ## test_datumobj_out(obj, format='dmj')
        ## test_datumobj_out(obj, format='d-m-j')
        ## test_datumobj_out(obj, format='jmd')
    ## log_handler = FileHandler('test_leerkracht.log', mode="w")
    ## with log_handler.applicationbound():
        ## test_leerkrachtenlijst()
        ## obj = test_leerkracht('')
        ## obj = test_leerkracht('snork')
        ## obj = test_leerkracht('00001')
    ## log_handler = FileHandler('test_groep.log', mode="w")
    ## with log_handler.applicationbound():
        ## test_groepenlijst()
        ## test_groependetailslijst()
        ## test_groep('')
        ## test_groep('snork')
        ## test_groep('00078')
    ## log_handler = FileHandler('test_leerling.log', mode="w")
    ## with log_handler.applicationbound():
        ## test_leerlingenlijst()
        ## test_leerlingenlijst(leerk='00001')
        ## test_leerlingenlijst(groep='00078')
        ## test_leerlingenlijst(leerk='00002', groep='00079')
        ## test_zoek_leerl('berg', 'scherm')
        ## test_zoek_leerl('jan', '')
        ## test_zoek_leerl('jan', 'toon_klas-00001')
        ## test_zoek_leerl('a', 'toon_absent')
        ## test_leerling('00125') # ('00005')
    log_handler = FileHandler('test_absenties.log', mode="w")
    with log_handler.applicationbound():
        test_absentenlijst()
        ## test_absenties('00010') # niks aanwezig
        ## test_absenties('00080') # wel wat aanwezig
