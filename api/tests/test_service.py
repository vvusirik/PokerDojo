import pytest
import requests
from testcontainers.core.container import DockerContainer
from testcontainers.core.wait_strategies import HttpWaitStrategy


@pytest.fixture(scope="module")
def api_container():
    container = (
        DockerContainer("poker-dojo-api:latest")
        .with_exposed_ports(8000)
        .waiting_for(HttpWaitStrategy(path="/", port=8000).for_status_code(200))
    )
    container.start()
    yield container
    container.stop()


@pytest.fixture(scope="module")
def api_url(api_container):
    host = api_container.get_container_host_ip()
    port = api_container.get_exposed_port(8000)
    return f"http://{host}:{port}/api/equity"


@pytest.mark.parametrize("hand", ["AhKh", "7h2s", "QdQc", "JhTs"])
def test_calculate_hand_vs_random_equity(api_url, hand):
    response = requests.post(f"{api_url}/hand-vs-random", json={"hand": hand})
    assert response.status_code == 200
    data = response.json()
    assert "equity" in data
    assert 0.0 <= data["equity"] <= 1.0


@pytest.mark.parametrize(
    "hero_hand,villain_hand",
    [
        ("AhKh", "QdQc"),
        ("7h2s", "AhAd"),
        ("JhTs", "9s8s"),
        ("KsKc", "AhKh"),
    ],
)
def test_calculate_hand_vs_hand_equity(api_url, hero_hand, villain_hand):
    response = requests.post(
        f"{api_url}/hand-vs-hand",
        json={"hero_hand": hero_hand, "villain_hand": villain_hand},
    )
    assert response.status_code == 200
    data = response.json()
    assert "equity" in data
    assert 0.0 <= data["equity"] <= 1.0


@pytest.mark.parametrize(
    "hand,range_str",
    [
        ("AhKh", "AA,KK,QQ"),
        ("7h2s", "22+,A2s+,K2s+"),
        ("QdQc", "AK,AQ"),
        ("JhTs", "88-JJ,ATs+"),
    ],
)
def test_calculate_hand_vs_range_equity(api_url, hand, range_str):
    response = requests.post(
        f"{api_url}/hand-vs-range", json={"hand": hand, "range": range_str}
    )
    assert response.status_code == 200
    data = response.json()
    assert "equity" in data
    assert 0.0 <= data["equity"] <= 1.0


def test_generate_range_heatmap(api_url):
    response = requests.post(f"{api_url}/range-heatmap", json={})
    assert response.status_code == 200
    data = response.json()
    assert "hands" in data
    assert "equities" in data
    assert len(data["hands"]) == len(data["equities"]) == 169
    assert all(0.0 <= equity <= 1.0 for equity in data["equities"])


@pytest.mark.parametrize("hand", ["AhKh", "7h2s", "QdQc", "JhTs"])
def test_generate_hand_vs_range_heatmap(api_url, hand):
    response = requests.post(f"{api_url}/hand-vs-range-heatmap", json={"hand": hand})
    assert response.status_code == 200
    data = response.json()
    assert "hands" in data
    assert "equities" in data
    assert len(data["hands"]) == len(data["equities"]) == 169
    assert all(0.0 <= equity <= 1.0 for equity in data["equities"])
