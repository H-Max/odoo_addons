# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Smile (<http: //www.smile.fr>). All Rights Reserved
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
#    along with this program.  If not, see <http: //www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv


class product_product(osv.osv):
    _inherit = "product.product"

    _columns = {
        'invoicing_plan_id': fields.many2one('account.invoicing_plan', 'Invoicing Plan'),
        'subscription_ok': fields.boolean('Is subscription', required=False),
    }

    _defaults = {
        'subscription_ok': lambda * a: False,
        }
product_product()