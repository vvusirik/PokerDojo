import pytest
from sim import (
    Action,
    ActionType,
    Card,
    Entrant,
    Event,
    GameFormat,
    Rank,
    Round,
    Suit,
    deal_next_hand,
    initialize_game,
    resolve_showdown,
    update,
)


@pytest.fixture
def sample_format():
    return GameFormat(small_blind_amount=1.0, big_blind_amount=2.0)


@pytest.fixture
def sample_entrants():
    return [
        Entrant(username="Alice", buy_in=100.0, seat=1),
        Entrant(username="Bob", buy_in=100.0, seat=2),
    ]


def test_initialize_game(sample_entrants, sample_format):
    state = initialize_game(sample_entrants, sample_format)
    assert len(state.players) == 2
    assert state.round == Round.PREFLOP
    assert state.pot_size == 0.0


def test_deal_next_hand(sample_entrants, sample_format):
    initial_state = initialize_game(sample_entrants, sample_format)
    dealt_state = deal_next_hand(initial_state)
    assert all(p.cards is not None for p in dealt_state.players if p.active)
    assert len(dealt_state.community_cards) == 0
    # Check blinds deducted
    assert dealt_state.small_blind_player.stack == 99.0
    assert dealt_state.big_blind_player.stack == 98.0


def test_update_fold(sample_entrants, sample_format):
    initial_state = initialize_game(sample_entrants, sample_format)
    dealt_state = deal_next_hand(initial_state)
    event = Event(
        username="Alice", action=Action(action_type=ActionType.FOLD, bet_amount=0.0)
    )
    updated_state = update(dealt_state, event)
    assert updated_state.username_to_player
    assert not updated_state.username_to_player["Alice"].active


def test_resolve_showdown(sample_entrants, sample_format):
    # Set up a state with active players and community cards
    initial_state = initialize_game(sample_entrants, sample_format)
    dealt_state = deal_next_hand(initial_state)
    # Manually set community cards for testing
    dealt_state.community_cards = [
        Card(rank=Rank.ACE, suit=Suit.HEARTS),
        Card(rank=Rank.KING, suit=Suit.HEARTS),
        Card(rank=Rank.QUEEN, suit=Suit.HEARTS),
        Card(rank=Rank.JACK, suit=Suit.HEARTS),
        Card(rank=Rank.TEN, suit=Suit.HEARTS),
    ]
    # Assume Alice has better hand
    alice = next(p for p in dealt_state.players if p.username == "Alice")
    alice.cards = (
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.ACE, suit=Suit.CLUBS),
    )
    bob = next(p for p in dealt_state.players if p.username == "Bob")
    bob.cards = (
        Card(rank=Rank.TWO, suit=Suit.SPADES),
        Card(rank=Rank.THREE, suit=Suit.CLUBS),
    )
    dealt_state.pot_size = 10.0
    resolved_state = resolve_showdown(dealt_state)
    alice_final = next(p for p in resolved_state.players if p.username == "Alice")
    assert alice_final.stack > 100.0  # Should win pot
    assert resolved_state.pot_size == 0.0
