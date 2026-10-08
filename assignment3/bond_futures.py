"""Assignment 3 bond-futures calculations in price points per 100 face value.

The bond starts immediately after a coupon date. Time is measured in years;
repo accrues with simple interest. Conversion factors use the assignment's
time-zero clean-price definition, and stay fixed for the contract.
"""

from dataclasses import dataclass
from math import isclose


@dataclass(frozen=True)
class Bond:
    coupon: float
    maturity: float
    frequency: int = 2
    face: float = 100.0

    def cashflows(self):
        count = round(self.maturity * self.frequency)
        if count < 1 or not isclose(count, self.maturity * self.frequency):
            raise ValueError("Maturity must contain a positive whole number of coupon periods")
        coupon_cash = self.face * self.coupon / self.frequency
        return [
            (i / self.frequency,
             coupon_cash + (self.face if i == count else 0.0))
            for i in range(1, count + 1)
        ]

    def clean_price(self, yield_rate, asof=0.0):
        """Clean price at asof; nominal yield compounded by frequency."""
        if yield_rate <= -self.frequency:
            raise ValueError("Yield creates a nonpositive discount base")
        dirty = sum(
            cash / (1 + yield_rate / self.frequency) ** ((t-asof) * self.frequency)
            for t, cash in self.cashflows() if t > asof
        )
        return dirty - self.accrued_interest(asof)

    def conversion_factor(self):
        return self.clean_price(0.06) / self.face

    def accrued_interest(self, delivery):
        if not 0 <= delivery < self.maturity:
            raise ValueError("Delivery must precede maturity")
        periods = delivery * self.frequency
        if isclose(periods, round(periods), abs_tol=1e-12):
            return 0.0  # delivery immediately after the coupon on a coupon date
        elapsed = delivery - int(periods) / self.frequency
        return self.face * self.coupon * elapsed


def clean_forward(bond, spot_clean, repo, delivery, asof=0.0):
    """Carry dirty price from asof; reinvest coupons through delivery."""
    if not 0 <= asof < delivery < bond.maturity:
        raise ValueError("Require 0 <= asof < delivery < maturity")
    spot_dirty = spot_clean + bond.accrued_interest(asof)
    dirty_forward = spot_dirty * (1 + repo * (delivery-asof))
    dirty_forward -= sum(
        cash * (1 + repo * (delivery - t))
        for t, cash in bond.cashflows() if asof < t <= delivery
    )
    return dirty_forward - bond.accrued_interest(delivery)


def implied_repo(bond, spot_clean, futures_price, delivery, asof=0.0):
    """Solve simple-interest cash-and-carry at the quoted futures price."""
    if not 0 <= asof < delivery < bond.maturity:
        raise ValueError("Require 0 <= asof < delivery < maturity")
    spot_dirty = spot_clean + bond.accrued_interest(asof)
    coupons = [(t, cash) for t, cash in bond.cashflows() if asof < t <= delivery]
    numerator = (
        futures_price * bond.conversion_factor()
        + bond.accrued_interest(delivery)
        + sum(cash for _, cash in coupons) - spot_dirty
    )
    denominator = spot_dirty * (delivery-asof) - sum(
        cash * (delivery - t) for t, cash in coupons
    )
    return numerator / denominator


def main():
    bond = Bond(coupon=0.04, maturity=9)
    spot, repo, delivery = 100.0, 0.02, 0.25
    bf = clean_forward(bond, spot, repo, delivery)
    k = bond.conversion_factor()
    print(f"Delivery accrued interest: {bond.accrued_interest(delivery):.6f}")
    print(f"Dirty forward price: {bf + bond.accrued_interest(delivery):.6f}")
    print(f"Clean forward price BF: {bf:.6f}")
    print(f"Conversion factor K: {k:.10f}")
    print(f"Normalized forward BF/K: {bf/k:.7f}")
    print(f"Implied repo for F=115.3670: {100*implied_repo(bond,spot,115.3670,delivery):.7f}%")
    print("\nIllustrative basket, 30-day-later yield scenarios (not actual market data)")
    basket = [Bond(0.04, 7), Bond(0.04, 9)]
    asof = 30/360
    print("yield    7Y normalized    9Y normalized    CTD")
    for y in [0.03, 0.04, 0.05, 0.06, 0.07]:
        prices = [clean_forward(b, b.clean_price(y,asof), repo, delivery,asof)/b.conversion_factor() for b in basket]
        winner = min(range(len(basket)), key=prices.__getitem__)
        print(f"{y:.0%}       {prices[0]:.6f}       {prices[1]:.6f}       {basket[winner].maturity}Y")


if __name__ == "__main__":
    main()
