{
    'name': 'Hoa Hồng', 
    'version': '1.0',
    'summary': 'Quản lý KPI và Doanh thu Hoa hồng cho công ty AAA',
    'author': 'Tô Thanh Phong', # Thêm tên bạn vào cho chuyên nghiệp
    'website': 'https://www.yourwebsite.com',
    
    # 1. PHẦN QUAN TRỌNG: Thêm 'om_hr_payroll' để kế thừa bảng lương
    # Nếu bạn dùng bản Enterprise thì đổi thành 'hr_payroll'
    'depends': ['base', 'hr', 'mail', 'om_hr_payroll'], 
    
    'data': [
        'security/ir.model.access.csv',
        'views/kpi_views.xml',
        # 2. PHẦN QUAN TRỌNG: Khai báo file giao diện phê duyệt bảng lương
        'views/hr_payslip_inherit_views.xml', 
    ],
    
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}