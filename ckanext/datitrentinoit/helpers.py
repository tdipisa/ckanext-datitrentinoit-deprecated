import logging
import operator
import json

import ckan
import ckan.model as model
import ckan.plugins as p
import ckan.lib.search as search
import ckan.lib.helpers as h

import ckan.logic as logic

from pylons.i18n.translation import get_lang
from ckanext.multilang.model import PackageMultilang

import ckanext.datitrentinoit.model.custom as custom

log = logging.getLogger(__file__)

def getLanguage():
    lang = get_lang()
    
    if lang is not None:
        lang = unicode(lang[0])        
    
    return lang

def getLocalizedFieldValue(field=None, pkg_dict=None):
    if field and pkg_dict:
        lang = getLanguage()
        if lang:
            localized_value = custom.get_field(field, pkg_dict.get('id'), lang)
            if localized_value:
                return localized_value.text
            else:
                return None
        else: 
            return None
    else:
        return None

def recent_updates(n):
    #
    # Return a list of the n most recently updated datasets.
    #
    log.debug('::::: Retrrieving latest datasets: %r' % n)
    context = {'model': model,
               'session': model.Session,
               'user': p.toolkit.c.user or p.toolkit.c.author}

    data_dict = {'rows': n, 'sort': u'metadata_modified desc', 'facet': u'false'}
	
    try:
        search_results = logic.get_action('package_search')(context, data_dict)
    except search.SearchError, e:
        log.error('Error searching for recently updated datasets')
        log.error(e)
        search_results = {}

    for item in search_results.get('results'):
        log.info(':::::::::::: Retrieving the corresponding localized title and abstract :::::::::::::::')

        lang = getLanguage()
        
        q_results = model.Session.query(PackageMultilang).filter(PackageMultilang.package_id == item.get('id'), PackageMultilang.lang == lang).all() 

        if q_results:
            for result in q_results:
                item[result.field] = result.text
	
    return search_results.get('results', [])