"""2026-11-03: `a place is not a catalogue` counts each button label once. A label written several times with
different conditions (first_term's dinner screen had 21 'Done.' variants) shows one at a time, so it is one
decision to the player."""
import importlib.util, pathlib

_spec = importlib.util.spec_from_file_location(
    "gates", pathlib.Path(__file__).resolve().parents[1] / "gates.py")
gates = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gates)


def _dedupe(choices):
    # the same expression the gate uses
    return list({str(ch.get("text") or ""): ch for ch in choices}.values())


def test_variants_of_one_label_count_once():
    choices = [{"text": "Done.", "targetType": "node", "conditions": {"items": [i]}} for i in range(21)]
    assert len(_dedupe(choices)) == 1


def test_different_labels_still_count():
    choices = [{"text": f"Act {i}.", "targetType": "node"} for i in range(9)]
    assert len(_dedupe(choices)) == 9


def test_the_gate_source_dedupes_by_label():
    src = (pathlib.Path(__file__).resolve().parents[1] / "gates.py").read_text()
    assert 'decisions = list({str(ch.get("text") or ""): ch for ch in decisions}.values())' in src
