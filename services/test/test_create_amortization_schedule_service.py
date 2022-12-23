"""Tests for CreateAmortizationScheduleService"""
import unittest
from dataclasses import dataclass
from decimal import Decimal
from services import CreateAmortizationScheduleService


class TestCreateAmortizationScheduleService(unittest.TestCase):
    def test_generate_amortization_schedule(self):
        @dataclass
        class Example:
            """Example class for test cases for amortization"""
            name: str

            amount: Decimal
            term_months: int
            interest_rate: Decimal

            expected: dict[int, dict[str, Decimal]]

        # Examples checked against https://www.calculator.net/amortization-calculator.html
        examples = [
            Example(
                name='$1000.00 12 months @ 10.00%',
                amount=Decimal('1000.00'),
                term_months=12,
                interest_rate=Decimal('0.1'),
                expected={
                    0: {
                        'balance': Decimal('1000.00'),
                        'payment': Decimal('0.00'),
                        'principal_paid': Decimal('0.00'),
                        'interest_paid': Decimal('0.00'),
                        'total_paid': Decimal('0.00'),
                        'total_principal_paid': Decimal('0.00'),
                        'total_interest_paid': Decimal('0.00')
                    },
                    6: {
                        'balance': Decimal('512.42'),
                        'payment': Decimal('87.92'),
                        'principal_paid': Decimal('82.96'),
                        'interest_paid': Decimal('4.96'),
                        'total_paid': Decimal('527.52'),
                        'total_principal_paid': Decimal('487.58'),
                        'total_interest_paid': Decimal('39.94')
                    },
                    12: {
                        'balance': Decimal('0.00'),
                        'payment': Decimal('87.87'),
                        'principal_paid': Decimal('87.14'),
                        'interest_paid': Decimal('0.73'),
                        'total_paid': Decimal('1054.99'),
                        'total_principal_paid': Decimal('1000.00'),
                        'total_interest_paid': Decimal('54.99')
                    }
                }),
            Example(
                name='$1000.10 12 months @ 10.00%',
                amount=Decimal('1000.10'),
                term_months=12,
                interest_rate=Decimal('0.1'),
                expected={
                    0: {
                        'balance': Decimal('1000.10'),
                        'payment': Decimal('0.00'),
                        'principal_paid': Decimal('0.00'),
                        'interest_paid': Decimal('0.00'),
                        'total_paid': Decimal('0.00'),
                        'total_principal_paid': Decimal('0.00'),
                        'total_interest_paid': Decimal('0.00')
                    },
                    6: {
                        'balance': Decimal('512.53'),
                        'payment': Decimal('87.92'),
                        'principal_paid': Decimal('82.96'),
                        'interest_paid': Decimal('4.96'),
                        'total_paid': Decimal('527.52'),
                        'total_principal_paid': Decimal('487.57'),
                        'total_interest_paid': Decimal('39.95')
                    },
                    12: {
                        'balance': Decimal('0.00'),
                        'payment': Decimal('87.98'),
                        'principal_paid': Decimal('87.25'),
                        'interest_paid': Decimal('0.73'),
                        'total_paid': Decimal('1055.10'),
                        'total_principal_paid': Decimal('1000.10'),
                        'total_interest_paid': Decimal('55.00')
                    }
                }),
            Example(
                name='$1000.20 12 months @ 10.00%',
                amount=Decimal('1000.20'),
                term_months=12,
                interest_rate=Decimal('0.1'),
                expected={
                    0: {
                        'balance': Decimal('1000.20'),
                        'payment': Decimal('0.00'),
                        'principal_paid': Decimal('0.00'),
                        'interest_paid': Decimal('0.00'),
                        'total_paid': Decimal('0.00'),
                        'total_principal_paid': Decimal('0.00'),
                        'total_interest_paid': Decimal('0.00')
                    },
                    6: {
                        'balance': Decimal('512.57'),
                        'payment': Decimal('87.93'),
                        'principal_paid': Decimal('82.97'),
                        'interest_paid': Decimal('4.96'),
                        'total_paid': Decimal('527.58'),
                        'total_principal_paid': Decimal('487.63'),
                        'total_interest_paid': Decimal('39.95')
                    },
                    12: {
                        'balance': Decimal('0.00'),
                        'payment': Decimal('87.97'),
                        'principal_paid': Decimal('87.24'),
                        'interest_paid': Decimal('0.73'),
                        'total_paid': Decimal('1055.20'),
                        'total_principal_paid': Decimal('1000.20'),
                        'total_interest_paid': Decimal('55.00')
                    }
                }),
            Example(
                name='$1000.00 12 months @ 0.00%',
                amount=Decimal('1000.00'),
                term_months=12,
                interest_rate=Decimal('0.0'),
                expected={
                    0: {
                        'balance': Decimal('1000.00'),
                        'payment': Decimal('0.00'),
                        'principal_paid': Decimal('0.00'),
                        'interest_paid': Decimal('0.00'),
                        'total_paid': Decimal('0.00'),
                        'total_principal_paid': Decimal('0.00'),
                        'total_interest_paid': Decimal('0.00')
                    },
                    6: {
                        'balance': Decimal('500.02'),
                        'payment': Decimal('83.33'),
                        'principal_paid': Decimal('83.33'),
                        'interest_paid': Decimal('0.00'),
                        'total_paid': Decimal('499.98'),
                        'total_principal_paid': Decimal('499.98'),
                        'total_interest_paid': Decimal('0.00')
                    },
                    12: {
                        'balance': Decimal('0.00'),
                        'payment': Decimal('83.37'),
                        'principal_paid': Decimal('83.37'),
                        'interest_paid': Decimal('0.00'),
                        'total_paid': Decimal('1000.00'),
                        'total_principal_paid': Decimal('1000.00'),
                        'total_interest_paid': Decimal('0.00')
                    }
                }),
            Example(
                name='$1000.00 1 months @ 10.00%',
                amount=Decimal('1000.00'),
                term_months=1,
                interest_rate=Decimal('0.1'),
                expected={
                    0: {
                        'balance': Decimal('1000.00'),
                        'payment': Decimal('0.00'),
                        'principal_paid': Decimal('0.00'),
                        'interest_paid': Decimal('0.00'),
                        'total_paid': Decimal('0.00'),
                        'total_principal_paid': Decimal('0.00'),
                        'total_interest_paid': Decimal('0.00')
                    },
                    1: {
                        'balance': Decimal('0.00'),
                        'payment': Decimal('1008.33'),
                        'principal_paid': Decimal('1000.00'),
                        'interest_paid': Decimal('8.33'),
                        'total_paid': Decimal('1008.33'),
                        'total_principal_paid': Decimal('1000.00'),
                        'total_interest_paid': Decimal('8.33')
                    }
                }),
            Example(
                name='$1000.00 12 months @ 3000.00% negative amortization/balloon payment',
                amount=Decimal('1000.00'),
                term_months=12,
                interest_rate=Decimal('30.00'),
                expected={
                    0: {
                        'balance': Decimal('1000.00'),
                        'payment': Decimal('0.00'),
                        'principal_paid': Decimal('0.00'),
                        'interest_paid': Decimal('0.00'),
                        'total_paid': Decimal('0.00'),
                        'total_principal_paid': Decimal('0.00'),
                        'total_interest_paid': Decimal('0.00')
                    },
                    6: {
                        'balance': Decimal('1000.00'),
                        'payment': Decimal('2500.00'),
                        'principal_paid': Decimal('0.00'),
                        'interest_paid': Decimal('2500.00'),
                        'total_paid': Decimal('15000.00'),
                        'total_principal_paid': Decimal('0.00'),
                        'total_interest_paid': Decimal('15000.00')
                    },
                    11: {
                        'balance': Decimal('1000.00'),
                        'payment': Decimal('2500.00'),
                        'principal_paid': Decimal('0.00'),
                        'interest_paid': Decimal('2500.00'),
                        'total_paid': Decimal('27500.00'),
                        'total_principal_paid': Decimal('0.00'),
                        'total_interest_paid': Decimal('27500.00')
                    },
                    12: {
                        'balance': Decimal('0.00'),
                        'payment': Decimal('3500.00'),
                        'principal_paid': Decimal('1000.00'),
                        'interest_paid': Decimal('2500.00'),
                        'total_paid': Decimal('31000.00'),
                        'total_principal_paid': Decimal('1000.00'),
                        'total_interest_paid': Decimal('30000.00')
                    }
                }),
        ]

        for example in examples:
            with self.subTest(example=example.name):
                schedule = CreateAmortizationScheduleService.generate_amortization_schedule(
                    example.amount,
                    example.term_months,
                    example.interest_rate)
                self.assertEqual(
                    example.term_months + 1,
                    len(schedule),
                    'failed {} length, expected {}, actual {}'.format(
                        example.name,
                        example.term_months + 1,
                        len(schedule)))
                for month in example.expected:
                    with self.subTest(month=month):
                        month_example = example.expected[month]
                        for parameter in month_example:
                            with self.subTest(parameter=parameter):
                                self.assertEqual(month_example[parameter], schedule[month][parameter])

    def test_generate_amortization_schedule_zero_amount(self):
        with self.assertRaises(Exception):
            CreateAmortizationScheduleService.generate_amortization_schedule(
                amount=Decimal('0.00'), term_months=12, interest_rate=Decimal('0.1'))

    def test_generate_amortization_schedule_negative_amount(self):
        with self.assertRaises(Exception):
            CreateAmortizationScheduleService.generate_amortization_schedule(
                amount=Decimal('-1.00'), term_months=12, interest_rate=Decimal('0.1'))

    def test_generate_amortization_schedule_zero_term_months(self):
        with self.assertRaises(Exception):
            CreateAmortizationScheduleService.generate_amortization_schedule(
                amount=Decimal('1000.00'), term_months=0, interest_rate=Decimal('0.1'))

    def test_generate_amortization_schedule_negative_term_months(self):
        with self.assertRaises(Exception):
            CreateAmortizationScheduleService.generate_amortization_schedule(
                amount=Decimal('1000.00'), term_months=-1, interest_rate=Decimal('0.1'))

    def test_generate_amortization_schedule_negative_interest_rate(self):
        with self.assertRaises(Exception):
            CreateAmortizationScheduleService.generate_amortization_schedule(
                amount=Decimal('1000.00'), term_months=12, interest_rate=Decimal('-0.1'))
