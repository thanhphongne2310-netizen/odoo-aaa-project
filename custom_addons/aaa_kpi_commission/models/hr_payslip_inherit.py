from . import kpi_record
from . import hr_payslip_inherit

class HrPayslip(models.Model):
    _inherit = 'hr.payslip' # Lệnh bám vào module Bảng lương gốc

    # Chèn thêm trạng thái "waiting_director" vào trường state có sẵn của Odoo
    state = fields.Selection(selection_add=[
        ('waiting_director', 'Chờ Giám đốc duyệt')
    ], ondelete={'waiting_director': 'set default'})

    # 1. Nút nhân viên/HR trình lên Giám đốc
    def action_submit_director(self):
        for rec in self:
            rec.state = 'waiting_director'
            rec.message_post(body="🚀 Bảng lương đã được trình lên Ban Giám đốc. Chờ phê duyệt.")

    # 2. Nút Giám đốc phê duyệt
    def action_director_approve(self):
        for rec in self:
            # Sau khi duyệt, gọi thẳng hàm chốt lương mặc định của Odoo để nó chuyển sang trạng thái Hoàn thành (Done)
            rec.action_payslip_done() 
            rec.message_post(body="✅ Giám đốc đã PHÊ DUYỆT bảng lương. Sẵn sàng chi trả!")

    # 3. Nút Giám đốc từ chối
    def action_director_reject(self):
        for rec in self:
            rec.state = 'draft' # Đẩy về lại trạng thái Nháp cho HR sửa
            rec.message_post(body="❌ Giám đốc đã TỪ CHỐI bảng lương. Vui lòng kiểm tra lại số liệu.")