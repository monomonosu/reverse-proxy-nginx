import unittest
import sys,os

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

    def test_get_invoice_items(self):
        print('---Invoice_Item全件読み込み---')
        invoiceItems = Invoice_Item.query.all()
        invoiceItemCount = len(invoiceItems)
        self.assertTrue(invoiceItemCount)
        print('---Invoice_Item→Customer全件取得---')
        customerCount = 0
        for invoiceItem in invoiceItems:
            if invoiceItem.invoice.customer is not None:
                customerCount += 1
        self.assertGreaterEqual(customerCount, 1)

    def test_get_invoice_items_dict(self):
        print('---InvoiceItem全件取得→Dict---')
        invoiceItems = Invoice_Item.query.all()
        sch = Invoice_ItemSchema(many=True).dump(invoiceItems)
        self.assertEqual(sch[0]['price'], 100)

    def test_get_invoice_item_byId(self):
        print('---Invoice_Item一件読み込み---')
        invoiceItem = Invoice_Item.query.filter(Invoice_Item.id == 1).first()
        self.assertTrue(invoiceItem)
        self.assertEqual(invoiceItem.count, 5)

        print('---Invoice_Item一件読み込み失敗---')
        invoiceItems = Invoice_Item.query.filter(Invoice_Item.id == 9999).all()
        self.assertFalse(invoiceItems)
        self.assertEqual(len(invoiceItems), 0)

    def test_update_invoice_item(self):
        print('---Invoice_Item一件更新---')
        invoiceItem = Invoice_Item.query.filter(Invoice_Item.id == 2).first()
        invoiceItem.count = 20
        db.session.commit()
        invoiceItem = Invoice_Item.query.filter(Invoice_Item.id == 2).first()
        self.assertEqual(invoiceItem.count, 20)

    def test_create_invoice_item(self):
        print('---Invoice_Item新規作成---')
        invoiceItems = [
            Invoice_Item(invoiceId=3, itemId=2, itemName='鉛筆',
                         price=100, cost=20, count=20, unit='本'),
            Invoice_Item(invoiceId=3, itemId=3, itemName='ラジオ',
                         price=200, cost=100, count=10, unit='台'),
        ]
        db.session.add_all(invoiceItems)
        db.session.commit()
        self.assertGreaterEqual(len(Invoice_Item.query.all()), 2)

    def test_delete_invoice_item(self):
        print('---Invoice_Item一件削除---')
        invoiceItem = Invoice_Item(
            invoiceId=1, itemId=1, itemName='りんご', price=999, cost=100, count=10, unit='個')
        db.session.add(invoiceItem)
        db.session.commit()
        newId = invoiceItem.id
        invoiceItem = Invoice_Item.query.filter(
            Invoice_Item.id == newId).delete()
        db.session.commit()

        invoiceItem = Invoice_Item.query.filter(Invoice_Item.id == newId).all()
        self.assertEqual(len(invoiceItem), 0)


if __name__ == '__main__':
    unittest.main()
