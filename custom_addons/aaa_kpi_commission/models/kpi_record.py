from odoo import models, fields, api

class KpiCommission(models.Model):
    _name = 'kpi.commission'
    _description = 'Quản lý KPI'

    # KẾ THỪA TÍNH NĂNG CHATTER (GỬI TIN NHẮN & LỊCH SỬ) CỦA ODOO
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # 1. Khai báo trường Trạng thái với 3 bước
    state = fields.Selection([
        ('draft', 'Nháp (Draft)'),
        ('waiting', 'Chờ duyệt (Waiting)'),
        ('approved', 'Đã duyệt (Approved)')
    ], string='Trạng thái', default='draft', tracking=True)

    # Thêm tracking=True để tự động ghi log khi có người sửa dữ liệu
    name = fields.Char(string='Kỳ đánh giá', required=True, help="Ví dụ: 03/2026")
    employee_id = fields.Many2one('hr.employee', string='Nhân viên', required=True, tracking=True)
    department_id = fields.Many2one(related='employee_id.department_id', string='Phòng ban', store=True)
    actual_revenue = fields.Float(string='Doanh thu thực tế', required=True, default=0.0, tracking=True)
    target_revenue = fields.Float(string='Chỉ tiêu Doanh thu', required=True, default=40000000.0, tracking=True)
    commission_rate = fields.Float(string='Tỷ lệ Hoa hồng (%)', default=5.0)
    
    # Trường tự động tính toán
    commission_amount = fields.Float(string='Tiền Hoa hồng', compute='_compute_commission', store=True, tracking=True)

    # --- ĐOẠN HÀM TÍNH TOÁN ---
    @api.depends('actual_revenue', 'target_revenue', 'commission_rate')
    def _compute_commission(self):
        for record in self:
            # Nếu Doanh thu thực tế >= Chỉ tiêu
            if record.actual_revenue >= record.target_revenue and record.target_revenue > 0:
                # Tính hoa hồng = Doanh thu thực tế * Tỷ lệ %
                record.commission_amount = record.actual_revenue * (record.commission_rate / 100.0)
            else:
                # Không đạt thì tiền hoa hồng = 0
                record.commission_amount = 0.0
    # -----------------------------------------------------

    # 2. Khai báo các hàm để nút bấm gọi tới (Thanh trạng thái)
    def action_submit(self):
        for record in self:
            record.state = 'waiting'

    def action_approve(self):
        for record in self:
            record.state = 'approved'

    def action_reject(self):
        for record in self:
            record.state = 'draft'
            
            # TỰ ĐỘNG GỬI THÔNG BÁO XUỐNG CHATTER KHI TỪ CHỐI
            record.message_post(
                body="⚠️ Quản lý đã TỪ CHỐI phiếu KPI này. Vui lòng kiểm tra lại số liệu và gửi duyệt lại!",
                subject="Thông báo từ chối KPI"
            )