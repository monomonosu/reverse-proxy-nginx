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

    def test_get_histories(self):
        print('---History全件読み込み---')
        histories = History.query.all()
        historyCount = len(histories)
        self.assertTrue(historyCount)

    def test_get_histories_dict(self):
        print('---History全件読み込み→Dict---')
        histories = History.query.all()
        sch = HistorySchema(many=True).dump(histories)
        self.assertEqual(sch[0]['userName'], 'tanaka_taro')

    def test_get_history_byId(self):
        print('---History一件読み込み---')
        history = History.query.filter(History.id == 1).first()
        self.assertTrue(history)
        self.assertEqual(history.userName, 'tanaka_taro')

        print('---History一件読み込み失敗---')
        histories = History.query.filter(History.id == 9999).all()
        self.assertFalse(histories)
        self.assertEqual(len(histories), 0)

    def test_update_history(self):
        print('---History一件更新---')
        history = History.query.filter(History.id == 2).first()
        history.userName = 'hogehoge'
        db.session.commit()
        history = History.query.filter(History.id == 2).first()
        self.assertEqual(history.userName, "hogehoge")

    def test_create_history(self):
        print('---History新規作成---')
        histories = [
            History(userName='kojima_siro', modelName='Customer',
                    modelId=1, action='GET',),
            History(userName='yamada_goro',
                    modelName='Item', modelId=2, action='POST',),
        ]
        db.session.add_all(histories)
        db.session.commit()
        self.assertGreaterEqual(len(History.query.all()), 2)

    def test_delete_history(self):
        print('---History一件削除---')
        history = History(userName='hogehoge',
                          modelName='Invoice', modelId=3, action='DELETE',)
        db.session.add(history)
        db.session.commit()
        newId = history.id
        history = History.query.filter(History.id == newId).delete()
        db.session.commit()

        history = History.query.filter(History.id == newId).all()
        self.assertEqual(len(history), 0)


if __name__ == '__main__':
    unittest.main()
