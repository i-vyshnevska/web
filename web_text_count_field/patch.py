# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

import logging

import odoo
from odoo.tools import pycompat

logger = logging.getLogger(__name__)


def convert_to_column(self, value, record, values=None):
    if value is None or value is False:
        return None
    # we need to convert the string to a unicode object to be able
    # to evaluate its length (and possibly truncate it) reliably
    return pycompat.to_text(value)[:self.size]


def convert_to_cache(self, value, record, validate=True):
    if value is None or value is False:
        return False
    return pycompat.to_text(value)[:self.size]


def patch_fields():

    Text = odoo.fields.Text
    slots = Text._slots
    slots['size'] = None
    setattr(Text, '_slots', slots)
    setattr(Text, 'convert_to_column', convert_to_column)
    setattr(Text, 'convert_to_column', convert_to_cache)
