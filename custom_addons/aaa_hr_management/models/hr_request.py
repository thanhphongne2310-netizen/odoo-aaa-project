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
    
    # Giữ lại trường content để ghi chú vi phạm
    content = fields.Text(string='Nội dung yêu cầu/Vi phạm')
    
    # --- THÊM 5 TRƯỜNG DỮ LIỆU CẤU TRÚC ĐỂ ĐỒNG BỘ ---
    new_department_id = fields.Many2one('hr.department', string='Phòng ban mới', tracking=True)
    new_job_id = fields.Many2one('hr.job', string='Vị trí công việc mới', tracking=True)
    new_parent_id = fields.Many2one('hr.employee', string='Người quản lý mới', tracking=True)
    new_work_email = fields.Char(string='Email công tác mới', tracking=True)
    new_work_phone = fields.Char(string='SĐT công tác mới', tracking=True)

    state = fields.Selection([
        ('draft', 'Nháp'),
        ('waiting', 'Chờ phê duyệt'),
        ('approved', 'Đã phê duyệt'),
        ('refused', 'Từ chối')
    ], default='draft', tracking=True)

    # -----------------------------------------------------------
    # 1. NÚT GỬI YÊU CẦU (Đã phân luồng tự động)
    # -----------------------------------------------------------
    def action_submit(self):
        for rec in self:
            if rec.request_type == 'violation':
                # Nếu là Vi phạm: Gọi thẳng hàm Duyệt để bỏ qua bước Chờ
                rec.action_approve()
            else:
                # Nếu là Cập nhật hồ sơ: Chuyển sang trạng thái chờ HR duyệt
                rec.state = 'waiting'
                rec.message_post(body="🚀 Đã gửi yêu cầu. Chờ phòng Nhân sự phê duyệt.")

    # -----------------------------------------------------------
    # 2. NÚT PHÊ DUYỆT (Xử lý lưu dữ liệu và Thông báo)
    # -----------------------------------------------------------
    def action_approve(self):
        for rec in self:
            # NHÁNH 1: TỰ ĐỘNG ĐỒNG BỘ DỮ LIỆU SANG MODULE NHÂN SỰ
            if rec.request_type == 'profile':
                update_data = {}
                
                if rec.new_department_id:
                    update_data['department_id'] = rec.new_department_id.id
                if rec.new_job_id:
                    update_data['job_id'] = rec.new_job_id.id
                if rec.new_parent_id:
                    update_data['parent_id'] = rec.new_parent_id.id
                if rec.new_work_email:
                    update_data['work_email'] = rec.new_work_email
                if rec.new_work_phone:
                    update_data['work_phone'] = rec.new_work_phone
                
                if update_data:
                    rec.employee_id.write(update_data)
                
                rec.employee_id.message_post(body="🔄 Hệ thống đã tự động đồng bộ hồ sơ từ phiếu yêu cầu.")
                rec.message_post(body="✅ Phê duyệt thành công. Dữ liệu đã ĐỒNG BỘ vào hồ sơ gốc!")

            # NHÁNH 2: LƯU VI PHẠM & BÁO CHO NHÂN VIÊN
            if rec.request_type == 'violation':
                # Ghi nối thêm vi phạm vào phần Ghi chú của nhân viên
                rec.employee_id.notes = (rec.employee_id.notes or "") + f"\n- Vi phạm: {rec.content}"
                
                # Bắn thông báo thẳng vào hồ sơ nhân viên (Nhân viên sẽ nhận được email/thông báo góc phải)
                rec.employee_id.message_post(body=f"⚠️ CẢNH BÁO VI PHẠM: Bạn vừa bị ghi nhận lỗi: '{rec.content}'. Vui lòng kiểm tra lại!")
                
                rec.message_post(body="🚩 Vi phạm đã được ghi nhận trực tiếp vào hồ sơ và đã gửi thông báo cho nhân viên.")

            # Đổi trạng thái phiếu thành Đã phê duyệt
            rec.state = 'approved'

    # -----------------------------------------------------------
    # 3. NÚT TỪ CHỐI (ĐÃ ĐỔI TÊN THÀNH action_reject ĐỂ TRÁNH LỖI)
    # -----------------------------------------------------------
    def action_reject(self):
        for rec in self:
            rec.state = 'refused'
            rec.message_post(body="❌ Yêu cầu bị từ chối do dữ liệu không hợp lệ.")