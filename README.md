# Useful Resources

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Byte manipulation](#byte-manipulation)
  - [Convert hex-encoded string to `bytes`](#convert-hex-encoded-string-to-bytes)
  - [Convert `bytes` back to hex-encoded string](#convert-bytes-back-to-hex-encoded-string)
  - [Inspect each byte within `bytes`](#inspect-each-byte-within-bytes)
  - [Convert array of integers to `bytes`](#convert-array-of-integers-to-bytes)
  - [Convert single integer to bytes and back](#convert-single-integer-to-bytes-and-back)
- [String Manipulation](#string-manipulation)
  - [Convert `bytes` to `str`](#convert-bytes-to-str)
  - [Convert `str` to `bytes`](#convert-str-to-bytes)
  - [Unicode Character Groups](#unicode-character-groups)
- [stdin/stdout/stderr](#stdinstdoutstderr)
  - [Read json from `stdin`](#read-json-from-stdin)
  - [Output json to `stdout` (just use `print`)](#output-json-to-stdout-just-use-print)
  - [Putting everything together (a bit of bash magic below)](#putting-everything-together-a-bit-of-bash-magic-below)
  - [Write to `stderr`](#write-to-stderr)
  - [Force everything to go to `stderr`](#force-everything-to-go-to-stderr)
  - [Get password from `stdin`](#get-password-from-stdin)
- [Iterating](#iterating)
  - [Add item index](#add-item-index)
  - [Combine multiple iterables](#combine-multiple-iterables)
  - [List Comprehensions](#list-comprehensions)
  - [Sorting](#sorting)
  - [Iterators/Generators](#iteratorsgenerators)
- [XOR bytes](#xor-bytes)
  - [XOR Iterators](#xor-iterators)
- [Basic Math](#basic-math)
  - [Modular Arithmetic](#modular-arithmetic)
  - [Exponentiation](#exponentiation)
  - [Modular Exponentiation](#modular-exponentiation)
- [Advanced Math](#advanced-math)
  - [Elliptic Curves](#elliptic-curves)
- [Random](#random)
  - [Generate random number](#generate-random-number)
  - [Generate random `bytes`](#generate-random-bytes)
- [Chunking Data](#chunking-data)
- [Python Features](#python-features)
  - [Inline Functions (lambda)](#inline-functions-lambda)
  - [Type Hints/Annotations](#type-hintsannotations)
  - [TypedDict](#typeddict)
- [CLI](#cli)
  - [Arguments Parsing](#arguments-parsing)
  - [Fail](#fail)
- [File Management](#file-management)
  - [Generate Path In Same Folder](#generate-path-in-same-folder)
  - [Read file](#read-file)
  - [Write file](#write-file)
- [Crypto](#crypto)
  - [CTR Mode](#ctr-mode)
- [Doctests](#doctests)
- [Library Recommendations](#library-recommendations)
- [Debugging](#debugging)
  - [REPL](#repl)
  - [Debugger](#debugger)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

**NOTE**: This document is meant for informational and reference purposes. Any
instructions or guidance given on assignments or tests supersedes any
directives here (although if there are **factual** discrepances across course
materials, please point that out to the TAs or professor so we can reconcile).

## Byte manipulation

### Convert hex-encoded string to `bytes`

- https://docs.python.org/3.10/library/stdtypes.html#bytes.fromhex

```python
>>> bytes.fromhex('00102030405060708090')
b'\x00\x10 0@P`p\x80\x90'

>>> bytes.fromhex('68656c6c6f')
b'hello'
```

### Convert `bytes` back to hex-encoded string

- https://docs.python.org/3.10/library/stdtypes.html#bytes.hex

```python
>>> b'\x00\x10\x20\x30\x40\x50\x60\x70\x80\x90'.hex()
'00102030405060708090'

>>> b'hello'.hex()
'68656c6c6f'
```

### Inspect each byte within `bytes`

- https://docs.python.org/3.10/library/stdtypes.html#bytes

```python
>>> list(b'hello')
[104, 101, 108, 108, 111]

>>> [i for i in b'hello']
[104, 101, 108, 108, 111]
```

### Convert array of integers to `bytes`

- https://docs.python.org/3.10/library/stdtypes.html#bytes

```python
>>> bytes([104, 101, 108, 108, 111])
b'hello'
```

Unless you understand the difference, `bytes` is simpler to use than
`bytearray`. `bytes` is immutable whereas `bytearray` is mutable. We dont need
any performance optimizations `bytearray` provides for these assignments so
`bytes` is sufficient here.

### Convert single integer to bytes and back

We can convert an `int` to a `bytes` using
[`int.to_bytes`](https://docs.python.org/3/library/stdtypes.html#int.to_bytes).
For example, to render the `bytes` prepresenting an integer value of `1` in
unsigned big-endian bytes, you could do the following for `0x00`-padding
lengths of 1, 2, and 8:

```
>>> one = 1
>>> one.to_bytes(length=1, byteorder="big", signed=False)
b'\x01'
>>> one.to_bytes(length=2, byteorder="big", signed=False)
b'\x00\x01'
>>> one.to_bytes(length=8, byteorder="big", signed=False)
b'\x00\x00\x00\x00\x00\x00\x00\x01'
```

Above, `byteorder` refers to
[endianness](https://en.wikipedia.org/wiki/Endianness), and `signed` refers to
[integer
signedness](https://en.wikipedia.org/wiki/Signed_number_representations). A
value of `unsigned` means that the highest-order bit is **not** reserved for
the integer's sign, and that consequently all possible values for the integer
are >= 0.

We can then use
[`int.from_bytes`](https://docs.python.org/3/library/stdtypes.html#int.from_bytes)
to convert the `bytes` back to an `int`, again specifying endianness and
signedness. When we do so and compare the result to our original integer, we
can see that they are equal:

```
>>> one_bytes = one.to_bytes(8, "big")
>>> one == int.from_bytes(one_bytes, byteorder="big", signed=False)
True
>>> one == int.from_bytes(one_bytes, byteorder="big", signed=False), one
(True, 1)
```

## String Manipulation

`bytes` is just a representation of 0s and 1s. They have no text meaning.
In Python `str` represents text which represent text.
Text can be encoded to binary or decoded from binary via different encodings.
Most common encoding is `utf-8`.

Great talk about unicode pain in Python:

- https://www.youtube.com/watch?v=sgHbC6udIqc

### Convert `bytes` to `str`

- https://docs.python.org/3.10/library/stdtypes.html#bytes.decode

```python
>>> b'hello'.decode('utf-8')
'hello'
>>> b'\xd0\xbf\xd1\x80\xd0\xb8\xd0\xb2\xd1\x96\xd1\x82'.decode('utf-8') # hello in Ukranian
'????????????'
```

### Convert `str` to `bytes`

- https://docs.python.org/3.10/library/stdtypes.html#str.encode

```python
>>> 'hello'.encode('utf-8')
b'hello'
>>> '????????????'.encode('utf-8') # hello in Ukranian
b'\xd0\xbf\xd1\x80\xd0\xb8\xd0\xb2\xd1\x96\xd1\x82'
```

### Unicode Character Groups

- https://docs.python.org/3.10/library/unicodedata.html#unicodedata.category
- https://www.unicode.org/L2/L1999/UnicodeData.html

```python
>>> unicodedata.category('??')
'Ll'
```

## stdin/stdout/stderr

### Read json from `stdin`

- https://docs.python.org/3.10/library/json.html#json.load
- https://docs.python.org/3.10/library/sys.html#sys.stdin

```
import json
import sys
data = json.load(sys.stdin)
```

### Output json to `stdout` (just use `print`)

- https://docs.python.org/3.10/library/functions.html#print
- https://docs.python.org/3.10/library/json.html#json.dumps

```
>>> import json
>>> print(json.dumps({"hello": "world"}, indent=4))
{
    "hello": "world"
}
```

### Putting everything together (a bit of bash magic below)

```bash
$ echo '{"hello":"world"}' | python <(cat <<EOF
import json
import sys
input_data = json.load(sys.stdin)
output_data = {"input": input_data}
print(json.dumps(output_data, indent=4))
EOF
)
{
    "input": {
        "hello": "world"
    }
}
```

### Write to `stderr`

- https://docs.python.org/3.10/library/sys.html#sys.stdout
- https://docs.python.org/3.10/library/functions.html#print

```python
>>> import sys
>>> print("printed to stderr", file=sys.stderr)
printed to stderr
```

### Force everything to go to `stderr`

```python
stdout = sys.stdout
stderr = sys.stderr
# force everything to go to stdout by default
sys.stdout = sys.stderr

print("goes to stderr")
print("still goes to stdout", file=stdout)
print("explicit to stderr", file=stderr)
```

### Get password from `stdin`

- https://docs.python.org/3.10/library/getpass.html#getpass.getpass
- https://docs.python.org/3.10/library/io.html#io.IOBase.isatty

```python
def get_password() -> str:
    if sys.stdin.isatty():
        return getpass.getpass("password: ")
    else:
        return sys.stdin.readline().strip()
```

## Iterating

### Add item index

- https://docs.python.org/3.10/library/functions.html#enumerate

```python
>>> list(enumerate([10, 20, 30, 40, 50]))
[(0, 10), (1, 20), (2, 30), (3, 40), (4, 50)]

>>> list(enumerate(b'hello'))
[(0, 104), (1, 101), (2, 108), (3, 108), (4, 111)]
```

### Combine multiple iterables

- https://docs.python.org/3.10/library/functions.html#zip

```python
>>> list(zip([1, 2, 3, 4, 5], [100, 200, 300, 400, 500]))
[(1, 100), (2, 200), (3, 300), (4, 400), (5, 500)]

>>> list(zip(b'hello', b'world'))
[(104, 119), (101, 111), (108, 114), (108, 108), (111, 100)]

>>> list(zip('hello', 'world'))
[('h', 'w'), ('e', 'o'), ('l', 'r'), ('l', 'l'), ('o', 'd')]
```

### List Comprehensions

- https://docs.python.org/3.10/tutorial/datastructures.html#list-comprehensions

```python
>>> [i for i in b'hello']
[104, 101, 108, 108, 111]
>>> [i + b for i, b in enumerate(b'hello')]
[104, 102, 110, 111, 115]
```

### Sorting

- https://docs.python.org/3.10/library/functions.html#sorted

```python
>>> sorted([3, 2, 4, 1, 5])
[1, 2, 3, 4, 5]
>>> sorted([3, 2, 4, 1, 5], reverse=True)
[5, 4, 3, 2, 1]
```

You can sort via a function:

```python
>>> data = ['9f', 'ee', 'e2', 'ef', 'bf', 'f3']
>>> sorted(data)
['9f', 'bf', 'e2', 'ee', 'ef', 'f3']
>>> sorted(data, key=lambda i: i[1])
['e2', 'f3', 'ee', '9f', 'ef', 'bf']
```

### Iterators/Generators

Python support a notion of an iterator and generator objects:

- https://docs.python.org/3.10/library/stdtypes.html#iterator-types
- https://docs.python.org/3.10/library/stdtypes.html#generator-types

Many built-in types are already iterators such as `str`, `bytes`, `list`.
Essentially iterators/generators allow to use an object in loop constructs in
Python by defining how an object is iterated.
In some cases iterators/generators allow to optimize things like memory usage.
Lets reimplement `range` for example:

```python
>>> def naive_range(limit: int) -> typing.List[int]:
  2     output = []
  3     i = 0
  4     while i < limit:
  5         output.append(i)
  6         i += 1
  7     return output
>>> for i in naive_range(5):
  2     print(i)
0
1
2
3
4
```

`naive_range` works however it's inefficient as it has to store all items
in-memory before returning a list. Lets recreate `range` as an iterator:

```python
>>> class RangeIterator:
  2     def __init__(self, limit: int):
  3         self.limit = limit
  4         self.i = 0
  5     def __iter__(self):
  6         return self
  7     def __next__(self):
  8         if self.i < self.limit:
  9             self.i += 1
 10             return self.i - 1
 11         else:
 12             raise StopIteration()
>>> for i in RangeIterator(5):
  2     print(i)
0
1
2
3
4
```

The output is the same however iterator is much more efficient as it returns a
value on each increment without needing to store full range list.

Generators take things a step further by allowing to easily create iterators
with a `yield` statement instead of all the magic methods (`__iter__` and `__next__`):

```python
>>> def range_generator(limit: int):
  2     i = 0
  3     while i < limit:
  4         yield i
  5         i += 1
>>> for i in range_generator(5):
  2     print(i)
0
1
2
3
4
```

This might be useful for things like generating unbound size streams of data
(e.g. keystreams :wink:)

## XOR bytes

- https://docs.python.org/3.10/library/stdtypes.html#numeric-types-int-float-complex
- https://docs.python.org/3.10/library/functools.html#functools.reduce

```python
import functools
def xor(*args: bytes) -> bytes:
    """
    >>> xor(b'hello', b'world')
    b'\x1f\n\x1e\x00\x0b'
    >>> xor(b'hello', b'world', b'hello') # note it has >2 parameters
    b'world'
    >>> xor(xor(b'hello', b'world'), b'hello') # equivalent to above but longer :D
    b'world'
    """
    return bytes(functools.reduce(lambda a, b: a ^ b, i) for i in zip(*args))
```

### XOR Iterators

Here is a similar version but which also supports `xor`ing iterators/generators:

- https://more-itertools.readthedocs.io/en/stable/api.html#more_itertools.flatten
- https://more-itertools.readthedocs.io/en/stable/api.html#more_itertools.collapse

```python
import functools
import more_itertools
def xor(*args: typing.Union[bytes, typing.Iterable[bytes]]) -> bytes:
    """
    >>> xor(b'hello', b'world').hex()
    '1f0a1e000b'
    >>> xor(b'hello', b'world', b'hello') # note it has >2 parameters
    b'world'
    >>> xor(xor(b'hello', b'world'), b'hello') # equivalent to above but longer :D
    b'world'

    >>> xor(b'hello', [b'world']).hex()
    '1f0a1e000b'

    >>> def g(i: bytes):
    ...     while True:
    ...         yield i

    >>> xor(b'hello', g(b'world')).hex()
    '1f0a1e000b'
    >>> xor(b'hellothere', b'worldthere', g(b'hello'))
    b'worldhello'
    """
    return bytes(
        functools.reduce(lambda a, b: a ^ b, i)
        for i in zip(
            *[more_itertools.flatten(more_itertools.collapse(i)) for i in args]
        )
    )
```

## Basic Math

### Modular Arithmetic

- https://en.wikipedia.org/wiki/Modular_arithmetic
- https://docs.python.org/3.10/reference/datamodel.html#object.__mod__
- https://docs.python.org/3.10/library/operator.html#operator.mod

In the example below `9 mod 5` is congruent to `4`, because `4` is the
remainder when `9` is divided by `5`.

```python
>>> 9 % 5
4
>>> [i % 5 for i in range(10)]
[0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
```

### Exponentiation

- https://docs.python.org/3.10/reference/datamodel.html#object.__pow__
- https://docs.python.org/3.10/library/operator.html#operator.pow

In some cases, you [need to be careful how you do
exponentiation](https://stackoverflow.com/a/18965845), but for most purposes,
the standard `**` operator is adequate (particularly when you don't have to
worry about overflow).

```python
>>> 2 ** 3
8
>>> 16 ** .5
4.0
```

You can also use the built-in `pow` function:

```python
>>> pow(2, 3)
8
>>> pow(16, .5)
4.0
```

### Modular Exponentiation

- https://docs.python.org/3/library/functions.html#pow

While it is possible to perform modular exponentiation using the `**` operator,
it is not recommended unless working with small integers:

```python
>>> 2 ** 8 % 3
1
```

The above expression will first perform the full exponentiation before
performing any modulation, which can be very expensive for large exponents. The
built-in `pow` function, on the other hand, takes in a modulus as an optional
third argument, and performs modulation on each round of exponentiation,
keeping the internal working values bounded by the modulus. This makes the
built-in `pow` function _much_ more efficient when working with large
exponents:

```python
>>> from timeit import timeit
>>> timeit(lambda: 2 ** 10000 % 17)
19.87240996499895
>>> timeit(lambda: pow(2, 10000, 17))
0.7652179340075236
```

## Advanced Math

### Elliptic Curves

- https://andrea.corbellini.name/ecc/interactive/modk-mul.html (interactive!)
- https://curves.xargs.org/ (animated!)
- https://en.wikipedia.org/wiki/Elliptic-curve_cryptography#Implementation
- https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
- https://en.wikipedia.org/wiki/Modular_multiplicative_inverse

## Random

### Generate random number

- https://docs.python.org/3.10/library/secrets.html#secrets.randbelow

```python
>>> import secrets
>>> secrets.randbelow(100)
74
```

### Generate random `bytes`

- https://docs.python.org/3.10/library/secrets.html#secrets.token_bytes

```python
>>> secrets.token_bytes(10)
b'\xca\x1ca7\xe6\xf5\xf4Kt\xe8'
```

## Chunking Data

- https://more-itertools.readthedocs.io/en/stable/api.html#more_itertools.chunked

```python
>>> import more_itertools

>>> list(more_itertools.chunked([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 5))
[[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]

>>> list(more_itertools.chunked(b'helloworld', 5))
[[104, 101, 108, 108, 111], [119, 111, 114, 108, 100]]

>>> list(more_itertools.chunked('helloworld', 5))
[['h', 'e', 'l', 'l', 'o'], ['w', 'o', 'r', 'l', 'd']]
```

## Python Features

### Inline Functions (lambda)

```python
>>> double = lambda i: i * 2
>>> double(2)
4
>>> def triple(i):
  2     return i * 3
>>> triple(2)
6
```

`lambda` is especially useful as inline parameter options:

```python
>>> list(filter(lambda i: i > 5, [1, 3, 5, 7, 9]))
[7, 9]
```

### Type Hints/Annotations

- https://peps.python.org/pep-0483/
- https://docs.python.org/3/library/typing.html
- http://mypy-lang.org/
- https://github.com/Microsoft/pyright

Python is not a statically typed language. It is a strongly typed language as
you cannot mix types at runtime:

```python
>>> 'a' + 5
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can only concatenate str (not "int") to str

can only concatenate str (not "int") to str
```

unlike for example javascript:

```js
> 'a' + 5
'a5'
```

However the strong runtime types dont really help with writing code in the editor
as that can only utilise static types. Thats where python type hints come in.
Its a relatively new feature in Python3.5+ which allows to annotate types
for variables, function parameters and function return values.
This allows to statically validate python code.

The basic syntax is:

```python
foo: <type> = <value>
def bar(param: <param type>) -> <return type>:
    ...
```

If the code is type-annotated most IDEs can statically validate it for you
although you might need to install appropriate extensions. You can also
validate types in CLI. For example, given the included
[`sample_types.py`](./sample_types.py), `mypy` will produce:

```bash
mypy types.py
??? mypy sample_types.py
sample_types.py:4: error: Incompatible return value type (got "bool", expected "bytes")
sample_types.py:6: error: Argument 1 to "foo" has incompatible type "int"; expected "str"
sample_types.py:16: error: Extra key "bar" for TypedDict "MyData"
Found 3 errors in 1 file (checked 1 source file)
```

### TypedDict

- https://docs.python.org/3.10/library/typing.html#typing.TypedDict

As of 3.8, python's `typing` module provides the `TypedDict` class, allowing
you to specify the member types and key names of a `dict`. This is useful for
declaring data classes as a distinct type, while still affording the ease of
use of a conventional dict. From the docs:

> TypedDict declares a dictionary type that expects all of its instances to
> have a certain set of keys, where each key is associated with a value of a
> consistent type. This expectation is not checked at runtime but is only
> enforced by type checkers.

Here's how to use it:

```python3
>>> import typing
>>> class MyData(typing.TypedDict):
...     a: int
...     b: int
...
>>> def foo(data: MyData) -> MyData:
...     return data
>>> foo({"a": 0, "b": 0}) # passes type checks
>>> foo({"foo": 0})       # fails type checks
```

## CLI

### Arguments Parsing

- https://docs.python.org/3.10/library/argparse.html#module-argparse
- https://docs.python.org/3.10/library/argparse.html#argparse.ArgumentParser.add_argument
- https://docs.python.org/3.10/library/argparse.html#action
- https://docs.python.org/3.10/library/argparse.html#argparse.ArgumentParser.add_mutually_exclusive_group

### Fail

-https://docs.python.org/3.10/library/sys.html#sys.exit

```python
sys.exit(1)
```

## File Management

- https://docs.python.org/3.10/library/pathlib.html#pathlib.Path
- https://docs.python.org/3.10/library/pathlib.html#pathlib.Path.exists
- https://docs.python.org/3.10/library/pathlib.html#pathlib.PurePath.name

### Generate Path In Same Folder

- https://docs.python.org/3.10/library/pathlib.html#pathlib.PurePath.with_name

```python
>>> pathlib.Path('foo').with_name('bar')
PosixPath('bar')
>>> pathlib.Path('foo').parent / 'bar'
PosixPath('bar')
```

### Read file

- https://docs.python.org/3.10/library/pathlib.html#pathlib.Path.read_bytes

```python
pathlib.Path('filepath').read_bytes()
```

### Write file

- https://docs.python.org/3.10/library/pathlib.html#pathlib.Path.write_bytes

```python
pathlib.Path('filepath').write_bytes(b'hello')
```

## Crypto

### CTR Mode

You can always implement CTR manually. It is a pretty simple cipher mode:

![CTR mode](https://upload.wikimedia.org/wikipedia/commons/3/3f/Ctr_encryption.png)

Or you can have the library do it for you. Only nuanced point about CTR mode
is that different implementations increment the nonce/counter/iv differently.
Some implementations use fixed size of nonce and counter within the IV (like
in screenshot above). For example 12 bytes for nonce and 4 bytes for counter
or both being 8 bytes. Yet other implementations treat the whole IV as a
single nonce/counter and increment it as a 16 byte integer. OpenSSL happens to
implement the approach of the whole nonce being a counter. Call chain:

- [`aes_ctr_cipher`](https://github.com/openssl/openssl/blob/70f39a487d3f7d976a01e0ee7ae98a82ceeea7a0/crypto/evp/e_aes.c#L2620-L2643)
- [`CRYPTO_ctr128_encrypt`](https://github.com/openssl/openssl/blob/1c0eede9827b0962f1d752fa4ab5d436fa039da4/crypto/modes/ctr128.c#L73-L148)
- [`ctr128_inc_aligned`](https://github.com/openssl/openssl/blob/1c0eede9827b0962f1d752fa4ab5d436fa039da4/crypto/modes/ctr128.c#L39-L60)
- [`ctr128_inc`](https://github.com/openssl/openssl/blob/1c0eede9827b0962f1d752fa4ab5d436fa039da4/crypto/modes/ctr128.c#L26-L37)

`ctr128_inc` is defined as:

```c
/* increment counter (128-bit int) by 1 */
static void ctr128_inc(unsigned char *counter)
{
    u32 n = 16, c = 1;

    do {
        --n;
        c += counter[n];
        counter[n] = (u8)c;
        c >>= 8;
    } while (n);
}
```

Looks complicated but it essentially increments 128-bit number and handles
overflow correctly. so `0xffffffffffffffffffffffffffffffff` overflows to
`0x00000000000000000000000000000000`.

Since [cryptography](https://www.pycryptodome.org/en/latest/) is a wrapper
around OpenSSL, if we use it for CTR mode, it automatically increments all of
16 bytes of the nonce for us. Lets prove that:

```python
>>> from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

>>> key = bytes(range(16))

>>> block_one = Cipher(algorithm=algorithms.AES(key), mode=modes.CBC(b"\xff" * 16)).encryptor().update(b"\x00" * 16)
>>> block_two = Cipher(algorithm=algorithms.AES(key), mode=modes.CBC(b"\x00" * 16)).encryptor().update(b"\x00" * 16)
>>> (block_one + block_two).hex()
'3c441f32ce07822364d7a2990e50bb13c6a13b37878f5b826f4f8162a1c8d879'

>>> Cipher(algorithm=algorithms.AES(key), mode=modes.CTR(b"\xff" * 16)).encryptor().update(b"\x00" * 32).hex()
'3c441f32ce07822364d7a2990e50bb13c6a13b37878f5b826f4f8162a1c8d879'
```

## Doctests

- https://docs.python.org/3.10/library/doctest.html#module-doctest
- https://docs.python.org/3.10/tutorial/controlflow.html#documentation-strings
- https://docs.pytest.org/en/stable/how-to/doctest.html

A really useful testing feature in Python are doctests which allow to include
tests in module/function doc strings.
(Some of the above examples actually already use doctests such as `xor`:D).
Adding tests directly in doc-string allows to use the code documentation as
both the documentation of example usage as well as runnable tests.
This is especially useful for utility functions which can themselves check
their correctness.

The way doctests work is they use Python docstrings. Any string after function
definition is considered a docstring in python. For example:

```python
>>> def foo():
  2     "docstring here"
>>> foo.__doc__
'docstring here'

>>> def bar(): pass
>>> bar.__doc__ # no output here

>>> def baz():
  2     pass
  3     "not a docsting as its not first statement inside function"
>>> baz.__doc__ # no output here
```

Python allows to have multiline strings with `"""` notation so usually docstrings
are defined using that:

```python
>>> def foo():
  2     """
  3     function description here
  4     which spans multiple lines
  5     """
>>> print(foo.__doc__)

    function description here
    which spans multiple lines

```

What doctest does is it finds all lines in docstring which start with `>>>`,
executes that code. For multiline statements subsequent lines need to start
with `...`. For example:

```python
>>> def foo():
  2     """
  3     >>> foo(
  4     ... )
  5     """
```

It then compares the output the code produced to the lines in docstring.
Note it matches things as strings, not Python values.
[`./doctests.py`](./doctests.py) has a few doctest examples.
To run tests you can use python itself:

```python
??? python -m doctest doctests.py
**********************************************************************
File "doctests.py", line 11, in doctests.bar
Failed example:
    bar()
Expected:
    'world'
Got:
    'hello'
**********************************************************************
File "doctests.py", line 19, in doctests.baz
Failed example:
    baz()
Expected nothing
Got:
    'hello'
**********************************************************************
2 items had failures:
   1 of   1 in doctests.bar
   1 of   1 in doctests.baz
***Test Failed*** 2 failures.
```

A better way to run doctests though is using `pytest`. It provides much more
useful error messages and has pretty colors :D:

```bash
??? pytest --doctest-modules --no-header --verbose doctests.py
==================== test session starts =====================
collected 3 items

doctests.py::doctests.bar FAILED                       [ 33%]
doctests.py::doctests.baz FAILED                       [ 66%]
doctests.py::doctests.foo PASSED                       [100%]

========================== FAILURES ==========================
___________________ [doctest] doctests.bar ___________________
010
011     >>> bar()
Expected:
    'world'
Got:
    'hello'

doctests.py:11: DocTestFailure
___________________ [doctest] doctests.baz ___________________
018
019     >>> baz()
Expected nothing
Got:
    'hello'

doctests.py:19: DocTestFailure
================== short test summary info ===================
FAILED doctests.py::doctests.bar
FAILED doctests.py::doctests.baz
================ 2 failed, 1 passed in 0.02s =================
```

## Library Recommendations

Crypto:

- https://docs.python.org/3.10/library/hashlib.html#module-hashlib
- https://docs.python.org/3.10/library/hmac.html#module-hmac
- https://cryptography.io/en/latest/
- https://www.pycryptodome.org/en/latest/

Regex:

- https://docs.python.org/3.10/library/re.html#module-re
- https://pypi.org/project/regex/ - unicode-friendly `re` clone

Wish was stdlib:

- https://more-itertools.readthedocs.io/en/stable/index.html - extended `itertools`

Useful stdlib:

- https://docs.python.org/3.10/library/functions.html
- https://docs.python.org/3.10/library/pathlib.html#module-pathlib
- https://docs.python.org/3.10/library/functools.html#module-functools
- https://docs.python.org/3.10/library/itertools.html#module-itertools
- https://docs.python.org/3.10/library/collections.html#module-collections
- https://docs.python.org/3.10/library/dataclasses.html#module-dataclasses

Testing:

- https://docs.pytest.org/en/stable/contents.html

## Debugging

### REPL

Much better REPL shell compared to standard REPL:

- https://github.com/prompt-toolkit/ptpython

![ptpython](https://github.com/jonathanslenders/ptpython/raw/master/docs/images/example1.png)

### Debugger

Much better `pdb` debugger. Highly recommend. If you try it, definitely check
the `sticky` mode.

- https://github.com/pdbpp/pdbpp

![pdbpp](https://user-images.githubusercontent.com/412005/64484794-2f373380-d20f-11e9-9f04-e1dabf113c6f.png)
