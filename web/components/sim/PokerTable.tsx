import { ReactNode, Children } from "react";
import { Player } from "./Player";

export function PokerTable({ children }: { children: ReactNode }) {
    const childrenArray = Children.toArray(children);
    const playerCount = childrenArray.length;

    return (
        <div className="relative w-[800px] h-[600px] mx-auto my-12">
            {/* Table surface */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[300px] bg-green-700 rounded-[50%] border-8 border-amber-900 shadow-2xl" />

            {/* Players positioned around the table */}
            {childrenArray.map((child, index) => {
                const angle = (index / playerCount) * 2 * Math.PI - Math.PI / 2;
                const radiusX = 350;
                const radiusY = 250;
                const x = Math.cos(angle) * radiusX;
                const y = Math.sin(angle) * radiusY;

                return (
                    <div
                        key={index}
                        className="absolute"
                        style={{
                            left: "50%",
                            top: "50%",
                            transform: `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`,
                        }}
                    >
                        {child}
                    </div>
                );
            })}
        </div>
    );
}
