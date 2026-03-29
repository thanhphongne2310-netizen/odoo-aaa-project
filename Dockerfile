
FROM odoo:17.0

USER root

# Tạo thư mục và copy Add-ons của nhóm vào Odoo
RUN mkdir -p /mnt/extra-addons
COPY ./custom_addons /mnt/extra-addons

# Phân quyền cho user Odoo
RUN chown -R odoo:odoo /mnt/extra-addons

USER odoo