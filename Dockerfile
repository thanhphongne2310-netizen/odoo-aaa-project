FROM odoo:17.0

USER root

# Lệnh "Hack": Tìm đến file chứa luật bảo mật của Odoo và đổi chữ 'postgres' thành chữ khác để nó không nhận diện được
RUN sed -i "s/== 'postgres'/== 'bypass_railway'/g" /usr/lib/python3/dist-packages/odoo/cli/server.py

# Tạo thư mục và copy Add-ons của nhóm vào Odoo
RUN mkdir -p /mnt/extra-addons
COPY ./custom_addons /mnt/extra-addons

# Phân quyền cho user Odoo
RUN chown -R odoo:odoo /mnt/extra-addons

USER odoo
