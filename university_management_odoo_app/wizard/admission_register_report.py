# -*- coding: utf-8 -*-

import logging

_logger = logging.getLogger(__name__)
from xlwt import easyxf
import io
from odoo import api, fields, models, _

try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')

try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class AdmissionRegisterReport(models.TransientModel):
    _name = "admission.register.report"
    _description = "Employee Payslip"

    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")
    course_id = fields.Many2one('university.course', string="Course")

    def action_excel_report(self):
        # Create an new Excel file and add a worksheet.
        import base64
        self.ensure_one()
        filename = 'admission_register_report.xls'
        workbook = xlwt.Workbook(encoding="utf-8")
        style = xlwt.XFStyle()
        worksheet = workbook.add_sheet('Sheet 1')
        heading_style = easyxf(
            'font:name Arial, bold on,height 300, color  dark_green; align: vert centre, horz center ;')
        first_col = worksheet.col(0)
        first_col.width = 256 * 30
        second_col = worksheet.col(1)
        second_col.width = 256 * 20
        three_col = worksheet.col(2)
        three_col.width = 256 * 20
        four_col = worksheet.col(5)
        four_col.width = 256 * 30
        five_col = worksheet.col(7)
        five_col.width = 256 * 20
        small_heading_style = easyxf(
            'font:  name  Century Gothic, bold on, color white , height 230 ; pattern: pattern solid,fore-colour dark_green; align: vert centre, horz center ;')
        bold = easyxf('font: bold on ')
        company_id = self.env.user.company_id
        worksheet.write_merge(0, 3, 0, 10, company_id.name, heading_style)
        worksheet.write_merge(4, 4, 0, 10, 'Admission Registration Report', small_heading_style)
        worksheet.write(5, 0, 'Start Date', bold)
        worksheet.write(5, 1, self.date_start.strftime("%d-%m-%Y"), bold)
        worksheet.write(5, 3, 'End Date', bold)
        worksheet.write(5, 4, self.date_end.strftime("%d-%m-%Y"), bold)
        row = 6
        col = 0
        worksheet.write(row, col, 'Student Name', bold)
        col += 1
        worksheet.write(row, col, 'Student Mobile No', bold)
        col += 1
        worksheet.write(row, col, 'Student Date Of Birth', bold)
        col += 1
        worksheet.write(row, col, 'Student Email', bold)
        col += 1
        worksheet.write(row, col, 'Application No', bold)
        col += 1
        worksheet.write(row, col, 'Course', bold)
        col += 1
        worksheet.write(row, col, 'Application Date', bold)
        col += 1
        worksheet.write(row, col, 'Admission Date', bold)
        col += 1
        worksheet.write(row, col, 'Batch', bold)
        col += 1
        worksheet.write(row, col, 'Fess', bold)
        col += 1
        worksheet.write(row, col, 'Academic Year', bold)
        col += 1
        row += 1

        registration_ids = self.env['admission.registration'].search([('course_id', '=', self.course_id.id),
                                                                      ('application_date', '>=', self.date_start),
                                                                      ('application_date', '<=', self.date_end)])
        for registration_id in registration_ids:
            col = 0
            worksheet.write(row, col, registration_id.student_name or '', )
            col += 1
            worksheet.write(row, col, registration_id.mobile or '', )
            col += 1
            if registration_id.date_of_birth:
                dob = registration_id.date_of_birth.strftime("%d-%m-%Y")
            else:
                dob = ''
            worksheet.write(row, col, dob or '', )
            col += 1
            worksheet.write(row, col, registration_id.email or '', )
            col += 1
            worksheet.write(row, col, registration_id.name or '', )
            col += 1
            worksheet.write(row, col, registration_id.course_id.name or '', )
            col += 1
            if registration_id.application_date:
                app_d = registration_id.date_of_birth.strftime("%d-%m-%Y")
            else:
                app_d = ''
            worksheet.write(row, col, app_d or '', )
            col += 1
            if registration_id.admission_date:
                adm_d = registration_id.date_of_birth.strftime("%d-%m-%Y")
            else:
                adm_d = ''
            worksheet.write(row, col, adm_d or '', )
            col += 1
            worksheet.write(row, col, registration_id.batch_id.name or '', )
            col += 1
            worksheet.write(row, col, registration_id.fees or '', )
            col += 1
            worksheet.write(row, col, registration_id.academic_year or '', )
            col += 1
            row += 1


        fp = io.BytesIO()

        workbook.save(fp)
        export_id = self.env['admission.register.excel.report'].create(
            {'excel_file': base64.encodestring(fp.getvalue()), 'file_name': filename})
        return {
            'view_mode': 'form',
            'res_id': export_id.id,
            'name': 'Admission Registration Report',
            'res_model': 'admission.register.excel.report',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


class AdmissionRegisterReport(models.TransientModel):
    _name = "admission.register.excel.report"
    _description = " Excel Report"

    excel_file = fields.Binary('Salary Monthly Excel Report', readonly=True)
    file_name = fields.Char('Excel File', size=64, readonly=True)
