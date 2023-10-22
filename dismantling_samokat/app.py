from flask import Flask
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from database import db
from models import MainLinks, ProductsFamilie, Product


app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567'

class MyAdminIndexView(AdminIndexView):
    @expose('/admin')
    def default_view(self):
        print(self.__dict__)
        return self.render('admin/index.html')

    def is_accessible(self):
        try:
            return True
        except Exception:
            pass

admin = Admin(
    app,
    name='',
    static_url_path='admin/static/',
    template_mode='bootstrap3',
    index_view=MyAdminIndexView(
        name='Админка',
        menu_icon_type='glyph',
        menu_icon_value='glyphicon-send',
    ),
)

admin.add_views(ModelView(MainLinks, db))
admin.add_views(ModelView(ProductsFamilie, db))
admin.add_views(ModelView(Product, db))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
