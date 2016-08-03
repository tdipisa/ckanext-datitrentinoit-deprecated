
import sys
import logging

from sqlalchemy import types, Column, Table, ForeignKey
from sqlalchemy import orm

from ckan.lib.base import config
from ckan import model
from ckan.model import Session
from ckan.model import meta
from ckan.model.domain_object import DomainObject

from ckan import model

log = logging.getLogger(__name__)

__all__ = ['CustomFieldMultilang', 'custom_field_table', 'get_field']

custom_field_table = Table('custom_field_table', meta.metadata,
    Column('id', types.Integer, primary_key=True),
    Column('package_id', types.UnicodeText, ForeignKey("package.id", ondelete="CASCADE"), nullable=False),
    Column('field', types.UnicodeText, nullable=False, index=True),
    Column('lang', types.UnicodeText, nullable=False, index=True),
    Column('text', types.UnicodeText, nullable=False, index=True))

def init_db():
    #Setting up custom fiels table for locales    
    try:
        custom_field_table.create()
    except Exception,e:
        # Make sure the table does not remain incorrectly created
        if custom_field_table.exists():
            Session.execute('DROP TABLE custom_field_table')
            Session.commit()

        raise e

    log.info('Custom field table created')

def get_field(field, package_id, lang):
    field_value = Session.query(CustomFieldMultilang).filter(CustomFieldMultilang.package_id == package_id, CustomFieldMultilang.field == field, CustomFieldMultilang.lang == lang).first() 
    return field_value

class CustomFieldMultilang(DomainObject):
    def __init__(cls, package_id=None, field=None, lang=None, text=None):
        cls.package_id = package_id
        cls.field = field
        cls.lang = lang
        cls.text = text

meta.mapper(CustomFieldMultilang, custom_field_table)