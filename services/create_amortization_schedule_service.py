'''Service for generating amortization schedules'''
import decimal
from decimal import Decimal


class CreateAmortizationScheduleService:
    """Service for generating amortization schedules"""
    @staticmethod
    def generate_amortization_schedule(amount: Decimal, term_months: int, interest_rate: Decimal):
        """Generate an amortization schedule

        The payment is always a full-cent amount which will leave usually leave
        a balance discrepancy at the end of the loan. This will be adjusted
        and will result in a balloon payment if the loan negatively amortizes.

        @:param amount: Amount of loan (positive)
        @:param term_months: Loan term in months (positive)
        @:param interest_rate: Interest rate (positive or zero)
        @:returns: Array of month schedules containing the remaining balance,
        monthly payment, principal and interest paid in the month, and running
        totals of the principal, interest, and total paid so far.
        """
        if amount <= 0:
            raise Exception('amount must be positive')
        if term_months <= 0:
            raise Exception('term_months must be 1 or longer')
        if interest_rate < 0:
            raise Exception('interest_rate must be 0.0 or greater')

        decimal.getcontext().rounding = decimal.ROUND_HALF_UP
        try:
            monthly_interest_rate = interest_rate / Decimal('12')
            payment = amount * \
                (monthly_interest_rate * (1 + monthly_interest_rate) ** term_months) / \
                ((1 + monthly_interest_rate) ** term_months - 1)
            # Actual payment can only be in whole cents. This will likely result
            # in a balance discrepancy which will be adjusted for at the end.
            payment = round(payment, 2)
        except decimal.InvalidOperation:
            # Handle 0% interest rate
            payment = round(amount / term_months, 2)

        schedule = [{
            'balance': amount,
            'payment': Decimal('0.00'),
            'principal_paid': Decimal('0.00'),
            'interest_paid': Decimal('0.00'),
            'total_paid': Decimal('0.00'),
            'total_principal_paid': Decimal('0.00'),
            'total_interest_paid': Decimal('0.00')
        }]

        for month in range(1, term_months + 1):
            previous_month = schedule[month - 1]

            accrued_interest = previous_month['balance'] * monthly_interest_rate
            principal_paid = payment - accrued_interest
            balance = previous_month['balance'] - principal_paid

            total_paid = previous_month['total_paid'] + payment
            total_principal_paid = previous_month['total_principal_paid'] + principal_paid
            total_interest_paid = previous_month['total_interest_paid'] + accrued_interest

            schedule.append({
                'balance': balance,
                'payment': payment,
                'principal_paid': principal_paid,
                'interest_paid': accrued_interest,
                'total_paid': total_paid,
                'total_principal_paid': total_principal_paid,
                'total_interest_paid': total_interest_paid
            })

        # Payment is always in a whole-cent value, but that might lead to a
        # small discrepancy as the final balance. Adjust final balances to
        # result in the final amounts (this makes a balloon payment in cases
        # where the loan has negative amortization).
        last_month = schedule[-1]
        balance_discrepancy = last_month['balance']
        last_month['balance'] = Decimal('0.00')
        last_month['payment'] += balance_discrepancy
        last_month['total_principal_paid'] += balance_discrepancy
        last_month['total_paid'] += balance_discrepancy

        # Final schedule only needs whole cents
        for month in range(1, term_months + 1):
            schedule[month]['balance'] = round(schedule[month]['balance'], 2)
            schedule[month]['payment'] = round(schedule[month]['payment'], 2)
            schedule[month]['principal_paid'] = round(schedule[month]['principal_paid'], 2)
            schedule[month]['interest_paid'] = round(schedule[month]['interest_paid'], 2)
            schedule[month]['total_paid'] = round(schedule[month]['total_paid'], 2)
            schedule[month]['total_principal_paid'] = round(schedule[month]['total_principal_paid'], 2)
            schedule[month]['total_interest_paid'] = round(schedule[month]['total_interest_paid'], 2)

        last_month = schedule[-1]
        # This field can be susceptible to rounding errors. Ensure these three
        # fields add up correctly.
        last_month['principal_paid'] = last_month['payment'] - last_month['interest_paid']

        return schedule
