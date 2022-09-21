from odoo import http, models
from odoo.http import request

from odoo.http import request
import json


# $$$$$$$$$$$$$$    MAST CONNECTOR AUTHENTICATION    &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class MastBeautyConnectorController(http.Controller):
    @http.route('/web/session/authenticate', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        session_details = request.env['ir.http'].session_info()
        return session_details


    @http.route('/web/get/product/category', type='json', auth='user')
    def get_mast_product_category(self):
        prod_categ_rec = request.env['product.category'].search([])
        product_categ_list = [{
            'id': rec.id,
            'name': rec.name,
            'parent_id': rec.parent_id.id,
            'parent_name': rec.parent_id.name,
            'costing_method': rec.property_cost_method,
            'inventory_valuation': rec.property_valuation,
            'income_account_name': rec.property_account_income_categ_id.name,
            'income_account': rec.property_account_income_categ_id.id,
            'expense_account_name': rec.property_account_expense_categ_id.name,
            'expense_account': rec.property_account_expense_categ_id.id

        } for rec in prod_categ_rec]

        return product_categ_list


    @http.route('/create/product/category', type='json', auth='user')
    def create_product_category(self, **rec):
        if rec:
            create_prod_category = request.env['product.category'].create({
                'name': rec.get('name'),
                # 'parent_id': rec.get('parent_id'),
                # 'property_cost_method': rec.get('costing_method'),
                # 'property_valuation': rec.get('inventory_valuation'),

            })
        return {'id': create_prod_category.id}

    #
    @http.route('/web/get/product/template', type='json', auth='user')
    def get_product_category(self):
        prod_template_rec = request.env['product.template'].search([])
        product_template_list = [{
            'id': rec.id,
            'can_be_sold': rec.sale_ok,
            'can_be_purchase': rec.purchase_ok,
            'product_type': rec.type,
            'product_category_id': rec.categ_id.id,
            'sale_price': rec.list_price,
            'cost_price': rec.standard_price,
        } for rec in prod_template_rec]

        return product_template_list

    @http.route('/create/product/template', type='json', auth='user')
    def create_product_template(self, **rec):
        if rec:
            # create_prod_category = request.env['product.template'].create({
            #     'name': rec.get('name'),
            # })
            for var in rec.get('variants'):
                create_attribute = request.env['product.attribute'].create({'name': var.get('attribute')})
                create_attribute_id = create_attribute.id
                # for vals in var.get('values'):
                create_values = [request.env['product.attribute.value'].create(
                    {'name': value, 'attribute_id': create_attribute.id}).id for value in var.get('values')]

                line_create = request.env['product.template'].create(
                    {
                        'name': rec.get('name'),
                        'list_price':rec.get('sale_price'),
                        'standard_price': rec.get('cost_price'),
                        'attribute_line_ids': [
                            (0, 0, {'attribute_id': create_attribute_id, 'value_ids': create_values, })]})

            return {'id': line_create.id}

    @http.route('/web/get/contacts', type='json', auth='user')
    def get_contacts(self):
        student_rec = request.env['res.partner'].search([])
        std_list = []
        for rec in student_rec:
            std_dic = {
                'id': rec.id,
                'name': rec.name,
                'email': rec.email,

            }
            std_list.append(std_dic)

        return std_list
