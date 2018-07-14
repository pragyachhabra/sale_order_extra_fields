# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import re


class SaleOrderExtraFieldsSaleOrder(models.Model):
    _inherit = "sale.order"

    customer_po_nr = fields.Char(string='Customer PO No.')

    quote_estimator = fields.Many2one('res.users', string='Estimate By', states={'draft': [('readonly', False)]},
                                      readonly=True)

    ptc_opp_ref = fields.Char(string='PTC Opportunity ID')
    ptc_maint_ref = fields.Char(string='PTC Maintenance ID')
    project_desc = fields.Text()

    show_attendee = fields.Boolean(readonly=True, compute='_compute_attendees')
    attendees_number = fields.Integer(readonly=True, compute='_compute_attendees')

    @api.model
    def create(self, vals):
        res = super(SaleOrderExtraFieldsSaleOrder, self).create(vals)

        if res.quote_estimator and not any(msg_follower.partner_id.id == res.quote_estimator.partner_id.id for msg_follower in res.message_follower_ids):
            gen, part = res.env['mail.followers'].\
                _add_follower_command(res._name, res.ids, {res.quote_estimator.partner_id.id: None}, {}, force=False)
            res.write({'message_follower_ids': gen})

        return res

    @api.multi
    def write(self, vals):
        res = super(SaleOrderExtraFieldsSaleOrder, self).write(vals)

        if 'quote_estimator' in vals:
            gen, part = self.env['mail.followers'].\
                _add_follower_command(self._name, self.ids, {self.quote_estimator.partner_id.id: None}, {}, force=False)
            self.write({'message_follower_ids': gen})

        return res

    @api.model
    def hide_invoice_order_button(self):
        """method to unbind Invoice Order button in sale order tree view"""
        invoice_order_action = self.env.ref('sale.action_view_sale_advance_payment_inv')
        if invoice_order_action and invoice_order_action.binding_model_id:
            invoice_order_action.binding_model_id = False

    @api.multi
    def action_confirm(self):
        return super(SaleOrderExtraFieldsSaleOrder, self.with_context(customer=self.partner_id, ptc_opp_ref=self.ptc_opp_ref, ptc_maint_ref=self.ptc_maint_ref)).action_confirm()


class SaleOrderExtraFieldsSaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _timesheet_find_project(self):
        return super(SaleOrderExtraFieldsSaleOrderLine, self.with_context(so_quote_estimator=self.order_id.quote_estimator))._timesheet_find_project()


class SaleOrderExtraFieldsSaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def create_invoices(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        customer_po_nrs = ''
        for order in sale_orders:
            customer_po_nrs += order.customer_po_nr + ', ' if order.customer_po_nr else ''
        if customer_po_nrs:
            customer_po_nrs = customer_po_nrs[:-2]
        return super(SaleOrderExtraFieldsSaleAdvancePaymentInv, self.with_context(customer_po_nrs=customer_po_nrs)).create_invoices()
