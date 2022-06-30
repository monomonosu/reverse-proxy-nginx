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

    def test_get_invoice_byId(self):
        print('---Invoice一件読み込み---')
        invoice = Invoice.query.filter(Invoice.id == 1).first()
        self.assertTrue(invoice)
        self.assertEqual(invoice.title, '○○株式会社への請求書')

        print('---Invoice一件読み込み失敗---')
        invoices = Invoice.query.filter(Invoice.id == 9999).all()
        self.assertFalse(invoices)
        self.assertEqual(len(invoices), 0)

    def test_update_invoice(self):
        print('---Invoice一件更新---')
        invoice = Invoice.query.filter(Invoice.id == 2).first()
        invoice.title = '××株式会社への請求書'
        db.session.commit()
        invoice = Invoice.query.filter(Invoice.id == 2).first()
        self.assertEqual(invoice.title, "××株式会社への請求書")

    def test_create_invoice(self):
        print('---Invoice新規作成---')
        invoices = [
            Invoice(customerId=1, customerName='○○建設', applyNumber=1000004, applyDate=datetime.now(), deadLine=datetime.now(),
                    title='○○建設への請求書', memo='これは請求書のメモです', remarks='これは請求書の備考です', isTaxExp=True, isDelete=False),
            Invoice(customerId=1, customerName='○○商店', applyNumber=1000005, applyDate=datetime.now(), deadLine=datetime.now(),
                    title='○○商店への請求書', memo='これは請求書のメモです', remarks='これは請求書の備考です', isTaxExp=True, isDelete=False),
        ]
        db.session.add_all(invoices)
        db.session.commit()
        self.assertGreaterEqual(len(Invoice.query.all()), 2)

    def test_delete_invoice(self):
        print('---Invoice一件削除---')
        invoice = Invoice(customerId=1, customerName='テスト会社', applyNumber=1000006, applyDate=datetime.now(), deadLine=datetime.now(),
                          title='デリートテスト会社への請求書', memo='これは請求書のメモです', remarks='これは請求書の備考です', isTaxExp=True, isDelete=False)
        db.session.add(invoice)
        db.session.commit()
        newId = invoice.id
        invoice = Invoice.query.filter(Invoice.id == newId).delete()
        db.session.commit()

        invoice = Invoice.query.filter(Invoice.id == newId).all()
        self.assertEqual(len(invoice), 0)


if __name__ == '__main__':
    unittest.main()
