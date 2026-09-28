# -*- coding: utf-8 -*-
# vim: tabstop=4 softtabstop=0 shiftwidth=4 smarttab expandtab fileformat=unix
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
{
    'name': "Delivery Address To Outgoing Transfers",
    'summary': "Auto-update the delivery address on open outgoing transfers when it changes on the order",
    'description': """
Delivery Address To Outgoing Transfers
========================================

Changing the delivery address on a confirmed sale order only gets you a
warning from core Odoo ("you may want to update the deliveries too") - the
related outgoing transfer keeps the old address until someone edits it by
hand.

This app does that update for you: whenever the delivery address changes on
an order, every related, not-yet-done outgoing transfer is updated to match,
with a note in both the order's and the transfer's chatter.
""",
    'version': "19.0.1.0.0",
    'author': "Hadron for Business sp. z o.o.",
    'website': "http://hadronforbusiness.com",
    'license': "OPL-1",
    'category': "Inventory/Inventory",
    'depends': [
        'sale_stock',
    ],
    'data': [],
    'images': [
        'static/description/banner_screenshot.png',
    ],
    'installable': True,
    'application': False,
}
