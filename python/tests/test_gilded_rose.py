import pytest

from gilded_rose import GildedRose, Item

BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS = "Sulfuras, Hand of Ragnaros"
CONJURED_MANA_CAKE = "Conjured Mana Cake"


@pytest.mark.parametrize(
    (
        "initial_sell_in",
        "initial_quality",
        "expected_sell_in",
        "expected_quality",
    ),
    [
        (10, 20, 9, 19),
        (0, 20, -1, 18),
        (-1, 20, -2, 18),
        (5, 0, 4, 0),
        (-1, 0, -2, 0),
    ],
)
def test_normal_item_degrades(
    initial_sell_in,
    initial_quality,
    expected_sell_in,
    expected_quality,
):
    item = Item(
        name="+5 Dexterity Vest",
        sell_in=initial_sell_in,
        quality=initial_quality,
    )

    GildedRose(items=[item]).update_quality()

    assert item.sell_in == expected_sell_in
    assert item.quality == expected_quality


@pytest.mark.parametrize(
    (
        "initial_sell_in",
        "initial_quality",
        "expected_sell_in",
        "expected_quality",
    ),
    [
        (2, 0, 1, 1),
        (0, 48, -1, 50),
        (-1, 10, -2, 12),
        (5, 50, 4, 50),
        (0, 50, -1, 50),
    ],
)
def test_aged_brie_increases_in_quality(
    initial_sell_in,
    initial_quality,
    expected_sell_in,
    expected_quality,
):
    item = Item(
        name="Aged Brie",
        sell_in=initial_sell_in,
        quality=initial_quality,
    )

    GildedRose(items=[item]).update_quality()

    assert item.sell_in == expected_sell_in
    assert item.quality == expected_quality


@pytest.mark.parametrize(
    (
        "initial_sell_in",
        "initial_quality",
        "expected_sell_in",
        "expected_quality",
    ),
    [
        (11, 20, 10, 21),
        (10, 20, 9, 22),
        (6, 20, 5, 22),
        (5, 20, 4, 23),
        (10, 49, 9, 50),
        (5, 48, 4, 50),
    ],
)
def test_backstage_passes_increase_in_quality_before_concert(
    initial_sell_in,
    initial_quality,
    expected_sell_in,
    expected_quality,
):
    item = Item(
        name=BACKSTAGE_PASSES,
        sell_in=initial_sell_in,
        quality=initial_quality,
    )

    GildedRose(items=[item]).update_quality()

    assert item.sell_in == expected_sell_in
    assert item.quality == expected_quality


@pytest.mark.parametrize(
    (
        "initial_sell_in",
        "initial_quality",
        "expected_sell_in",
        "expected_quality",
    ),
    [
        (0, 20, -1, 0),
        (-1, 30, -2, 0),
    ],
)
def test_backstage_passes_drop_to_zero_after_concert(
    initial_sell_in,
    initial_quality,
    expected_sell_in,
    expected_quality,
):
    item = Item(
        name=BACKSTAGE_PASSES,
        sell_in=initial_sell_in,
        quality=initial_quality,
    )

    GildedRose(items=[item]).update_quality()

    assert item.sell_in == expected_sell_in
    assert item.quality == expected_quality


@pytest.mark.parametrize(
    ("initial_sell_in", "initial_quality"),
    [
        (10, 80),
        (0, 80),
        (-1, 80),
    ],
)
def test_sulfuras_never_changes(initial_sell_in, initial_quality):
    item = Item(
        name=SULFURAS,
        sell_in=initial_sell_in,
        quality=initial_quality,
    )

    GildedRose(items=[item]).update_quality()

    assert item.sell_in == initial_sell_in
    assert item.quality == initial_quality


@pytest.mark.parametrize(
    (
        "initial_sell_in",
        "initial_quality",
        "expected_sell_in",
        "expected_quality",
    ),
    [
        (10, 20, 9, 18),
        (0, 20, -1, 16),
        (5, 1, 4, 0),
        (-1, 2, -2, 0),
    ],
)
def test_conjured_item_degrades_twice_as_fast(
    initial_sell_in,
    initial_quality,
    expected_sell_in,
    expected_quality,
):
    item = Item(
        name=CONJURED_MANA_CAKE,
        sell_in=initial_sell_in,
        quality=initial_quality,
    )

    GildedRose(items=[item]).update_quality()

    assert item.sell_in == expected_sell_in
    assert item.quality == expected_quality


@pytest.mark.parametrize(
    ("name", "expected_sell_in", "expected_quality"),
    [
        ("Conjured", 9, 18),
        ("Conjuredness", 9, 19),
    ],
)
def test_conjured_name_matching(name, expected_sell_in, expected_quality):
    item = Item(name=name, sell_in=10, quality=20)

    GildedRose(items=[item]).update_quality()

    assert item.sell_in == expected_sell_in
    assert item.quality == expected_quality
