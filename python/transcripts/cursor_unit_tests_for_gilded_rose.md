# Unit tests for Gilded Rose
_Exported on 19/08/2026 at 12:28:29 EEST from Cursor (3.16.29)_

---

**User**

Write unit tests for the @python/gilded_rose.py module. The specification is in @GildedRoseRequirements.md. All the restrictions in the specification should be tested. Unit tests should follow the convention in @python/tests 

---

**Cursor**

I'll read the requirements, implementation, and existing test patterns so we can plan unit tests that cover every spec rule.


Checking how tests are run from the python directory:


**Test framework choice**

> **The existing unit test file uses unittest.TestCase (README: `python -m unittest`), while requirements.txt includes pytest. Which style should the new tests use?**
> - unittest.TestCase in test_gilded_rose.py (match current file and README)
> - pytest-style functions with parametrize in test_gilded_rose.py ✔

I have enough context: the spec rules, the current implementation (including missing Conjured support), and the unittest style in `python/tests/`.


You chose pytest — I'll plan the tests around pytest functions and parametrize.


---

**User**

Implement the plan as specified, it is attached for your reference. Do NOT edit the plan file itself.

To-do's from the plan have already been created. Do not create them again. Mark them as in_progress as you work, starting with the first one. Don't stop until you have completed all the to-dos.

---

**Cursor**

I'll run the baseline test suite first, then implement the pytest tests per the plan.


Installing dependencies, then re-running the baseline.


Baseline recorded: 2 tests, both failing. Implementing the full test file.


Characterization tests pass; only the two conjured degradation cases fail as expected. Running the full suite.


All todos are done. Here is what was implemented.

## Summary

Replaced the placeholder in [`python/tests/test_gilded_rose.py`](python/tests/test_gilded_rose.py) with **25 pytest tests** covering every rule in the spec. Each test builds its own `Item` directly (no helpers, fixtures, or factories).

### Test coverage

| Category | Tests | Cases |
|----------|-------|-------|
| Normal items | `test_normal_item_degrades` | 5 — daily decay, double decay after sell date, quality floor at 0 |
| Aged Brie | `test_aged_brie_increases_in_quality` | 5 — increase before/after sell date, cap at 50 |
| Backstage passes | `test_backstage_passes_increase_in_quality_before_concert` | 6 — thresholds at 11, 10, 6, 5 days, cap at 50 |
| Backstage passes | `test_backstage_passes_drop_to_zero_after_concert` | 2 — quality → 0 after concert |
| Sulfuras | `test_sulfuras_never_changes` | 3 — quality and sell_in unchanged |
| Conjured | `test_conjured_item_degrades_twice_as_fast` | 4 — 2× degradation before/after sell date, quality floor |

### Baseline vs final results

**Baseline** (before edits): 2 tests, **2 failed**
- `test_foo` — placeholder assertion
- `test_gilded_rose_approvals` — missing ApprovalTests reporter config

**Final** (`python -m pytest -v` from `python/`): 26 tests, **23 passed**, **3 failed**

All **21 characterization tests pass**. The only new failures are the **2 Conjured degradation cases** (expected — Conjured is not implemented yet):

| Case | Expected | Actual |
|------|----------|--------|
| `(sell_in=10, quality=20)` | quality **18** | quality **19** |
| `(sell_in=0, quality=20)` | quality **16** | quality **18** |

The other 2 Conjured floor cases pass by coincidence with normal-item behavior.

The pre-existing **`test_gilded_rose_approvals`** failure is unchanged (reporter config, not related to these unit tests).

Run tests with:
```bash
cd python && source .venv/bin/activate && python -m pytest tests/test_gilded_rose.py -v
```

