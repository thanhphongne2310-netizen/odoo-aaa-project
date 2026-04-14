from odoo import models, fields, api

class KpiRecord(models.Model):
    _name = 'kpi.record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Báo cáo Doanh thu và Hoa hồng KPI'

    name = fields.Char(string='Kỳ đánh giá', required=True, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Nhân viên', required=True, tracking=True)
    department_id = fields.Many2one('hr.department', string='Phòng ban', related='employee_id.department_id', store=True)
    
    # Quan hệ One2many để chứa danh sách các đơn bảo hiểm (Detail)
    line_ids = fields.One2many('kpi.record.line', 'kpi_id', string='Chi tiết doanh thu')

    # Các trường tổng hợp (Tổng doanh thu và Tổng hoa hồng)
    actual_revenue = fields.Float(string='Tổng phí bảo hiểm', compute='_compute_totals', store=True, tracking=True)
    total_commission = fields.Float(string='Tổng hoa hồng thực nhận', compute='_compute_totals', store=True, tracking=True)

    state = fields.Selection([
        ('draft', 'Nháp'),
        ('waiting', 'Chờ phê duyệt'),
        ('approved', 'Đã duyệt')
    ], default='draft', tracking=True)

    @api.depends('line_ids.revenue', 'line_ids.commission_amount')
    def _compute_totals(self):
        for rec in self:
            rec.actual_revenue = sum(line.revenue for line in rec.line_ids)
            rec.total_commission = sum(line.commission_amount for line in rec.line_ids)

# Lớp con lưu trữ từng dòng hợp đồng bảo hiểm
class KpiRecordLine(models.Model):
    _name = 'kpi.record.line'
    _description = 'Dòng chi tiết doanh thu bảo hiểm'

    kpi_id = fields.Many2one('kpi.record', string='Phiếu KPI gốc', ondelete='cascade')
    
    product_code = fields.Char(string='Mã Sản phẩm')
    contract_number = fields.Char(string='Số hợp đồng')
    revenue = fields.Float(string='Phí gốc')
    commission_rate = fields.Float(string='Tỷ lệ HH (%)')
    commission_amount = fields.Float(string='Tiền hoa hồng', compute='_compute_line_commission', store=True)

    @api.depends('revenue', 'commission_rate')
    def _compute_line_commission(self):
        for line in self:
            line.commission_amount = line.revenue * (line.commission_rate / 100.0)