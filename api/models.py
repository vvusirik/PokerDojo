from pydantic import BaseModel, Field

HandField = Field(..., description="Hand string (e.g., 'AhKh')", examples=["AhKh"])
RangeField = Field(
    ...,
    description="Range string (e.g., 'AA,KK,QQ')",
    examples=["AA", "AJo", "AJs", "AA,KK,QQ", "22+", "33-JJ", "KQ+", "JJ, 0.8(QQ+)"],
)


class HandVsRandomEquityRequest(BaseModel):
    hand: str = HandField


class HandVsHandEquityRequest(BaseModel):
    hero_hand: str = HandField
    villain_hand: str = HandField


class HandVsRangeEquityRequest(BaseModel):
    hand: str = HandField
    range: str = RangeField


class RangeHeatmapRequest(BaseModel):
    pass


class HandVsRangeHeatmapRequest(BaseModel):
    hand: str = HandField


class SingleEquityResponse(BaseModel):
    equity: float = Field(
        ..., description="Calculated equity value between 0.0 and 1.0"
    )


class HeatmapResponse(BaseModel):
    hands: list[str] = Field(..., description="List of hand strings")
    equities: list[float] = Field(..., description="List of equity values")
