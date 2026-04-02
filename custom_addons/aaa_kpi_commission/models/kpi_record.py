from odoo import models, fields, api

class KPIRecord(models.Model):
    _name = 'kpi.commission'
    _description = 'Bản ghi Doanh thu KPI'

    name = fields.Char(string='Kỳ đánh giá', required=True, help="Ví dụ: 03/2026")
    employee_id = fields.Many2one('hr.employee', string='Nhân viên', required=True)
    department_id = fields.Many2one(related='employee_id.department_id', string='Phòng ban', store=True)
    actual_revenue = fields.Float(string='Doanh thu thực tế', required=True, default=0.0)
    commission_rate = fields.Float(string='Tỷ lệ Hoa hồng (%)', default=5.0)
    commission_amount = fields.Float(string='Tiền Hoa hồng', compute='_compute_commission', store=True)

    @api.depends('actual_revenue', 'commission_rate')
    def _compute_commission(self):
        for record in self:
            record.commission_amount = record.actual_revenue * (record.commission_rate / 100.0)