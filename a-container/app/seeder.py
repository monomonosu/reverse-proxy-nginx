from datetime import date
from app import db, app
from models import *
from werkzeug.security import generate_password_hash, check_password_hash


def seeder():

    models = [User, Customer, Item, Invoice,
              Invoice_Item, Invoice_Payment, Quotation, Quotation_Item, Memo, Unit, Category, Maker, History, Setting]

    for model in models:
        db.session.query(model).delete()
        db.session.commit()

    # -----Users-----
    print('----Users----')
    users = [
        User(id=1, anyNumber=1, anyName='田中太郎', name='tanaka_taro', password=generate_password_hash('password'),
             group='operator', role='crescom_support'),
        User(id=2, anyNumber=2, anyName='鈴木次郎', name='suzuki_jiro', password=generate_password_hash('password'),
             group='guest', role='admin'),
        User(id=3, anyNumber=3, anyName='佐藤三郎', name='satou_saburo', password=generate_password_hash('password'),
             group='guest', role='user'),
    ]
    db.session.add_all(users)
    db.session.commit()

    users = User.query.all()
    for user in users:
        print(user.name)

    # -------------Customers---------------
    print('----Customers----')
    customers = [
        Customer(id=1, anyNumber=10000, closingMonth=4, customerName="○○株式会社", customerKana='カブシキガイシャ', honorificTitle='御中', department='部署名', postNumber='000-0000',
                 address='鹿沼市板荷', addressSub='000', telNumber='000-0000-0000', faxNumber='000-0000-0000', url='example.com',
                 email='example@co.jp', manager='田中太郎', representative='田中代表', customerCategory='corporation', isHide=False,
                 isFavorite=False, memo='これは○○株式会社のメモです',),
        Customer(id=2, anyNumber=10001, closingMonth=7, customerName="○○有限会社", customerKana='ユウゲンガイシャ', honorificTitle='御中', department='部署名', postNumber='111-1111',
                 address='鹿沼市板荷', addressSub='111', telNumber='111-1111-1111', faxNumber='111-1111-1111', url='example.com',
                 email='example@co.jp', manager='田中次郎', representative='田中代表', customerCategory='corporation', isHide=False,
                 isFavorite=False, memo='これは○○有限会社のメモです',),
        Customer(id=3, anyNumber=10002, closingMonth=10, customerName="○○商事", customerKana='ショウジ', honorificTitle='御中', department='部署名', postNumber='222-2222',
                 address='鹿沼市板荷', addressSub='222', telNumber='222-2222-2222', faxNumber='222-2222-2222', url='example.com',
                 email='example@co.jp', manager='田中三郎', representative='田中代表', customerCategory='corporation', isHide=False,
                 isFavorite=False, memo='これは○○商事のメモです',)
    ]
    db.session.add_all(customers)
    db.session.commit()

    customers = Customer.query.all()
    for customer in customers:
        print(customer.customerName)

    # -----Items-----
    print('----Items----')
    items = [
        Item(id=1, itemName='りんご', itemCode='11111', model='APP001', category='食料品', maker='apple青果店', supplier='A問屋', unit='個', basePrice=100,
             baseCost=50, isHide=False, memo='これはりんごのメモです', numberOfAttachments=0),
        Item(id=2, itemName='鉛筆', itemCode='22222', model='PEN001', category='事務用品', maker='トンビ鉛筆', supplier='B問屋', unit='本', basePrice=20,
             baseCost=5, isHide=False, memo='これは鉛筆のメモです', numberOfAttachments=0),
        Item(id=3, itemName='ラジオ', itemCode='33333', model='RAD001', category='家電', maker='zony', supplier='C問屋', unit='台', basePrice=1000,
             baseCost=300, isHide=False, memo='これはラジオのメモです', numberOfAttachments=0),
    ]
    db.session.add_all(items)
    db.session.commit()

    items = Item.query.all()
    for item in items:
        print(item.itemName)

    # -----Invoices-----
    print('----Invoices-----')
    invoices = [
        Invoice(customerId=1, customerName='○○株式会社', customerAnyNumber=10000, honorificTitle='御中', department='部署1', manager='田中太郎', otherPartyManager='先方太郎', applyDate=date(2022, 1, 1), deadLine=date(2022, 1, 1),
                paymentDate=date(2022, 1, 1), isPaid=False, title='○○株式会社への請求書', memo='これは請求書のメモです', remarks='これは請求書の備考です', tax=10, isTaxExp=True, numberOfAttachments=0),
        Invoice(customerId=2, customerName="○○有限会社", customerAnyNumber=10001, honorificTitle='御中', department='部署2', manager='田中次郎', otherPartyManager='先方次郎', applyDate=date(2022, 1, 1), deadLine=date(2022, 1, 1),
                paymentDate=date(2022, 1, 1), isPaid=False, title='○○有限会社への請求書', memo='これは請求書のメモです', remarks='これは請求書の備考です', tax=10, isTaxExp=True, numberOfAttachments=0),
        Invoice(customerId=3, customerName="○○商事", customerAnyNumber=10002, honorificTitle='御中', department='部署3', manager='田中三郎', otherPartyManager='先方三郎', applyDate=date(2022, 1, 1), deadLine=date(2022, 1, 1),
                paymentDate=date(2022, 1, 1), isPaid=False, title='○○商事への請求書', memo='これは請求書のメモです', remarks='これは請求書の備考です', tax=10, isTaxExp=True, numberOfAttachments=0),
    ]
    db.session.add_all(invoices)
    db.session.commit()

    invoices = Invoice.query.all()
    for invoice in invoices:
        print(invoice.title)

    # -----Invoice_Items-----
    print('----Invoice_Items----')
    invoice_items = [
        Invoice_Item(id=1, invoiceId=1, itemId=1, rowNum=1, any='01',
                     itemName='りんご', price=100, cost=50, count=5, unit="個", remarks='明細備考1'),
        Invoice_Item(id=2, invoiceId=1, itemId=2, rowNum=2, any='02',
                     itemName='鉛筆', price=20, cost=5, count=10, unit="本", remarks='明細備考2'),
        Invoice_Item(id=3, invoiceId=2, itemId=2, rowNum=1, any='01',
                     itemName='鉛筆', price=30, cost=5, count=15, unit="本", remarks='明細備考3'),
        Invoice_Item(id=4, invoiceId=2, itemId=3, rowNum=2, any='02',
                     itemName='ラジオ', price=1100, cost=300, count=2, unit="台", remarks='明細備考4'),
        Invoice_Item(id=5, invoiceId=3, itemId=1, rowNum=1, any='01',
                     itemName='りんご', price=120, cost=50, count=30, unit="個", remarks='明細備考5'),
    ]
    db.session.add_all(invoice_items)
    db.session.commit()

    invoice_items = Invoice_Item.query.all()
    for invoice_item in invoice_items:
        print(invoice_item.count)

    # -----Invoice_Payments-----
    print('----Invoice_Payments----')
    invoice_payments = [
        Invoice_Payment(invoiceId=1, paymentDate=date(2022, 1, 1),
                        paymentMethod='口座振込', paymentAmount=100, remarks="備考１"),
        Invoice_Payment(invoiceId=1, paymentDate=date(2022, 1, 1),
                        paymentMethod='現金', paymentAmount=20, remarks="備考２"),
        Invoice_Payment(invoiceId=2, paymentDate=date(2022, 1, 1),
                        paymentMethod='クレジット', paymentAmount=30, remarks="備考３"),
        Invoice_Payment(invoiceId=2, paymentDate=date(2022, 1, 1),
                        paymentMethod='口座振込', paymentAmount=1100,  remarks="備考４"),
        Invoice_Payment(invoiceId=3, paymentDate=date(2022, 1, 1),
                        paymentMethod='クレジット', paymentAmount=120,  remarks="備考５"),
    ]
    db.session.add_all(invoice_payments)
    db.session.commit()

    invoice_payments = Invoice_Payment.query.all()
    for invoice_payment in invoice_payments:
        print(invoice_payment.paymentAmount)

    # -----Quotations-----
    print('----Quotations----')
    quotations = [
        Quotation(customerId=1, customerName='○○株式会社', customerAnyNumber=10000, honorificTitle='御中', department='部署1', manager='田中太郎', otherPartyManager='先方太郎', applyDate=date(2022, 1, 1), expiry='2週間以内',
                  dayOfDelivery='受注後1週間以内', termOfSale='御社決済条件にて', isConvert=False, title='○○株式会社への見積書', memo='これは見積書のメモです', remarks='これは見積書の備考です', tax=10, isTaxExp=True, numberOfAttachments=0),
        Quotation(customerId=2, customerName="○○有限会社", customerAnyNumber=10001, honorificTitle='御中', department='部署2', manager='田中次郎', otherPartyManager='先方次郎', applyDate=date(2022, 1, 1), expiry='1ヶ月以内',
                  dayOfDelivery='受注後2週間以内', termOfSale='代金引換', isConvert=False, title='○○有限会社への見積書', memo='これは見積書のメモです', remarks='これは見積書の備考です', tax=10, isTaxExp=True, numberOfAttachments=0),
        Quotation(customerId=3, customerName="○○商事", customerAnyNumber=10002, honorificTitle='御中', department='部署3', manager='田中三郎', otherPartyManager='先方三郎', applyDate=date(2022, 1, 1), expiry='2ヶ月以内',
                  dayOfDelivery='受注後1ヶ月以内', termOfSale='応相談', isConvert=False, title='○○商事への見積書', memo='これは見積書のメモです', remarks='これは見積書の備考です', tax=10, isTaxExp=True, numberOfAttachments=0),
    ]
    db.session.add_all(quotations)
    db.session.commit()

    quotations = Quotation.query.all()
    for quotation in quotations:
        print(quotation.title)

    # -----Quotation_Items-----
    print('----Quotation_Items----')
    quotation_items = [
        Quotation_Item(id=1, quotationId=1, itemId=1, rowNum=1, any='01',
                       itemName='りんご', price=100, cost=50, count=5, unit="個", remarks='明細備考1'),
        Quotation_Item(id=2, quotationId=1, itemId=2, rowNum=2, any='02',
                       itemName='鉛筆', price=20, cost=5, count=10, unit="本", remarks='明細備考2'),
        Quotation_Item(id=3, quotationId=2, itemId=2, rowNum=1, any='01',
                       itemName='鉛筆', price=30, cost=5, count=15, unit="本", remarks='明細備考3'),
        Quotation_Item(id=4, quotationId=2, itemId=3, rowNum=2, any='02',
                       itemName='ラジオ', price=1100, cost=300, count=2, unit="台", remarks='明細備考4'),
        Quotation_Item(id=5, quotationId=3, itemId=1, rowNum=1, any='01',
                       itemName='りんご', price=120, cost=50, count=30, unit="個", remarks='明細備考5'),
    ]
    db.session.add_all(quotation_items)
    db.session.commit()

    quotation_items = Quotation_Item.query.all()
    for quotation_item in quotation_items:
        print(quotation_item.count)

    # -----Memos-----
    print('----Memos----')
    memos = [
        Memo(id=1, title='メモのタイトル１', manager='担当者1',
             isFavorite=False, content='メモの内容１'),
        Memo(id=2, title='メモのタイトル２', manager='担当者2',
             isFavorite=False, content='メモの内容２'),
        Memo(id=3, title='メモのタイトル３', manager='担当者3',
             isFavorite=False, content='メモの内容３'),
    ]
    db.session.add_all(memos)
    db.session.commit()

    memos = Memo.query.all()
    for memo in memos:
        print(memo.title)

    # -----Units-----
    print('----Units----')
    units = [
        Unit(id=1, unitName='個'),
        Unit(id=2, unitName='本'),
        Unit(id=3, unitName='台'),
    ]
    db.session.add_all(units)
    db.session.commit()

    units = Unit.query.all()
    for unit in units:
        print(unit.unitName)

    # -----Categories-----
    print('----Categories----')
    categories = [
        Category(id=1, categoryName='食料品'),
        Category(id=2, categoryName='事務用品'),
        Category(id=3, categoryName='家電'),
    ]
    db.session.add_all(categories)
    db.session.commit()

    categories = Category.query.all()
    for category in categories:
        print(category.categoryName)

    # -----Makers-----
    print('----Makers----')
    makers = [
        Maker(id=1, makerName='apple青果店'),
        Maker(id=2, makerName='トンビ鉛筆'),
        Maker(id=3, makerName='zony'),
    ]
    db.session.add_all(makers)
    db.session.commit()

    makers = Maker.query.all()
    for maker in makers:
        print(maker.makerName)

    # -----History-----
    print('----History----')
    history = [
        History(id=1, userName='tanaka_taro',
                modelName='Customer', modelId=1, action='GET',),
        History(id=2, userName='suzuki_jiro',
                modelName='Item', modelId=2, action='POST',),
        History(id=3, userName='satou_saburo',
                modelName='Invoice', modelId=3, action='DELETE',),
    ]
    db.session.add_all(history)
    db.session.commit()

    histories = History.query.all()
    for history in histories:
        print(history.userName)

    # -----Setting-----
    print('----Setting----')
    setting = [
        Setting(id=1, companyName='自社株式会社', registerNumber=1111111111111, representative='自社代表者', administrator='管理者太郎', postNumber='000-0000', address='宇都宮市北若松原',
                telNumber='000-0000-0000', faxNumber='000-0000-0000', url='mypage.com',
                email='mymail@co.jp', payee='テスト銀行　本店(999) 普通 9999999', accountHolder='自社株式会社', accountHolderKana='カ）ジシャ', logoFilePath='./static/asset/logo/logo2.jpg', logoHeight=100, logoWidth=100,
                stampFilePath='./static/asset/stamp/inkan.png', stampHeight=100, stampWidth=100, isDisplayQuotationLogo=True, isDisplayInvoiceLogo=True, isDisplayDeliveryLogo=True,
                isDisplayQuotationStamp=True, isDisplayInvoiceStamp=True, isDisplayDeliveryStamp=True, defaultTax=10)
    ]
    db.session.add_all(setting)
    db.session.commit()

    setting = Setting.query.all()
    print(setting[0].companyName)


if __name__ == '__main__':
    seeder()
