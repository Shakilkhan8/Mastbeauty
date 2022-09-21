# -*- coding: utf-8 -*-
import requests
import base64
from odoo import models, fields, api, _


class LaravelInheritProductCategory(models.Model):
    _inherit = "product.category"
    unique_id = fields.Char(required=False)


class LaravelInheritProductBrand(models.Model):
    _inherit = "product.brand"
    unique_id = fields.Char(required=False)

class LaravelInheritRespartner(models.Model):
    _inherit = "res.partner"
    unique_id = fields.Char(required=False)

class LaravelInheritProductTemplate(models.Model):
    _inherit = "product.template"
    unique_id = fields.Char(required=False)


class LaravelConnectorOperations(models.TransientModel):
    _name = 'laravel.connector.operations'

    name = fields.Selection(string="Select Operation",
                            selection=[('p_category', 'Product Category'), ('p_brand', 'Product Brand'),('product', 'Product'),('customer', 'Customer') ],
                            required=True, )

    def create_product_category(self, *data):
        if data:
            for li in data:
                for rec in li:
                    unique_id = self.env['product.category'].search([]).mapped('unique_id')
                    if not rec['unique_id'] in unique_id:
                        category = self.env['product.category'].create({
                            'name': rec['name'],
                            'unique_id': rec['unique_id']
                        })
                    if rec['subcatagory']:
                        if category:
                            parent_category_for_sub = category.id
                        else:
                            parent_category_for_sub = self.env['product.category'].search([('unique_id','=',rec['unique_id'])]).id
                        for subcateg in rec['subcatagory']:
                            if not subcateg['unique_id'] in unique_id:
                                sub_category = self.env['product.category'].create({
                                'name': subcateg['name'],
                                'parent_id': parent_category_for_sub,
                                'unique_id': subcateg['unique_id']
                            })
                            if subcateg['subtosub_catagory']:
                                if sub_category:
                                    parent_category_for_sub_sub = sub_category.id
                                else:
                                    parent_category_for_sub_sub = self.env['product.category'].search([('unique_id','=',subcateg['unique_id'])]).id
                                for subsubcateg in subcateg['subtosub_catagory']:
                                    if not subsubcateg['unique_id'] in unique_id:
                                        sub_sub__category = self.env['product.category'].create({
                                        'name': subsubcateg['name'],
                                        'parent_id': parent_category_for_sub_sub ,
                                        'unique_id': subsubcateg['unique_id']
                                    })

    def create_product_brand(self, *data):
        if data:
            for li in data:
                for rec in li:
                    unique_id = self.env['product.brand'].search([]).mapped('unique_id')
                    if not str(rec['id']) in unique_id:
                        self.env['product.brand'].create({
                            'name': rec['name'],
                            'unique_id': rec['id']
                        })

    def create_laravel_customers(self,*data):
        if data:
            for li in data:
                for rec in li:
                    # fff = self.env['res.partner'].browse(14)
                    # img = rec['image_user']
                    # b_img = requests.post(url=img).content
                    unique_id = self.env['res.partner'].search([]).mapped('unique_id')
                    if not str(rec['id']) in unique_id:
                        self.env['res.partner'].create({
                            'name': rec['name'],
                            'unique_id': rec['id'],
                            'phone': rec['phone'],
                            'email': rec['email'],
                            # 'image_1920': b_img,
                        })

    def create_laravel_products(self, *data):
        if data:
            for li in data:
                for rec in li:
                    unique_id = self.env['product.template'].search([]).mapped('unique_id')
                    if not str(rec['id']) in unique_id:
                        self.env['product.template'].create({
                            'name': rec['title'],
                            'unique_id': rec['id'],
                            'barcode': rec['sku'],
                        })

    def sync_action(self):
        for rec in self:
            if rec.name == 'p_category':
                try:
                    request_data = requests.post(url='https://mastbeauty.com/api/get-category/')
                    collected_data = request_data.json().get('data')
                    rec.create_product_category(collected_data)
                except Exception as e:
                    print(e)

            if rec.name == 'p_brand':
                try:
                    request_data = requests.post(url='https://mastbeauty.com/api/get-brand/')
                    collected_data = request_data.json().get('data')
                    rec.create_product_brand(collected_data)
                except Exception as e:
                    print(e)

            if rec.name == 'customer':
                try:
                    request_data = requests.post(url='https://mastbeauty.com/api/get-users/')
                    collected_data = request_data.json().get('data')
                    rec.create_laravel_customers(collected_data)
                except Exception as e:
                    print(e)

            if rec.name == 'product':
                try:
                    request_data = requests.post(url='https://mastbeauty.com/api/get-product/')
                    collected_data = request_data.json().get('data')
                    rec.create_laravel_products(collected_data)
                except Exception as e:
                    print(e)
