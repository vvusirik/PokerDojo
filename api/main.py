import logging

import uvicorn
from calculators.equity import (
    hand_vs_hand_equity,
    hand_vs_random_equity_heatmap,
    hand_vs_random_hand_equity,
    hand_vs_range_equity,
    hand_vs_range_equity_heatmap,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import (
    HandVsHandEquityRequest,
    HandVsRandomEquityRequest,
    HandVsRangeEquityRequest,
    HandVsRangeHeatmapRequest,
    HeatmapResponse,
    RangeHeatmapRequest,
    SingleEquityResponse,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Poker Equity Calculator API",
    description="REST API for calculating poker hand equities",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Poker Equity Calculator API"}


@app.post("/api/equity/hand-vs-random", response_model=SingleEquityResponse)
def calculate_hand_vs_random_equity(request: HandVsRandomEquityRequest):
    """Calculate equity of a hand versus a random hand."""
    equity = hand_vs_random_hand_equity(request.hand)
    return SingleEquityResponse(equity=equity)


@app.post("/api/equity/hand-vs-hand", response_model=SingleEquityResponse)
def calculate_hand_vs_hand_equity(request: HandVsHandEquityRequest):
    """Calculate equity of a hand versus another specific hand."""
    equity = hand_vs_hand_equity(request.hero_hand, request.villain_hand)
    return SingleEquityResponse(equity=equity)


@app.post("/api/equity/hand-vs-range", response_model=SingleEquityResponse)
def calculate_hand_vs_range_equity(request: HandVsRangeEquityRequest):
    """Calculate equity of a hand versus a range of hands."""
    equity = hand_vs_range_equity(request.hand, request.range)
    return SingleEquityResponse(equity=equity)


@app.post("/api/equity/range-heatmap", response_model=HeatmapResponse)
def generate_range_heatmap(request: RangeHeatmapRequest = RangeHeatmapRequest()):
    """Generate a heatmap for all possible hands."""
    hands_equity = hand_vs_random_equity_heatmap()
    return HeatmapResponse(
        hands=list(hands_equity.keys()), equities=list(hands_equity.values())
    )


@app.post("/api/equity/hand-vs-range-heatmap", response_model=HeatmapResponse)
def generate_hand_vs_range_heatmap(request: HandVsRangeHeatmapRequest):
    """Generate a heatmap for a specific hand versus all possible hands."""
    hands_equity = hand_vs_range_equity_heatmap(request.hand)
    return HeatmapResponse(
        hands=list(hands_equity.keys()), equities=list(hands_equity.values())
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
