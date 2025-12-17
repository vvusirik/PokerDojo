import { Card } from "./Card";

interface PlayerState {
    username: string;
    chips: number;
    bet: number;
}

export function Player(state: PlayerState) {
    return (
        <div className="border-2 border-gray-800 rounded-xl p-4 min-w-[200px] bg-white shadow-md">
            <div className="font-bold text-black text-lg mb-2">{state.username}</div>
            <div className="text-gray-600 mb-1">
                Chips: ${state.chips.toLocaleString()}
            </div>
            <div className="text-red-600 font-semibold">
                Bet: ${state.bet.toLocaleString()}
            </div>
            <div className="flex justify-center">
                <Card rank="A" suit="spades" />
                <Card rank="A" suit="spades" faceDown />
            </div>
        </div>
    );
}
