from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.addons.base.tests.test_display_name import TestEveryModel


# ── Approach 1: Monkey Patching ───────────────────────────────────────────────
# def pass_test(self):
#     pass
# TestEveryModel.test_display_name_new_record = pass_test


# # ── Approach 2: Inheritance ───────────────────────────────────────────────────
# class PatchedTestEveryModel(TestEveryModel):
#     def test_display_name_new_record(self):
#         pass


@tagged("newton")
class TestEagleProperty(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property = cls.env["eagle.property"].create({
            "name": "TestProperty",           # no spaces — name constraint
            "construction_date": "2020-01-01", # required for display_name now
        })

    def test_property_creation(self):
        self.assertEqual(self.property.name, "TestProperty")
        self.assertEqual(str(self.property.construction_date), "2020-01-01")

    def test_construction_date_in_future_raises(self):
        with self.assertRaises(ValidationError):
            self.env["eagle.property"].create({
                "name": "FutureProperty",
                "construction_date": "2099-01-01",
            })

    def test_name_with_spaces_raises(self):
        """Breaking change: names with spaces are now rejected."""
        with self.assertRaises(ValidationError):
            self.env["eagle.property"].create({
                "name": "Invalid Name",
                "construction_date": "2020-01-01",
            })
