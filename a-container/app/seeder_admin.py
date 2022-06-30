from datetime import date
from app import db, app
from models import *
from werkzeug.security import generate_password_hash, check_password_hash


def seeder():

    models = [User, Customer, Item, Invoice,
              Invoice_Item, Quotation, Quotation_Item, Memo, Unit, Category, Maker, History, Setting]

    for model in models:
        db.session.query(model).delete()
        db.session.commit()

    # -----Users-----
    print('----Users----')
    users = [
        User(id=1, anyNumber=9999, name='admin', password=generate_password_hash('password'),
             group='operator', role='admin'),
    ]
    db.session.add_all(users)
    db.session.commit()

    users = User.query.all()
    for user in users:
        print(user.name)

    # -----Units-----
    print('----Units----')
    units = [
        Unit(id=1, unitName='個'),
        Unit(id=2, unitName='本'),
        Unit(id=3, unitName='台'),
        Unit(id=4, unitName='式'),
    ]
    db.session.add_all(units)
    db.session.commit()

    units = Unit.query.all()
    for unit in units:
        print(unit.unitName)

    # -----Setting-----
    print('----Setting----')
    setting = [
        Setting(id=1, logoFilePath='./static/asset/logo/logo.png', logoHeight=60, logoWidth=60, stampFilePath='./static/asset/stamp/inkan.png', stampHeight=60, stampWidth=60,
                isDisplayQuotationLogo=True, isDisplayInvoiceLogo=True, isDisplayDeliveryLogo=True, isDisplayQuotationStamp=True, isDisplayInvoiceStamp=True, isDisplayDeliveryStamp=True, defaultTax=10)
    ]
    db.session.add_all(setting)
    db.session.commit()

    setting = Setting.query.all()
    print(setting[0].defaultTax)


if __name__ == '__main__':
    seeder()
