import unittest

from mock import Mock

from ticketing_machine import TicketingMachine


class TestTicketingMachine(unittest.TestCase):

    def _create_mock_card_writer(self):
        card_writer = Mock()

        class MockTicket(object):
            def __init__(self, printed_time):
                self.printed_time = printed_time

        def track_last_card(current_time):
            ticket = MockTicket(current_time)
            card_writer.last_printed_card = ticket
            return ticket

        def get_last_ticket():
            return card_writer.last_printed_card

        card_writer.create_new_card.side_effect = track_last_card
        card_writer.get_last_printed_ticket = get_last_ticket
        return card_writer

    def _create_mock_payment_calc(self):
        payment_calculator = Mock()
        payment_calculator.calculate_payment.return_value = 0
        return payment_calculator

    def _create_default_ticketing_machine(self):
        self.card_writer = self._create_mock_card_writer()
        self.card_reader = Mock()
        self.output = Mock()
        self.time_provider = Mock()
        self.payment_calculator = self._create_mock_payment_calc()
        return TicketingMachine(card_writer=self.card_writer, card_reader=self.card_reader,
                                output=self.output, time_provider=self.time_provider,
                                payment_calculator=self.payment_calculator)

    def test_get_new_card(self):
        machine = self._create_default_ticketing_machine()
        machine.get_new_ticket()
        self.card_writer.create_new_card.assert_called_once()

    def test_new_card_no_payment(self):
        machine = self._create_default_ticketing_machine()
        machine.get_new_ticket()
        ticket = self.card_writer.get_last_printed_ticket()
        machine.read_ticket(ticket)
        self.output.display.assert_called_once_with(TicketingMachine.NO_PAYMENT_TEXT)

    def test_one_hour_payment(self):
        machine = self._create_default_ticketing_machine()
        self.payment_calculator.calculate_payment.return_value = 10
        self.time_provider.get_current_time.return_value = 0
        machine.get_new_ticket()
        ticket = self.card_writer.get_last_printed_ticket()
        self.time_provider.get_current_time.return_value = 60 * 60
        machine.read_ticket(ticket)
        self.payment_calculator.calculate_payment.assert_called_once_with(start_time=0, end_time=60*60)
        self.output.display.assert_called_once_with(TicketingMachine.PAYMENT_TEXT.format(
            required_payment=10))
