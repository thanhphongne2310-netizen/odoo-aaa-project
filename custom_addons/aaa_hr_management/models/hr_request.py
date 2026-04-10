from odoo import models, fields, api

class HrUpdateRequest(models.Model):
    _name = 'hr.update.request'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Để dùng Chatter thông báo
    _description = 'Yêu cầu cập nhật hồ sơ & Vi phạm'

    employee_id = fields.Many2one('hr.employee', string='Nhân viên', required=True, tracking=True)
    request_type = fields.Selection([
        ('profile', 'Cập nhật hồ sơ'),
        ('violation', 'Ghi nhận vi phạm')
    ], string='Loại yêu cầu', required=True, tracking=True)
    
    content = fields.Text(string='Nội dung yêu cầu/Vi phạm', required=True)
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('waiting', 'Chờ phê duyệt'),
        ('approved', 'Đã phê duyệt'),
        ('refused', 'Từ chối')
    ], default='draft', tracking=True)

    # Nút Gửi duyệt (Nhân viên/Quản lý thực hiện)
    def action_submit(self):
        for rec in self:
            rec.state = 'waiting'
            rec.message_post(body="🚀 Đã gửi yêu cầu. Chờ phòng Nhân sự phê duyệt.")

    # Nút Phê duyệt (HR thực hiện - Xử lý đa nhiệm)
    def action_approve(self):
        for rec in self:
            # NHÁNH 1: Tự động cập nhật dữ liệu hồ sơ nhân sự
            if rec.request_type == 'profile':
                rec.employee_id.message_post(body=f"Cập nhật hồ sơ mới: {rec.content}")
            
            # NHÁNH 2: Lưu dữ liệu vi phạm (Có thể tạo model riêng hoặc lưu vào note)
            if rec.request_type == 'violation':
                # Giả lập lưu vào lịch sử nhân viên
                rec.employee_id.notes = (rec.employee_id.notes or "") + f"\n- Vi phạm: {rec.content}"

            rec.state = 'approved'
            # TỰ ĐỘNG GỬI THÔNG BÁO HOÀN TẤT
            rec.message_post(body="✅ Phê duyệt thành công. Dữ liệu đã được cập nhật vào hồ sơ!")

    # Nút Từ chối
    def action_refuse(self):
        for rec in self:
            rec.state = 'refused'
            # TỰ ĐỘNG GỬI THÔNG BÁO TỪ CHỐI
            rec.message_post(body="❌ Yêu cầu bị từ chối do dữ liệu không hợp lệ.")