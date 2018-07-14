# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################
{
    "name": "Sale Order Extra Fields",
    "version": "1.0",
    "author": "Linserv AB",
    "category": "Sales",
    "summary": "Sale Order Extra Fields",
    "website": "www.linserv.se",
    "contributors": [
        'Gediminas Venclova <gediminasv@live.com>'
    ],
    "license": "",
    "depends": ['base', 'sale', 'website_quote'],
    'description': """
        
        Additional fields,
        Hides "Invoice Order" button in Sales Order, which prevents invoice creation from multiple sale orders,
        Sale Order's Estimate By field to Project.
        
    """,
    "demo": [],
    "data": [
        'views/inherited_sale.xml',
        'views/inherited_sale_order.xml',
        'views/inherited_sale_report_templates.xml',
    ],
    "test": [],
    "js": [],
    "css": [],
    "qweb": [],
    "installable": True,
    "auto_install": False,
}
