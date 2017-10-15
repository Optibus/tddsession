class TicketingMachine(object):
    NO_PAYMENT_TEXT = "Free of charge!"
    PAYMENT_TEXT = "Pay up bitch {required_payment}$!"

    def __init__(self, card_writer, card_reader, output, time_provider, payment_calculator):
        self.card_writer = card_writer
        self.card_reader = card_reader
        self.output = output
        self.time_provider = time_provider
        self.payment_calculator = payment_calculator

    def get_new_ticket(self):
        self.card_writer.create_new_card(self.time_provider.get_current_time())

    def read_ticket(self, ticket):
        current_time = self.time_provider.get_current_time()
        required_payment = self.payment_calculator.calculate_payment(
            start_time=ticket.printed_time, end_time=current_time)
        if required_payment == 0:
            self.output.display(self.NO_PAYMENT_TEXT)
        else:
            self.output.display(self.PAYMENT_TEXT.format(required_payment=required_payment))