# LoopInt

<!-- Badges -->
<p align="center">
    <a href="https://pypi.org/project/loopint/"><img src="https://img.shields.io/pypi/v/loopint" alt="PyPI version"></a>
    <a href="https://pypi.org/project/loopint/"><img src="https://img.shields.io/pypi/pyversions/loopint" alt="Python versions"></a>
    <a href="https://github.com/DasKaroWow/loopint/actions"><img src="https://img.shields.io/github/actions/workflow/status/DasKaroWow/loopint/ci.yml" alt="Tests"></a>
    <a href="https://github.com/DasKaroWow/loopint"><img src="https://img.shields.io/github/license/DasKaroWow/loopint" alt="License"></a>
    <a href="#"><img src="https://img.shields.io/badge/type--hints-100%25-blue" alt="Typing"></a>
    <a href="https://pypistats.org/packages/loopint"><img src="https://img.shields.io/pypi/dm/loopint" alt="Downloads"></a>
    <a href="#"><img src="https://img.shields.io/badge/ruff-linter%2Bformatter-blue" alt="Ruff Linter & Formatter"></a>
    <a href="#"><img src="https://img.shields.io/badge/basedpyright-typechecker-orange" alt="basedpyright"></a>
</p>

**LoopInt** is a lightweight Python library that provides a cyclic integer type
with precise range semantics **[left; right)** and natural integer-like behavior.

It behaves like a regular integer but wraps around within a fixed interval.
This makes it useful for cyclic counters, circular buffers, modular arithmetic,
clock-like values, and more.

---

## 🔧 Features

- Fixed interval semantics: **[left; right)**
- Modular wrap-around on `+`, `-`, `+=`, `-=`
- Behaves like `int` in:
  - comparisons
  - hashing
  - indexing (`__index__`)
  - formatting (`__format__`)
  - `int()` conversion
- Safe arithmetic:
  - `LoopInt + int` supported
  - `LoopInt += int` supported
  - Adding two `LoopInt` objects is intentionally forbidden
- Fully typed (Python ≥ 3.12)

---

## 📦 Installation

```bash
pip install loopint
```

Or with **uv**:

```bash
uv add loopint
```

---

## 🚀 Usage

```python
from loopint import LoopInt

x = LoopInt(0, right=5)

print(int(x))      # 0

x += 7
print(int(x))      # 2   (wrap-around: 7 % 5 == 2)

y = x + 10
print(int(y))      # 2   (non-mutating)

assert x == 2
assert y == x
```

### Custom range

```python
x = LoopInt(0, right=2, left=-1)
print(int(x))  # 0

x += 1
print(int(x))  # 1

x += 2         # wraps in [-1; 2)
print(int(x))  # 0
```

---

## 📚 API Overview

### `LoopInt(current, /, right, *, left=0)`
Create a cyclic integer constrained to the interval **[left; right)** with modular wrap-around.

**Parameters:**
- `current` — initial value (any integer-like object supporting `__index__`)
- `right` — exclusive upper bound  
- `left` — inclusive lower bound (default: `0`)

**Interval semantics:**  
```
value ∈ [left; right)
span = right − left
value = left + ((current − left) mod span)
```

---

## 🔹 Properties

### `value: int`
Returns the **visible integer value** of the `LoopInt` instance.

Equivalent to:

```python
int(loopint_instance)
```

Example:

```python
x = LoopInt(5, right=8, left=2)
assert x.value == 5
```

---

### `left: int`
Returns the **inclusive lower bound** of the interval.

Example:

```python
LoopInt(0, right=5, left=-2).left  # → -2
```

---

### `right: int`
Returns the **exclusive upper bound** of the interval.

Example:

```python
LoopInt(0, right=5).right  # → 5
```

---

### `span: int`
Size of the interval:

```
span = right - left
```

Example:

```python
LoopInt(0, right=5, left=2).span  # → 3
```

---

## 🔹 Methods

### `to_string() -> str`
Return the value as a string.
Equivalent to:

```python
str(int(self))
```

Example:

```python
x = LoopInt(4, right=10)
x.to_string()   # → "4"
```

---

### Arithmetic

#### `__add__(other) -> LoopInt`
Non-mutating addition with wrap-around.

```python
x + n  # returns a new LoopInt
```

---

#### `__iadd__(other) -> Self`
In-place addition (`+=`) with wrap-around.

```python
x += 3
```

---

#### `__sub__(other) -> LoopInt`
Non-mutating subtraction.

---

#### `__isub__(other) -> Self`
In-place subtraction (`-=`).

#### `__neg__() -> LoopInt`
Modular negation:

```
int(-x) == (-int(x)) mod span
```

Example:

```python
x = LoopInt(1, right=5)
y = -x      # → 4
```

#### `__radd__(other) -> LoopInt`
Enables: `int + LoopInt`.

Example:

```python
3 + LoopInt(2, right=5)  # → 0
```

#### `__rsub__(other) -> LoopInt`
Implements: `other - self` using modular arithmetic.

```
other - x == -(x - other)
```

Example:

```python
3 - LoopInt(1, right=5)   # → 2
0 - LoopInt(1, right=5)   # → 4
```


---

### Comparison & hashing

#### `__eq__(other)`
LoopInt compares equal to anything whose integer value equals `int(self)`.

Examples:

```python
LoopInt(0, right=5) == 0            # True
LoopInt(3, right=10) == LoopInt(3, right=100)  # True
```

---

#### `__hash__() -> int`
Hash is consistent with `int(self)`:

```python
hash(LoopInt(3, right=10)) == hash(3)
```

---

## 🧪 Testing

```bash
pytest .
```

Both unit tests and property-based tests (Hypothesis) are included.

---

## 📄 License

MIT License.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or pull requests.
