from __future__ import annotations

from copy import copy

from hypothesis import given
from hypothesis import strategies as st

from loopint import LoopInt

type LoopParams = tuple[int, int, int]


def loop_params() -> st.SearchStrategy[LoopParams]:
    left = st.integers(min_value=-1000, max_value=1000)
    span = st.integers(min_value=1, max_value=1000)
    current = st.integers(min_value=-10_000, max_value=10_000)

    def _builder(current: int, left: int, span: int) -> LoopParams:
        return (current, left, left + span)

    return st.builds(_builder, current, left, span)


@given(loop_params())
def test_value_always_in_range(params: LoopParams) -> None:
    current, left, right = params
    loop = LoopInt(current, left=left, right=right)

    value = int(loop)
    assert left <= value < right


@given(loop_params(), st.integers(min_value=-10_000, max_value=10_000))
def test_iadd_isub_roundtrip(params: LoopParams, step: int) -> None:
    current, left, right = params
    loop = LoopInt(current, left=left, right=right)

    original_value = int(loop)

    loop += step
    loop -= step

    assert int(loop) == original_value


@given(loop_params(), st.integers(min_value=-10_000, max_value=10_000))
def test_add_corresponds_to_modular_arithmetic(params: LoopParams, step: int) -> None:
    current, left, right = params
    loop = LoopInt(current, right=right, left=left)

    span = loop.span
    value = int(loop)

    expected = left + ((value + step) - left) % span
    result = loop + step

    assert isinstance(result, LoopInt)
    assert int(result) == expected


@given(loop_params())
def test_equality_with_int_is_consistent(params: LoopParams) -> None:
    current, left, right = params
    loop = LoopInt(current, right=right, left=left)

    value = int(loop)

    assert loop == value
    assert value == loop


@given(loop_params())
def test_hash_is_consistent_with_int(params: LoopParams) -> None:
    current, left, right = params
    loop = LoopInt(current, right=right, left=left)

    value = int(loop)

    assert hash(loop) == hash(value)


@given(loop_params())
def test_copy_preserves_invariants(params: LoopParams) -> None:
    current, left, right = params
    loop = LoopInt(current, right=right, left=left)
    clone = copy(loop)

    assert isinstance(clone, LoopInt)
    assert clone is not loop
    assert int(clone) == int(loop)
    assert clone.left == loop.left
    assert clone.right == loop.right
    assert clone.span == loop.span

    original_value = int(loop)

    clone += 1

    assert int(loop) == original_value
