import unittest
from src.core.casino import player, admin

class backendTest(unittest.TestCase):
    def setUp(self):
        self.player = player()
        self.admin = admin()
        self.admin.createPlayer("test", "test", "test", "test")

    def test_balanceAccount(self):
        self.admin.addWinnings("test", 100)
        win = self.player.getWinnings("test")
        self.assertEqual(win, 100)

    def test_checkLogin(self):
        ad = self.admin.checkAdmin("test", "test")
        pl = self.player.checkLogin("test", "test")

        self.assertTrue(pl)
        self.assertFalse(ad)

    def tearDown(self):
        self.admin.removePlayer("test")
if __name__ == '__main__':
    unittest.main()