import logging
from concurrent.futures import ThreadPoolExecutor

import equity_pb2
import equity_pb2_grpc
import grpc
from utils.equity import (
    hand_vs_hand_equity,
    hand_vs_random_equity_heatmap,
    hand_vs_random_hand_equity,
    hand_vs_range_equity,
    hand_vs_range_equity_heatmap,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class EquityCalculatorServicer(equity_pb2_grpc.EquityCalculatorServiceServicer):
    """Implementation of the EquityCalculatorService gRPC service."""

    def CalculateHandVsRandomEquity(
        self, request: equity_pb2.HandVsRandomEquityRequest, context
    ):
        """Calculate equity of a hand versus a random hand.

        Args:
            request: HandVsRandomEquityRequest containing the hand
            context: gRPC context

        Returns:
            SingleEquityResponse with calculated equity
        """
        return equity_pb2.SingleEquityResponse(
            equity=hand_vs_random_hand_equity(request.hand)
        )

    def CalculateHandVsHandEquity(self, request, context):
        """Calculate equity of a hand versus another specific hand.

        Args:
            request: HandVsHandEquityRequest containing hero_hand and villain_hand
            context: gRPC context

        Returns:
            SingleEquityResponse with calculated equity
        """
        return equity_pb2.SingleEquityResponse(
            equity=hand_vs_hand_equity(request.hero_hand, request.villain_hand)
        )

    def CalculateHandVsRangeEquity(self, request, context):
        """Calculate equity of a hand versus a range of hands.

        Args:
            request: HandVsRangeEquityRequest containing hand and range
            context: gRPC context

        Returns:
            SingleEquityResponse with calculated equity
        """
        return equity_pb2.SingleEquityResponse(
            equity=hand_vs_range_equity(request.hand, request.range)
        )

    def GenerateRangeHeatmap(self, request, context):
        """Generate a heatmap for all possible hands.

        Args:
            request: RangeHeatmapRequest (empty)
            context: gRPC context

        Returns:
            HeatmapResponse with hands and their equities
        """
        hands_equity = hand_vs_random_equity_heatmap()
        return equity_pb2.HeatmapResponse(
            hands=list(hands_equity.keys()), equities=list(hands_equity.values())
        )

    def GenerateHandVsRangeHeatmap(self, request, context):
        """Generate a heatmap for a specific hand versus all possible hands.

        Args:
            request: HandVsRangeHeatmapRequest containing the hand
            context: gRPC context

        Returns:
            HeatmapResponse with hands and their equities
        """
        hands_equity = hand_vs_range_equity_heatmap(request.hand)
        return equity_pb2.HeatmapResponse(
            hands=list(hands_equity.keys()), equities=list(hands_equity.values())
        )


def serve(port=50051):
    """Start the gRPC server.

    Args:
        port: Port number to listen on (default: 50051)
    """
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    equity_pb2_grpc.add_EquityCalculatorServiceServicer_to_server(
        EquityCalculatorServicer(), server
    )
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info(f"Server started on port {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
