"""World and Systems PRD S10: with `want.hold_kind = "bill"` the pitch pack's promise block says the
engine collects the bill at midnight on the due day, so a pitch never puts a scene on the payment.
Nothing in games/ is read or written."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import pitch_pack  # noqa: E402


def test_bill_prints_the_midnight_line(capsys):
    pitch_pack._print_promise({"hold_kind": "bill"})
    out = capsys.readouterr().out
    assert "00:00 on the due day" in out
    assert "beside the payment, never on it" in out


def test_other_holds_print_nothing_about_the_bill(capsys):
    pitch_pack._print_promise({"hold_kind": "ambition"})
    assert "00:00 on the due day" not in capsys.readouterr().out
