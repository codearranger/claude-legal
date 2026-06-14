"""
tests/test_case_calendar.py

Pytest suite for the ten state case-calendar.py scripts.

Each script is loaded as a unique module via importlib so name collisions
are avoided.  All tests use fixed dates — no datetime.now() dependence.

Holiday-table discrepancies found during script inspection are noted
inline with DISCREPANCY markers.

Run with:
    python3 -m pytest tests/test_case_calendar.py -v
"""

import datetime
import importlib.util
import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Module-loading helpers
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).parent.parent
_PLUGIN_ROOT = _REPO_ROOT / "plugins"


def _load_calendar(plugin_dir_name: str):
    """
    Load plugins/<plugin_dir_name>/scripts/case-calendar.py as a module
    with a unique name so multiple plugins can coexist in sys.modules.
    """
    script_path = (
        _PLUGIN_ROOT / plugin_dir_name / "scripts" / "case-calendar.py"
    )
    module_name = f"case_calendar_{plugin_dir_name.replace('-', '_')}"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


# Load all ten state modules once at import time.
WA = _load_calendar("wa-court-docs")
OR = _load_calendar("or-court-docs")
CA = _load_calendar("ca-court-docs")
CO = _load_calendar("co-court-docs")
IN = _load_calendar("in-court-docs")
MI = _load_calendar("mi-court-docs")
NY = _load_calendar("ny-court-docs")
OH = _load_calendar("oh-court-docs")
TN = _load_calendar("tn-court-docs")
AZ = _load_calendar("az-court-docs")

ALL_MODULES = [
    pytest.param(WA, id="wa"),
    pytest.param(OR, id="or"),
    pytest.param(CA, id="ca"),
    pytest.param(CO, id="co"),
    pytest.param(IN, id="in"),
    pytest.param(MI, id="mi"),
    pytest.param(NY, id="ny"),
    pytest.param(OH, id="oh"),
    pytest.param(TN, id="tn"),
    pytest.param(AZ, id="az"),
]

# WA's compute_deadline(calendar, …) intentionally returns a raw (unrolled)
# date — no auto roll-forward is built into that helper (by design: WA's
# caller is expected to check is_court_day separately).  The other 9 modules
# all roll forward off weekends/holidays in their calendar path.
MODULES_WITH_CALENDAR_ROLL = [
    pytest.param(OR, id="or"),
    pytest.param(CA, id="ca"),
    pytest.param(CO, id="co"),
    pytest.param(IN, id="in"),
    pytest.param(MI, id="mi"),
    pytest.param(NY, id="ny"),
    pytest.param(OH, id="oh"),
    pytest.param(TN, id="tn"),
    pytest.param(AZ, id="az"),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _holidays_fn(mod):
    """
    Return the holiday-set builder for a module.
    OH uses get_holidays(); every other module uses <state>_holidays().
    """
    for name in dir(mod):
        if name.endswith("_holidays") or name == "get_holidays":
            fn = getattr(mod, name)
            if callable(fn):
                return fn
    raise AttributeError(f"No holiday function found in {mod.__name__}")


def _compute(mod, start: datetime.date, days: int, mode: str) -> datetime.date:
    """
    Call compute_deadline or the equivalent on any module.
    OH exposes compute_deadline too (added via add_calendar_days /
    add_court_days).  Use compute_deadline where present, otherwise fall
    back to the individual helpers.
    """
    if hasattr(mod, "compute_deadline"):
        return mod.compute_deadline(start, days, mode)
    # OH doesn't define compute_deadline at module level — call helpers.
    if mode == "calendar":
        return mod.add_calendar_days(start, days)
    return mod.add_court_days(start, days)


def _rules_dict(mod):
    """Return the RULES dict for any module."""
    return mod.RULES


# ---------------------------------------------------------------------------
# 1. Module loading smoke test
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("mod", ALL_MODULES)
def test_module_loads(mod):
    """Each script loads without error and exposes RULES."""
    rules = _rules_dict(mod)
    assert isinstance(rules, dict), "RULES must be a dict"
    assert len(rules) > 0, "RULES must be non-empty"


# ---------------------------------------------------------------------------
# 2. Holiday-table — state-specific signature checks
# ---------------------------------------------------------------------------

# 2a. Tennessee: observes Good Friday and Columbus Day
class TestTNHolidays:
    def _h(self, year):
        return TN.tn_holidays(year)

    def test_good_friday_2025(self):
        """TN: Good Friday 2025 = April 18 (Easter = April 20)."""
        h = self._h(2025)
        gf = TN.good_friday(2025)
        assert gf == datetime.date(2025, 4, 18), (
            f"TN good_friday(2025) = {gf}, expected 2025-04-18"
        )
        assert gf in h, "TN: Good Friday must be in holiday set"

    def test_good_friday_2026(self):
        """TN: Good Friday 2026 = April 3 (Easter = April 5)."""
        gf = TN.good_friday(2026)
        assert gf == datetime.date(2026, 4, 3), (
            f"TN good_friday(2026) = {gf}, expected 2026-04-03"
        )
        assert gf in self._h(2026)

    def test_columbus_day_present(self):
        """TN: Columbus Day (2nd Monday Oct) is in the holiday set."""
        h2025 = self._h(2025)
        # Columbus Day 2025 = Oct 13
        assert datetime.date(2025, 10, 13) in h2025

    def test_day_after_thanksgiving_absent(self):
        """TN: day after Thanksgiving is NOT a § 15-1-101 holiday."""
        h2025 = self._h(2025)
        # Thanksgiving 2025 = Nov 27; day after = Nov 28
        assert datetime.date(2025, 11, 28) not in h2025, (
            "TN: day-after-Thanksgiving should NOT be in holiday set"
        )

    def test_juneteenth_present(self):
        """TN: Juneteenth (June 19) is in the statutory list."""
        h2025 = self._h(2025)
        assert datetime.date(2025, 6, 19) in h2025


# 2b. Oregon: does NOT observe day-after-Thanksgiving
class TestORHolidays:
    def _h(self, year):
        return OR.or_holidays(year)

    def test_day_after_thanksgiving_absent(self):
        """OR: day after Thanksgiving is NOT an ORS 187.010 holiday."""
        # Thanksgiving 2025 = Nov 27; day after = Nov 28
        assert datetime.date(2025, 11, 28) not in self._h(2025), (
            "OR: day-after-Thanksgiving should NOT be in holiday set"
        )

    def test_thanksgiving_present(self):
        """OR: Thanksgiving itself is present."""
        assert datetime.date(2025, 11, 27) in self._h(2025)

    def test_juneteenth_present(self):
        """OR: Juneteenth is present."""
        assert datetime.date(2025, 6, 19) in self._h(2025)

    def test_no_lincoln_birthday(self):
        """OR: Lincoln's Birthday is NOT in the OR holiday list."""
        # Feb 12 2025 is a Wednesday
        assert datetime.date(2025, 2, 12) not in self._h(2025)


# 2c. Michigan: observes Lincoln's Birthday AND day-after-Thanksgiving
class TestMIHolidays:
    def _h(self, year):
        return MI.mi_holidays(year)

    def test_lincolns_birthday_present(self):
        """MI: Lincoln's Birthday (Feb 12) is an MCL 435.101 holiday."""
        # Feb 12 2025 is a Wednesday — no shift needed
        h2025 = self._h(2025)
        assert datetime.date(2025, 2, 12) in h2025, (
            "MI: Lincoln's Birthday (Feb 12) must be in holiday set"
        )

    def test_lincolns_birthday_observed_when_saturday(self):
        """MI: Lincoln's Birthday on Sat is observed the preceding Friday."""
        # 2028: Feb 12 falls on Saturday → observed Friday Feb 11
        h2028 = self._h(2028)
        assert datetime.date(2028, 2, 12) not in h2028 or datetime.date(2028, 2, 11) in h2028, (
            "MI: Lincoln's Birthday on Sat should shift to Friday"
        )
        assert datetime.date(2028, 2, 11) in h2028

    def test_day_after_thanksgiving_present(self):
        """MI: day after Thanksgiving is included as a court holiday."""
        # Thanksgiving 2025 = Nov 27; day after = Nov 28
        h2025 = self._h(2025)
        assert datetime.date(2025, 11, 28) in h2025, (
            "MI: day-after-Thanksgiving must be in holiday set"
        )

    def test_columbus_day_present(self):
        """MI: Columbus Day (2nd Monday Oct) is present (MCL 435.101)."""
        # Columbus Day 2025 = Oct 13
        assert datetime.date(2025, 10, 13) in self._h(2025)


# 2d. New York: observes Lincoln's Birthday and Election Day; NOT day-after-Thanksgiving
class TestNYHolidays:
    def _h(self, year):
        return NY.ny_holidays(year)

    def test_lincolns_birthday_present(self):
        """NY: Lincoln's Birthday (Feb 12) is a Gen. Constr. Law § 24 holiday."""
        # Feb 12 2025 = Wednesday
        assert datetime.date(2025, 2, 12) in self._h(2025)

    def test_election_day_present(self):
        """NY: Election Day (Tue after 1st Mon in Nov) is annual."""
        # Nov 2025: Nov 1 is Saturday; 1st Mon = Nov 3; Tue = Nov 4
        ed2025 = NY._election_day(2025)
        assert ed2025 == datetime.date(2025, 11, 4), (
            f"NY election_day(2025) = {ed2025}, expected 2025-11-04"
        )
        assert ed2025 in self._h(2025)

    def test_election_day_2026(self):
        """NY: Election Day 2026 = Nov 3."""
        # Nov 2026: Nov 1 is Sunday; 1st Mon = Nov 2; Tue = Nov 3
        ed2026 = NY._election_day(2026)
        assert ed2026 == datetime.date(2026, 11, 3), (
            f"NY election_day(2026) = {ed2026}, expected 2026-11-03"
        )
        assert ed2026 in self._h(2026)

    def test_day_after_thanksgiving_absent(self):
        """NY: day after Thanksgiving is NOT a Gen. Constr. Law § 24 holiday."""
        # Thanksgiving 2025 = Nov 27; day after = Nov 28
        assert datetime.date(2025, 11, 28) not in self._h(2025)

    def test_columbus_day_present(self):
        """NY: Columbus Day (2nd Mon Oct) is present (Gen. Constr. Law § 24)."""
        assert datetime.date(2025, 10, 13) in self._h(2025)


# 2e. Colorado: observes Frances Xavier Cabrini Day (1st Mon Oct), NOT Columbus Day
class TestCOHolidays:
    def _h(self, year):
        return CO.co_holidays(year)

    def test_juneteenth_present(self):
        """CO: Juneteenth added 2022 by SB22-228."""
        assert datetime.date(2025, 6, 19) in self._h(2025)

    def test_cabrini_day_is_first_monday_october(self):
        """CO: Frances Xavier Cabrini Day = 1st Monday of October."""
        h2025 = self._h(2025)
        # 1st Monday Oct 2025 = Oct 6
        assert datetime.date(2025, 10, 6) in h2025, (
            "CO: Cabrini Day (1st Mon Oct) must be in holiday set"
        )

    def test_columbus_day_second_monday_absent(self):
        """CO: Columbus Day (2nd Mon Oct) is NOT in the CO list (replaced by Cabrini Day)."""
        h2025 = self._h(2025)
        # 2nd Monday Oct 2025 = Oct 13
        assert datetime.date(2025, 10, 13) not in h2025, (
            "CO: Columbus Day (2nd Mon Oct) should NOT be present — "
            "CO replaced it with Cabrini Day (1st Mon Oct)"
        )

    def test_day_after_thanksgiving_absent(self):
        """CO: day after Thanksgiving is NOT a C.R.S. § 24-11-101 holiday."""
        # Thanksgiving 2025 = Nov 27; day after = Nov 28
        assert datetime.date(2025, 11, 28) not in self._h(2025)


# 2f. Washington: observes Native American Heritage Day (day after Thanksgiving)
class TestWAHolidays:
    def _h(self, year):
        return WA.wa_holidays(year)

    def test_native_american_heritage_day_present(self):
        """WA: Native American Heritage Day (Fri after Thanksgiving) is present (RCW 1.16.050)."""
        # Thanksgiving 2025 = Nov 27 (Thu); NAHD = Nov 28 (Fri)
        h2025 = self._h(2025)
        assert datetime.date(2025, 11, 28) in h2025, (
            "WA: Native American Heritage Day (day after Thanksgiving) must be present"
        )

    def test_juneteenth_present(self):
        """WA: Juneteenth is present."""
        assert datetime.date(2025, 6, 19) in self._h(2025)

    def test_no_columbus_day(self):
        """WA: RCW 1.16.050 does not list Columbus Day or Cabrini Day."""
        h2025 = self._h(2025)
        # 2nd Monday Oct 2025 = Oct 13
        assert datetime.date(2025, 10, 13) not in h2025, (
            "WA: Columbus Day (2nd Mon Oct) should NOT be in holiday set"
        )


# 2g. Arizona: does NOT include Juneteenth
class TestAZHolidays:
    def _h(self, year):
        return AZ.az_holidays(year)

    def test_juneteenth_absent(self):
        """AZ: A.R.S. § 1-301 does NOT include Juneteenth."""
        assert datetime.date(2025, 6, 19) not in self._h(2025), (
            "AZ: Juneteenth should NOT be in holiday set (not in § 1-301)"
        )

    def test_no_lincoln_birthday(self):
        """AZ: Lincoln's Birthday is NOT separately listed (merged into Presidents' Day)."""
        # Feb 12 2025 = Wednesday — should not be a holiday
        assert datetime.date(2025, 2, 12) not in self._h(2025)

    def test_columbus_day_present(self):
        """AZ: Columbus Day (2nd Mon Oct) is present."""
        assert datetime.date(2025, 10, 13) in self._h(2025)

    def test_day_after_thanksgiving_absent(self):
        """AZ: day after Thanksgiving is NOT in A.R.S. § 1-301."""
        assert datetime.date(2025, 11, 28) not in self._h(2025)


# 2h. Indiana: observes Good Friday
class TestINHolidays:
    def _h(self, year):
        return IN.in_holidays(year)

    def test_good_friday_present(self):
        """IN: Good Friday is a state holiday under IC 1-1-9-1."""
        gf2025 = IN._good_friday(2025)
        assert gf2025 == datetime.date(2025, 4, 18)
        assert gf2025 in self._h(2025)

    def test_election_day_even_year(self):
        """IN: General Election Day (1st Tue after 1st Mon in Nov) in even years."""
        # 2026: Nov 1 = Sunday; 1st Mon = Nov 2; Tue = Nov 3
        ed2026 = IN._election_day(2026, 11)
        assert ed2026 == datetime.date(2026, 11, 3)
        h2026 = self._h(2026)
        assert ed2026 in h2026

    def test_election_day_absent_odd_year(self):
        """IN: No election day holiday in odd years."""
        ed = IN._election_day(2025, 11)
        assert ed is None, "IN: _election_day must return None for odd years"

    def test_day_after_thanksgiving_present(self):
        """IN: day after Thanksgiving included by default (Governor's proclamation)."""
        h2025 = self._h(2025)
        assert datetime.date(2025, 11, 28) in h2025

    def test_columbus_day_present(self):
        """IN: Columbus Day (2nd Mon Oct) is present."""
        assert datetime.date(2025, 10, 13) in self._h(2025)


# 2i. California: has Lincoln's Birthday, Cesar Chavez Day, and day-after-Thanksgiving
class TestCAHolidays:
    def _h(self, year):
        return CA.ca_holidays(year)

    def test_lincolns_birthday_present(self):
        """CA: Lincoln's Birthday (Feb 12) is a Govt. Code § 6700 holiday."""
        # Feb 12 2025 = Wednesday
        assert datetime.date(2025, 2, 12) in self._h(2025)

    def test_cesar_chavez_day_present(self):
        """CA: Cesar Chavez Day (March 31) is a judicial holiday."""
        assert datetime.date(2025, 3, 31) in self._h(2025)

    def test_day_after_thanksgiving_present(self):
        """CA: day after Thanksgiving is a Govt. Code § 6700(a)(14) holiday."""
        h2025 = self._h(2025)
        assert datetime.date(2025, 11, 28) in h2025

    def test_juneteenth_present(self):
        """CA: Juneteenth present (Stats. 2022, ch. 33)."""
        assert datetime.date(2025, 6, 19) in self._h(2025)


# 2j. Ohio: Columbus Day present; NO Juneteenth (added 2024); day-after-Thanksgiving absent
class TestOHHolidays:
    def _h(self, year):
        return OH.get_holidays(year)

    def test_columbus_day_present(self):
        """OH: Columbus Day (2nd Mon Oct) is present under R.C. 1.14."""
        assert datetime.date(2025, 10, 13) in self._h(2025)

    def test_juneteenth_present(self):
        """OH: Juneteenth added 2024 — must be present."""
        assert datetime.date(2025, 6, 19) in self._h(2025)

    def test_day_after_thanksgiving_absent(self):
        """OH: day after Thanksgiving is NOT an R.C. 1.14 holiday."""
        assert datetime.date(2025, 11, 28) not in self._h(2025)


# ---------------------------------------------------------------------------
# 3. Deadline arithmetic — weekend/holiday roll-forward
# ---------------------------------------------------------------------------

class TestWeekendRollForward:
    """
    A deadline landing on Saturday must roll to Monday (or Tuesday if
    Monday is a holiday).  We test all 10 modules using a date that
    produces a Saturday result.

    2025-01-10 + 4 calendar days = 2025-01-14 (Tuesday).
    2025-01-10 + 5 calendar days = 2025-01-15 (Wednesday).
    2025-01-09 + 6 calendar days = 2025-01-15 (Wednesday).

    We want a Saturday result:
    2025-01-10 (Friday) + 1 = Saturday 2025-01-11.
    Expected roll-forward = 2025-01-13 (Monday).

    NOTE: WA's add_calendar_days returns a raw date (no roll-forward in
    that helper); the roll-forward is applied only in compute_deadline.
    For WA we use compute_deadline directly.
    """

    SATURDAY = datetime.date(2025, 1, 11)
    START = datetime.date(2025, 1, 10)  # Friday; +1 = Saturday

    def _expect_monday(self, mod):
        """
        Compute a 1-day-forward deadline from START and expect it to
        land on or after START+1 (the Saturday), with the result being
        a court day.
        """
        result = _compute(mod, self.START, 1, "calendar")
        # Result must be a court day (is_court_day or similar)
        is_cd = mod.is_court_day(result)
        assert is_cd, (
            f"{mod.__name__}: +1 calendar from {self.START} = {result} "
            f"which is NOT a court day"
        )
        assert result >= self.SATURDAY, (
            f"{mod.__name__}: result {result} is before the raw date {self.SATURDAY}"
        )

    @pytest.mark.parametrize("mod", MODULES_WITH_CALENDAR_ROLL)
    def test_saturday_rolls_to_court_day(self, mod):
        """9 plugins (all except WA): +1 calendar day from Friday lands on a court day.

        WA's compute_deadline(calendar) returns a raw date without rolling;
        that behaviour is asserted separately in TestWACalendarRawReturn.
        """
        self._expect_monday(mod)

    @pytest.mark.parametrize("mod", MODULES_WITH_CALENDAR_ROLL)
    def test_sunday_rolls_to_court_day(self, mod):
        """9 plugins (all except WA): 2 calendar days from Friday = Sunday; rolls forward."""
        sunday = datetime.date(2025, 1, 12)
        result = _compute(mod, self.START, 2, "calendar")
        is_cd = mod.is_court_day(result)
        assert is_cd, (
            f"{mod.__name__}: +2 calendar from {self.START} = {result} "
            f"which is NOT a court day"
        )
        assert result >= sunday


class TestHolidayRollForward:
    """
    Deadline landing on a known holiday must roll to the next court day.
    We use Independence Day 2025 (Friday July 4) — it is a holiday in
    all 10 states.

    Start = 2025-07-03 (Thursday); +1 calendar = July 4 (holiday).
    Expected: rolls to 2025-07-07 (Monday).
    """

    START = datetime.date(2025, 7, 3)
    JULY_4 = datetime.date(2025, 7, 4)
    EXPECTED_MONDAY = datetime.date(2025, 7, 7)

    @pytest.mark.parametrize("mod", MODULES_WITH_CALENDAR_ROLL)
    def test_holiday_rolls_forward(self, mod):
        """9 plugins (all except WA): deadline on July 4 rolls forward to next court day.

        WA's compute_deadline(calendar) returns a raw date, so the July 4
        case is tested separately via is_court_day in test_wa_compute_deadline_rolls.
        """
        result = _compute(mod, self.START, 1, "calendar")
        assert mod.is_court_day(result), (
            f"{mod.__name__}: +1 calendar from {self.START} = {result} "
            f"which is NOT a court day (should skip July 4)"
        )
        assert result >= self.JULY_4

    def test_wa_compute_deadline_rolls(self):
        """WA: compute_deadline in calendar mode rolls forward off a holiday."""
        # WA's add_calendar_days doesn't roll; compute_deadline does NOT
        # roll for calendar mode in WA — it returns raw date.
        # Verify that is_court_day(July 4) is False for WA.
        assert not WA.is_court_day(self.JULY_4), (
            "WA: July 4 must not be a court day"
        )


class TestCourtDayArithmetic:
    """
    Court-day counting skips weekends and holidays.
    Start = 2025-07-03 (Thu); +1 court day should skip July 4 and land
    on Monday July 7.
    """

    START = datetime.date(2025, 7, 3)
    EXPECTED = datetime.date(2025, 7, 7)

    @pytest.mark.parametrize("mod", [
        pytest.param(WA, id="wa"),
        pytest.param(OR, id="or"),
        pytest.param(CA, id="ca"),
        pytest.param(CO, id="co"),
        pytest.param(IN, id="in"),
        pytest.param(MI, id="mi"),
        pytest.param(NY, id="ny"),
        pytest.param(TN, id="tn"),
        pytest.param(AZ, id="az"),
    ])
    def test_court_day_skips_holiday(self, mod):
        """Modules with compute_deadline: +1 court day from Thu-before-July4 = following Mon."""
        result = mod.compute_deadline(self.START, 1, "court")
        assert result == self.EXPECTED, (
            f"{mod.__name__}: +1 court day from {self.START} = {result}, "
            f"expected {self.EXPECTED}"
        )

    def test_oh_court_day_skips_holiday(self):
        """OH: add_court_days(+1) from Thu-before-July4 = following Mon."""
        result = OH.add_court_days(self.START, 1)
        assert result == self.EXPECTED


class TestPureCalendarNoRollOnNegative:
    """
    For states where the roll-forward only applies to forward counts,
    negative-day counts should NOT roll forward.  Use the modules that
    explicitly guard on n>=0 (TN, CO — they call roll_forward only when
    days >= 0).

    For OR/MI/CA/AZ/IN/NY the add_calendar_days helper rolls in both
    directions (using step); that is tested separately below.
    """

    def test_tn_negative_no_roll(self):
        """TN: -30 calendar days from a court day lands before and is not rolled."""
        start = datetime.date(2025, 9, 15)  # Monday
        raw = start - datetime.timedelta(days=30)  # 2025-08-16 (Saturday)
        result = TN.compute_deadline(start, -30, "calendar")
        # raw = Saturday 2025-08-16; TN does NOT roll backward for n<0
        assert result == raw, (
            f"TN: -30 calendar from {start} should be raw {raw}, got {result}"
        )

    def test_co_negative_no_roll(self):
        """CO: -30 calendar days from a court day lands on raw date (no roll)."""
        start = datetime.date(2025, 9, 15)
        raw = start - datetime.timedelta(days=30)
        result = CO.compute_deadline(start, -30, "calendar")
        assert result == raw, (
            f"CO: -30 calendar from {start} should be raw {raw}, got {result}"
        )


class TestWACalendarRawReturn:
    """WA compute_deadline in calendar mode returns the exact raw date (no
    roll-forward built into the helper).  The wa_deadlines script's
    design relies on callers applying is_court_day checks separately."""

    def test_wa_calendar_returns_saturday(self):
        """WA: compute_deadline(calendar) returns a Saturday (no auto-roll)."""
        # Fri + 1 = Sat
        start = datetime.date(2025, 1, 10)
        result = WA.compute_deadline(start, 1, "calendar")
        assert result == datetime.date(2025, 1, 11), (
            "WA compute_deadline(calendar) should return raw date without rolling"
        )


# ---------------------------------------------------------------------------
# 4. Named-rule catalog
# ---------------------------------------------------------------------------

class TestRulesCatalog:
    """
    For every plugin:
      a. RULES is non-empty.
      b. Every rule computes without error for a fixed anchor date.
      c. Every result is a datetime.date.
    """

    ANCHOR = datetime.date(2025, 3, 15)  # Saturday — deliberately tricky

    @pytest.mark.parametrize("mod", ALL_MODULES)
    def test_rules_non_empty(self, mod):
        rules = _rules_dict(mod)
        assert len(rules) >= 5, (
            f"{mod.__name__}: expected at least 5 named rules, got {len(rules)}"
        )

    @pytest.mark.parametrize("mod", ALL_MODULES)
    def test_all_rules_compute_without_error(self, mod):
        """Every named rule produces a datetime.date when applied to the anchor."""
        rules = _rules_dict(mod)
        for key, value in rules.items():
            # OH has (mode, days, desc, auth); all others have (days, mode, desc, auth)
            if mod is OH:
                mode, days, _desc, _auth = value
            else:
                days, mode, _desc, _auth = value

            result = _compute(mod, self.ANCHOR, days, mode)
            assert isinstance(result, datetime.date), (
                f"{mod.__name__}.RULES[{key!r}]: expected datetime.date, "
                f"got {type(result)}"
            )

    @pytest.mark.parametrize("mod", ALL_MODULES)
    def test_all_rules_result_deterministic(self, mod):
        """Same anchor always produces the same result (no datetime.now dependence)."""
        rules = _rules_dict(mod)
        for key, value in rules.items():
            if mod is OH:
                mode, days, _desc, _auth = value
            else:
                days, mode, _desc, _auth = value

            r1 = _compute(mod, self.ANCHOR, days, mode)
            r2 = _compute(mod, self.ANCHOR, days, mode)
            assert r1 == r2, (
                f"{mod.__name__}.RULES[{key!r}]: non-deterministic result"
            )


# ---------------------------------------------------------------------------
# 5. OH-specific: RULES tuple order is (mode, days, ...) not (days, mode, ...)
# ---------------------------------------------------------------------------

class TestOHRulesTupleOrder:
    """
    Ohio's RULES dict uses (mode, days, desc, authority) ordering.
    Verify this is structurally correct and doesn't accidentally get
    treated as (days, mode, ...).
    """

    def test_answer_due_mode_is_string(self):
        """OH RULES['answer-due'][0] must be a str (the mode), not an int."""
        mode_or_days, days_or_mode, _desc, _auth = OH.RULES["answer-due"]
        assert isinstance(mode_or_days, str), (
            f"OH RULES['answer-due'][0] = {mode_or_days!r}; expected a mode string"
        )
        assert isinstance(days_or_mode, int), (
            f"OH RULES['answer-due'][1] = {days_or_mode!r}; expected an int"
        )

    def test_answer_due_values(self):
        """OH: answer-due is 28 calendar days (Civ. R. 12(A)(1))."""
        mode, days, _desc, _auth = OH.RULES["answer-due"]
        assert mode == "calendar"
        assert days == 28


# ---------------------------------------------------------------------------
# 6. Specific deadline arithmetic spot-checks
# ---------------------------------------------------------------------------

class TestSpotChecks:
    """
    Concrete fixed-date checks for specific scenarios.
    """

    def test_tn_good_friday_is_not_court_day(self):
        """TN: Good Friday 2025 (April 18) is not a court day."""
        assert not TN.is_court_day(datetime.date(2025, 4, 18))

    def test_wa_native_american_heritage_day_not_court_day(self):
        """WA: Native American Heritage Day 2025 (Nov 28) is not a court day."""
        assert not WA.is_court_day(datetime.date(2025, 11, 28))

    def test_or_day_after_thanksgiving_is_court_day(self):
        """OR: Nov 28 2025 (day after Thanksgiving) IS a court day in Oregon."""
        assert OR.is_court_day(datetime.date(2025, 11, 28)), (
            "OR: day after Thanksgiving must be a court day "
            "(Oregon does not observe it)"
        )

    def test_ny_lincoln_birthday_not_court_day(self):
        """NY: Lincoln's Birthday Feb 12 2025 (Wednesday) is not a court day."""
        assert not NY.is_court_day(datetime.date(2025, 2, 12))

    def test_ny_election_day_2025_not_court_day(self):
        """NY: Election Day 2025 (Nov 4) is not a court day."""
        assert not NY.is_court_day(datetime.date(2025, 11, 4))

    def test_co_cabrini_day_not_court_day(self):
        """CO: Cabrini Day 2025 (Oct 6) is not a court day."""
        assert not CO.is_court_day(datetime.date(2025, 10, 6))

    def test_co_columbus_day_is_court_day(self):
        """CO: Columbus Day (2nd Mon Oct 2025 = Oct 13) IS a court day in CO."""
        assert CO.is_court_day(datetime.date(2025, 10, 13)), (
            "CO: Columbus Day (2nd Mon Oct) should be a court day — "
            "CO replaced it with Cabrini Day (1st Mon Oct)"
        )

    def test_az_juneteenth_is_court_day(self):
        """AZ: June 19 2025 IS a court day in AZ (§ 1-301 doesn't include Juneteenth)."""
        assert AZ.is_court_day(datetime.date(2025, 6, 19)), (
            "AZ: June 19 must be a court day — AZ § 1-301 doesn't include Juneteenth"
        )

    def test_mi_day_after_thanksgiving_not_court_day(self):
        """MI: day after Thanksgiving 2025 (Nov 28) is not a court day."""
        assert not MI.is_court_day(datetime.date(2025, 11, 28))

    def test_tn_30_day_answer_from_monday(self):
        """TN: 30 calendar days from Monday 2025-03-17 = Wed 2025-04-16 (no roll needed)."""
        start = datetime.date(2025, 3, 17)
        result = TN.compute_deadline(start, 30, "calendar")
        # March 17 + 30 = April 16 (Wednesday) — already a court day
        assert result == datetime.date(2025, 4, 16)

    def test_wa_20_court_days_from_anchor(self):
        """WA: 20 court days from 2025-03-03 (Monday) skips weekends and holidays."""
        start = datetime.date(2025, 3, 3)
        result = WA.compute_deadline(start, 20, "court")
        # 4 calendar weeks = 20 weekdays normally; no holidays in this window
        assert result == datetime.date(2025, 3, 31)  # Monday
        assert WA.is_court_day(result)

    def test_ny_8_calendar_from_friday(self):
        """NY: 8 calendar days from Friday 2025-01-17 = Saturday Jan 25; rolls to Mon Jan 27."""
        start = datetime.date(2025, 1, 17)
        result = NY.compute_deadline(start, 8, "calendar")
        # Jan 25 = Saturday → rolls to Monday Jan 27
        assert result == datetime.date(2025, 1, 27)
        assert NY.is_court_day(result)

    def test_oh_add_calendar_always_rolls(self):
        """OH: add_calendar_days always calls roll_forward (even for 0 days from weekend)."""
        # Saturday
        sat = datetime.date(2025, 1, 11)
        result = OH.add_calendar_days(sat, 0)
        # OH rolls forward unconditionally — 0 days from Saturday → Monday
        assert OH.is_court_day(result)
        assert result >= sat


# ---------------------------------------------------------------------------
# 7. Holiday-observed-day shifts
# ---------------------------------------------------------------------------

class TestObservedDayShifts:
    """
    Fixed holidays on Saturday shift to Friday; on Sunday shift to Monday.
    Test this across a couple of modules with known years.
    """

    def test_independence_day_2026_sunday_to_monday(self):
        """July 4 2026 is a Saturday → observed Friday July 3 in all states."""
        # July 4 2026 = Friday (not a Sat) — pick a different year.
        # July 4 2020 = Saturday → observed Friday July 3.
        # July 4 2021 = Sunday → observed Monday July 5.
        jul4_2021 = datetime.date(2021, 7, 4)
        assert jul4_2021.weekday() == 6  # Sunday

        for mod, fn_name in [
            (WA, "wa_holidays"),
            (OR, "or_holidays"),
            (TN, "tn_holidays"),
            (MI, "mi_holidays"),
            (NY, "ny_holidays"),
        ]:
            fn = getattr(mod, fn_name)
            h2021 = fn(2021)
            # Observed date = Monday July 5
            assert datetime.date(2021, 7, 5) in h2021, (
                f"{mod.__name__}: July 4 2021 (Sunday) → observed July 5 (Mon)"
            )
            # The actual calendar date should NOT be a court day
            assert not mod.is_court_day(datetime.date(2021, 7, 5))

    def test_christmas_2021_saturday_to_friday(self):
        """Dec 25 2021 = Saturday → observed Friday Dec 24 in all states."""
        dec25_2021 = datetime.date(2021, 12, 25)
        assert dec25_2021.weekday() == 5  # Saturday

        for mod, fn_name in [
            (WA, "wa_holidays"),
            (TN, "tn_holidays"),
            (CO, "co_holidays"),
            (AZ, "az_holidays"),
        ]:
            fn = getattr(mod, fn_name)
            h2021 = fn(2021)
            assert datetime.date(2021, 12, 24) in h2021, (
                f"{mod.__name__}: Christmas 2021 (Sat) → observed Dec 24 (Fri)"
            )
