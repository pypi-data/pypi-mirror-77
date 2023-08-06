# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo.tests import SavepointCase


class TestAbcLocation(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        ref = cls.env.ref
        cls.stock_location = ref("stock.stock_location_stock")
        cls.cardboxes_location = ref("stock_storage_type.stock_location_cardboxes")
        cls.pallets_location = ref("stock_storage_type.stock_location_pallets")
        cls.cardboxes_bin_1_location = ref(
            "stock_storage_type.stock_location_cardboxes_bin_1"
        )
        cls.cardboxes_bin_2_location = ref(
            "stock_storage_type.stock_location_cardboxes_bin_2"
        )
        cls.cardboxes_bin_3_location = ref(
            "stock_storage_type.stock_location_cardboxes_bin_3"
        )
        cls.pallets_bin_1_location = ref(
            "stock_storage_type.stock_location_pallets_bin_1"
        )
        cls.pallets_bin_2_location = ref(
            "stock_storage_type.stock_location_pallets_bin_2"
        )
        cls.pallets_bin_3_location = ref(
            "stock_storage_type.stock_location_pallets_bin_3"
        )
        cls.product = ref("product.product_product_9")

    def test_display_abc_storage_one_level(self):
        self.cardboxes_location.write({"pack_putaway_strategy": "abc"})
        self.assertTrue(self.cardboxes_bin_1_location.display_abc_storage)
        self.assertTrue(self.cardboxes_bin_2_location.display_abc_storage)
        self.assertTrue(self.cardboxes_bin_3_location.display_abc_storage)
        self.assertFalse(self.pallets_bin_1_location.display_abc_storage)
        self.assertFalse(self.pallets_bin_2_location.display_abc_storage)
        self.assertFalse(self.pallets_bin_3_location.display_abc_storage)
        self.cardboxes_location.write({"pack_putaway_strategy": "ordered_locations"})
        self.assertFalse(self.cardboxes_bin_1_location.display_abc_storage)
        self.assertFalse(self.cardboxes_bin_2_location.display_abc_storage)
        self.assertFalse(self.cardboxes_bin_3_location.display_abc_storage)
        self.assertFalse(self.pallets_bin_1_location.display_abc_storage)
        self.assertFalse(self.pallets_bin_2_location.display_abc_storage)
        self.assertFalse(self.pallets_bin_3_location.display_abc_storage)

    def test_display_abc_storage_two_levels(self):
        self.stock_location.write({"pack_putaway_strategy": "abc"})
        self.assertTrue(self.cardboxes_bin_1_location.display_abc_storage)
        self.assertTrue(self.cardboxes_bin_2_location.display_abc_storage)
        self.assertTrue(self.cardboxes_bin_3_location.display_abc_storage)
        self.assertTrue(self.pallets_bin_1_location.display_abc_storage)
        self.assertTrue(self.pallets_bin_2_location.display_abc_storage)
        self.assertTrue(self.pallets_bin_3_location.display_abc_storage)
        self.stock_location.write({"pack_putaway_strategy": "none"})
        self.assertFalse(self.cardboxes_bin_1_location.display_abc_storage)
        self.assertFalse(self.cardboxes_bin_2_location.display_abc_storage)
        self.assertFalse(self.cardboxes_bin_3_location.display_abc_storage)
        self.assertFalse(self.pallets_bin_1_location.display_abc_storage)
        self.assertFalse(self.pallets_bin_2_location.display_abc_storage)
        self.assertFalse(self.pallets_bin_3_location.display_abc_storage)

    def test_abc_ordered(self):
        self.cardboxes_location.write({"pack_putaway_strategy": "abc"})
        self.cardboxes_bin_1_location.write({"abc_storage": "b"})
        self.cardboxes_bin_2_location.write({"abc_storage": "a"})
        self.cardboxes_bin_3_location.write({"abc_storage": "c"})
        self.product.write({"abc_storage": "a"})
        ordered_locations = self.cardboxes_location.get_storage_locations(self.product)
        self.assertEqual(
            ordered_locations,
            self.cardboxes_bin_2_location
            | self.cardboxes_bin_1_location
            | self.cardboxes_bin_3_location,
        )
        self.product.write({"abc_storage": "b"})
        ordered_locations = self.cardboxes_location.get_storage_locations(self.product)
        self.assertEqual(
            ordered_locations,
            self.cardboxes_bin_1_location
            | self.cardboxes_bin_3_location
            | self.cardboxes_bin_2_location,
        )
        self.product.write({"abc_storage": "c"})
        ordered_locations = self.cardboxes_location.get_storage_locations(self.product)
        self.assertEqual(
            ordered_locations,
            self.cardboxes_bin_3_location
            | self.cardboxes_bin_2_location
            | self.cardboxes_bin_1_location,
        )
