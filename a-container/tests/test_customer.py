from logging import captureWarnings
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

    def test_get_costomers(self):
        print('---Customer全件読み込み---')
        customers = Customer.query.all()
        c_count = len(customers)
        self.assertTrue(c_count)
        # Invoice_Itemまで全件取得
        print('Customer→Invoice_Item全件取得')
        invoiceItemCount = 0
        quotationItemCount = 0
        for customer in customers:
            for invoice in customer.invoices:
                for invoiceItem in invoice.invoice_items:
                    invoiceItemCount += 1
        self.assertGreaterEqual(invoiceItemCount, 1)
        print('Customer→Quotation_Item全件取得')
        for customer in customers:
            for quotation in customer.quotations:
                for quotationItem in quotation.quotation_items:
                    quotationItemCount += 1
        self.assertGreaterEqual(quotationItemCount, 1)

    def test_get_customers_dict(self):
        print('---Customer全件読み込み→Dict---')
        customers = Customer.query.all()
        sch = CustomerSchema(many=True).dump(customers)
        self.assertEqual(sch[0]['customerName'], '○○株式会社')

    def test_get_customer_byId(self):
        print('---Customer一件読み込み---')
        customer = Customer.query.filter(Customer.id == 1).first()
        self.assertTrue(customer)
        self.assertEqual(customer.customerName, '○○株式会社')

        print('---Customer一件読み込み失敗---')
        customers = Customer.query.filter(Customer.id == 9999).all()
        self.assertFalse(customers)
        self.assertEqual(len(customers), 0)

    def test_update_customer(self):
        print('---Customer一件更新---')
        customer = Customer.query.filter(Customer.id == 2).first()
        customer.customerName = 'テスト株式会社'
        db.session.commit()
        customer = Customer.query.filter(Customer.id == 2).first()
        self.assertEqual(customer.customerName, "テスト株式会社")

    def test_create_customer(self):
        print('---Customer新規作成---')
        customers = [
            Customer(customerName='テストクリエイト株式会社', honorificTitle='御中', postNumber='000-0000', address='鹿沼市板荷000', telNumber='000-0000-0000',
                     faxNumber='000-0000-0000', url='example.com', email='example@co.jp', manager='田中太郎', representative='田中代表', memo='これは○○株式会社のメモです'),
            Customer(customerName='テストクリエイト株式会社2', honorificTitle='御中', postNumber='000-0000', address='鹿沼市板荷000', telNumber='000-0000-0000',
                     faxNumber='000-0000-0000', url='example.com', email='example@co.jp', manager='田中太郎', representative='田中代表', memo='これは○○株式会社のメモです'),
        ]
        db.session.add_all(customers)
        db.session.commit()
        self.assertGreaterEqual(len(Customer.query.all()), 2)

    def test_delete_customer(self):
        print('---Customer一件削除---')
        customer = Customer(customerName='デリートテスト会社', honorificTitle='御中', postNumber='000-0000', address='鹿沼市板荷000', telNumber='000-0000-0000',
                            faxNumber='000-0000-0000', url='example.com', email='example@co.jp', manager='田中太郎', representative='田中代表', memo='これは○○株式会社のメモです')
        db.session.add(customer)
        db.session.commit()
        newId = customer.id
        customer = Customer.query.filter(Customer.id == newId).delete()
        db.session.commit()

        customer = Customer.query.filter(Customer.id == newId).all()
        self.assertEqual(len(customer), 0)


if __name__ == '__main__':
    unittest.main()
