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

    def test_get_makers(self):
        print('---Maker全件読み込み---')
        makers = Maker.query.all()
        makerCount = len(makers)
        self.assertTrue(makerCount)

    def test_get_makers_dict(self):
        print('---Maker全件読込→Dict---')
        makers = Maker.query.all()
        sch = MakerSchema(many=True).dump(makers)
        self.assertEqual(sch[0]['makerName'], 'apple青果店')

    def test_get_maker_byId(self):
        print('---Maker一件読み込み---')
        maker = Maker.query.filter(Maker.id == 1).first()
        self.assertTrue(maker)
        self.assertEqual(maker.makerName, 'apple青果店')

        print('---Maker一件読み込み失敗---')
        makers = Maker.query.filter(Maker.id == 9999).all()
        self.assertFalse(makers)
        self.assertEqual(len(makers), 0)

    def test_update_maker(self):
        print('---Maker一件更新---')
        maker = Maker.query.filter(Maker.id == 2).first()
        maker.makerName = 'メーカー変更'
        db.session.commit()
        maker = Maker.query.filter(Maker.id == 2).first()
        self.assertEqual(maker.makerName, "メーカー変更")

    def test_create_maker(self):
        print('---Maker新規作成---')
        makers = [
            Maker(makerName='ダイハツ'),
            Maker(makerName='スズキ'),
        ]
        db.session.add_all(makers)
        db.session.commit()
        self.assertGreaterEqual(len(Maker.query.all()), 2)

    def test_delete_maker(self):
        print('---Maker一件削除---')
        maker = Maker(makerName='ホンダ')
        db.session.add(maker)
        db.session.commit()
        newId = maker.id
        maker = Maker.query.filter(Maker.id == newId).delete()
        db.session.commit()

        maker = Maker.query.filter(Maker.id == newId).all()
        self.assertEqual(len(maker), 0)


if __name__ == '__main__':
    unittest.main()
