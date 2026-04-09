from odoo import models, fields, api

class KpiCommission(models.Model):
    _name = 'kpi.commission'
    _description = 'Quản lý KPI'

    # 1. Khai báo trường Trạng thái với 3 bước
    state = fields.Selection([
        ('draft', 'Nháp (Draft)'),
        ('waiting', 'Chờ duyệt (Waiting)'),
        ('approved', 'Đã duyệt (Approved)')
    ], string='Trạng thái', default='draft', tracking=True)

    name = fields.Char(string='Kỳ đánh giá', required=True, help="Ví dụ: 03/2026")
    employee_id = fields.Many2one('hr.employee', string='Nhân viên', required=True)
    department_id = fields.Many2one(related='employee_id.department_id', string='Phòng ban', store=True)
    actual_revenue = fields.Float(string='Doanh thu thực tế', required=True, default=0.0)
    target_revenue = fields.Float(string='Chỉ tiêu Doanh thu', required=True, default=40000000)
    commission_rate = fields.Float(string='Tỷ lệ Hoa hồng (%)', default=5.0)
    commission_amount = fields.Float(string='Tiền Hoa hồng', compute='_compute_commission', store=True)

   # 2. Khai báo các hàm để nút bấm gọi tới
    def action_submit(self):
        # Chuyển trạng thái từ Nháp sang Chờ duyệt
        for record in self:
            record.state = 'waiting'

    def action_approve(self):
        # Chuyển trạng thái sang Đã duyệt
        for record in self:
            record.state = 'approved'

    def action_reject(self):
        # Từ chối thì đẩy trả về Nháp để sửa
        for record in self:
            record.state = 'draft'