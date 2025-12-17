from enum import StrEnum, auto
from functools import reduce
from typing import Annotated, Optional

import eval7 as e7
from pydantic import AfterValidator, BaseModel, model_validator


class Rank(StrEnum):
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    JACK = auto()
    QUEEN = auto()
    KING = auto()
    ACE = auto()


class Suit(StrEnum):
    CLUBS = auto()
    HEARTS = auto()
    DIAMONDS = auto()
    SPADES = auto()


class Card(BaseModel):
    rank: Optional[Rank]
    suit: Optional[Suit]


class Position(StrEnum):
    SMALL_BLIND = auto()
    BIG_BLIND = auto()
    UTG = auto()
    MP = auto()
    CO = auto()
    BTN = auto()


class PlayerState(BaseModel):
    username: str
    stack: float
    seat: int
    active: bool
    position: Optional[Position] = None
    cards: Optional[tuple[Card, Card]] = None


class Round(StrEnum):
    PREFLOP = auto()
    FLOP = auto()
    TURN = auto()
    RIVER = auto()


class GameFormat(BaseModel):
    small_blind_amount: float
    big_blind_amount: float


class GameState(BaseModel):
    game_format: GameFormat
    players: Annotated[
        list[PlayerState], AfterValidator(lambda l: sorted(l, key=lambda p: p.seat))
    ]
    acting_seat: int
    deck: list[Card]
    community_cards: list[Card]
    round: Round
    pot_size: float
    bet_amount: float

    # Set by validator hooks
    sb_seat: Optional[int] = None
    bb_seat: Optional[int] = None
    seats: Optional[list[int]] = None
    seat_to_player: Optional[dict[int, PlayerState]] = None
    username_to_player: Optional[dict[str, PlayerState]] = None

    @model_validator(mode="after")
    def validate_seats(self):
        assert len(self.players) >= 2, "Game must have at least 2 players"
        sb_seat: Optional[int] = None
        bb_seat: Optional[int] = None
        seat_to_player: dict[int, PlayerState] = {}
        username_to_player: dict[str, PlayerState] = {}

        for player in self.players:
            seat_to_player[player.seat] = player
            username_to_player[player.username] = player
            if player.position is Position.SMALL_BLIND:
                sb_seat = player.seat
            elif player.position is Position.BIG_BLIND:
                bb_seat = player.seat

        assert sb_seat is not None, "Game state must have a small blind"
        assert bb_seat is not None, "Game state must have a big blind"

        self.seat_to_player = dict(sorted(seat_to_player.items()))
        self.seats = list(seat_to_player.keys())
        assert (
            bb_seat == self.seats[(self.seats.index(sb_seat) + 1) % len(self.seats)]
        ), "Game state invariant violated: BB must be one seat to the left of the SB"

        self.sb_seat = sb_seat
        self.bb_seat = bb_seat
        self.seat_to_player = seat_to_player
        self.username_to_player = username_to_player

        return self

    def advance_acting_seat(self):
        assert self.seats is not None
        assert self.seat_to_player is not None

        next_seat: int = self.acting_seat
        while (
            next_seat == self.acting_seat or not self.seat_to_player[next_seat].active
        ):
            next_seat = self.seats[(self.seats.index(next_seat) + 1) % len(self.seats)]

            if next_seat == self.acting_seat:
                raise RuntimeError("No possible next player")
        self.acting_seat = next_seat

    def advance_blinds(self):
        assert self.seats is not None
        assert self.sb_seat is not None
        assert self.bb_seat is not None
        assert self.seat_to_player is not None

        # Find next SB seat
        sb_index = self.seats.index(self.sb_seat)
        new_sb_index = (sb_index + 1) % len(self.seats)
        new_sb_seat = self.seats[new_sb_index]

        # Find next BB seat
        new_bb_index = (new_sb_index + 1) % len(self.seats)
        new_bb_seat = self.seats[new_bb_index]

        # Clear positions
        for player in self.players:
            if player.position in [Position.SMALL_BLIND, Position.BIG_BLIND]:
                player.position = None

        # Set new positions
        self.seat_to_player[new_sb_seat].position = Position.SMALL_BLIND
        self.seat_to_player[new_bb_seat].position = Position.BIG_BLIND

        # Update sb_seat and bb_seat
        self.sb_seat = new_sb_seat
        self.bb_seat = new_bb_seat

    @property
    def num_active_players(self) -> int:
        return reduce(lambda n, p: n + int(p.active), self.players, 0)

    @property
    def acting_player(self) -> PlayerState:
        assert self.seat_to_player is not None
        return self.seat_to_player[self.acting_seat]

    @property
    def small_blind_player(self) -> PlayerState:
        return next(p for p in self.players if p.position == Position.SMALL_BLIND)

    @property
    def big_blind_player(self) -> PlayerState:
        return next(p for p in self.players if p.position == Position.BIG_BLIND)


class ActionType(StrEnum):
    CHECK = auto()
    RAISE = auto()
    CALL = auto()
    FOLD = auto()
    ALL_IN = auto()


class Action(BaseModel):
    action_type: ActionType
    bet_amount: float


class Event(BaseModel):
    username: str
    action: Action


class Entrant(BaseModel):
    username: str
    buy_in: float
    seat: int


def initialize_game(entrants: list[Entrant], format: GameFormat) -> GameState:
    players = [
        PlayerState(
            username=entrant.username,
            stack=entrant.buy_in,
            seat=entrant.seat,
            active=True,
        )
        for entrant in entrants
    ]
    players = sorted(players, key=lambda p: p.seat)
    assert len(players) >= 2

    # Assign positions: assume first is SB, second is BB
    players[0].position = Position.SMALL_BLIND
    players[1].position = Position.BIG_BLIND

    deck = e7.Deck()
    deck.shuffle()

    game_state = GameState(
        game_format=format,
        players=players,
        acting_seat=players[0].seat,
        deck=list(map(to_card, deck.cards)),
        community_cards=[],
        round=Round.PREFLOP,
        pot_size=0.0,
        bet_amount=0.0,
    )
    return game_state


def to_eval7(card: Card) -> e7.Card:
    if card.rank is None or card.suit is None:
        raise ValueError("Card must have both rank and suit")

    rank_to_char = {
        Rank.TWO: "2",
        Rank.THREE: "3",
        Rank.FOUR: "4",
        Rank.FIVE: "5",
        Rank.SIX: "6",
        Rank.SEVEN: "7",
        Rank.EIGHT: "8",
        Rank.NINE: "9",
        Rank.TEN: "T",
        Rank.JACK: "J",
        Rank.QUEEN: "Q",
        Rank.KING: "K",
        Rank.ACE: "A",
    }
    suit_to_char = {
        Suit.CLUBS: "c",
        Suit.DIAMONDS: "d",
        Suit.HEARTS: "h",
        Suit.SPADES: "s",
    }
    return e7.Card(rank_to_char[card.rank] + suit_to_char[card.suit])


def to_card(card: e7.Card) -> Card:
    rank_map = dict(enumerate(Rank))
    suit_map = {
        0: Suit.CLUBS,
        1: Suit.DIAMONDS,
        2: Suit.HEARTS,
        3: Suit.SPADES,
    }
    return Card(rank=rank_map[card.rank], suit=suit_map[card.suit])


def deal_next_hand(state: GameState) -> GameState:
    new_state = state.model_copy(deep=True)

    # 1. Collect blinds
    for player in new_state.players:
        if player.position is Position.SMALL_BLIND:
            player.stack -= new_state.game_format.small_blind_amount
        elif player.position is Position.BIG_BLIND:
            player.stack -= new_state.game_format.big_blind_amount

    # 2. Deal cards to players
    deck = e7.Deck()
    deck.shuffle()
    for player in new_state.players:
        dealt = deck.deal(2)
        player.cards = (to_card(dealt[0]), to_card(dealt[1]))
    new_state.deck = list(map(to_card, deck.cards))

    # 3. Set first player to act (left of BB)
    assert new_state.bb_seat is not None
    new_state.acting_seat = new_state.bb_seat
    new_state.advance_acting_seat()
    return new_state


def update(state: GameState, event: Event) -> GameState:
    new_state = state.model_copy(deep=True)
    assert new_state.username_to_player is not None
    if event.action.action_type == ActionType.FOLD:
        new_state.username_to_player[event.username].active = False

    if event.action.action_type == ActionType.CHECK:
        pass

    if event.action.action_type == ActionType.CALL:
        new_state.acting_player.stack -= event.action.bet_amount

    # TODO: if player is last to act, then deal next card
    if new_state.num_active_players > 1:
        new_state.advance_acting_seat()
    else:
        # TODO: resolve hand
        pass

    return new_state


def resolve_showdown(state: GameState) -> GameState:
    """Resolve a hand at showdown.

    Evaluates all active players' hole cards + the current board and awards the
    pot to the best hand(s). Ties split the pot evenly.
    """

    new_state = state.model_copy(deep=True)

    # If the board is incomplete, run out remaining cards.
    if len(new_state.community_cards) < 5:
        needed = 5 - len(new_state.community_cards)
        assert (
            len(new_state.deck) >= needed
        ), "Not enough cards in deck to run out board"
        new_state.community_cards.extend(new_state.deck[:needed])
        new_state.deck = new_state.deck[needed:]

    active_players = [p for p in new_state.players if p.active]
    if len(active_players) <= 1:
        return new_state

    board = [to_eval7(c) for c in new_state.community_cards]

    scored: list[tuple[int, PlayerState]] = []
    for player in active_players:
        assert player.cards is not None, "Active players must have hole cards"
        hole = [to_eval7(c) for c in player.cards]
        scored.append((e7.evaluate(hole + board), player))

    best_score = max(score for score, _ in scored)
    winners = [player for score, player in scored if score == best_score]
    assert winners, "Showdown must have at least one winner"

    payout = new_state.pot_size / len(winners)
    for winner in winners:
        winner.stack += payout

    new_state.pot_size = 0.0
    new_state.bet_amount = 0.0

    return new_state
