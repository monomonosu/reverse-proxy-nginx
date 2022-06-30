from datetime import datetime
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

    def test_get_quotations(self):
        print('---Quotation全件読み込み---')
        quotations = Quotation.query.all()
        quotationCount = len(quotations)
        self.assertTrue(quotationCount)

        # Customerまで全件取得
        print('Quotation→Customer全件取得')
        customerCount = 0
        for quotation in quotations:
            if(quotation.customer is not None):
                customerCount += 1
        self.assertGreaterEqual(customerCount, 1)

        # Quotation_Itemまで取得
        print('Quotation→Quotation_Item全件取得')
        quotationItemCount = 0
        for quotation in quotations:
            for quotationItem in quotation.quotation_items:
                quotationItemCount += 1
        self.assertGreaterEqual(quotationItemCount, 1)

    def test_get_quotations_dict(self):
        print('---Quotation全件読込→Dict---')
        quotations = Quotation.query.all()
        sch = QuotationSchema(many=True).dump(quotations)
        self.assertEqual(sch[0]['title'], '○○株式会社への見積書')

    def test_get_quotation_byId(self):
        print('---Quotation一件読み込み---')
        quotation = Quotation.query.filter(Quotation.id == 1).first()
        self.assertTrue(quotation)
        self.assertEqual(quotation.title, '○○株式会社への見積書')

        print('---Quotation一件読み込み失敗---')
        quotations = Quotation.query.filter(Quotation.id == 9999).all()
        self.assertFalse(quotations)
        self.assertEqual(len(quotations), 0)

    def test_update_quotation(self):
        print('---Quotation一件更新---')
        quotation = Quotation.query.filter(Quotation.id == 2).first()
        quotation.title = '××株式会社への見積書'
        db.session.commit()
        quotation = Quotation.query.filter(Quotation.id == 2).first()
        self.assertEqual(quotation.title, "××株式会社への見積書")

    def test_create_quotation(self):
        print('---Quotation新規作成---')
        quotations = [
            Quotation(customerId=1, customerName='○○建設', applyNumber=1000004, applyDate=datetime.now(), expiry=datetime.now(),
                      title='○○建設への見積書', memo='これは見積書のメモです', remarks='これは見積書の備考です', isTaxExp=True, isDelete=False),
            Quotation(customerId=1, customerName='○○商店', applyNumber=1000005, applyDate=datetime.now(), expiry=datetime.now(),
                      title='○○商店への見積書', memo='これは見積書のメモです', remarks='これは見積書の備考です', isTaxExp=True, isDelete=False),
        ]
        db.session.add_all(quotations)
        db.session.commit()
        self.assertGreaterEqual(len(Quotation.query.all()), 2)

    def test_delete_quotation(self):
        print('---Quotation一件削除---')
        quotation = Quotation(customerId=1, customerName='テスト会社', applyNumber=1000006, applyDate=datetime.now(), expiry=datetime.now(),
                              title='○○株式会社への見積書', memo='これは見積書のメモです', remarks='これは見積書の備考です', isTaxExp=True, isDelete=False)
        db.session.add(quotation)
        db.session.commit()
        newId = quotation.id
        quotation = Quotation.query.filter(Quotation.id == newId).delete()
        db.session.commit()

        quotation = Quotation.query.filter(Quotation.id == newId).all()
        self.assertEqual(len(quotation), 0)


if __name__ == '__main__':
    unittest.main()
