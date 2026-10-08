"""Contract and numerical checks beyond the instructor's notebook examples."""

import unittest
from math import isclose

from fixedincomelib import (
    qfCreateProductFixedAccruedCashflow as fixed,
    qfCreateProductOvernightIndexCashflow as overnight,
    qfDisplayProduct,
)
from fixedincomelib.product import (
    ProductFixedAccruedCashflow, ProductOvernightIndexCashflow,
    ProductDisplayVisitor,
)
from bond_futures import Bond, clean_forward, implied_repo


class SolutionChecks(unittest.TestCase):
    def test_fixed_contract_accrual_and_payment(self):
        p = fixed("2026-01-02", "2026-04-02", "USD", 1e6, "ACT/360", "2026-04-06")
        self.assertEqual(p.accrued, 90/360)
        self.assertEqual(p.first_date.ISO(), "2026-01-02")
        self.assertEqual(p.termination_date.ISO(), "2026-04-02")
        self.assertEqual(p.last_date.ISO(), "2026-04-06")

    def test_defaults_and_signed_notional(self):
        p = fixed("2026-01-02", "2026-04-02", "USD", -1e6, "ACT/360")
        self.assertEqual(p.payment_date, p.termination_date)
        self.assertEqual(p.business_day_convention.value_str, "F")
        self.assertEqual(p.holiday_convention.value_str, "USGS")
        self.assertEqual(p.long_or_short.to_string(), "short")

    def test_index_currency_and_case(self):
        for key, currency in [("sofr-1b", "USD"), ("ff-1b", "USD"), ("sonia-1b", "GBP")]:
            p = overnight("2026-01-02", "3M", key, 500_000, "arithmetic")
            self.assertEqual(p.currency.value_str, currency)
            self.assertEqual(p.serialize()["ON_INDEX"], key.upper())
            self.assertEqual(p.payment_date, p.termination_date)

    def test_tenor_business_day_and_explicit_date(self):
        # 2 May 2026 is Saturday; SOFR's Following convention advances to Monday.
        p = overnight("2026-02-02", "3M", "SOFR-1B", 1)
        self.assertEqual(p.termination_date.ISO(), "2026-05-04")
        q = overnight("2026-02-02", "2026-05-02", "SOFR-1B", 1)
        self.assertEqual(q.termination_date.ISO(), "2026-05-02")

    def test_serialization_round_trip(self):
        p = fixed("2026-01-02", "2026-04-02", "USD", -1e6, "ACT/360", "2026-04-06")
        q = overnight("2026-01-02", "3M", "SOFR-1B", -1e6, "compound", .001, "2026-04-06")
        for product, cls in [(p, ProductFixedAccruedCashflow), (q, ProductOvernightIndexCashflow)]:
            copy = cls.deserialize(product.serialize())
            self.assertEqual(copy.serialize(), product.serialize())
            self.assertEqual(copy.first_date, product.first_date)
            self.assertEqual(copy.last_date, product.last_date)

    def test_invalid_contracts_rejected(self):
        calls = [
            lambda: fixed("2026-04-02", "2026-01-02", "USD", 1, "ACT/360"),
            lambda: overnight("2026-01-02", "3M", "UNKNOWN", 1),
            lambda: overnight("2026-01-02", "3M", "SOFR-1B", 1, spread=float("nan")),
        ]
        for call in calls:
            with self.assertRaises(ValueError):
                call()

    def test_visitor_dispatch_return_and_field_replacement(self):
        p = fixed("2026-01-02", "2026-04-02", "USD", 1, "ACT/360")
        q = overnight("2026-01-02", "3M", "SONIA-1B", -1)
        sentinel = object()
        class ReturningVisitor:
            def visit(self, product):
                return sentinel
        self.assertIs(p.accept(ReturningVisitor()), sentinel)
        self.assertIs(q.accept(ReturningVisitor()), sentinel)
        visitor = ProductDisplayVisitor()
        p.accept(visitor)
        q.accept(visitor)
        table = visitor.display()
        self.assertEqual(len(table), 10)
        self.assertNotIn("Accrual Basis", table.Name.tolist())
        self.assertEqual(qfDisplayProduct(q).Value.tolist()[2:4], ["GBP", "SHORT"])

    def test_bond_numbers_and_repo_inversion(self):
        b = Bond(.04, 9)
        self.assertAlmostEqual(b.conversion_factor(), .8624648692054273)
        self.assertAlmostEqual(clean_forward(b, 100, .02, .25), 99.5)
        self.assertAlmostEqual(implied_repo(b, 100, 115.3670, .25), .0199993826249)
        # Inversion also needs to work across a coupon and after time advances.
        for delivery, asof in [(.25, 0), (.75, 0), (.75, .1)]:
            spot = b.clean_price(.045, asof)
            f = clean_forward(b, spot, .027, delivery, asof)/b.conversion_factor()
            self.assertTrue(isclose(implied_repo(b, spot, f, delivery, asof), .027, abs_tol=1e-12))


if __name__ == "__main__":
    unittest.main(verbosity=2)
