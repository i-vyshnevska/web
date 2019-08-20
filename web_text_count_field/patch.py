# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

import logging

import odoo
from odoo.tools import pycompat
from operator import attrgetter

logger = logging.getLogger(__name__)


def Text__convert_to_column(self, value, record, values=None, validate=True):
    if value is None or value is False:
        return None
    if  hasattr(self, 'size') and self.size != False:
        return pycompat.to_text(value)[:self.size]
    else:
        return self.orig_convert_to_column(value, record, values, validate)


def Text__convert_to_cache(self, value, record, validate=True):
    if value is None or value is False:
        return False
    if  hasattr(self, 'size') and self.size != False:
        return pycompat.to_text(value)[:self.size]
    else:
        return self.orig_convert_to_cache(value, record, validate)


def patch_fields():

    Text = odoo.fields.Text
    slots = Text._slots
    slots['size'] = None
    setattr(Text, '_slots', slots)
    setattr(Text, '_related_size', property(attrgetter('size')))
    Text.orig_convert_to_column = Text.convert_to_column
    Text.convert_to_column = Text__convert_to_column
    
    Text.orig_convert_to_cache = Text.convert_to_cache
    Text.convert_to_cache = Text__convert_to_cache

