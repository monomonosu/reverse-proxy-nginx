import sqlite3
from app import app
from models import *
from flask import jsonify, request
import json
from datetime import date, datetime
from dateutil import relativedelta
from sqlalchemy import desc, or_, and_, extract, func
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash


_LIMIT_NUM = 100

# -----ユーザー(Users)-----


@app.route('/users', methods=['GET'])
def user_index():
    users = User.query.all()
    newHistory = History(
        userName=current_user.id,
        modelName='User',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(UserSchema(many=True).dump(users))


@app.route('/user/<id>', methods=['GET'])
def user_show(id):
    userCount = User.query.filter(User.id == id).count()
    if userCount:
        user = User.query.filter(User.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='User',
            modelId=id,
            action='get'
        )
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(UserSchema().dump(user))
    else:
        return jsonify([])


@app.route('/user', methods=['POST'])
def user_create():
    data = request.json
    anyNum = User.query.filter(User.anyNumber == data.get('anyNumber'))
    anyName = User.query.filter(User.anyName == data.get('anyName'))
    if db.session.query(anyNum.exists()).scalar():
        return jsonify({"result": "error", "message": "入力した任意番号は既に存在します。存在しない値を入力してください。"}), 500
    if db.session.query(anyName.exists()).scalar():
        return jsonify({"result": "error", "message": "入力した任意名は既に存在します。存在しない値を入力してください。"}), 500
    if data.get('anyNumber') is None or data.get('anyName') is None or data.get('name') is None or data.get('password') is None or data.get('anyNumber') == '' or data.get('anyName') == '' or data.get('name') == '' or data.get('password') == '':
        return jsonify({"result": "error", "message": "必須項目に空欄があります。値を入力してください。"}), 500
    newUser = User(
        anyNumber=data.get('anyNumber'),
        anyName=data.get('anyName')if data.get('anyName') else None,
        name=data.get('name')if data.get('name') else None,
        password=generate_password_hash(data.get('password')),
        group=data.get('group')if data.get('group') else None,
        role=data.get('role')if data.get('role') else None,
    )
    db.session.add(newUser)
    db.session.commit()
    id = newUser.id
    newHistory = History(
        userName=current_user.id,
        modelName='User',
        modelId=id,
        action='post'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/user/<id>', methods=['PUT'])
def user_update(id):
    data = request.json
    anyNum = User.query.filter(User.anyNumber == data.get('anyNumber'))
    anyName = User.query.filter(User.anyName == data.get('anyName'))
    user = User.query.filter(User.id == id).one()
    if db.session.query(anyNum.exists()).scalar() and user.anyNumber != data.get('anyNumber'):
        return jsonify({"result": "error", "message": "入力した任意番号は既に存在します。存在しない値を入力してください。"}), 500
    if db.session.query(anyName.exists()).scalar() and user.anyName != data.get('anyName'):
        return jsonify({"result": "error", "message": "入力した任意名は既に存在します。存在しない値を入力してください。"}), 500
    if data.get('anyNumber') is None or data.get('anyName') is None or data.get('name') is None or data.get('password') is None or data.get('anyNumber') == '' or data.get('anyName') == '' or data.get('name') == '' or data.get('password') == '':
        return jsonify({"result": "error", "message": "必須項目に空欄があります。値を入力してください。"}), 500

    user.anyNumber = data.get('anyNumber')
    user.anyName = data.get('anyName')if data.get('anyName') else None
    user.name = data.get('name')if data.get('name') else None
    user.password = generate_password_hash(data.get('password'))
    user.group = data.get('group')if data.get('group') else None
    user.role = data.get('role')if data.get('role') else None

    newHistory = History(
        userName=current_user.id,
        modelName='User',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/user/<id>', methods=['DELETE'])
def user_destroy(id):
    user = User.query.filter(User.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='User',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# -----得意先(Customers)-----
@app.route('/v1/customers', methods=['GET'])
@app.route('/customers', methods=['GET'])
def customer_index_v1():
    # パラメータを準備
    req = request.args
    searchWord = req.get('search')
    moreCheck = req.get('moreCheck') if req.get('moreCheck') else False
    # テスト的に300に
    limit = int(req.get('limit')) if req.get('limit') else 300
    offset = int(req.get('offset')) if req.get('offset') else 0
    # 各種フィルタリング処理
    if searchWord:
        customers = Customer.query.filter(or_(
            Customer.customerName.like('%'+searchWord+'%'),
            Customer.customerKana.like('%'+searchWord+'%'),
            Customer.anyNumber == searchWord,
        ))
    else:
        customers = Customer.query
    customers_tmp = customers
    if offset:
        customers = customers.offset(offset)
    if limit:
        customers = customers.limit(limit)

    newHistory = History(
        userName=current_user.id,
        modelName='Customer',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()

    if moreCheck:
        totalRecordCount = customers_tmp.count()
        nowRecordCount = limit+offset
        isMore = True if nowRecordCount < totalRecordCount else False
        return jsonify({'customers': CustomerSchema(many=True).dump(customers), 'isMore': isMore})

    return jsonify(CustomerSchema(many=True).dump(customers))


@app.route('/v1/customer/<id>', methods=['GET'])
@app.route('/customer/<id>', methods=['GET'])
def customer_show(id):
    customerCount = Customer.query.filter(Customer.id == id).count()
    if customerCount:
        customer = Customer.query.filter(Customer.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='Customer',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(CustomerSchema().dump(customer))
    else:
        return jsonify([])


@app.route('/v1/customer', methods=['POST'])
@app.route('/customer', methods=['POST'])
def customer_create():
    data = request.json
    query = Customer.query.filter(Customer.anyNumber == data.get('anyNumber'))
    if db.session.query(query.exists()).scalar():
        return jsonify({"result": "error", "message": "入力した任意番号は既に存在します。存在しない値を入力してください。"}), 500
    if data.get('anyNumber') is None or data.get('anyNumber') == '':
        return jsonify({"result": "error", "message": "必須項目に空欄があります。値を入力してください。"}), 500
    newCustomer = Customer(
        anyNumber=data.get('anyNumber'),
        closingMonth=data.get('closingMonth') if data.get(
            'closingMonth') else None,
        customerName=data.get('customerName')if data.get(
            'customerName') else None,
        customerKana=data.get('customerKana')if data.get(
            'customerKana') else None,
        honorificTitle=data.get('honorificTitle')if data.get(
            'honorificTitle') else None,
        department=data.get('department')if data.get('department') else None,
        postNumber=data.get('postNumber')if data.get('postNumber') else None,
        address=data.get('address')if data.get('address') else None,
        addressSub=data.get('addressSub')if data.get('addressSub') else None,
        telNumber=data.get('telNumber')if data.get('telNumber') else None,
        faxNumber=data.get('faxNumber')if data.get('faxNumber') else None,
        url=data.get('url')if data.get('url') else None,
        email=data.get('email')if data.get('email') else None,
        manager=data.get('manager')if data.get('manager') else None,
        representative=data.get('representative')if data.get(
            'representative') else None,
        customerCategory=data.get('customerCategory')if data.get(
            'customerCategory') else None,
        isHide=data.get('isHide'),
        isFavorite=data.get('isFavorite'),
        memo=data.get('memo')if data.get('memo') else None,
    )
    db.session.add(newCustomer)
    db.session.commit()
    id = newCustomer.id
    newHistory = History(
        userName=current_user.id,
        modelName='Customer',
        modelId=id,
        action='post'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/customer/<id>', methods=['PUT'])
@app.route('/customer/<id>', methods=['PUT'])
def customer_update(id):
    data = request.json
    query = Customer.query.filter(Customer.anyNumber == data.get('anyNumber'))
    customer = Customer.query.filter(Customer.id == id).one()
    if db.session.query(query.exists()).scalar() and customer.anyNumber != data.get('anyNumber'):
        return jsonify({"result": "error", "message": "入力した任意番号は既に存在します。存在しない値を入力してください。"}), 500
    if data.get('anyNumber') is None or data.get('anyNumber') == '':
        return jsonify({"result": "error", "message": "必須項目に空欄があります。値を入力してください。"}), 500

    customer.anyNumber = data.get('anyNumber')
    customer.closingMonth = data.get(
        'closingMonth')if data.get('closingMonth') else None
    customer.customerName = data.get(
        'customerName')if data.get('customerName') else None
    customer.customerKana = data.get(
        'customerKana')if data.get('customerKana') else None
    customer.honorificTitle = data.get(
        'honorificTitle')if data.get('honorificTitle') else None
    customer.department = data.get(
        'department')if data.get('department') else None
    customer.postNumber = data.get(
        'postNumber')if data.get('postNumber') else None
    customer.address = data.get('address')if data.get('address') else None
    customer.addressSub = data.get(
        'addressSub')if data.get('addressSub') else None
    customer.telNumber = data.get(
        'telNumber')if data.get('telNumber') else None
    customer.faxNumber = data.get(
        'faxNumber')if data.get('faxNumber') else None
    customer.url = data.get('url')if data.get('url') else None
    customer.email = data.get('email')if data.get('email') else None
    customer.manager = data.get('manager')if data.get('manager') else None
    customer.representative = data.get(
        'representative')if data.get('representative') else None
    customer.customerCategory = data.get('customerCategory')if data.get(
        'customerCategory') else 'corporation'  # ページリロード後、更新時のエラー防止
    customer.isHide = data.get('isHide')if data.get(
        'isHide') else False  # ページリロード後、更新時のエラー防止
    customer.isFavorite = data.get('isFavorite')if data.get(
        'isFavorite') else False  # ページリロード後、更新時のエラー防止
    customer.memo = data.get('memo')if data.get('memo') else None

    newHistory = History(
        userName=current_user.id,
        modelName='Customer',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/customer/<id>', methods=['DELETE'])
@app.route('/customer/<id>', methods=['DELETE'])
def customer_destroy(id):
    customer = Customer.query.filter(Customer.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='Customer',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# -----商品(Items)-----
@app.route('/v1/items', methods=['GET'])
@app.route('/items', methods=['GET'])
def item_index_v1():
    # パラメータを準備
    req = request.args
    searchWord = req.get('search')
    moreCheck = req.get('moreCheck') if req.get('moreCheck') else False
    limit = int(req.get('limit')) if req.get('limit') else _LIMIT_NUM
    offset = int(req.get('offset')) if req.get('offset') else 0
    # 各種フィルタリング処理
    if searchWord:
        items = Item.query.filter(or_(
            Item.itemName.like('%'+searchWord+'%'),
            Item.itemCode.like('%'+searchWord+'%'),
            Item.model.like('%'+searchWord+'%'),
        ))
    else:
        items = Item.query
    items_tmp = items
    if offset:
        items = items.offset(offset)
    if limit:
        items = items.limit(limit)

    newHistory = History(
        userName=current_user.id,
        modelName='Item',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()

    if moreCheck:
        totalRecordCount = items_tmp.count()
        nowRecordCount = limit+offset
        isMore = True if nowRecordCount < totalRecordCount else False
        return jsonify({'items': ItemSchema(many=True).dump(items), 'isMore': isMore})

    return jsonify(ItemSchema(many=True).dump(items))


@app.route('/v1/item/<id>', methods=['GET'])
@app.route('/item/<id>', methods=['GET'])
def item_show(id):
    itemCount = Item.query.filter(Item.id == id).count()
    if itemCount:
        item = Item.query.filter(Item.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='Item',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(ItemSchema().dump(item))
    else:
        return jsonify({})


@app.route('/v1/item', methods=['POST'])
def item_create():
    data = request.json
    query = Item.query.filter(Item.itemCode == data.get('itemCode'))
    if db.session.query(query.exists()).scalar() and data.get('itemCode') != None and data.get('itemCode') != '':
        return jsonify({"result": "error", "message": "入力した商品コードは既に存在します。存在しない値を入力してください。"}), 500
    newItem = Item(
        itemName=data.get('itemName')if data.get('itemName') else None,
        itemCode=data.get('itemCode')if data.get('itemCode') else None,
        model=data.get('model')if data.get('model') else None,
        category=data.get('category')if data.get('category') else None,
        maker=data.get('maker')if data.get('maker') else None,
        supplier=data.get('supplier')if data.get('supplier') else None,
        unit=data.get('unit')if data.get('unit') else None,
        basePrice=data.get('basePrice')if data.get('basePrice') else None,
        baseCost=data.get('baseCost')if data.get('baseCost') else None,
        isHide=data.get('isHide'),
        memo=data.get('memo')if data.get('memo') else None,
        numberOfAttachments=data.get('numberOfAttachments'),
    )
    db.session.add(newItem)
    db.session.commit()
    id = newItem.id
    newHistory = History(
        userName=current_user.id,
        modelName='Item',
        modelId=id,
        action='post'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/item/<id>', methods=['PUT'])
def item_update(id):
    data = request.json
    item = Item.query.filter(Item.id == id).one()
    query = Item.query.filter(Item.itemCode == data.get('itemCode'))
    if db.session.query(query.exists()).scalar() and item.itemCode != data.get('itemCode') and (data.get('itemCode') != None and data.get('itemCode') != ''):
        return jsonify({"result": "error", "message": "入力した商品コードは既に存在します。存在しない値を入力してください。"}), 500

    item.itemName = data.get('itemName')if data.get('itemName') else None
    item.itemCode = data.get('itemCode')if data.get('itemCode') else None
    item.model = data.get('model')if data.get('model') else None
    item.category = data.get('category')if data.get('category') else None
    item.maker = data.get('maker')if data.get('maker') else None
    item.supplier = data.get('supplier')if data.get('supplier') else None
    item.unit = data.get('unit')if data.get('unit') else None
    item.basePrice = data.get('basePrice')if data.get('basePrice') else None
    item.baseCost = data.get('baseCost')if data.get('baseCost') else None
    item.isHide = data.get('isHide')if data.get(
        'isHide') else False  # ページリロード後、更新時のエラー防止
    item.memo = data.get('memo')if data.get('memo') else None
    item.numberOfAttachments = data.get('numberOfAttachments')

    newHistory = History(
        userName=current_user.id,
        modelName='Item',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/item/<id>', methods=['DELETE'])
def item_destroy(id):
    item = Item.query.filter(Item.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='Item',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# -----請求書(Invoices)-----
@app.route('/v1/invoices', methods=['GET'])
@app.route('/invoices', methods=['GET'])
def invoice_index_v1():
    # パラメータを準備
    req = request.args
    searchWord = req.get('search')
    moreCheck = req.get('moreCheck') if req.get('moreCheck') else False
    # テスト的に300に
    limit = int(req.get('limit')) if req.get('limit') else 300
    offset = int(req.get('offset')) if req.get('offset') else 0
    # 各種フィルタリング処理
    if searchWord:
        if len(searchWord) == 4:
            invoices = Invoice.query.filter(and_(Invoice.isDelete == False, or_(
                extract('year', Invoice.applyDate) == searchWord, Invoice.customerName.like('%'+searchWord+'%'), Invoice.customerAnyNumber == searchWord,)))
        elif len(searchWord) == 6:
            year = searchWord[:4]
            month = searchWord[4:]
            invoices = Invoice.query.filter(and_(Invoice.isDelete == False, or_(
                Invoice.customerName.like('%'+searchWord+'%'), Invoice.customerAnyNumber == searchWord, and_(
                    extract('year', Invoice.applyDate) == year, extract('month', Invoice.applyDate) == month))))
        elif len(searchWord) == 8:
            year = searchWord[:4]
            month = searchWord[4:6]
            day = searchWord[6:]
            invoices = Invoice.query.filter(and_(Invoice.isDelete == False, or_(
                Invoice.customerName.like('%'+searchWord+'%'), Invoice.customerAnyNumber == searchWord, and_(
                    extract('year', Invoice.applyDate) == year, extract('month', Invoice.applyDate) == month, extract('day', Invoice.applyDate) == day))))
        else:
            invoices = Invoice.query.filter(
                and_(Invoice.isDelete == False, or_(Invoice.customerName.like('%'+searchWord+'%'), Invoice.customerAnyNumber == searchWord)))

    else:
        invoices = Invoice.query.filter(Invoice.isDelete == False)
    invoices_tmp = invoices
    if offset:
        invoices = invoices.offset(offset)
    if limit:
        invoices = invoices.limit(limit)

    newHistory = History(
        userName=current_user.id,
        modelName='Invoice',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()

    if moreCheck:
        totalRecordCount = invoices_tmp.count()
        nowRecordCount = limit+offset
        isMore = True if nowRecordCount < totalRecordCount else False
        return jsonify({'invoices': InvoiceSchema(many=True).dump(invoices), 'isMore': isMore})

    return jsonify(InvoiceSchema(many=True).dump(invoices))


@app.route('/v1/achievements', methods=['GET'])
@app.route('/achievements', methods=['GET'])
def invoice_achievement_v1():
    # パラメータを準備
    req = request.args
    reqMonth = int(req.get('month')) if req.get('month') else None
    reqYear = int(req.get('year')) if req.get('year') else None

    if reqYear and reqMonth:
        beforeDate = date(reqYear, reqMonth, 1)
        afterDate = beforeDate + \
            relativedelta.relativedelta(
                years=1)-relativedelta.relativedelta(days=1)
        invoices = Invoice.query.filter(and_(
            Invoice.isDelete == False, Invoice.applyDate.between(beforeDate, afterDate)))
    else:
        invoices = Invoice.query.filter(Invoice.isDelete == False)

    newHistory = History(
        userName=current_user.id,
        modelName='Invoice',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(InvoiceSchema(many=True).dump(invoices))


def multiply(price, count, tax):
    # 単純な数値は認識されない？
    return price*count*(1+tax/100.0)


def multiplyTaxIncluded(price, count):
    return price*count


def profit(price, count, tax, cost):
    return multiply(price, count, tax)-(cost*count)


def profitTaxIncluded(price, count, cost):
    return multiplyTaxIncluded(price, count)-(cost*count)


@app.route('/v1/achievements-group', methods=['GET'])
@app.route('/achievements-group', methods=['GET'])
def invoice_achievement_group_v1():
    # パラメータを準備
    req = request.args
    reqMonth = int(req.get('month')) if req.get('month') else None
    reqYear = int(req.get('year')) if req.get('year') else None
    isTax = bool(int(req.get('isTax')))
    isPreviousYear = req.get('isPreviousYear') if req.get(
        'isPreviousYear') else False

    if reqYear and reqMonth:
        beforeDate = date(reqYear, reqMonth, 1)
        afterDate = beforeDate + \
            relativedelta.relativedelta(
                years=1)-relativedelta.relativedelta(days=1)
        beforeDate_previousYear = beforeDate + \
            relativedelta.relativedelta(years=-1)
        afterDate_previousYear = afterDate + \
            relativedelta.relativedelta(years=-1)
        if isPreviousYear:
            # func.sum内でInvoice.isTaxのbool値が使えないので
            if isTax:
                achievements = db.session.query(func.strftime(
                    "%Y-%m", Invoice.applyDate).label("applyDate"), func.sum(multiply(Invoice_Item.price, Invoice_Item.count, Invoice.tax)).label("monthlySales_previousYear"),
                    func.sum(profit(Invoice_Item.price, Invoice_Item.count, Invoice.tax, Invoice_Item.cost)).label("monthlyProfit_previousYear")) \
                    .filter(and_(Invoice.isDelete == False, Invoice.isTaxExp == True, Invoice.applyDate.between(beforeDate_previousYear, afterDate_previousYear))) \
                    .join(Invoice_Item).group_by(func.strftime("%Y-%m", Invoice.applyDate)).all()
            else:
                achievements = db.session.query(func.strftime(
                    "%Y-%m", Invoice.applyDate).label("applyDate"), func.sum(multiplyTaxIncluded(Invoice_Item.price, Invoice_Item.count,)).label("monthlySales_previousYear"),
                    func.sum(profitTaxIncluded(Invoice_Item.price, Invoice_Item.count, Invoice_Item.cost)).label("monthlyProfit_previousYear")) \
                    .filter(and_(Invoice.isDelete == False, Invoice.isTaxExp == False, Invoice.applyDate.between(beforeDate_previousYear, afterDate_previousYear))) \
                    .join(Invoice_Item).group_by(func.strftime("%Y-%m", Invoice.applyDate)).all()
        else:
            if isTax:
                achievements = db.session.query(func.strftime(
                    "%Y-%m", Invoice.applyDate).label("applyDate"), func.sum(multiply(Invoice_Item.price, Invoice_Item.count, Invoice.tax)).label("monthlySales"),
                    func.sum(profit(Invoice_Item.price, Invoice_Item.count, Invoice.tax, Invoice_Item.cost)).label("monthlyProfit")) \
                    .filter(and_(Invoice.isDelete == False, Invoice.isTaxExp == True, Invoice.applyDate.between(beforeDate, afterDate))) \
                    .join(Invoice_Item).group_by(func.strftime("%Y-%m", Invoice.applyDate)).all()
            else:
                achievements = db.session.query(func.strftime(
                    "%Y-%m", Invoice.applyDate).label("applyDate"), func.sum(multiplyTaxIncluded(Invoice_Item.price, Invoice_Item.count,)).label("monthlySales"),
                    func.sum(profitTaxIncluded(Invoice_Item.price, Invoice_Item.count, Invoice_Item.cost)).label("monthlyProfit")) \
                    .filter(and_(Invoice.isDelete == False, Invoice.isTaxExp == False, Invoice.applyDate.between(beforeDate, afterDate))) \
                    .join(Invoice_Item).group_by(func.strftime("%Y-%m", Invoice.applyDate)).all()
    else:
        achievements = Invoice.query.filter(Invoice.isDelete == False)

    newHistory = History(
        userName=current_user.id,
        modelName='Invoice',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    if isPreviousYear:
        return jsonify(AchievementPreviousYearSchema(many=True).dump(achievements))
    else:
        return jsonify(AchievementSchema(many=True).dump(achievements))


@app.route('/v1/dust-invoices', methods=['GET'])
@app.route('/dust-invoices', methods=['GET'])
def dust_invoice_index_v1():
    # パラメータを準備
    req = request.args
    searchWord = req.get('search')
    moreCheck = req.get('moreCheck') if req.get('moreCheck') else False
    # テスト的に300に
    limit = int(req.get('limit')) if req.get('limit') else 300
    offset = int(req.get('offset')) if req.get('offset') else 0
    # 各種フィルタリング処理
    if searchWord:
        if len(searchWord) == 4:
            invoices = Invoice.query.filter(and_(Invoice.isDelete == True, or_(
                extract('year', Invoice.applyDate) == searchWord, Invoice.customerName.like('%'+searchWord+'%'))))
        elif len(searchWord) == 6:
            year = searchWord[:4]
            month = searchWord[4:]
            invoices = Invoice.query.filter(and_(Invoice.isDelete == True, or_(
                Invoice.customerName.like('%'+searchWord+'%'), and_(
                    extract('year', Invoice.applyDate) == year, extract('month', Invoice.applyDate) == month))))
        elif len(searchWord) == 8:
            year = searchWord[:4]
            month = searchWord[4:6]
            day = searchWord[6:]
            invoices = Invoice.query.filter(and_(Invoice.isDelete == True, or_(
                Invoice.customerName.like('%'+searchWord+'%'), and_(
                    extract('year', Invoice.applyDate) == year, extract('month', Invoice.applyDate) == month, extract('day', Invoice.applyDate) == day))))
        else:
            invoices = Invoice.query.filter(
                and_(Invoice.isDelete == True, Invoice.customerName.like('%'+searchWord+'%')))
    else:
        invoices = Invoice.query.filter(Invoice.isDelete == True)
    invoices_tmp = invoices
    if offset:
        invoices = invoices.offset(offset)
    if limit:
        invoices = invoices.limit(limit)

    newHistory = History(
        userName=current_user.id,
        modelName='Invoice(dust)',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()

    if moreCheck:
        totalRecordCount = invoices_tmp.count()
        nowRecordCount = limit+offset
        isMore = True if nowRecordCount < totalRecordCount else False
        return jsonify({'invoices': InvoiceSchema(many=True).dump(invoices), 'isMore': isMore})

    return jsonify(InvoiceSchema(many=True).dump(invoices))


@app.route('/v1/invoice/<id>', methods=['GET'])
@app.route('/invoice/<id>', methods=['GET'])
def invoice_show(id):
    invoiceCount = Invoice.query.filter(Invoice.id == id).count()
    if invoiceCount:
        invoice = Invoice.query.filter(Invoice.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='Invoice',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(InvoiceSchema().dump(invoice))
    else:
        return jsonify([])


@app.route('/v1/invoice', methods=['POST'])
@app.route('/invoice', methods=['POST'])
def invoice_create():
    data = request.json
    newInvoiceItems = []
    if data.get('invoice_items'):
        for item in data.get('invoice_items'):
            if item.get('isDelete'):
                if item['isDelete']:
                    continue
            newInvoiceItems.append(
                Invoice_Item(
                    invoiceId=item.get('invoiceId'),
                    itemId=item.get('itemId'),
                    any=item.get('any')if item.get('any') else None,
                    itemName=item.get('itemName')if item.get(
                        'itemName') else None,
                    price=item.get('price')if item.get('price') else None,
                    cost=item.get('cost')if item.get('cost') else 0,
                    count=item.get('count')if item.get('count') else None,
                    unit=item.get('unit')if item.get('unit') else None,
                    remarks=item.get('remarks')if item.get(
                        'remarks') else None,
                )
            )

        # newInvoiceItems = [
        #    Invoice_Item(
        #        invoiceId=item.get('invoiceId'),
        #        itemId=item.get('itemId'),
        #        price=item.get('price'),
        #        count=item.get('count'),
        #        unit=item.get('unit'),
        #        itemName=item.get('itemName'),
        #    )
        #    for item in data.get('invoice_items')
        # ]

    newInvoice = Invoice(
        customerId=data.get('customerId'),
        customerName=data.get('customerName'),
        customerAnyNumber=data.get('customerAnyNumber'),
        honorificTitle=data.get('honorificTitle')if data.get(
            'honorificTitle') else None,
        department=data.get('department')if data.get('department') else None,
        manager=data.get('manager')if data.get('manager') else None,
        otherPartyManager=data.get('otherPartyManager')if data.get(
            'otherPartyManager') else None,
        applyDate=datetime.strptime(
            data.get('applyDate'), "%Y-%m-%d") if data.get('applyDate') else None,
        deadLine=datetime.strptime(
            data.get('deadLine'), "%Y-%m-%d") if data.get('deadLine') else None,
        paymentDate=datetime.strptime(
            data.get('paymentDate'), "%Y-%m-%d") if data.get('paymentDate') else None,
        isPaid=data.get('isPaid'),
        title=data.get('title')if data.get('title') else None,
        memo=data.get('memo')if data.get('memo') else None,
        remarks=data.get('remarks')if data.get('remarks') else None,
        tax=data.get('tax'),
        isTaxExp=data.get('isTaxExp'),
        numberOfAttachments=data.get('numberOfAttachments'),
        invoice_items=newInvoiceItems,
    )
    db.session.add(newInvoice)
    db.session.commit()
    id = newInvoice.id
    newHistory = History(
        userName=current_user.id,
        modelName='Invoice',
        modelId=id,
        action='post'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/invoice/<id>', methods=['PUT'])
@app.route('/invoice/<id>', methods=['PUT'])
def invoice_update(id):
    data = request.json

    invoice = Invoice.query.filter(Invoice.id == id).one()
    invoiceItemsIds = db.session.query(Invoice_Item.id).filter(
        Invoice_Item.invoiceId == id).all()
    if not invoice:
        return jsonify({"result": "No Data", "id": id, "data": data})

    invoice.customerId = data.get('customerId')
    invoice.customerName = data.get('customerName')
    invoice.customerAnyNumber = data.get('customerAnyNumber')
    invoice.honorificTitle = data.get(
        'honorificTitle')if data.get('honorificTitle') else None
    invoice.department = data.get(
        'department')if data.get('department') else None
    invoice.manager = data.get('manager')if data.get('manager') else None
    invoice.otherPartyManager = data.get(
        'otherPartyManager')if data.get('otherPartyManager') else None
    invoice.applyNumber = data.get('applyNumber')
    invoice.applyDate = datetime.strptime(
        data.get('applyDate'), "%Y-%m-%d") if data.get('applyDate') else None
    invoice.deadLine = datetime.strptime(
        data.get('deadLine'), "%Y-%m-%d") if data.get('deadLine') else None
    invoice.paymentDate = datetime.strptime(
        data.get('paymentDate'), "%Y-%m-%d") if data.get('paymentDate') else None
    invoice.isPaid = data.get('isPaid')
    invoice.title = data.get('title')if data.get('title') else None
    invoice.memo = data.get('memo')if data.get('memo') else None
    invoice.remarks = data.get('remarks')if data.get('remarks') else None
    invoice.tax = data.get('tax')
    invoice.isTaxExp = data.get('isTaxExp')
    invoice.numberOfAttachments = data.get('numberOfAttachments')

    if data.get('invoice_items'):
        update_list = []
        insert_list = []
        delete_in_list = []
        for i in invoiceItemsIds:
            delete_in_list.append(i.id)
        for item in data['invoice_items']:
            if 'createdAt' in item:
                del(item['createdAt'])
            if 'updatedAt' in item:
                del(item['updatedAt'])
            for columnName in item.keys():
                if columnName == 'cost':
                    if item['cost'] == '' or item['cost'] == None:
                        item['cost'] = 0
                elif item[columnName] == '':
                    item[columnName] = None

            if item.get('id'):
                update_list.append(item)
                index = next((i for i, x in enumerate(
                    delete_in_list) if x == item['id']), None)
                if index != None:
                    delete_in_list.pop(index)
            else:
                insert_list.append(item)

        db.session.bulk_update_mappings(Invoice_Item, update_list)
        db.session.bulk_insert_mappings(Invoice_Item, insert_list)
        db.session.query(Invoice_Item).filter(Invoice_Item.id.in_(
            delete_in_list)).delete(synchronize_session='fetch')

    newHistory = History(
        userName=current_user.id,
        modelName='Invoice',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/invoice_delete/<id>', methods=['PUT'])
@app.route('/invoice_delete/<id>', methods=['PUT'])
def invoice_destroy(id):
    invoice = Invoice.query.filter(Invoice.id == id).one()
    invoice.isDelete = True
    newHistory = History(
        userName=current_user.id,
        modelName='Invoice',
        modelId=id,
        action='put(dust)'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ""})


# 請求書＿商品(Invoice_Items)
@app.route('/invoice_items', methods=['GET'])
def invoice_item_index():
    invoiceItems = Invoice_Item.query.all()
    newHistory = History(
        userName=current_user.id,
        modelName='InvoiceItems',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(Invoice_ItemSchema(many=True).dump(invoiceItems))


@app.route('/invoice_item/<id>', methods=['GET'])
def invoice_item_show(id):
    invoiceItemCount = Invoice_Item.query.filter(Invoice_Item.id == id).count()
    if invoiceItemCount:
        invoiceItem = Invoice_Item.query.filter(Invoice_Item.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='InvoiceItems',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(Invoice_ItemSchema().dump(invoiceItem))
    else:
        return jsonify([])


@app.route('/invoice_items/<hid>', methods=['GET'])
def invoice_item_show_by_invoiceId(hid):
    invoiceItems = Invoice_Item.query.filter(
        Invoice_Item.invoiceId == hid).all()
    newHistory = History(
        userName=current_user.id,
        modelName='InvoiceItems',
        modelId=hid,
        action='gets')
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(Invoice_ItemSchema(many=True).dump(invoiceItems))


@app.route('/invoice_item', methods=['POST'])
def invoice_item_create():
    data = request.json
    newInvoiceItem = Invoice_Item(
        invoiceId=data.get('invoiceId'),
        itemId=data.get('itemId'),
        itemName=data.get('itemName'),
        price=data.get('price'),
        cost=data.get('cost'),
        count=data.get('count'),
        unit=data.get('unit'),
        remarks=data.get('remarks'),
    )
    db.session.add(newInvoiceItem)
    db.session.commit()
    id = newInvoiceItem.id
    newHistory = History(
        userName=current_user.id,
        modelName='InvoiceItems',
        modelId=id,
        action='post')
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/invoice_item/<id>', methods=['PUT'])
def invoice_item_update(id):
    data = request.json
    invoiceItem = Invoice_Item.query.filter(Invoice_Item.id == id).one()
    invoiceItem.invoiceId = data.get('invoiceId')
    invoiceItem.itemId = data.get('itemId')
    invoiceItem.itemName = data.get('itemName')
    invoiceItem.price = data.get('price')
    invoiceItem.cost = data.get('cost')
    invoiceItem.count = data.get('count')
    invoiceItem.unit = data.get('unit')
    invoiceItem.remarks = data.get('remarks')

    newHistory = History(
        userName=current_user.id,
        modelName='InvoiceItems',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/invoice_item/<id>', methods=['DELETE'])
def invoice_item_destroy(id):
    invoiceItem = Invoice_Item.query.filter(Invoice_Item.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='InvoiceItems',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# 請求書＿入金(Invoice_Payments)
@app.route('/invoice_payments', methods=['GET'])
def invoice_payment_index():
    invoicePayments = Invoice_Payment.query.all()
    newHistory = History(
        userName=current_user.id,
        modelName='InvoicePayments',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(Invoice_PaymentSchema(many=True).dump(invoicePayments))


@app.route('/invoice_payment/<id>', methods=['GET'])
def invoice_payment_show(id):
    invoicePaymentCount = Invoice_Payment.query.filter(
        Invoice_Payment.id == id).count()
    if invoicePaymentCount:
        invoicePayment = Invoice_Payment.query.filter(
            Invoice_Payment.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='InvoicePayments',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(Invoice_PaymentSchema().dump(invoicePayment))
    else:
        return jsonify([])


@app.route('/invoice_payments/<hid>', methods=['GET'])
def invoice_payment_show_by_invoiceId(hid):
    invoicePayments = Invoice_Payment.query.filter(
        Invoice_Payment.invoiceId == hid).all()
    newHistory = History(
        userName=current_user.id,
        modelName='InvoicePayments',
        modelId=hid,
        action='gets')
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(Invoice_PaymentSchema(many=True).dump(invoicePayments))


@app.route('/invoice_payment', methods=['POST'])
def invoice_payment_create():
    data = request.json
    newInvoiceItem = Invoice_Payment(
        invoiceId=data.get('invoiceId'),
        paymentDate=data.get('paymentDate'),
        paymentMethod=data.get('paymentMethod'),
        paymentAmount=data.get('paymentAmount'),
        remarks=data.get('remarks'),
    )
    db.session.add(newInvoiceItem)
    db.session.commit()
    id = newInvoiceItem.id
    newHistory = History(
        userName=current_user.id,
        modelName='InvoicePayments',
        modelId=id,
        action='post')
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/invoice_payment/<id>', methods=['PUT'])
def invoice_payment_update(id):
    data = request.json
    req = request.args
    priceIncludingTax = int(req.get('priceIncludingTax'))
    paymentSum = int(req.get('paymentSum'))
    invoice = Invoice.query.filter(Invoice.id == id).one()
    invoicePaymentIds = db.session.query(Invoice_Payment.id).filter(
        Invoice_Payment.invoiceId == id).all()
    if not invoice:
        return jsonify({"result": "No Data", "id": id, "data": data})

    if data.get('invoice_payments'):
        update_list = []
        insert_list = []
        delete_in_list = []
        for i in invoicePaymentIds:
            delete_in_list.append(i.id)
        for item in data['invoice_payments']:
            if 'createdAt' in item:
                del(item['createdAt'])
            if 'updatedAt' in item:
                del(item['updatedAt'])

            item['paymentDate'] = datetime.strptime(
                item.get('paymentDate'), "%Y-%m-%d") if item.get('paymentDate') else None
            for columnName in item.keys():
                if item[columnName] == '':
                    item[columnName] = None

            if item.get('id'):
                update_list.append(item)
                index = next((i for i, x in enumerate(
                    delete_in_list) if x == item['id']), None)
                if index != None:
                    delete_in_list.pop(index)
            else:
                insert_list.append(item)

        db.session.bulk_update_mappings(Invoice_Payment, update_list)
        db.session.bulk_insert_mappings(Invoice_Payment, insert_list)
        db.session.query(Invoice_Payment).filter(Invoice_Payment.id.in_(
            delete_in_list)).delete(synchronize_session='fetch')

    else:
        db.session.query(Invoice_Payment).filter(
            Invoice_Payment.invoiceId == id).delete()

    # 入金合計額が上回れば入金済みに（変動）
    if paymentSum >= priceIncludingTax:
        invoice.isPaid = True
    else:
        invoice.isPaid = False

    newHistory = History(
        userName=current_user.id,
        modelName='InvoicePayments',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/invoice_payment/<id>', methods=['DELETE'])
def invoice_payment_destroy(id):
    invoicePayment = Invoice_Payment.query.filter(
        Invoice_Payment.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='InvoicePayments',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# 見積書(Quotations)
@app.route('/v1/quotations', methods=['GET'])
@app.route('/quotations', methods=['GET'])
def quotation_index_v1():
    # パラメータを準備
    req = request.args
    searchWord = req.get('search')
    moreCheck = req.get('moreCheck') if req.get('moreCheck') else False
    limit = int(req.get('limit')) if req.get('limit') else _LIMIT_NUM
    offset = int(req.get('offset')) if req.get('offset') else 0
    # 各種フィルタリング処理
    if searchWord:
        if len(searchWord) == 4:
            quotations = Quotation.query.filter(and_(Invoice.isDelete == False, or_(
                extract('year', Quotation.applyDate) == searchWord, Quotation.customerName.like('%'+searchWord+'%'))))
        elif len(searchWord) == 6:
            year = searchWord[:4]
            month = searchWord[4:]
            quotations = Quotation.query.filter(and_(Invoice.isDelete == False, or_(
                Quotation.customerName.like('%'+searchWord+'%'), and_(
                    extract('year', Quotation.applyDate) == year, extract('month', Quotation.applyDate) == month))))
        elif len(searchWord) == 8:
            year = searchWord[:4]
            month = searchWord[4:6]
            day = searchWord[6:]
            quotations = Quotation.query.filter(and_(Invoice.isDelete == False, or_(
                Quotation.customerName.like('%'+searchWord+'%'), and_(
                    extract('year', Quotation.applyDate) == year, extract('month', Quotation.applyDate) == month, extract('day', Quotation.applyDate) == day))))
        else:
            quotations = Quotation.query.filter(
                and_(Quotation.isDelete == False, Quotation.customerName.like('%'+searchWord+'%')))
    else:
        quotations = Quotation.query.filter(Quotation.isDelete == False)
    quotations_tmp = quotations
    if offset:
        quotations = quotations.offset(offset)
    if limit:
        quotations = quotations.limit(limit)

    newHistory = History(
        userName=current_user.id,
        modelName='Quotation',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()

    if moreCheck:
        totalRecordCount = quotations_tmp.count()
        nowRecordCount = limit+offset
        isMore = True if nowRecordCount < totalRecordCount else False
        return jsonify({'quotations': QuotationSchema(many=True).dump(quotations), 'isMore': isMore})

    return jsonify(QuotationSchema(many=True).dump(quotations))


@app.route('/v1/dust-quotations', methods=['GET'])
@app.route('/dust-quotations', methods=['GET'])
def dust_quotation_index_v1():
    # パラメータを準備
    req = request.args
    searchWord = req.get('search')
    moreCheck = req.get('moreCheck') if req.get('moreCheck') else False
    limit = int(req.get('limit')) if req.get('limit') else _LIMIT_NUM
    offset = int(req.get('offset')) if req.get('offset') else 0
    # 各種フィルタリング処理
    if searchWord:
        if len(searchWord) == 4:
            quotations = Quotation.query.filter(and_(Quotation.isDelete == True, or_(
                extract('year', Quotation.applyDate) == searchWord, Quotation.customerName.like('%'+searchWord+'%'))))
        elif len(searchWord) == 6:
            year = searchWord[:4]
            month = searchWord[4:]
            quotations = Quotation.query.filter(and_(Quotation.isDelete == True, or_(
                Quotation.customerName.like('%'+searchWord+'%'), and_(
                    extract('year', Quotation.applyDate) == year, extract('month', Quotation.applyDate) == month))))
        elif len(searchWord) == 8:
            year = searchWord[:4]
            month = searchWord[4:6]
            day = searchWord[6:]
            quotations = Quotation.query.filter(and_(Quotation.isDelete == True, or_(
                Quotation.customerName.like('%'+searchWord+'%'), and_(
                    extract('year', Quotation.applyDate) == year, extract('month', Quotation.applyDate) == month, extract('day', Quotation.applyDate) == day))))
        else:
            quotations = Quotation.query.filter(
                and_(Quotation.isDelete == True, Quotation.customerName.like('%'+searchWord+'%')))
    else:
        quotations = Quotation.query.filter(Quotation.isDelete == True)
    quotations_tmp = quotations
    if offset:
        quotations = quotations.offset(offset)
    if limit:
        quotations = quotations.limit(limit)

    newHistory = History(
        userName=current_user.id,
        modelName='Quotation(dust)',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()

    if moreCheck:
        totalRecordCount = quotations_tmp.count()
        nowRecordCount = limit+offset
        isMore = True if nowRecordCount < totalRecordCount else False
        return jsonify({'quotations': QuotationSchema(many=True).dump(quotations), 'isMore': isMore})

    return jsonify(QuotationSchema(many=True).dump(quotations))


@app.route('/v1/quotation/<id>', methods=['GET'])
@app.route('/quotation/<id>', methods=['GET'])
def quotation_show(id):
    quotationCount = Quotation.query.filter(Quotation.id == id).count()
    if quotationCount:
        quotation = Quotation.query.filter(Quotation.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='Quotation',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(QuotationSchema().dump(quotation))
    else:
        return jsonify([])


@app.route('/v1/quotation', methods=['POST'])
@app.route('/quotation', methods=['POST'])
def quotation_create():
    data = request.json
    newQuotationItems = []
    if data.get('quotation_items'):
        for item in data.get('quotation_items'):
            if item.get('isDelete'):
                if item['isDelete']:
                    continue

            newQuotationItems.append(
                Quotation_Item(
                    quotationId=item.get('quotationId'),
                    itemId=item.get('itemId'),
                    any=item.get('any')if item.get('any') else None,
                    itemName=item.get('itemName')if item.get(
                        'itemName') else None,
                    price=item.get('price')if item.get('price') else None,
                    cost=item.get('cost')if item.get('cost') else 0,
                    count=item.get('count')if item.get('count') else None,
                    unit=item.get('unit')if item.get('unit') else None,
                    remarks=item.get('remarks')if item.get(
                        'remarks') else None,
                )
            )

    newQuotation = Quotation(
        customerId=data.get('customerId'),
        customerName=data.get('customerName'),
        customerAnyNumber=data.get('customerAnyNumber'),
        honorificTitle=data.get('honorificTitle')if data.get(
            'honorificTitle') else None,
        department=data.get('department')if data.get('department') else None,
        manager=data.get('manager')if data.get('manager') else None,
        otherPartyManager=data.get('otherPartyManager')if data.get(
            'otherPartyManager') else None,
        applyDate=datetime.strptime(
            data.get('applyDate'), "%Y-%m-%d") if data.get('applyDate') else None,
        expiry=data.get('expiry'),
        dayOfDelivery=data.get('dayOfDelivery'),
        termOfSale=data.get('termOfSale'),
        isConvert=data.get('isConvert') if data.get('isConvert') else False,
        title=data.get('title')if data.get('title') else None,
        memo=data.get('memo')if data.get('memo') else None,
        remarks=data.get('remarks')if data.get('remarks') else None,
        tax=data.get('tax'),
        isTaxExp=data.get('isTaxExp'),
        numberOfAttachments=data.get('numberOfAttachments'),
        quotation_items=newQuotationItems,
    )
    db.session.add(newQuotation)
    db.session.commit()
    id = newQuotation.id
    newHistory = History(
        userName=current_user.id,
        modelName='Quotation',
        modelId=id,
        action='post'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/quotation/<id>', methods=['PUT'])
@app.route('/quotation/<id>', methods=['PUT'])
def quotation_update(id):
    data = request.json

    quotation = Quotation.query.filter(Quotation.id == id).one()
    quotationItemsIds = db.session.query(Quotation_Item.id).filter(
        Quotation_Item.quotationId == id).all()
    if not quotation:
        return jsonify({"result": "No Data", "id": id, "data": data})

    quotation.customerId = data.get('customerId')
    quotation.customerName = data.get('customerName')
    quotation.customerAnyNumber = data.get('customerAnyNumber')
    quotation.honorificTitle = data.get(
        'honorificTitle')if data.get('honorificTitle') else None
    quotation.department = data.get(
        'department')if data.get('department') else None
    quotation.manager = data.get('manager')if data.get('manager') else None
    quotation.otherPartyManager = data.get(
        'otherPartyManager')if data.get('otherPartyManager') else None
    quotation.applyNumber = data.get('applyNumber')
    quotation.applyDate = datetime.strptime(
        data.get('applyDate'), "%Y-%m-%d") if data.get('applyDate') else None
    quotation.expiry = data.get('expiry')
    quotation.dayOfDelivery = data.get('dayOfDelivery')
    quotation.termOfSale = data.get('termOfSale')
    quotation.isConvert = data.get(
        'isConvert') if data.get('isConvert') else False
    quotation.title = data.get('title')if data.get('title') else None
    quotation.memo = data.get('memo')if data.get('memo') else None
    quotation.remarks = data.get('remarks')if data.get('remarks') else None
    quotation.tax = data.get('tax')
    quotation.isTaxExp = data.get('isTaxExp')
    quotation.numberOfAttachments = data.get('numberOfAttachments')

    if data.get('quotation_items'):
        update_list = []
        insert_list = []
        delete_in_list = []
        for i in quotationItemsIds:
            delete_in_list.append(i.id)
        for item in data['quotation_items']:
            print(item)
            if 'createdAt' in item:
                del(item['createdAt'])
            if 'updatedAt' in item:
                del(item['updatedAt'])
            for columnName in item.keys():
                if columnName == 'cost':
                    if item['cost'] == '' or item['cost'] == None:
                        item['cost'] = 0
                elif item[columnName] == '':
                    item[columnName] = None

            if item.get('id'):
                update_list.append(item)
                index = next((i for i, x in enumerate(
                    delete_in_list) if x == item['id']), None)
                if index != None:
                    delete_in_list.pop(index)
            else:
                insert_list.append(item)

        db.session.bulk_update_mappings(Quotation_Item, update_list)
        db.session.bulk_insert_mappings(Quotation_Item, insert_list)
        db.session.query(Quotation_Item).filter(Quotation_Item.id.in_(
            delete_in_list)).delete(synchronize_session='fetch')

    newHistory = History(
        userName=current_user.id,
        modelName='Quotation',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/quotation_delete/<id>', methods=['PUT'])
@app.route('/quotation_delete/<id>', methods=['PUT'])
def quotation_destroy(id):
    quotation = Quotation.query.filter(Quotation.id == id).one()
    quotation.isDelete = True
    newHistory = History(
        userName=current_user.id,
        modelName='Quotation',
        modelId=id,
        action='put(dust)'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ""})


# 見積書＿商品(Quotation_Items)
@app.route('/quotation_items', methods=['GET'])
def quotation_item_index():
    quotationItems = Quotation_Item.query.all()
    newHistory = History(
        userName=current_user.id,
        modelName='QuotationItems',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(Quotation_ItemSchema(many=True).dump(quotationItems))


@app.route('/quotation_item/<id>', methods=['GET'])
def quotation_item_show(id):
    quotationItemCount = Quotation_Item.query.filter(
        Quotation_Item.id == id).count()
    if quotationItemCount:
        quotationItem = Quotation_Item.query.filter(
            Quotation_Item.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='QuotationItems',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(Quotation_ItemSchema().dump(quotationItem))
    else:
        return jsonify([])


@app.route('/quotation_items/<hid>', methods=['GET'])
def quotation_item_show_by_quotationId(hid):
    quotationItems = Quotation_Item.query.filter(
        Quotation_Item.quotationId == hid).all()
    newHistory = History(
        userName=current_user.id,
        modelName='QuotationItems',
        modelId=hid,
        action='gets')
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(Quotation_ItemSchema(many=True).dump(quotationItems))


@app.route('/quotation_item', methods=['POST'])
def quotation_item_create():
    data = request.json
    newQuotationItem = Quotation_Item(
        quotationId=data.get('quotationId'),
        itemId=data.get('itemId'),
        itemName=data.get('itemName'),
        price=data.get('price'),
        cost=data.get('cost'),
        count=data.get('count'),
        unit=data.get('unit'),
        remarks=data.get('remarks'),
    )
    db.session.add(newQuotationItem)
    db.session.commit()
    id = newQuotationItem.id

    newHistory = History(
        userName=current_user.id,
        modelName='QuotationItems',
        modelId=id,
        action='post')
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/quotation_item/<id>', methods=['PUT'])
def quotation_item_update(id):
    data = request.json
    quotationItem = Quotation_Item.query.filter(Quotation_Item.id == id).one()
    quotationItem.quotationId = data.get('quotationId')
    quotationItem.itemId = data.get('itemId')
    quotationItem.itemName = data.get('itemName')
    quotationItem.price = data.get('price')
    quotationItem.cost = data.get('cost')
    quotationItem.count = data.get('count')
    quotationItem.unit = data.get('unit')
    quotationItem.remarks = data.get('remarks')

    newHistory = History(
        userName=current_user.id,
        modelName='QuotationItems',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/quotation_item/<id>', methods=['DELETE'])
def quotation_item_destroy(id):
    quotationItem = Quotation_Item.query.filter(
        Quotation_Item.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='QuotationItems',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# メモ(Memos)
@app.route('/v1/memos', methods=['GET'])
@app.route('/memos', methods=['GET'])
def memo_index_v1():
   # パラメータを準備
    req = request.args
    searchWord = req.get('search')
    moreCheck = req.get('moreCheck') if req.get('moreCheck') else False
    limit = int(req.get('limit')) if req.get('limit') else _LIMIT_NUM
    offset = int(req.get('offset')) if req.get('offset') else 0
    # 各種フィルタリング処理
    if searchWord:
        if len(searchWord) == 4:
            memos = Memo.query.filter(or_(
                extract('year', Memo.createdAt) == searchWord, Memo.manager.like('%'+searchWord+'%')))
        elif len(searchWord) == 6:
            year = searchWord[:4]
            month = searchWord[4:]
            memos = Memo.query.filter(or_(Memo.manager.like('%'+searchWord+'%'), and_(
                extract('year', Memo.createdAt) == year, extract('month', Memo.createdAt) == month)))
        elif len(searchWord) == 8:
            year = searchWord[:4]
            month = searchWord[4:6]
            day = searchWord[6:]
            memos = Memo.query.filter(or_(Memo.manager.like('%'+searchWord+'%'), and_(
                extract('year', Memo.createdAt) == year, extract('month', Memo.createdAt) == month, extract('day', Memo.createdAt) == day)))
        else:
            memos = Memo.query.filter(
                Memo.manager.like('%'+searchWord+'%'))
    else:
        memos = Memo.query
    memos_tmp = memos
    if offset:
        memos = memos.offset(offset)
    if limit:
        memos = memos.limit(limit)

    newHistory = History(
        userName=current_user.id,
        modelName='Memo',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()

    if moreCheck:
        totalRecordCount = memos_tmp.count()
        nowRecordCount = limit+offset
        isMore = True if nowRecordCount < totalRecordCount else False
        return jsonify({'memos': MemoSchema(many=True).dump(memos), 'isMore': isMore})

    return jsonify(MemoSchema(many=True).dump(memos))


@app.route('/v1/memo/<id>', methods=['GET'])
@app.route('/memo/<id>', methods=['GET'])
def memo_show(id):
    memoCount = Memo.query.filter(Memo.id == id).count()
    if memoCount:
        memo = Memo.query.filter(Memo.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='Memo',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(MemoSchema().dump(memo))
    else:
        return jsonify([])


@app.route('/v1/memo', methods=['POST'])
@app.route('/memo', methods=['POST'])
def memo_create():
    data = request.json
    newMemo = Memo(
        title=data.get('title')if data.get('title') else None,
        manager=data.get('manager')if data.get('manager') else None,
        isFavorite=data.get('isFavorite'),
        content=data.get('content')if data.get('content') else None,
    )
    db.session.add(newMemo)
    db.session.commit()
    id = newMemo.id
    newHistory = History(
        userName=current_user.id,
        modelName='Memo',
        modelId=id,
        action='post'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/memo/<id>', methods=['PUT'])
@app.route('/memo/<id>', methods=['PUT'])
def memo_update(id):
    data = request.json
    memo = Memo.query.filter(Memo.id == id).one()

    memo.title = data.get('title')if data.get('title') else None
    memo.manager = data.get('manager')if data.get('manager') else None
    memo.isFavorite = data.get('isFavorite') if data.get(
        'isFavorite') else False  # ページリロード後、更新時のエラー防止
    memo.content = data.get('content')if data.get('content') else None

    newHistory = History(
        userName=current_user.id,
        modelName='Memo',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/memo/<id>', methods=['DELETE'])
@app.route('/memo/<id>', methods=['DELETE'])
def memo_destroy(id):
    memo = Memo.query.filter(Memo.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='Memo',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# 単位(Units)
@app.route('/units', methods=['GET'])
def unit_index():
    units = Unit.query.all()
    newHistory = History(
        userName=current_user.id,
        modelName='Unit',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(UnitSchema(many=True).dump(units))


@app.route('/unit/<id>', methods=['GET'])
def unit_show(id):
    unitCount = Unit.query.filter(Unit.id == id).count()
    if unitCount:
        unit = Unit.query.filter(Unit.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='Unit',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(UnitSchema().dump(unit))
    else:
        return jsonify([])


@app.route('/unit', methods=['POST'])
def unit_create():
    data = request.json
    newUnit = Unit(
        unitName=data.get('unitName')if data.get('unitName') else None,
    )
    db.session.add(newUnit)
    db.session.commit()
    id = newUnit.id
    newHistory = History(
        userName=current_user.id,
        modelName='Unit',
        modelId=id,
        action='post'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/unit/<id>', methods=['PUT'])
def unit_update(id):
    data = request.json
    unit = Unit.query.filter(Unit.id == id).one()

    unit.unitName = data.get('unitName')if data.get('unitName') else None
    newHistory = History(
        userName=current_user.id,
        modelName='Unit',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/unit/<id>', methods=['DELETE'])
def unit_destroy(id):
    unit = Unit.query.filter(Unit.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='Unit',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# カテゴリー(categories)
@app.route('/categories', methods=['GET'])
def category_index():
    categories = Category.query.all()
    newHistory = History(
        userName=current_user.id,
        modelName='Category',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(CategorySchema(many=True).dump(categories))


@app.route('/category/<id>', methods=['GET'])
def category_show(id):
    categoryCount = Category.query.filter(Category.id == id).count()
    if categoryCount:
        category = Category.query.filter(Category.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='Category',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(CategorySchema().dump(category))
    else:
        return jsonify([])


@app.route('/category', methods=['POST'])
def category_create():
    data = request.json
    newCategory = Category(
        categoryName=data.get('categoryName')if data.get(
            'categoryName') else None,
    )
    db.session.add(newCategory)
    db.session.commit()
    id = newCategory.id

    newHistory = History(
        userName=current_user.id,
        modelName='Category',
        modelId=id,
        action='post'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/category/<id>', methods=['PUT'])
def category_update(id):
    data = request.json
    category = Category.query.filter(Category.id == id).one()

    category.categoryName = data.get(
        'categoryName')if data.get('categoryName') else None

    newHistory = History(
        userName=current_user.id,
        modelName='Category',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/category/<id>', methods=['DELETE'])
def category_destroy(id):
    category = Category.query.filter(Category.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='Category',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# メーカー(Makers)
@app.route('/makers', methods=['GET'])
def maker_index():
    makers = Maker.query.all()
    newHistory = History(
        userName=current_user.id,
        modelName='Maker',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(MakerSchema(many=True).dump(makers))


@app.route('/maker/<id>', methods=['GET'])
def maker_show(id):
    makerCount = Maker.query.filter(Maker.id == id).count()
    if makerCount:
        maker = Maker.query.filter(Maker.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='Maker',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(MakerSchema().dump(maker))
    else:
        return jsonify([])


@app.route('/maker', methods=['POST'])
def maker_create():
    data = request.json
    newMaker = Maker(
        makerName=data.get('makerName')if data.get('makerName') else None,
    )
    db.session.add(newMaker)
    db.session.commit()
    id = newMaker.id

    newHistory = History(
        userName=current_user.id,
        modelName='Maker',
        modelId=id,
        action='post'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/maker/<id>', methods=['PUT'])
def maker_update(id):
    data = request.json
    maker = Maker.query.filter(Maker.id == id).one()

    maker.makerName = data.get('makerName')if data.get('makerName') else None

    newHistory = History(
        userName=current_user.id,
        modelName='Maker',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/maker/<id>', methods=['DELETE'])
def maker_destroy(id):
    maker = Maker.query.filter(Maker.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='Maker',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


@app.route('/setting', methods=['GET'])
def setting_show():
    setting = Setting.query.filter(Setting.id == 1).first()
    newHistory = History(
        userName=current_user.id,
        modelName='Setting',
        modelId=1,
        action='get')
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(SettingSchema().dump(setting))


@app.route('/setting/<id>', methods=['PUT'])
def setting_update(id):
    data = request.json
    setting = Setting.query.filter(Setting.id == id).one()

    setting.companyName = data.get(
        'companyName')if data.get('companyName') else None
    setting.registerNumber = data.get(
        'registerNumber')if data.get('registerNumber') else None
    setting.representative = data.get(
        'representative')if data.get('representative') else None
    setting.administrator = data.get(
        'administrator')if data.get('administrator') else None
    setting.postNumber = data.get(
        'postNumber')if data.get('postNumber') else None
    setting.address = data.get('address')if data.get('address') else None
    setting.telNumber = data.get('telNumber')if data.get('telNumber') else None
    setting.faxNumber = data.get('faxNumber')if data.get('faxNumber') else None
    setting.url = data.get('url')if data.get('url') else None
    setting.email = data.get('email')if data.get('email') else None
    setting.payee = data.get('payee')if data.get('payee') else None
    setting.accountHolder = data.get(
        'accountHolder')if data.get('accountHolder') else None
    setting.accountHolderKana = data.get(
        'accountHolderKana')if data.get('accountHolderKana') else None
    setting.logoFilePath = data.get(
        'logoFilePath')if data.get('logoFilePath') else None
    setting.logoHeight = data.get(
        'logoHeight')if data.get('logoHeight') else None
    setting.logoWidth = data.get('logoWidth')if data.get('logoWidth') else None
    setting.stampFilePath = data.get(
        'stampFilePath')if data.get('stampFilePath') else None
    setting.stampHeight = data.get(
        'stampHeight')if data.get('stampHeight') else None
    setting.stampWidth = data.get(
        'stampWidth')if data.get('stampWidth') else None
    setting.isDisplayQuotationLogo = data.get('isDisplayQuotationLogo')
    setting.isDisplayInvoiceLogo = data.get('isDisplayInvoiceLogo')
    setting.isDisplayDeliveryLogo = data.get('isDisplayDeliveryLogo')
    setting.isDisplayQuotationStamp = data.get('isDisplayQuotationStamp')
    setting.isDisplayInvoiceStamp = data.get('isDisplayInvoiceStamp')
    setting.isDisplayDeliveryStamp = data.get('isDisplayDeliveryStamp')
    setting.defaultTax = data.get(
        'defaultTax')if data.get('defaultTax') else None

    newHistory = History(
        userName=current_user.id,
        modelName='Setting',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


# 操作履歴(Histories)
@app.route('/histories', methods=['GET'])
def history_index():
    histories = History.query.all()
    newHistory = History(
        userName=current_user.id,
        modelName='History',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(HistorySchema(many=True).dump(histories))


@app.route('/login-histories', methods=['GET'])
def login_history_index():
    loginHistories = History.query.order_by(desc(History.id)).limit(_LIMIT_NUM)
    return jsonify(HistorySchema(many=True).dump(loginHistories))


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5010, debug=True)
