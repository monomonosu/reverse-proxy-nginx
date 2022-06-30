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

    def test_get_items(self):
        print('---Item全件読み込み---')
        items = Item.query.all()
        itemCount = len(items)
        self.assertTrue(itemCount)

    def test_get_items_dict(self):
        print('---Item全件読込→Dict---')
        items = Item.query.all()
        sch = ItemSchema(many=True).dump(items)
        self.assertEqual(sch[0]['itemName'], 'りんご')

    def test_get_item_byId(self):
        print('---Item一件読み込み---')
        item = Item.query.filter(Item.id == 1).first()
        self.assertTrue(item)
        self.assertEqual(item.itemName, 'りんご')

        print('---Item一件読み込み失敗---')
        items = Item.query.filter(Item.id == 9999).all()
        self.assertFalse(items)
        self.assertEqual(len(items), 0)

    def test_update_item(self):
        print('---Item一件更新---')
        item = Item.query.filter(Item.id == 2).first()
        item.itemName = 'ボールペン'
        db.session.commit()
        item = Item.query.filter(Item.id == 2).first()
        self.assertEqual(item.itemName, "ボールペン")

    def test_create_item(self):
        print('---Item新規作成---')
        items = [
            Item(itemName='みかん', unit='個', basePrice=50,
                 cost=20, memo='これはみかんのメモです'),
            Item(itemName='ボールペン', unit='本', basePrice=100,
                 cost=10, memo='これはボールペンのメモです'),
        ]
        db.session.add_all(items)
        db.session.commit()
        self.assertGreaterEqual(len(Item.query.all()), 2)

    def test_delete_item(self):
        print('---Item一件削除---')
        item = Item(itemName='ボール', unit='個', basePrice=50,
                    cost=20, memo='これはボールのメモです')
        db.session.add(item)
        db.session.commit()
        newId = item.id
        item = Item.query.filter(Item.id == newId).delete()
        db.session.commit()

        item = Item.query.filter(Item.id == newId).all()
        self.assertEqual(len(item), 0)


if __name__ == '__main__':
    unittest.main()
