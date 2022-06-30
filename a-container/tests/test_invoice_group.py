from datetime import datetime
import unittest
import sys
import os
#from app.models import Invoice_Item

sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))
from app import db, app
from models import *
from seeder import seeder


class BasicTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # print('-----setUp-----')
        pass

    # テスト後にシーダーを流しなおす
    @classmethod
    def tearDownClass(cls):
        print("---tearDown---")
        seeder()

    def test_get_invoices(self):
        print('---Invoice全件読み込み---')
        invoices = Invoice.query.all()
        invoiceCount = len(invoices)
        self.assertTrue(invoiceCount)
        # customerまで全件取得
        print('Invoice→Customer全件読込')
        customerCount = 0
        for invoice in invoices:
            if(invoice.customer is not None):
                customerCount += 1
        self.assertGreaterEqual(customerCount, 1)

        # Invoice_Itemまで取得
        print('Invoice→Invoice_Item全件取得')
        invoiceItemCount = 0
        for invoice in invoices:
            for invoiceItem in invoice.invoice_items:
                invoiceItemCount += 1
        self.assertGreaterEqual(invoiceItemCount, 1)

    def test_get_invoices_dict(self):
        print('---Invoice全件読込→Dict---')
        invoices = Invoice.query.all()
        sch = InvoiceSchema(many=True).dump(invoices)
        self.assertEqual(sch[0]['title'], '○○株式会社への請求書')

    # def my_func(self,p):
    #    return p+1

    def total_price(self, items):
        price = 0
        print("items:", items[0])

        # for item in items:
        #    print("invoice_items",item)
        #    price += 1
        return True

    def test_get_invoices_group(self):
        def my_calc(price, count):
            return price*count
        print('---Invoice全件読み込み(group前)---')
        invoices = Invoice.query.all()
        invoiceCount = len(invoices)
        self.assertTrue(invoiceCount)
        # ------ group --------
        # invoices = db.session.query(func.strftime("%Y-%m", Invoice.applyDate), func.sum(
        #    Invoice.tax).label('total_tax')).group_by(func.strftime("%Y-%m", Invoice.applyDate)).all()

        print("-------invoices を全件取得------------------")
        invoices = db.session.query(Invoice.applyDate, Invoice.id).all()
        for invoice in invoices:
            print(invoice)
        #    print(invoice.applyDate, invoice.title,invoice.invoice_items)
        print("--------invoice_itemsを全件取得-----------------")
        invoice_items = db.session.query(Invoice_Item.invoiceId, my_calc(
            Invoice_Item.price, Invoice_Item.count)).all()
        for item in invoice_items:
            print(item)
        print("--------invoice_itemsの計算値取得-----------------")
        invoice_items = db.session.query(Invoice_Item.invoiceId, func.sum(my_calc(
            Invoice_Item.price, Invoice_Item.count))).group_by(Invoice_Item.invoiceId).all()
        for item in invoice_items:
            print(item)
        print("--------JOIN INVOCES に計算値をJOIN -----------------")
        calc_joins = db.session.query(Invoice.id, Invoice.title, my_calc(
            Invoice_Item.price, Invoice_Item.count)).join(Invoice_Item, Invoice.id == Invoice_Item.invoiceId).all()
        for join in calc_joins:
            print(join)
        print("--------同上 外部キー指定があるのでキーの条件指定をはずしてみる -----------------")
        calc_joins = db.session.query(Invoice.id, Invoice.title, my_calc(
            Invoice_Item.price, Invoice_Item.count)).join(Invoice_Item).all()
        for join in calc_joins:
            print(join)
        print("--------JOIN 日付 に計算値をJOIN -----------------")
        day_calc_joins = db.session.query(Invoice.applyDate, my_calc(
            Invoice_Item.price, Invoice_Item.count)).join(Invoice_Item).all()
        for join in day_calc_joins:
            print(join)
        print("--------JOIN 日付(年月) に計算値をJOIN -----------------")
        ym_calc_joins = db.session.query(func.strftime("%Y-%m", Invoice.applyDate), my_calc(
            Invoice_Item.price, Invoice_Item.count)).join(Invoice_Item).all()
        for join in ym_calc_joins:
            print(join)
        print("--------JOIN 日付(年月) に計算値をJOINして、日付（年月）でgroupby,及び 合計の計算 -----------------")
        ym_calc_joins_grp = db.session.query(func.strftime("%Y-%m", Invoice.applyDate), \
                            func.sum(my_calc(Invoice_Item.price, Invoice_Item.count)))\
                            .join(Invoice_Item)\
                            .group_by(func.strftime("%Y-%m", Invoice.applyDate)).all()
        for join in ym_calc_joins_grp:
            print(join)


if __name__ == '__main__':
    unittest.main()
