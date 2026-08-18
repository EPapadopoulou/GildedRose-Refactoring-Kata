---
name: Gilded Rose unit tests
overview: Replace the placeholder test with behavior-focused pytest characterization tests and separate expected-failing Conjured cases. Item construction remains visible, and related boundary cases use meaningful input/output parameters.
todos:
  - id: baseline
    content: Run the complete existing Python test suite and record its baseline result before editing
    status: completed
  - id: rewrite-test-file
    content: Replace the unittest placeholder with pytest tests that construct Item objects directly
    status: completed
  - id: characterization-tests
    content: Add passing characterization tests for normal items, Aged Brie, Backstage passes, and Sulfuras
    status: pending
  - id: conjured-tests
    content: Add separate Conjured tests for doubled degradation and the quality floor
    status: completed
  - id: final-suite
    content: Run the complete suite and report totals, failing Conjured cases, and absence of other new failures
    status: pending
isProject: false
---

# Gilded Rose unit tests plan

## Scope and constraints

- Use [`GildedRoseRequirements.md`](GildedRoseRequirements.md) as the specification.
- Where its wording is ambiguous, preserve the observed behavior of [`python/gilded_rose.py`](python/gilded_rose.py).
- Modify only [`python/tests/test_gilded_rose.py`](python/tests/test_gilded_rose.py).
- Do not modify production code or [`python/tests/conftest.py`](python/tests/conftest.py).
- Do not use fixtures, factories, or `request.getfixturevalue()`.
- Construct every `Item` directly inside its test so the initial state is visible.
- Keep unrelated item categories in separate behavior-focused tests.

## 1. Record the baseline

Before editing, run the complete Python suite from [`python/`](python/):

```bash
python -m pytest -v
```

Record the total passed, failed, and skipped tests and the identity of any existing failures. If the baseline is not green, retain that evidence so the final comparison distinguishes pre-existing failures from new ones.

## 2. Replace the placeholder test

Remove the starter `unittest.TestCase`, `test_foo`, and `unittest.main()` boilerplate from [`python/tests/test_gilded_rose.py`](python/tests/test_gilded_rose.py). Import `pytest`, `GildedRose`, and `Item`.

Each test will construct its item explicitly:

```python
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
```

## 3. Add passing characterization tests

Organize these tests by behavior. All cases must pass against the current implementation.

### Normal items

- Parameterize ordinary degradation before the sell date and doubled degradation when the date is reached or passed.
- Include the lower boundary to prove quality never becomes negative.
- Parameter sets will expose initial and expected `sell_in` and quality.
- Representative cases: `(10, 20) → (9, 19)`, `(0, 20) → (-1, 18)`, `(-1, 20) → (-2, 18)`, and quality `0 → 0`.

### Aged Brie

- Parameterize quality increase before and after the sell date.
- Parameterize the upper boundary, including quality `49` reaching `50` and quality `50` remaining `50`.
- Assert both resulting `sell_in` and quality.

### Backstage passes

- Parameterize threshold transitions around 10 and 5 days: `11`, `10`, `6`, and `5`.
- Add separate parametrized cases for quality dropping to `0` once the concert has passed.
- Parameterize upper-bound cases so increases at each threshold never exceed `50`.
- Assert both resulting `sell_in` and quality.

### Sulfuras

- Keep focused tests for the legendary item.
- Show that quality remains `80` and `sell_in` is unchanged before, on, and after the sell date.
- Do not combine Sulfuras with another item category.

## 4. Add separate Conjured feature tests

Keep Conjured cases in clearly named tests separate from characterization tests:

- Parameterize doubled degradation before the sell date: quality decreases by `2`.
- Parameterize degradation after the sell date: quality decreases by `4`.
- Parameterize lower-bound inputs to prove quality does not become negative.
- Include initial and expected `sell_in` and quality in each case.

These tests express the new requirement and are expected to expose the missing Conjured behavior. No existing-behavior test should fail.

## 5. Verify the complete suite

After editing, run the same complete-suite command:

```bash
python -m pytest -v
```

Report:

- the recorded baseline result;
- the final number of passing tests;
- every failing Conjured parameter case, with its expected and actual result;
- confirmation that all characterization and pre-existing tests pass, with no non-Conjured regression.

Do not change [`python/gilded_rose.py`](python/gilded_rose.py) to make the Conjured tests pass.
