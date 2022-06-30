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

    def test_get_memos(self):
        print('---Memo全件読み込み---')
        memos = Memo.query.all()
        memoCount = len(memos)
        self.assertTrue(memoCount)

    def test_get_memos_dict(self):
        print('---Memo全件読込→Dict---')
        memos = Memo.query.all()
        sch = MemoSchema(many=True).dump(memos)
        self.assertEqual(sch[0]['title'], 'メモのタイトル１')

    def test_get_memo_byId(self):
        print('---Memo一件読み込み---')
        memo = Memo.query.filter(Memo.id == 1).first()
        self.assertTrue(memo)
        self.assertEqual(memo.title, 'メモのタイトル１')

        print('---Memo一件読み込み失敗---')
        memos = Memo.query.filter(Memo.id == 9999).all()
        self.assertFalse(memos)
        self.assertEqual(len(memos), 0)

    def test_update_memo(self):
        print('---Memo一件更新---')
        memo = Memo.query.filter(Memo.id == 2).first()
        memo.title = 'メモのタイトル変更'
        db.session.commit()
        memo = Memo.query.filter(Memo.id == 2).first()
        self.assertEqual(memo.title, "メモのタイトル変更")

    def test_create_memo(self):
        print('---Memo新規作成---')
        memos = [
            Memo(title='メモのタイトル４', content='メモの内容４'),
            Memo(title='メモのタイトル５', content='メモの内容５'),
        ]
        db.session.add_all(memos)
        db.session.commit()
        self.assertGreaterEqual(len(Memo.query.all()), 2)

    def test_delete_memo(self):
        print('---Memo一件削除---')
        memo = Memo(title='メモのタイトル６', content='メモの内容６')
        db.session.add(memo)
        db.session.commit()
        newId = memo.id
        memo = Memo.query.filter(Memo.id == newId).delete()
        db.session.commit()

        memo = Memo.query.filter(Memo.id == newId).all()
        self.assertEqual(len(memo), 0)


if __name__ == '__main__':
    unittest.main()
