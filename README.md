# Delivery Address To Outgoing Transfers

Keeps a sale order's delivery address and its related outgoing transfers in
sync - automatically.

## The problem

Change the delivery address on a confirmed sale order and Odoo's own
`sale_stock` only pops up a warning suggesting you also update the related
deliveries. It doesn't do it for you - the outgoing transfer keeps the old
address until someone edits it by hand.

## How it works

- `sale.order.write()` detects a `partner_shipping_id` change and, after the
  write goes through, calls `_propagate_shipping_address_to_pickings()`.
- That method updates `partner_id` on every related outgoing transfer that
  is not yet `done`/`cancel`, and posts a note on both the transfer and the
  order.
- The native onchange warning message is replaced with one saying the
  update will happen automatically on save, instead of asking the user to
  do it by hand.

## Technical

- `models/sale_order_delivery_address_to_wz.py`
- No new models, no views, no data, no security rules.
- Depends on: `sale_stock`.

## Status

Extracted from a client-specific module (`hfb_bannerstop_invoice_total`) as
part of the generic app extraction workflow. Missing
`static/description/icon.png` (and optionally a `*_screenshot.png`) before
it can be submitted to Odoo Apps.
