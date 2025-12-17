import * as styles from "@/lib/styles";

interface CardProps {
    rank:
    | "A"
    | "2"
    | "3"
    | "4"
    | "5"
    | "6"
    | "7"
    | "8"
    | "9"
    | "T"
    | "J"
    | "Q"
    | "K";
    suit: "hearts" | "diamonds" | "clubs" | "spades";
    faceDown?: boolean;
}

const SUIT_SYMBOLS = {
    hearts: "♥",
    diamonds: "♦",
    clubs: "♣",
    spades: "♠",
};

const SUIT_COLORS = {
    hearts: "text-red-600",
    diamonds: "text-blue-600",
    clubs: "text-green-600",
    spades: "text-black",
};

export function Card({ rank, suit, faceDown = false }: CardProps) {
    if (faceDown) {
        return (
            <div className="w-16 h-24 bg-blue-600 border-2 border-gray-300 rounded-lg shadow-md flex items-center justify-center">
                <div className="text-white text-2xl font-bold">🂠</div>
            </div>
        );
    }

    const suitSymbol = SUIT_SYMBOLS[suit];
    const colorClass = SUIT_COLORS[suit];

    return (
        <div className="w-16 h-24 bg-white border-2 border-gray-300 rounded-lg shadow-md p-1 flex flex-col">
            <div className={`${colorClass} text-2xl`}>{rank}</div>
            <div className={styles.center}>
                <span className={`${colorClass} text-4xl`}>{suitSymbol}</span>
            </div>
        </div>
    );
}
