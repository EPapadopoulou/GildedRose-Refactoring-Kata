# New name-selection tests
_Exported on 19/08/2026 at 13:59:28 EEST from Cursor (3.16.29)_

---

**User**

Add tests for the new name-selection logic. @python/gilded_rose.py:70 

---

**Cursor**

I'll read the implementation and existing Python tests so we can add coverage for the Conjured name-selection logic.


Existing tests cover `"Conjured Mana Cake"` behavior; I'll add direct tests for `update_strategy_for` to cover exact `"Conjured"`, prefixed names, and false positives like `"Conjuredness"`.


Added 10 tests in `python/tests/test_gilded_rose.py` for the name-selection logic in `update_strategy_for()`.

**Strategy selection tests** — verify which strategy is chosen:
- **Matches Conjured:** `"Conjured"`, `"Conjured Mana Cake"`, `"Conjured Widget"`
- **Does not match:** `"Conjuredness"`, `"UnConjured"`, `"conjured"`, `"ConjuredMana Cake"`, normal items

**Behavior tests** — confirm the choice affects degradation:
- `"Conjured"` → quality 20 → 18 (2× degradation)
- `"Conjuredness"` → quality 20 → 19 (normal degradation)

All 35 unit tests pass.

---

**User**

adding 10 extra test cases for such a small change is an overkill. the existing Conjured test already proves that "Conjured Mana Cake" follows the prefix rule. So we only need two cases: exact "Conjured" behaves as Conjured and "Conjuredness" remains a normal item. 
Also, "conjured" tests case sensitivity that I never mentioned 

---

**Cursor**

I'll trim the Conjured name-matching tests down to the two cases you asked for.


Removing the strategy-selection tests and extra imports; keeping only the two behavioral cases.


Fair point. I trimmed it down to one parametrized test with two cases:

- `"Conjured"` → quality 18 (Conjured degradation)
- `"Conjuredness"` → quality 19 (normal degradation)

The prefix rule stays covered by the existing `"Conjured Mana Cake"` tests. All 27 tests pass.

