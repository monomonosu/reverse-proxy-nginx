from app import db, app, ma
from datetime import datetime
from datetime import date
from sqlalchemy.sql import func
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import Insert
from marshmallow import Schema, fields


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    anyNumber = db.Column(db.Integer, unique=True)
    anyName = db.Column(db.String, unique=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    group = db.Column(db.String(255))
    role = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now, onupdate=datetime.now)


class Customer(db.Model):

    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    anyNumber = db.Column(db.Integer, unique=True)
    closingMonth = db.Column(db.Integer)
    customerName = db.Column(db.String)
    customerKana = db.Column(db.String)
    honorificTitle = db.Column(db.String)
    department = db.Column(db.String)
    postNumber = db.Column(db.String(20))
    address = db.Column(db.String)
    addressSub = db.Column(db.String)
    telNumber = db.Column(db.String(30))
    faxNumber = db.Column(db.String(30))
    url = db.Column(db.String)
    email = db.Column(db.String)
    manager = db.Column(db.String)
    representative = db.Column(db.String)
    customerCategory = db.Column(
        db.String, nullable=False, default='corporation')
    isHide = db.Column(db.Boolean, nullable=False, default=False)
    isFavorite = db.Column(db.Boolean, nullable=False,
                           default=False, server_default=db.text('0'))
    memo = db.Column(db.String)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)
    # invoices = db.relationship(
    #     'Invoice', backref='customer', uselist=True, cascade='all, delete',)
    # quotations = db.relationship(
    #     'Quotation', backref='customer', uselist=True, cascade='all, delete',)


class Item(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String)
    itemCode = db.Column(db.String)
    model = db.Column(db.String)
    category = db.Column(db.String)
    maker = db.Column(db.String)
    supplier = db.Column(db.String)
    unit = db.Column(db.String)
    basePrice = db.Column(db.Integer)
    baseCost = db.Column(db.Integer)
    isHide = db.Column(db.Boolean, nullable=False,
                       default=False, server_default=db.text('0'))
    memo = db.Column(db.String)
    numberOfAttachments = db.Column(
        db.Integer, default=0, server_default=db.text('0'))
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)


# 請求番号自動生成
def edited_invoice_number():

    nowYearFormat = datetime.now().strftime('%y')
    nowYear = datetime.now().year
    yearStart = date(nowYear, 1, 1)
    # 年末を含めてしまうのを防ぐ
    yearEnd = date(nowYear+1, 1, 1)
    maxNumberForYear = db.session.query(
        func.max(Invoice.applyNumber)).filter(Invoice.createdAt >= yearStart, Invoice.createdAt < yearEnd).first()[0]
    if maxNumberForYear:
        maxNumberForYear_s = str(maxNumberForYear)
        maxApplyNumber_s = maxNumberForYear_s[2:]
        maxApplyNumber = int(maxApplyNumber_s)
        nextNumber = format(maxApplyNumber+1, '0>5')
    else:
        nextNumber = '00001'
    return str(nowYearFormat) + str(nextNumber)


class Invoice(db.Model):

    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    customerId = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customerName = db.Column(db.String)
    customerAnyNumber = db.Column(db.Integer)
    honorificTitle = db.Column(db.String)
    department = db.Column(db.String)
    manager = db.Column(db.String)
    otherPartyManager = db.Column(db.String)
    applyNumber = db.Column(db.Integer, default=edited_invoice_number)
    applyDate = db.Column(db.Date)
    deadLine = db.Column(db.Date)
    paymentDate = db.Column(db.Date)
    isPaid = db.Column(db.Boolean, nullable=False,
                       default=False, server_default=db.text('0'))
    title = db.Column(db.String)
    memo = db.Column(db.String)
    remarks = db.Column(db.String)
    tax = db.Column(db.Integer, nullable=False, default=10,
                    server_default=db.text('10'))
    isTaxExp = db.Column(db.Boolean, nullable=False, default=True)
    isDelete = db.Column(db.Boolean, nullable=False, default=False)
    numberOfAttachments = db.Column(
        db.Integer, default=0, server_default=db.text('0'))
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)
    invoice_items = db.relationship(
        'Invoice_Item', backref='invoice', uselist=True, cascade='all, delete',)
    invoice_payments = db.relationship(
        'Invoice_Payment', backref='invoice', uselist=True, cascade='all, delete',)


class Invoice_Item(db.Model):

    __tablename__ = 'invoice_items'

    id = db.Column(db.Integer, primary_key=True)
    invoiceId = db.Column(db.Integer, db.ForeignKey('invoices.id'))
    itemId = db.Column(db.Integer, db.ForeignKey('items.id'))
    rowNum = db.Column(db.Integer)
    any = db.Column(db.String)
    itemName = db.Column(db.String)
    price = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    count = db.Column(db.Integer)
    unit = db.Column(db.String)
    remarks = db.Column(db.String)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)


class Invoice_Payment(db.Model):

    __tablename__ = 'invoice_payments'

    id = db.Column(db.Integer, primary_key=True)
    invoiceId = db.Column(db.Integer, db.ForeignKey('invoices.id'))
    paymentDate = db.Column(db.Date)
    paymentMethod = db.Column(db.String)
    paymentAmount = db.Column(db.Integer)
    remarks = db.Column(db.String)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)


# 見積番号自動生成
def edited_quotation_number():

    nowYearFormat = datetime.now().strftime('%y')
    nowYear = datetime.now().year
    yearStart = date(nowYear, 1, 1)
    # 年末を含めてしまうのを防ぐ
    yearEnd = date(nowYear+1, 1, 1)
    maxNumberForYear = db.session.query(
        func.max(Quotation.applyNumber)).filter(Quotation.createdAt >= yearStart, Quotation.createdAt < yearEnd).first()[0]
    if maxNumberForYear:
        maxNumberForYear_s = str(maxNumberForYear)
        maxApplyNumber_s = maxNumberForYear_s[2:]
        maxApplyNumber = int(maxApplyNumber_s)
        nextNumber = format(maxApplyNumber+1, '0>5')
    else:
        nextNumber = '00001'
    return str(nowYearFormat) + str(nextNumber)


class Quotation(db.Model):

    __tablename__ = 'quotations'

    id = db.Column(db.Integer, primary_key=True)
    customerId = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customerName = db.Column(db.String)
    customerAnyNumber = db.Column(db.Integer)
    honorificTitle = db.Column(db.String)
    department = db.Column(db.String)
    manager = db.Column(db.String)
    otherPartyManager = db.Column(db.String)
    applyNumber = db.Column(db.Integer, default=edited_quotation_number)
    applyDate = db.Column(db.Date)
    expiry = db.Column(db.String)
    dayOfDelivery = db.Column(db.String)
    termOfSale = db.Column(db.String)
    isConvert = db.Column(db.Boolean, nullable=False,
                          default=False, server_default=db.text('0'))
    title = db.Column(db.String)
    memo = db.Column(db.String)
    remarks = db.Column(db.String)
    tax = db.Column(db.Integer, nullable=False, default=10,
                    server_default=db.text('10'))
    isTaxExp = db.Column(db.Boolean, nullable=False, default=True)
    isDelete = db.Column(db.Boolean, nullable=False, default=False)
    numberOfAttachments = db.Column(
        db.Integer, default=0, server_default=db.text('0'))
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)
    quotation_items = db.relationship(
        'Quotation_Item', backref='quotation', uselist=True, cascade='all, delete',)


class Quotation_Item(db.Model):

    __tablename__ = 'quotation_items'

    id = db.Column(db.Integer, primary_key=True)
    quotationId = db.Column(db.Integer, db.ForeignKey('quotations.id'))
    itemId = db.Column(db.Integer, db.ForeignKey('items.id'))
    rowNum = db.Column(db.Integer)
    any = db.Column(db.String)
    itemName = db.Column(db.String)
    price = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    count = db.Column(db.Integer)
    unit = db.Column(db.String)
    remarks = db.Column(db.String)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)


class Memo(db.Model):

    __tablename__ = 'memos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    manager = db.Column(db.String)
    isFavorite = db.Column(db.Boolean, nullable=False,
                           default=False, server_default=db.text('0'))
    content = db.Column(db.String)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)


class Unit(db.Model):

    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)
    unitName = db.Column(db.String)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)


class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    categoryName = db.Column(db.String)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)


class Maker(db.Model):

    __tablename__ = 'maker'

    id = db.Column(db.Integer, primary_key=True)
    makerName = db.Column(db.String)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)


class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String)
    modelName = db.Column(db.String)
    modelId = db.Column(db.Integer)
    action = db.Column(db.String)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)


class Setting(db.Model):

    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    # 会社情報
    companyName = db.Column(db.String)
    registerNumber = db.Column(db.Integer)
    representative = db.Column(db.String)
    administrator = db.Column(db.String)
    postNumber = db.Column(db.String(20))
    address = db.Column(db.String)
    telNumber = db.Column(db.String(30))
    faxNumber = db.Column(db.String(30))
    url = db.Column(db.String)
    email = db.Column(db.String)
    payee = db.Column(db.String)
    accountHolder = db.Column(db.String)
    accountHolderKana = db.Column(db.String)
    # ロゴ・印鑑
    logoFilePath = db.Column(db.String)
    logoHeight = db.Column(db.Integer)
    logoWidth = db.Column(db.Integer)
    stampFilePath = db.Column(db.String)
    stampHeight = db.Column(db.Integer)
    stampWidth = db.Column(db.Integer)
    isDisplayQuotationLogo = db.Column(
        db.Boolean, nullable=False, default=True)
    isDisplayInvoiceLogo = db.Column(db.Boolean, nullable=False, default=True)
    isDisplayDeliveryLogo = db.Column(db.Boolean, nullable=False, default=True)
    isDisplayQuotationStamp = db.Column(
        db.Boolean, nullable=False, default=True)
    isDisplayInvoiceStamp = db.Column(db.Boolean, nullable=False, default=True)
    isDisplayDeliveryStamp = db.Column(
        db.Boolean, nullable=False, default=True)
    # 設定
    defaultTax = db.Column(db.Integer, nullable=False,
                           default=10, server_default=db.text('10'))
    updatedAt = updatedAt = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


# -----Json変換-----


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item


class Invoice_ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Invoice_Item
        include_fk = True


class Invoice_PaymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Invoice_Payment
        include_fk = True


class InvoiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Invoice
        include_fk = True
    invoice_items = ma.Nested(Invoice_ItemSchema, many=True)
    invoice_payments = ma.Nested(Invoice_PaymentSchema, many=True)


class Quotation_ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Quotation_Item
        include_fk = True


class QuotationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Quotation
        include_fk = True
    quotation_items = ma.Nested(Quotation_ItemSchema, many=True)


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        include_fk = True
    invoices = ma.Nested(InvoiceSchema, many=True)
    quotations = ma.Nested(QuotationSchema, many=True)


class MemoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Memo


class UnitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Unit


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category


class MakerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Maker


class HistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = History


class SettingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Setting


# 独自定義
class AchievementSchema(Schema):
    applyDate = fields.Str()
    monthlySales = fields.Int()
    monthlyProfit = fields.Int()


class AchievementPreviousYearSchema(Schema):
    applyDate = fields.Str()
    monthlySales_previousYear = fields.Int()
    monthlyProfit_previousYear = fields.Int()
