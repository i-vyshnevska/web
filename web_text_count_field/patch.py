# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

import logging

import odoo
from odoo.tools import pycompat, pg_varchar, sql
from operator import attrgetter

logger = logging.getLogger(__name__)


def Text__convert_to_column(self, value, record, values=None, validate=True):
    if value is None or value is False:
        return None
    if  hasattr(self, 'size'):
        return pycompat.to_text(value)[:self.size]
    else:
        return self.orig_convert_to_column(value, record, values, validate)


def Text__convert_to_cache(self, value, record, validate=True):
    if value is None or value is False:
        return False
    if  hasattr(self, 'size'):
        return pycompat.to_text(value)[:self.size]
    else:
        return self.orig_convert_to_cache(value, record, validate)

def Text__update_db_column(self, model, column):
    if (
        column and column['udt_name'] == 'varchar' and column['character_maximum_length'] and
        (self.size is None or column['character_maximum_length'] < self.size)
    ):
        # the column's varchar size does not match self.size; convert it
        sql.convert_column(model._cr, model._table, self.name, self.column_type[1])
    super(odoo.fields.Text, self).update_db_column(model, column)


def patch_fields():

    Text = odoo.fields.Text
    # slots = Text._slots
    # slots['size'] = None
    # setattr(Text, '_slots', slots)
    # setattr(Text, '_related_size', property(attrgetter('size')))
    Text.orig_convert_to_column = Text.convert_to_column
    Text.convert_to_column = Text__convert_to_column
    
    Text.orig_convert_to_cache = Text.convert_to_cache
    Text.convert_to_cache = Text__convert_to_cache
    Text.update_db_column = Text__update_db_column

