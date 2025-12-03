import hypothesis.strategies as st
import pytest
from hypothesis import given

from loopint import LoopList


def test_getitem_wraps_positive_index() -> None:
    lst = LoopList([10, 20, 30])
    assert lst[0] == 10
    assert lst[1] == 20
    assert lst[2] == 30

    assert lst[3] == 10
    assert lst[4] == 20
    assert lst[5] == 30


def test_getitem_wraps_negative_index() -> None:
    lst = LoopList([10, 20, 30])
    assert lst[-1] == 30
    assert lst[-2] == 20
    assert lst[-3] == 10

    assert lst[-4] == 30
    assert lst[-5] == 20
    assert lst[-6] == 10


def test_pop_wraps_index() -> None:
    lst = LoopList([1, 2, 3])
    # 3 -> 0
    assert lst.pop(3) == 1
    assert lst == [2, 3]

    # 4 -> 1
    lst = LoopList([1, 2, 3])
    assert lst.pop(4) == 2


def test_pop_wraps_negative_index() -> None:
    lst = LoopList([1, 2, 3])
    assert lst.pop(-4) == 3


def test_setitem_wraps_index() -> None:
    lst = LoopList([1, 2, 3])
    lst[3] = 10  # 3 % 3 = 0
    assert lst == [10, 2, 3]

    lst[-4] = 99  # (-4) % 3 = 2
    assert lst == [10, 2, 99]


def test_delitem_wraps_index() -> None:
    lst = LoopList([1, 2, 3, 4])
    del lst[4]  # 4 % 4 = 0
    assert lst == [2, 3, 4]

    lst = LoopList([1, 2, 3, 4])
    del lst[-5]  # (-5) % 4 = 3
    assert lst == [1, 2, 3]


def test_getitem_slice_behaves_like_list() -> None:
    base = [1, 2, 3, 4, 5]
    lst = LoopList(base)

    assert list(lst[1:4]) == base[1:4]
    assert list(lst[:]) == base[:]
    assert list(lst[::2]) == base[::2]
    assert list(lst[1:-1]) == base[1:-1]


def test_setitem_slice_behaves_like_list() -> None:
    base = [1, 2, 3, 4, 5]
    lst = LoopList(base)

    lst[1:4] = [10, 20, 30]
    base[1:4] = [10, 20, 30]

    assert list(lst) == base


def test_delitem_slice_behaves_like_list() -> None:
    base = [1, 2, 3, 4, 5]
    lst = LoopList(base)

    del lst[1:4]
    del base[1:4]

    assert list(lst) == base


def test_pop_empty_raises_indexerror_not_zerodivision() -> None:
    lst = LoopList([])  # pyright: ignore[reportUnknownVariableType]
    with pytest.raises(IndexError):
        lst.pop()


def test_getitem_empty_raises_indexerror() -> None:
    lst = LoopList([])  # pyright: ignore[reportUnknownVariableType]
    with pytest.raises(IndexError):
        _ = lst[0]  # pyright: ignore[reportUnknownVariableType]


def test_setitem_empty_raises_indexerror() -> None:
    lst = LoopList([])  # pyright: ignore[reportUnknownVariableType]
    with pytest.raises(IndexError):
        lst[0] = 1


def test_delitem_empty_raises_indexerror() -> None:
    lst = LoopList([])  # pyright: ignore[reportUnknownVariableType]
    with pytest.raises(IndexError):
        del lst[0]


@given(st.lists(st.integers(), min_size=1), st.integers())
def test_getitem_matches_modulo(base: list[int], idx: int) -> None:
    lst = LoopList(base)
    assert lst[idx] == base[idx % len(base)]
