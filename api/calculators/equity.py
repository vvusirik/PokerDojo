import os
from functools import lru_cache, partial
from typing import Optional

import eval7
import numpy as np
from eval7 import Card, Deck, HandRange
from utils.constants import STARTING_HANDS
from utils.parallelize import process_map

_CACHE_SIZE = 2048


def _remove_cards_from_deck(deck: Deck, cards: list[Card]) -> Deck:
    deck.cards = [card for card in deck.cards if card not in cards]
    return deck


def _hand_str_to_cards(hand_str: str) -> list[Card]:
    hand_str = hand_str.replace(" ", "").strip()
    assert len(hand_str) == 4, "Hand string must be 4 characters long."
    hand_cards = [Card(hand_str[:2]), Card(hand_str[2:])]
    assert len(set(hand_cards)) == 2, "Hand must consist of two unique cards."
    return hand_cards


def _detect_duplicates(hand1: list[Card], hand2: list[Card]):
    return any(card in hand1 for card in hand2)


def _filter_valid_hands(
    hero_hand: tuple[Card, Card], villain_hand_range: HandRange
) -> HandRange:
    villain_hand_range.hands = [
        (villain_hand, weight)
        for villain_hand, weight in villain_hand_range.hands
        if not _detect_duplicates(list(hero_hand), villain_hand)
    ]
    return villain_hand_range


@lru_cache(maxsize=_CACHE_SIZE)
def hand_vs_random_hand_equity(hand_str: str, iterations: int = int(1e5)) -> float:
    hand_cards = _hand_str_to_cards(hand_str)
    wins, ties, losses = 0, 0, 0
    for _ in range(iterations):
        deck = _remove_cards_from_deck(Deck(), hand_cards)
        deck.shuffle()

        # Deal villain cards
        villain_hand = deck.deal(2)

        # Deal community cards
        board_cards = deck.deal(5)

        # Evaluate winner
        hero_score = eval7.evaluate(hand_cards + board_cards)
        villain_score = eval7.evaluate(villain_hand + board_cards)

        wins += hero_score > villain_score
        ties += hero_score == villain_score
        losses += hero_score < villain_score

    return (wins + 0.5 * ties) / iterations


@lru_cache(maxsize=_CACHE_SIZE)
def hand_vs_hand_equity(
    hero_hand: str, villain_hand: str, iterations: int = int(1e5)
) -> float:
    hero_hand_cards: list[Card] = _hand_str_to_cards(hero_hand)
    villain_hand_cards: list[Card] = _hand_str_to_cards(villain_hand)
    assert not _detect_duplicates(
        hero_hand_cards, villain_hand_cards
    ), "Cannot have the same cards in hero and villain hands"

    wins, ties, losses = 0, 0, 0
    for _ in range(iterations):
        deck = _remove_cards_from_deck(Deck(), hero_hand_cards + villain_hand_cards)
        deck.shuffle()

        # Deal community cards
        board_cards = deck.deal(5)

        # Evaluate winner
        hero_score = eval7.evaluate(hero_hand_cards + board_cards)
        villain_score = eval7.evaluate(villain_hand_cards + board_cards)

        wins += hero_score > villain_score
        ties += hero_score == villain_score
        losses += hero_score < villain_score

    return (wins + 0.5 * ties) / iterations


@lru_cache(maxsize=_CACHE_SIZE)
def hand_vs_range_equity(
    hand_str: str, range_str: str, iterations: int = int(1e5)
) -> float:
    hand_cards = _hand_str_to_cards(hand_str)
    wins, ties, losses = 0, 0, 0

    hand_range = _filter_valid_hands(tuple(hand_cards), HandRange(range_str))
    hands = [list(h[0]) for h in hand_range.hands]
    weights = [h[1] for h in hand_range.hands]
    weights = np.array(weights) / np.sum(weights)
    idxs = np.random.choice(len(hands), iterations, p=list(weights))

    for idx in idxs:
        villain_hand = hands[idx]
        deck = _remove_cards_from_deck(Deck(), hand_cards + villain_hand)
        deck.shuffle()

        # Deal community cards
        board_cards = deck.deal(5)

        # Evaluate winner
        hero_score = eval7.evaluate(hand_cards + board_cards)
        villain_score = eval7.evaluate(villain_hand + board_cards)

        wins += hero_score > villain_score
        ties += hero_score == villain_score
        losses += hero_score < villain_score

    return (wins + 0.5 * ties) / iterations


@lru_cache(maxsize=_CACHE_SIZE)
def hand_range_vs_random_equity(range_str: str, iterations: int = int(1e5)) -> float:
    wins, ties, losses = 0, 0, 0
    hand_range = HandRange(range_str)
    hands = [list(h[0]) for h in hand_range.hands]
    weights = [h[1] for h in hand_range.hands]
    weights = np.array(weights) / np.sum(weights)
    idxs = np.random.choice(len(hands), iterations, p=list(weights))

    for idx in idxs:
        hero_hand = hands[idx]
        villain_hand = []

        deck = Deck()
        deck = _remove_cards_from_deck(deck, hero_hand)
        deck.shuffle()

        # Deal villain cards
        villain_hand = deck.deal(2)

        # Deal community cards
        board_cards = deck.deal(5)

        # Evaluate winner
        hero_score = eval7.evaluate(hero_hand + board_cards)
        villain_score = eval7.evaluate(villain_hand + board_cards)

        wins += hero_score > villain_score
        ties += hero_score == villain_score
        losses += hero_score < villain_score

    return (wins + 0.5 * ties) / iterations


def hand_vs_random_equity_heatmap(workers: Optional[int] = None) -> dict[str, float]:
    workers = workers or os.cpu_count()
    equities = process_map(hand_range_vs_random_equity, STARTING_HANDS, workers)
    equity_grid = dict(zip(STARTING_HANDS, equities))
    return equity_grid


def hand_vs_range_equity_heatmap(
    hand_str: str, workers: Optional[int] = None
) -> dict[str, float]:
    workers = workers or os.cpu_count()
    equities = process_map(partial(hand_vs_range_equity, hand_str), STARTING_HANDS, 16)
    equity_grid = dict(zip(STARTING_HANDS, equities))
    return equity_grid
