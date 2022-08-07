import unittest
from src.core.casino import player, admin


#TODO: Fix search functions so they return False when no result is found

class adminTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.gid = 0
        self.gameDiff = 1
        self.player = player()
        self.admin = admin()
        self.admin.createAdmin("testAdmin", "test", "test", "test")
        self.player.createPlayer("test", "test", "test", "test", 100)

    #test login with incorrect credentials
    def testFalseLogin(self):
        self.assertFalse(self.admin.checkAdmin("testFail", 'pword'),
                         "Expected error while login")

    #test login with correct UID & password
    def testLogin(self):
        self.assertTrue(self.admin.checkAdmin("testAdmin", 'test'), 
                        "Expected successful login")

    def testGetAdmins(self):
        out = self.admin.getAdmins()
        self.assertIsNotNone(out) #check to make sure none is not returned, if so an error occured

    def testUpdateInfo(self):
        out = self.admin.updateAdminInfo("test", '', "newName")
        self.assertTrue(out)

    def testAddGame(self):
        self.gid = self.admin.addGame("slots", "test", 100, 400)
        self.assertIsNotNone(self.gid) #check to make sure none is not returned, if so an error occured

    def testGetGameHistory(self):
        out = self.admin.getGameHistory()
        self.assertIsNotNone(out) #check to make sure none is not returned, if so an error occured

    def testGetGameByName(self):
        out = self.admin.getGameByName("slots")
        self.assertIsNotNone(out) #check to make sure none is not returned, if so an error occured

    def testGetGameByPlayer(self):
        out = self.admin.getGameByPlayer("test")
        self.assertIsNotNone(out) #check to make sure none is not returned, if so an error occured

    def testCheckBalance(self):
        out = self.admin.checkPlayerBalance("test")
        self.assertIsNotNone(out) #check to make sure none is not returned, if so an error occured

    def testCheckIfEnough(self):
        out = self.admin.checkIfEnough("test", 1000)
        self.assertFalse(out) #check to make sure none is not returned, if so an error occured

    def testGenerateGraphData(self):
        out = self.admin.generateGraphData()
        self.assertIsNotNone(out) #check to make sure none is not returned, if so an error occured

    def testSearchForGame(self):
        out = self.admin.searchForGame("gameType","slots")
        self.assertIsNotNone(out) #check to make sure none is not returned, if so an error occured

    def testSearchForAdmin(self):
        out = self.admin.searchForAdmin("userID","testAdmin")
        self.assertIsNotNone(out) #check to make sure none is not returned, if so an error occured

    def testSearchForPlayer(self):
        out = self.admin.searchForPlayer("userID","test")
        self.assertIsNotNone(out) #check to make sure none is not returned, if so an error occured

    def testGetGameDifficulty(self):
        self.gameDiff = self.admin.getGameDifficulty("slots")
        self.assertIsNotNone(self.gameDiff) #check to make sure none is not returned, if so an error occured

    def testSetGameDifficulty(self):
        out = self.admin.setGameDifficulty("slots", self.gameDiff)
        self.assertIsNotNone(out) #check to make sure none is not returned, if so an error occured

    def testCheckCasinoWinnings(self):
        out = self.admin.checkCasinoWinnings()
        self.assertIsNotNone(out) #check to make sure none is not returned, if so an error occured

    def testCheckGamwWinnings(self):
        out = self.admin.checkGameWinnings("slots")
        self.assertIsNotNone(out) #check to make sure none is not returned, if so an error occured

    @classmethod
    def tearDownClass(self):
        self.player.removePlayer("testAdmin")
        self.player.removePlayer("test")

class userTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.player = player()
        self.admin = admin()
        self.player.createPlayer("test", "test", "test", "test", 100)

    #test login with incorrect credentials
    def testFalseLogin(self):
        self.assertFalse(self.player.checkLogin("testFail", 'pword'),
                         "Expected error while login")

    #test login with correct UID & password
    def testLogin(self):
        self.assertTrue(self.player.checkLogin("test", 'test'), 
                        "Expected successful login")

    def testBalance(self):
        win = self.player.getWinnings("test")
        self.assertEqual(win, 100)

    def testUpdateInfo(self):
        out = self.player.updateInfo("test", '', "newName")
        self.assertTrue(out)

    def testGetNameFromUID(self):
        out = self.player.getNameFromUID("test")
        self.assertEquals(out, "test test")
    
    def testGetPlayers(self):
        out = self.player.getPlayers()
        self.assertIsNotNone(out) #check to make sure none is not returned, if so an error occured
    @classmethod
    def tearDownClass(self):
        self.player.removePlayer("test")

if __name__ == '__main__':
    unittest.main()
    