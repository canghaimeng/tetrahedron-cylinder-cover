#!/usr/bin/env python3
"""Recompute the archived exact certificates using only the standard library.

Run without Python's -O option. This script does not verify the universal
geometric argument; proof status and scope are recorded in result.json.
"""
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def main():
    require(__debug__, "Run without -O: imported exact programs use assertions")
    generator = module("constructor", "code/retuned_secants.py")
    independent = module("power_sums", "checkers/check_retuned.py")
    reviewer = module("reviewer", "checkers/independent_geometry.py")
    saved = json.loads((ROOT / "checkers/retuned_certificate.json").read_text())
    saved_power = json.loads((ROOT / "checkers/power_sum_bounds.json").read_text())
    require(not reviewer.identity_difference(), "Overlap identity is not zero")
    intervals = {}
    for label, e in (("candidate", F(13, 125)), ("baseline", F(1, 10))):
        current = generator.certificate(e, 10000)
        require(current == saved[label], label + ": archived integer certificate differs")
        bounds = independent.bounds(e)
        for endpoint in ("lower", "upper"):
            require(bounds[endpoint] == F(saved_power[label][endpoint]),
                    label + ": archived power-sum certificate differs")
        separate = reviewer.area_bounds(e)
        require(separate["lower_int"] == int(current["lower_integer"]),
                label + ": reviewer lower bound differs")
        require(separate["upper_int"] == int(current["upper_integer"]),
                label + ": reviewer upper bound differs")
        require(bounds["lower"] <= F(current["lower"])
                and F(current["upper"]) <= bounds["upper"],
                label + ": integer enclosure lies outside Taylor enclosure")
        intervals[label] = bounds
    threshold = F("0.499921585997001774")
    require(intervals["candidate"]["upper"] < F(4999213, 10**7)
            < F(4999215, 10**7) < intervals["baseline"]["lower"],
            "Independent strict comparison failed")
    require(intervals["candidate"]["upper"] < threshold, "Frozen target failed")
    eps = F(1, 2000)
    original_lower = F(1, 2) - F(13, 6000) * eps**2 - 2 * eps**4
    original_upper = F(1, 2) - F(13, 6000) * eps**2 + 2 * eps**4
    require(original_lower > F(4999215, 10**7), "Original-instance comparison failed")
    result = {
        "status": "PASS",
        "python": sys.version.split()[0],
        "arithmetic": "integer and rational only",
        "overlap_polynomial_nonzero_coefficients": 0,
        "cells_checked_per_instance": 10000,
        "instances": ["13/125", "1/10"],
        "candidate_upper": saved["candidate"]["upper"],
        "baseline_lower": saved["baseline"]["lower"],
        "comparison": "R_new < 4999213/10^7 < 4999215/10^7 < R_old",
        "openai_displayed_epsilon": str(eps),
        "openai_displayed_cylinder_count": 16000000,
        "openai_displayed_area_lower": str(original_lower),
        "openai_displayed_area_upper": str(original_upper),
        "coverage_method": "universal analytic proof in main.tex; no sampling",
        "proof_status_reference": "result.json; computational checks complement the universal proof"
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
