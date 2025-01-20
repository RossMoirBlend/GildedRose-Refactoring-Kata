# -*- coding: utf-8 -*-
BETTER_AGED_NON_EXPIRE: list = ["Aged Brie"]
BETTER_AGED_EXPIRE: list = ["Backstage passes to a TAFKAL80ETC concert"]
LEGENDARY_ITEMS: list = ["Sulfuras, Hand of Ragnaros"]
CONJURED_ITEMS: list = ["Conjured Mana Cake"]

MAX_QUALITY: int = 50
MIN_QUALITY: int = 0
BASE_QUALITY_CHANGE: int = -1


class Item(object):
    def __init__(self, name, sell_in, quality) -> None:
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self) -> str:
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class GildedRose(object):

    def __init__(self, items: list[Item]) -> None:
        self.items = items

    @staticmethod
    def apply_quality_change(item, quality_change: int) -> None:
        item.quality = max(
            MIN_QUALITY,
            min(MAX_QUALITY, item.quality + quality_change),
        )

    @staticmethod
    def update_item_sell_in(item: Item) -> None:
        item.sell_in -= 1

    def update_item_quality(self, item: Item) -> None:
        depreciation_multiplier: int = 2 if item.name in CONJURED_ITEMS else 1

        if item.name in BETTER_AGED_NON_EXPIRE:
            self.apply_quality_change(item, 1)
        elif item.name in BETTER_AGED_EXPIRE:
            if item.sell_in <= 0:
                self.apply_quality_change(item, MIN_QUALITY - MAX_QUALITY)
            elif item.sell_in <= 5:
                self.apply_quality_change(item, 3)
            elif item.sell_in <= 10:
                self.apply_quality_change(item, 2)
            else:
                self.apply_quality_change(item, 1)
        else:
            if item.sell_in <= 0:
                depreciation_multiplier *= 2
            self.apply_quality_change(
                item, BASE_QUALITY_CHANGE * depreciation_multiplier
            )

    def update_quality(self) -> None:
        for item in self.items:
            if item.name in LEGENDARY_ITEMS:
                continue
            self.update_item_sell_in(item=item)
            self.update_item_quality(item=item)
