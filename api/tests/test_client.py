import equity_pb2
import equity_pb2_grpc
import grpc
import pytest


@pytest.fixture
def service_stub():
    channel = grpc.insecure_channel("localhost:50051")
    stub = equity_pb2_grpc.EquityCalculatorServiceStub(channel)
    yield stub
    channel.close()


@pytest.mark.parametrize("hand", ["AhKh", "7h2s", "QdQc", "JhTs"])
def test_calculate_hand_vs_random_equity(service_stub, hand):
    request = equity_pb2.HandVsRandomEquityRequest(hand=hand)
    response = service_stub.CalculateHandVsRandomEquity(request)
    assert 0.0 <= response.equity <= 1.0


@pytest.mark.parametrize(
    "hero_hand,villain_hand",
    [
        ("AhKh", "QdQc"),
        ("7h2s", "AhAd"),
        ("JhTs", "9s8s"),
        ("KsKc", "AhKh"),
    ],
)
def test_calculate_hand_vs_hand_equity(service_stub, hero_hand, villain_hand):
    request = equity_pb2.HandVsHandEquityRequest(
        hero_hand=hero_hand, villain_hand=villain_hand
    )
    response = service_stub.CalculateHandVsHandEquity(request)
    assert 0.0 <= response.equity <= 1.0


@pytest.mark.parametrize(
    "hand,range_str",
    [
        ("AhKh", "AA,KK,QQ"),
        ("7h2s", "22+,A2s+,K2s+"),
        ("QdQc", "AK,AQ"),
        ("JhTs", "88-JJ,ATs+"),
    ],
)
def test_calculate_hand_vs_range_equity(service_stub, hand, range_str):
    request = equity_pb2.HandVsRangeEquityRequest(hand=hand, range=range_str)
    response = service_stub.CalculateHandVsRangeEquity(request)
    assert 0.0 <= response.equity <= 1.0


def test_generate_range_heatmap(service_stub):
    request = equity_pb2.RangeHeatmapRequest()
    response = service_stub.GenerateRangeHeatmap(request)
    assert len(response.hands) == len(response.equities) == 169
    assert all(0.0 <= equity <= 1.0 for equity in response.equities)


@pytest.mark.parametrize("hand", ["AhKh", "7h2s", "QdQc", "JhTs"])
def test_generate_hand_vs_range_heatmap(service_stub, hand):
    request = equity_pb2.HandVsRangeHeatmapRequest(hand=hand)
    response = service_stub.GenerateHandVsRangeHeatmap(request)
    assert len(response.hands) == len(response.equities) == 169
    assert all(0.0 <= equity <= 1.0 for equity in response.equities)
