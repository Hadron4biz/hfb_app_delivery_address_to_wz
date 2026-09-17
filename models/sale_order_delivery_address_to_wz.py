# -*- coding: utf-8 -*-
#################################################################################
#
# Odoo, Open Source Management Solution
# Copyright (C) 2017-2026 Hadron for Business sp. z o.o. (http://hadronforbusiness.com)
#
# This program is proprietary software, licensed under the Odoo Proprietary
# License v1.0 (OPL-1). Its use is governed by the Odoo Apps terms available
# at https://www.odoo.com/documentation/user/legal/licenses.html and the
# license agreement accepted at purchase / installation.
#
# It is forbidden to publish, distribute, sublicense, or sell copies of the
# Software or modified copies of the Software.
#
# The above copyright notice and this permission notice must be included in
# all copies or substantial portions of the Software.
#
#################################################################################
""" @version	17.0.1.0.0
	@owner  Hadron for Business
	@author Hadron for Business sp. z o.o.
	@date   2026.09.17

	Delivery Address To Outgoing Transfers
	Propagates a delivery address change on a sale order to its related,
	not-yet-done outgoing transfers - core Odoo only warns about the
	mismatch, it never updates the transfer itself.
"""
from odoo import _, api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        # Changing the delivery address on the order should carry over to
        # its related, not-yet-done outgoing transfers - core Odoo only
        # shows a warning, the transfer is left with the old address.
        shipping_changed = self.browse()
        if vals.get('partner_shipping_id'):
            shipping_changed = self.filtered(
                lambda o: o.partner_shipping_id.id != vals['partner_shipping_id']
            )

        res = super().write(vals)

        if shipping_changed:
            shipping_changed._propagate_shipping_address_to_pickings()

        return res

    def _propagate_shipping_address_to_pickings(self):
        """Copy the order's delivery address onto its related, not-yet-done
        outgoing transfers. Called after partner_shipping_id changes on a
        confirmed order."""
        for order in self:
            pickings = order.picking_ids.filtered(
                lambda p: p.state not in ('done', 'cancel')
                and p.picking_type_code == 'outgoing'
                and p.partner_id != order.partner_shipping_id
            )
            if not pickings:
                continue

            pickings.write({'partner_id': order.partner_shipping_id.id})

            for picking in pickings:
                picking.message_post(body=_(
                    "Delivery address automatically updated from order "
                    "%(order)s to: %(addr)s",
                    order=order.name,
                    addr=order.partner_shipping_id.display_name,
                ))

            order.message_post(body=_(
                "Delivery address propagated to outgoing transfers: %s",
                ", ".join(pickings.mapped('name')),
            ))

    @api.onchange('partner_shipping_id')
    def _onchange_partner_shipping_id(self):
        # Replace the native "don't forget to update the deliveries"
        # warning (sale_stock) with one saying the update will happen
        # automatically.
        _super = getattr(super(), '_onchange_partner_shipping_id', None)
        res = _super() if _super else None
        if isinstance(res, dict) and res.get('warning'):
            pickings = self.picking_ids.filtered(
                lambda p: p.state not in ('done', 'cancel')
                and p.picking_type_code == 'outgoing'
            )
            if pickings:
                res['warning']['message'] = _(
                    "The delivery address will be automatically updated on "
                    "the related outgoing transfers (%s) when the order is "
                    "saved.",
                    ", ".join(pickings.mapped('name')),
                )
        return res

#EoF
