# -*- coding: utf-8 -*-


class ItemUpdateStrategy:
    MAX_QUALITY = 50

    def __init__(self, item):
        self.item = item

    def update(self):
        self.update_quality()
        self.item.sell_in -= 1

    def update_quality(self):
        raise NotImplementedError

    def increase_quality(self, amount):
        self.item.quality = min(self.MAX_QUALITY, self.item.quality + amount)

    def decrease_quality(self, amount):
        self.item.quality = max(0, self.item.quality - amount)


class NormalItemUpdateStrategy(ItemUpdateStrategy):
    def update_quality(self):
        degradation = 2 if self.item.sell_in <= 0 else 1
        self.decrease_quality(degradation)


class AgedBrieUpdateStrategy(ItemUpdateStrategy):
    def update_quality(self):
        increase = 2 if self.item.sell_in <= 0 else 1
        self.increase_quality(increase)


class BackstagePassUpdateStrategy(ItemUpdateStrategy):
    def update_quality(self):
        if self.item.sell_in <= 0:
            self.item.quality = 0
        elif self.item.sell_in <= 5:
            self.increase_quality(3)
        elif self.item.sell_in <= 10:
            self.increase_quality(2)
        else:
            self.increase_quality(1)


class SulfurasUpdateStrategy(ItemUpdateStrategy):
    def update(self):
        pass

    def update_quality(self):
        pass


class ConjuredItemUpdateStrategy(ItemUpdateStrategy):
    def update_quality(self):
        degradation = 4 if self.item.sell_in <= 0 else 2
        self.decrease_quality(degradation)


STRATEGIES_BY_NAME = {
    "Aged Brie": AgedBrieUpdateStrategy,
    "Backstage passes to a TAFKAL80ETC concert": BackstagePassUpdateStrategy,
    "Sulfuras, Hand of Ragnaros": SulfurasUpdateStrategy,
}


def update_strategy_for(item):
    if item.name.startswith("Conjured"):
        return ConjuredItemUpdateStrategy(item)
    strategy = STRATEGIES_BY_NAME.get(item.name, NormalItemUpdateStrategy)
    return strategy(item)


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            update_strategy_for(item).update()


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
