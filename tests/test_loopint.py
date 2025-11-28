from __future__ import annotations

from copy import copy

import pytest

from loopint import LoopInt


def test_basic_init_and_value() -> None:
    loop = LoopInt(0, right=5)
    assert int(loop) == 0
    assert loop.value == 0
    assert loop.left == 0
    assert loop.right == 5
    assert loop.span == 5


def test_init_with_left_offset() -> None:
    loop = LoopInt(0, right=2, left=-1)
    # [left; right) = [-1; 2), span = 3, internal value 0
    assert loop.left == -1
    assert loop.right == 2
    assert loop.span == 3
    assert int(loop) == 0
    assert loop.value == 0


def test_span_validation_error() -> None:
    with pytest.raises(ValueError, match="Left border must be less than right border"):
        _ = LoopInt(0, right=0)

    with pytest.raises(ValueError, match="Left border must be less than right border"):
        _ = LoopInt(0, right=-1)

    with pytest.raises(ValueError, match="Left border must be less than right border"):
        _ = LoopInt(0, right=1, left=1)  # span == 0


def test_wrap_around_positive() -> None:
    loop = LoopInt(0, right=3)
    loop += 1
    assert int(loop) == 1
    loop += 2  # 1 + 2 = 3 -> 0 (mod 3)
    assert int(loop) == 0
    loop += 5  # 0 + 5 = 5 -> 2 (mod 3)
    assert int(loop) == 2


def test_wrap_around_negative() -> None:
    loop = LoopInt(0, right=4)
    loop -= 1  # 0 - 1 = -1 -> 3 (mod 4)
    assert int(loop) == 3
    loop -= 5  # 3 - 5 = -2 -> 2 (mod 4)
    assert int(loop) == 2


def test_add_returns_new_instance_and_does_not_mutate_original() -> None:
    loop = LoopInt(0, right=5)
    other = loop + 3
    assert isinstance(other, LoopInt)
    assert other is not loop
    assert int(loop) == 0
    assert int(other) == 3


def test_sub_returns_new_instance_and_does_not_mutate_original() -> None:
    loop = LoopInt(0, right=5)
    other = loop - 1
    assert isinstance(other, LoopInt)
    assert other is not loop
    assert int(loop) == 0
    # 0 - 1 = -1 -> 4 (mod 5)
    assert int(other) == 4


def test_iadd_isub_reject_loopint_argument() -> None:
    loop = LoopInt(0, right=5)
    other = LoopInt(1, right=5)

    with pytest.raises(TypeError):
        loop += other

    with pytest.raises(TypeError):
        loop -= other


def test_equality_with_int_and_other_loopint() -> None:
    a = LoopInt(0, right=2, left=-1)
    b = LoopInt(0, right=3, left=-2)
    c = LoopInt(1, right=3, left=-2)

    assert int(a) == 0
    assert int(b) == 0
    assert int(c) == 1

    assert a == b
    assert a == 0
    assert b == 0
    assert c != a
    assert c != 0

    assert (a == "0") is False


def test_hash_compatible_with_int_and_sets() -> None:
    loop = LoopInt(0, right=10)

    assert hash(loop) == hash(0)

    s = {loop}
    assert 0 in s
    assert LoopInt(0, right=5) in s
    assert 1 not in s


def test_index_protocol_works_in_sequences() -> None:
    data = ["zero", "one", "two"]
    idx = LoopInt(1, right=3)
    assert data[idx] == "one"

    idx2 = LoopInt(-1, right=3)  # -1 -> 2 (mod 3)
    assert data[idx2] == "two"


def test_format_and_to_string() -> None:
    loop = LoopInt(7, right=10)
    assert format(loop, "03d") == "007"
    assert loop.to_string() == "7"
    assert f"{loop:>4}" == "   7"


def test_repr_contains_key_information() -> None:
    loop = LoopInt(0, right=5)
    text = repr(loop)
    assert "LoopInt" in text
    assert "current_number=0" in text
    assert "left_border=0" in text
    assert "right_border=5" in text


def test_copy_creates_independent_instance() -> None:
    loop = LoopInt(0, right=5, left=-1)
    clone = copy(loop)

    assert isinstance(clone, LoopInt)
    assert clone is not loop
    assert int(clone) == int(loop)
    assert clone.left == loop.left
    assert clone.right == loop.right
    assert clone.span == loop.span

    clone += 1
    assert int(clone) != int(loop)


def test_left_right_with_non_zero_offset() -> None:
    loop = LoopInt(-1, right=2, left=-1)
    # [-1; 2), span = 3; current_number = -1 - (-1) = 0
    assert loop.left == -1
    assert loop.right == 2
    assert loop.span == 3
    assert int(loop) == -1

    loop += 1  # -1 + 1 = 0
    assert int(loop) == 0

    loop += 3  # 0 + 3 = 3 -> 0 (mod 3)
    assert int(loop) == 0


def test_radd_int_plus_loopint() -> None:
    """Check that int + LoopInt uses __radd__ and wraps correctly."""
    x = LoopInt(2, right=5)  # visible = 2
    result = 3 + x  # 3 + 2 = 5 → 0 mod 5
    assert isinstance(result, LoopInt)
    assert int(result) == 0

    assert int(0 + x) == 2
    assert int(-1 + x) == 1
    assert int(10 + x) == 2  # 10 + 2 = 12 → 12 mod 5 = 2


def test_rsub_int_minus_loopint() -> None:
    """Check that int - LoopInt uses __rsub__ and computes modular difference."""
    x = LoopInt(1, right=5)  # visible = 1

    result = 3 - x  # 3 - 1 = 2
    assert isinstance(result, LoopInt)
    assert int(result) == 2

    assert int(0 - x) == 4  # 0 - 1 = -1 → 4 mod 5
    assert int(-2 - x) == 2  # -2 - 1 = -3 → 2 mod 5
    assert int(10 - x) == 4  # 10 - 1 = 9 → 4 mod 5
