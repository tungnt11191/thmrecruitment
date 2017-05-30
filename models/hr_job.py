# -*- coding: utf-8 -*-
from odoo import models, fields, api

from odoo.exceptions import UserError, ValidationError
#Import logger
import logging
#Get the logger
_logger = logging.getLogger(__name__)

#External import
import datetime
import requests, json

class scheduler_demo(models.Model):
    _inherit = "hr.job"
    code = fields.Char(string='Code', required=True, index=True)

    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'Code must be unique'),
    ]
    @api.multi
    def sync(self):
        url = 'http://192.168.5.246/www/career/blog/odoo/test_python'
        payload = {'param1' : 1}
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        # self.env['hr.job'].create({
        #     'name': 'Job Title',
        #     'code': 'test'
        # })

        # self.env['hr.job'].browse(11).write({
        #     'name': 'Job Title wrtie',
        #     'code': 'test'
        # })

        jobs = json.loads(response.text)

        Hr_Job = self.env['hr.job']
        for j in jobs:
            exist_job = Hr_Job.search([('code', '=', j.get('id'))])
            data = {
                'name': j.get('job_name'),
                'code': j.get('id'),
            }
            if(exist_job):
                Hr_Job.browse(exist_job[0].id).write(data)
            else:
                self.env['hr.job'].create(data)

        return response