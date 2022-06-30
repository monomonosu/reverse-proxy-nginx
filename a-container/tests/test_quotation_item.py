import unittest
import sys,os

sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))
from app import db, app
from models import *
import unittest
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

    def test_get_quotation_items(self):
        print('---Quotation_Item全件読み込み---')
        quotationItems = Quotation_Item.query.all()
        quotationItemCount = len(quotationItems)
        self.assertTrue(quotationItemCount)
        print('---Quotation_Item→Customer全件取得---')
        customerCount = 0
        for quotationItem in quotationItems:
            if quotationItem.quotation.customer is not None:
                customerCount += 1
        self.assertGreaterEqual(customerCount, 1)

    def test_get_quotation_item_byId(self):
        print('---Quotation_Item全件取得→Dict---')
        quotationItems = Quotation_Item.query.all()
        sch = Quotation_ItemSchema(many=True).dump(quotationItems)
        self.assertEqual(sch[0]['price'], 100)

    def test_get_quotation_item_byId(self):
        print('---Quotation_Item一件読み込み---')
        quotationItem = Quotation_Item.query.filter(
            Quotation_Item.id == 1).first()
        self.assertTrue(quotationItem)
        self.assertEqual(quotationItem.count, 5)

        print('---Quotation_Item一件読み込み失敗---')
        quotationItems = Quotation_Item.query.filter(
            Quotation_Item.id == 9999).all()
        self.assertFalse(quotationItems)
        self.assertEqual(len(quotationItems), 0)

    def test_update_quotation_item(self):
        print('---Quotation_Item一件更新---')
        quotationItem = Quotation_Item.query.filter(
            Quotation_Item.id == 2).first()
        quotationItem.count = 20
        db.session.commit()
        quotationItem = Quotation_Item.query.filter(
            Quotation_Item.id == 2).first()
        self.assertEqual(quotationItem.count, 20)

    def test_create_quotation_item(self):
        print('---Quotation_Item新規作成---')
        quotationItems = [
            Quotation_Item(quotationId=3, itemId=2, itemName='鉛筆',
                           price=100, cost=20, count=20, unit='本'),
            Quotation_Item(quotationId=3, itemId=3, itemName='ラジオ',
                           price=200, cost=100, count=10, unit='台'),
        ]
        db.session.add_all(quotationItems)
        db.session.commit()
        self.assertGreaterEqual(len(Quotation_Item.query.all()), 2)

    def test_delete_quotation_item(self):
        print('---Quotation_Item一件削除---')
        quotationItem = Quotation_Item(
            quotationId=1, itemId=1, itemName='りんご', price=999, cost=100, count=10, unit='個')
        db.session.add(quotationItem)
        db.session.commit()
        newId = quotationItem.id
        quotationItem = Quotation_Item.query.filter(
            Quotation_Item.id == newId).delete()
        db.session.commit()

        quotationItem = Quotation_Item.query.filter(
            Quotation_Item.id == newId).all()
        self.assertEqual(len(quotationItem), 0)


if __name__ == '__main__':
    unittest.main()
