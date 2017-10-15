import unittest


class PaymentCalculator(object):

    def __init__(self, hour_rate, free_time):
        self.hour_rate = hour_rate
        self.free_time = free_time

    def calculate_payment(self, start_time, end_time):
        duration = (end_time - start_time)
        if duration <= self.free_time * 60:
            return 0
        return (duration / 3600.0) * self.hour_rate


class TestPaymentCalculator(unittest.TestCase):

    def _create_default_payment_calculator(self, hour_rate=10, free_time=0):
        return PaymentCalculator(hour_rate=hour_rate, free_time=free_time)

    def test_no_payment_calc(self):
        calculator = self._create_default_payment_calculator()
        self.assertEqual(0, calculator.calculate_payment(start_time=0, end_time=0))

    def test_one_hour_payment(self):
        calculator = self._create_default_payment_calculator(hour_rate=10)
        self.assertEqual(10, calculator.calculate_payment(start_time=0, end_time=3600))

    def test_first_15_minutes_free(self):
        calculator = self._create_default_payment_calculator(free_time=15)
        self.assertEqual(0, calculator.calculate_payment(start_time=0, end_time=15 * 60))
        self.assertNotEqual(0, calculator.calculate_payment(start_time=0, end_time=16 * 60))

