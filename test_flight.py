import unittest
from unittest.mock import Mock
from flight import Flight, BookingSystem

class TestFlight(unittest.TestCase):

    def setUp(self):
        self.flug = Flight("OS101", 3)

    def test_sitzplaetze_am_anfang(self):
        self.assertEqual(self.flug.get_available_seats(), 3)

    def test_book_seat(self):
        sitz = self.flug.book_seat("Fritz")
        self.assertEqual(sitz, 1)
        self.assertEqual(self.flug.get_available_seats(), 2)

    def test_sitznummern_aufsteigend(self):
        self.assertEqual(self.flug.book_seat("A"), 1)
        self.assertEqual(self.flug.book_seat("B"), 2)
        self.assertEqual(self.flug.book_seat("C"), 3)

    def test_flug_voll(self):
        self.flug.book_seat("A")
        self.flug.book_seat("B")
        self.flug.book_seat("C")
        # jetzt ist kein platz mehr
        with self.assertRaises(ValueError):
            self.flug.book_seat("D")


class TestBookingSystem(unittest.TestCase):

    def setUp(self):
        # payment gateway wird gemockt damit nicht zufaellig true/false kommt
        self.gateway = Mock()
        self.system = BookingSystem(self.gateway)
        self.flug = Flight("OS101", 2)
        self.system.add_flight(self.flug)

    def test_buchung_erfolgreich(self):
        self.gateway.process_payment.return_value = True
        sitz = self.system.book_ticket("OS101", "Fritz", "4111222233334444", 200)
        self.assertEqual(sitz, 1)
        self.assertEqual(len(self.system.transactions), 1)

    def test_zahlung_fehlgeschlagen(self):
        self.gateway.process_payment.return_value = False
        with self.assertRaises(ValueError):
            self.system.book_ticket("OS101", "Fritz", "4111222233334444", 200)
        # sitz darf nicht gebucht worden sein
        self.assertEqual(self.flug.get_available_seats(), 2)

    def test_flug_nicht_gefunden(self):
        self.gateway.process_payment.return_value = True
        with self.assertRaises(ValueError):
            self.system.book_ticket("LH999", "Fritz", "4111222233334444", 200)

    def test_gateway_wird_richtig_aufgerufen(self):
        self.gateway.process_payment.return_value = True
        self.system.book_ticket("OS101", "Fritz", "4111222233334444", 200)
        # pruefen ob der mock mit den richtigen werten aufgerufen wurde
        self.gateway.process_payment.assert_called_once_with(200, "4111222233334444")

    def test_ungueltige_karte(self):
        # der mock wirft die exception wie die echte klasse
        self.gateway.process_payment.side_effect = ValueError("Ungueltige Kreditkarte")
        with self.assertRaises(ValueError):
            self.system.book_ticket("OS101", "Fritz", "5111222233334444", 200)


if __name__ == '__main__':
    unittest.main()
