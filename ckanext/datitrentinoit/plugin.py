# -*- coding: utf-8 -*-

# Plugin for http://dati.trentino.it
# Ckan: 2.2a

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

import ckan.plugins as plugins
import logging

import ckan.lib.base as base
import ckan.plugins.toolkit as plugins_toolkit
import routes.mapper as routes_mapper

import ckanext.datitrentinoit.helpers as helpers

import ckanext.datitrentinoit.model.custom as custom

log = logging.getLogger(__name__)

static_pages = ['faq', 'acknowledgements', 'legal_notes', 'privacy']

class DatiTrentinoPlugin(plugins.SingletonPlugin, plugins_toolkit.DefaultDatasetForm):

    custom_fields = [
        {'key': 'holder', 'localized': True},
        {'key': 'geographical_coverage', 'localized': True},
        {'key': 'temporal_coverage_start', 'localized': False},
        {'key': 'temporal_coverage_end', 'localized': False},
        {'key': 'update_frequency', 'localized': True},
        {'key': 'creation_date', 'localized': False},
        {'key': 'publication_date', 'localized': False},
        {'key': 'revision_date', 'localized': False},
        {'key': 'encoding', 'localized': False},
        {'key': 'site_url', 'localized': True},
        {'key': 'contact', 'localized': True},
        {'key': 'fields_description', 'localized': True}
    ]

    """Controller used to load custom templates/resources/pages"""

    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IPackageController, inherit=True)


    # Implementation of IConfigurer :(
    # ------------------------------------------------------------

    def update_config(self, config):
        plugins_toolkit.add_public_directory(config, 'public')
        plugins_toolkit.add_template_directory(config, 'templates')
        plugins_toolkit.add_resource('fanstatic', 'ckanext-datitrentinoit')

    # Implementation of IConfigurable :(
    # ------------------------------------------------------------

    def configure(self, config):
        self.ga_conf = {
            'id': config.get('googleanalytics.id'),
            'domain': config.get('googleanalytics.domain'),
        }

    # Implementation of IRoutes :(
    # ------------------------------------------------------------

    def before_map(self, routes):
        controller = 'ckanext.datitrentinoit.plugin:DatiTrentinoController'
        with routes_mapper.SubMapper(routes, controller=controller) as m:
            for page_name in static_pages:
                page_slug = page_name.replace('_', '-')
                m.connect(page_name, '/' + page_slug, action=page_name)
        return routes

    def after_map(self, routes):
        return routes

    # Implementation of ITemplateHelpers :(
    # ------------------------------------------------------------

    def get_helpers(self):
        return {
            'dti_ga_site_id': self._get_ga_site_id,
            'dti_ga_site_domain': self._get_ga_site_domain,
            'dti_recent_updates': helpers.recent_updates,
            'dti_get_custom_fields': self._dti_get_custom_fields,
            'dti_get_localized_field_value': helpers.getLocalizedFieldValue,
            'dti_get_language': helpers.getLanguage
        }

    def _get_ga_site_id(self):
        return self.ga_conf['id']

    def _get_ga_site_domain(self):
        return self.ga_conf['domain']

    def _dti_get_custom_fields(self):
        return self._custom_text_fields

    def _modify_package_schema_for_edit(self, schema):
        for field in self.custom_fields:
            schema.update({
                field['key']: [
                    plugins_toolkit.get_validator('ignore_missing'),
                    plugins_toolkit.get_converter('convert_to_extras')
                ]
            })

        return schema

    def _modify_package_schema_for_read(self, schema):
        for field in self.custom_fields:
            schema.update({
                field['key']: [
                    plugins_toolkit.get_converter('convert_from_extras'), 
                    plugins_toolkit.get_validator('ignore_missing')
                ]
            })

        return schema

    def create_package_schema(self):
        schema = super(DatiTrentinoPlugin, self).create_package_schema()
        schema = self._modify_package_schema_for_edit(schema)
        return schema

    def update_package_schema(self):
        schema = super(DatiTrentinoPlugin, self).update_package_schema()
        schema = self._modify_package_schema_for_edit(schema)
        return schema

    def show_package_schema(self):
        schema = super(DatiTrentinoPlugin, self).show_package_schema()
        schema = self._modify_package_schema_for_read(schema)
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def after_create(self, context, pkg_dict):
        # During the harvest the get_lang() is not defined
        lang = helpers.getLanguage()

        if lang:    
            for extra in pkg_dict.get('extras'):
                for field in self.custom_fields:
                    if extra.get('key') == field['key'] and field.localized == True:
                        log.info(':::::::::::::::Localizing custom field: %r', field['key'])
                        
                        # Create the localized field record
                        self.createLocField(extra, lang, pkg_dict.get('id'))

    def after_update(self, context, pkg_dict):
        # During the harvest the get_lang() is not defined
        lang = helpers.getLanguage()

        if lang:             
            for extra in pkg_dict.get('extras'):
                for field in self.custom_fields:
                    if extra.get('key') == field['key'] and field['localized'] == True:
                        log.info(':::::::::::::::Localizing custom field: %r', field['key'])
                        f = custom.get_field(extra.get('key'), pkg_dict.get('id'), lang)
                        if f:
                            if extra.get('value') == '':
                                f.purge()
                            elif f.text != extra.get('value'):
                                # Update the localized field value for the current language
                                f.text = extra.get('value')
                                f.save()

                                log.info('Custom field updated successfully')

                        elif extra.get('value') != '':
                            # Create the localized field record
                            self.createLocField(extra, lang, pkg_dict.get('id'))

    def createLocField(self, extra, lang, package_id): 
        log.debug('Creating createLocField for package ID: %r', str(package_id))

        new_loc_field = custom.CustomFieldMultilang(package_id, extra.get('key'), lang, extra.get('value'))
        custom.CustomFieldMultilang.save(new_loc_field)

        log.info('Custom field created successfully')

class DatiTrentinoController(base.BaseController):
    """Controller used to add custom pages"""


for page_name in static_pages:
    def get_action(name):
        def action(self):
            return base.render('pages/{0}.html'.format(name))
        return action
    action = get_action(page_name)
    action.__name__ = page_name
    setattr(DatiTrentinoController, page_name, action)
