# -*- coding: utf-8 -*-
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


class BasicItem(Item):
    def __init__(self, name, sell_in, quality) -> None:
        super().__init__(name, sell_in, quality)

    def apply_quality_change(self, quality_change: int) -> None:
        self.quality = max(
            MIN_QUALITY,
            min(MAX_QUALITY, self.quality + quality_change),
        )

    def update_item_sell_in(self) -> None:
        self.sell_in -= 1

    def update_item_quality(self) -> None:
        depreciation_multiplier = 1
        if self.sell_in <= 0:
            depreciation_multiplier *= 2
        self.apply_quality_change(BASE_QUALITY_CHANGE * depreciation_multiplier)


class LegendaryItem(BasicItem):
    def __init__(self, name, sell_in, quality) -> None:
        super().__init__(name, sell_in, quality)

    def update_item_sell_in(self) -> None:
        return None

    def update_item_quality(self) -> None:
        return None


class ConjuredItem(BasicItem):
    def __init__(self, name, sell_in, quality) -> None:
        super().__init__(name, sell_in, quality)

    def update_item_quality(self) -> None:
        depreciation_multiplier = 2
        if self.sell_in <= 0:
            depreciation_multiplier *= 2
        self.apply_quality_change(BASE_QUALITY_CHANGE * depreciation_multiplier)


class AgedItem(BasicItem):
    def __init__(self, name, sell_in, quality, expires=False) -> None:
        super().__init__(name, sell_in, quality)
        self.expires: bool = expires

    def update_item_quality(self) -> None:
        if not self.expires or self.sell_in > 10:
            self.apply_quality_change(1)
        elif self.sell_in <= 0:
            self.apply_quality_change(MIN_QUALITY - MAX_QUALITY)
        elif self.sell_in <= 5:
            self.apply_quality_change(3)
        else:
            self.apply_quality_change(2)


class GildedRose(object):

    def __init__(self, items: list[BasicItem]) -> None:
        self.items = items

    def update_quality(self) -> None:
        for item in self.items:
            item.update_item_sell_in()
            item.update_item_quality()
