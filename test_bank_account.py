import unittest
from bank_account import BankAccount

class TestBankAccount(unittest.TestCase):

    # vor jedem test ein neues konto anlegen
    def setUp(self):
        self.konto = BankAccount("Fritz", 100.0)

    def test_startguthaben(self):
        self.assertEqual(self.konto.get_balance(), 100.0)

    def test_negatives_startguthaben(self):
        # darf nicht gehen
        with self.assertRaises(ValueError):
            BankAccount("Fritz", -50)

    def test_deposit(self):
        self.konto.deposit(50)
        self.assertEqual(self.konto.get_balance(), 150.0)

    def test_deposit_negativ(self):
        with self.assertRaises(ValueError):
            self.konto.deposit(-10)

    def test_deposit_null(self):
        # 0 einzahlen darf auch nicht gehen
        with self.assertRaises(ValueError):
            self.konto.deposit(0)

    def test_withdraw(self):
        self.konto.withdraw(30)
        self.assertEqual(self.konto.get_balance(), 70.0)

    def test_withdraw_zu_viel(self):
        # mehr abheben als am konto ist
        with self.assertRaises(ValueError):
            self.konto.withdraw(500)

    def test_withdraw_negativ(self):
        with self.assertRaises(ValueError):
            self.konto.withdraw(-20)

    def test_transaktionen(self):
        self.konto.deposit(50)
        self.konto.withdraw(20)
        verlauf = self.konto.get_transaction_history()
        self.assertEqual(len(verlauf), 2)
        self.assertEqual(verlauf[0], "Einzahlung: +50.00 EUR")
        self.assertEqual(verlauf[1], "Abhebung: -20.00 EUR")

    def test_transaktionen_leer(self):
        # am anfang keine transaktionen
        self.assertEqual(self.konto.get_transaction_history(), [])


if __name__ == '__main__':
    unittest.main()
