import typing


def foo(a: str) -> bytes:
    return True


foo(1)


class MyData(typing.TypedDict):
    a: int
    b: int


def bar(data: MyData) -> MyData:
    return data


bar({"a": 0, "b": 0})  # passes type checks
bar({"bar": 0})  # fails type checks
