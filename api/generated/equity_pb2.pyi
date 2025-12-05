from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class HandVsRandomEquityRequest(_message.Message):
    __slots__ = ("hand",)
    HAND_FIELD_NUMBER: _ClassVar[int]
    hand: str
    def __init__(self, hand: _Optional[str] = ...) -> None: ...

class HandVsHandEquityRequest(_message.Message):
    __slots__ = ("hero_hand", "villain_hand")
    HERO_HAND_FIELD_NUMBER: _ClassVar[int]
    VILLAIN_HAND_FIELD_NUMBER: _ClassVar[int]
    hero_hand: str
    villain_hand: str
    def __init__(self, hero_hand: _Optional[str] = ..., villain_hand: _Optional[str] = ...) -> None: ...

class HandVsRangeEquityRequest(_message.Message):
    __slots__ = ("hand", "range")
    HAND_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    hand: str
    range: str
    def __init__(self, hand: _Optional[str] = ..., range: _Optional[str] = ...) -> None: ...

class RangeHeatmapRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HandVsRangeHeatmapRequest(_message.Message):
    __slots__ = ("hand",)
    HAND_FIELD_NUMBER: _ClassVar[int]
    hand: str
    def __init__(self, hand: _Optional[str] = ...) -> None: ...

class SingleEquityResponse(_message.Message):
    __slots__ = ("equity",)
    EQUITY_FIELD_NUMBER: _ClassVar[int]
    equity: float
    def __init__(self, equity: _Optional[float] = ...) -> None: ...

class HeatmapResponse(_message.Message):
    __slots__ = ("hands", "equities")
    HANDS_FIELD_NUMBER: _ClassVar[int]
    EQUITIES_FIELD_NUMBER: _ClassVar[int]
    hands: _containers.RepeatedScalarFieldContainer[str]
    equities: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, hands: _Optional[_Iterable[str]] = ..., equities: _Optional[_Iterable[float]] = ...) -> None: ...
