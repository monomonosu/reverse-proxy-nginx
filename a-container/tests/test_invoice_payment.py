import unittest
import sys,os
from datetime import date

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

    def test_get_invoice_payments(self):
        print('---Invoice_Payment全件読み込み---')
        invoicePayments = Invoice_Payment.query.all()
        invoicePaymentCount = len(invoicePayments)
        self.assertTrue(invoicePaymentCount)
        print('---Invoice_Payment→Customer全件取得---')
        customerCount = 0
        for invoicePayment in invoicePayments:
            if invoicePayment.invoice.customer is not None:
                customerCount += 1
        self.assertGreaterEqual(customerCount, 1)

    def test_get_invoice_payment_byId(self):
        print('---Invoice_Payment全件取得→Dict---')
        invoicePayments = Invoice_Payment.query.all()
        sch = Invoice_PaymentSchema(many=True).dump(invoicePayments)
        self.assertEqual(sch[0]['paymentAmount'], 100)

    def test_get_invoice_payment_byId(self):
        print('---Invoice_Payment一件読み込み---')
        invoicePayment = Invoice_Payment.query.filter(
            Invoice_Payment.id == 1).first()
        self.assertTrue(invoicePayment)
        self.assertEqual(invoicePayment.paymentAmount, 100)

        print('---Invoice_Payment一件読み込み失敗---')
        invoicePayments = Invoice_Payment.query.filter(
            Invoice_Payment.id == 9999).all()
        self.assertFalse(invoicePayments)
        self.assertEqual(len(invoicePayments), 0)

    def test_update_invoice_payment(self):
        print('---Invoice_Payment一件更新---')
        invoicePayment = Invoice_Payment.query.filter(
            Invoice_Payment.id == 2).first()
        invoicePayment.paymentAmount = 200
        db.session.commit()
        invoicePayment = Invoice_Payment.query.filter(
            Invoice_Payment.id == 2).first()
        self.assertEqual(invoicePayment.paymentAmount, 200)

    def test_create_invoice_payment(self):
        print('---Invoice_Payment新規作成---')
        invoicePayments = [
            Invoice_Payment(invoiceId=3, paymentDate=date(2022, 1, 1),
                            paymentMethod='現金', paymentAmount=1200,  remarks="備考６"),
            Invoice_Payment(invoiceId=1, paymentDate=date(2022, 1, 1),
                            paymentMethod='クレジット', paymentAmount=1000, remarks="備考７"),
        ]
        db.session.add_all(invoicePayments)
        db.session.commit()
        self.assertGreaterEqual(len(Invoice_Payment.query.all()), 2)

    def test_delete_invoice_payment(self):
        print('---Invoice_Payment一件削除---')
        invoicePayment = Invoice_Payment(
            invoiceId=2, paymentDate=date(2022, 1, 1),
            paymentMethod='現金', paymentAmount=300, remarks="削除備考")
        db.session.add(invoicePayment)
        db.session.commit()
        newId = invoicePayment.id
        invoicePayment = Invoice_Payment.query.filter(
            Invoice_Payment.id == newId).delete()
        db.session.commit()

        invoicePayment = Invoice_Payment.query.filter(
            Invoice_Payment.id == newId).all()
        self.assertEqual(len(invoicePayment), 0)


if __name__ == '__main__':
    unittest.main()
