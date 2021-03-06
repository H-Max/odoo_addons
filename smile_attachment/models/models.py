# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Smile (<http://www.smile.fr>). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from lxml import etree

from openerp import api, fields
from openerp.models import Model

native__init__ = Model.__init__
native_fields_view_get = Model.fields_view_get


def _get_attachments_field_name(self):
    name = 'attachment_ids'
    if self._inherits:
        name = 'attachment_%s_ids' % self._table
    return name


@api.one
@api.depends()
def _get_attachments(self):
    name = self._get_attachments_field_name()
    setattr(self, name, False)


def _search_attachments(self, operator, value):
    recs = self.env['ir.attachment'].search([('res_model', '=', self._name),
                                             '|', '|',
                                             ('description', operator, value),
                                             ('index_content', operator, value),
                                             ('datas_fname', operator, value)])
    return [('id', 'in', [rec.res_id for rec in recs])]


def new__init__(self, pool, cr):
    native__init__(self, pool, cr)
    name = self._get_attachments_field_name()
    if name not in self._fields and name not in self._columns:
        field = fields.One2many('ir.attachment', None, 'Attachments', automatic=True,
                                compute='_get_attachments', search='_search_attachments')
        self._add_field(name, field)


@api.v7
def new_fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
    res = native_fields_view_get(self, cr, uid, view_id, view_type, context, toolbar, submenu)
    name = self._get_attachments_field_name()
    if view_type == 'search' and (name in self._fields or name in self._columns):
        View = self.pool['ir.ui.view']
        arch_etree = etree.fromstring(res['arch'])
        element = etree.Element('field', name=name)
        arch_etree.insert(-1, element)
        res['arch'], res['fields'] = View.postprocess_and_fields(cr, uid, self._name, arch_etree, view_id, context=context)
    return res


@api.v8
def new_fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    res = native_fields_view_get(self, view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    name = self._get_attachments_field_name()
    if view_type == 'search' and (name in self._fields or name in self._columns):
        View = self.env['ir.ui.view']
        arch_etree = etree.fromstring(res['arch'])
        element = etree.Element('field', name=name)
        arch_etree.insert(-1, element)
        res['arch'], res['fields'] = View.postprocess_and_fields(self._name, arch_etree, view_id)
    return res

Model._get_attachments_field_name = _get_attachments_field_name
Model.__init__ = new__init__
Model._get_attachments = _get_attachments
Model._search_attachments = _search_attachments
Model.fields_view_get = new_fields_view_get
