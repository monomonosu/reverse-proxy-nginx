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

    def test_get_users(self):
        print('---User全件読み込み---')
        users = User.query.all()
        userCount = len(users)
        self.assertTrue(userCount)

    def test_get_users_dict(self):
        print('---User全件読み込み→Dict---')
        users = User.query.all()
        sch = UserSchema(many=True).dump(users)
        self.assertEqual(sch[0]['name'], 'tanaka_taro')

    def test_get_user_byId(self):
        print('---User一件読み込み---')
        user = User.query.filter(User.id == 1).first()
        self.assertTrue(user)
        self.assertEqual(user.name, 'tanaka_taro')

        print('---User一件読み込み失敗---')
        users = User.query.filter(User.id == 9999).all()
        self.assertFalse(users)
        self.assertEqual(len(users), 0)

    def test_update_user(self):
        print('---User一件更新---')
        user = User.query.filter(User.id == 2).first()
        user.name = 'hogehoge'
        db.session.commit()
        user = User.query.filter(User.id == 2).first()
        self.assertEqual(user.name, "hogehoge")

    def test_create_user(self):
        print('---User新規作成---')
        users = [
            User(name='kojima_siro', password='password',
                 group='operator', role='admin'),
            User(name='yamada_goro', password='password',
                 group='guest', role='admin'),
        ]
        db.session.add_all(users)
        db.session.commit()
        self.assertGreaterEqual(len(User.query.all()), 2)

    def test_delete_user(self):
        print('---User一件削除---')
        user = User(name='hogehoge', password='password',
                    group='guest', role='admin')
        db.session.add(user)
        db.session.commit()
        newId = user.id
        user = User.query.filter(User.id == newId).delete()
        db.session.commit()

        user = User.query.filter(User.id == newId).all()
        self.assertEqual(len(user), 0)


if __name__ == '__main__':
    unittest.main()
