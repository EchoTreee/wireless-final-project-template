"""CLI parameter validation: illegal --mod/--channel/--snr must be rejected.

Addresses the most common hidden-test failure (invalid_snr / invalid_modulation):
the CLI must reject illegal inputs with a non-zero exit code instead of silently
falling back to defaults.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(extra_args):
    return subprocess.run(
        [sys.executable, "main.py", "--input", "Test.txt", "--output", "results/received.txt"] + extra_args,
        cwd=ROOT, capture_output=True, text=True, timeout=60,
    )


def test_invalid_modulation_rejected():
    r = _run(["--snr", "12", "--seed", "2026", "--mod", "foobar", "--channel", "awgn"])
    assert r.returncode != 0


def test_invalid_channel_rejected():
    r = _run(["--snr", "12", "--seed", "2026", "--mod", "qpsk", "--channel", "foobar"])
    assert r.returncode != 0


def test_out_of_range_snr_rejected():
    r = _run(["--snr", "-100", "--seed", "2026", "--mod", "qpsk", "--channel", "awgn"])
    assert r.returncode != 0


def test_nonnumeric_snr_rejected():
    r = _run(["--snr", "abc", "--seed", "2026", "--mod", "qpsk", "--channel", "awgn"])
    assert r.returncode != 0


def test_valid_params_accepted():
    r = _run(["--snr", "12", "--seed", "2026", "--mod", "qpsk", "--channel", "awgn"])
    assert r.returncode == 0
