"use client";

import { useState } from "react";
import { AgCharts } from "ag-charts-react";
import { StartingHands } from "../utils/constants";
import "ag-charts-enterprise";

function getData(): Array<{
    rankX: string;
    rankY: string;
    equity: number;
}> {
    let hands = [];
    for (let i = 0; i < 13; i++) {
        for (let j = 0; j < 13; j++) {
            hands.push({
                rankX: i.toString(),
                rankY: j.toString(),
                equity: 0,
            });
        }
    }
    return hands;
}

export default function EquityGrid() {
    const [options, setOptions] = useState({
        data: getData(),
        title: {
            text: "Hand Equity",
        },
        series: [
            {
                type: "heatmap",
                xKey: "rankX",
                xName: "Rank",
                yKey: "rankY",
                yName: "Rank",
                colorKey: "equity",
                colorName: "Equity",
                label: {
                    enabled: true,
                    formatter: ({ datum: { equity } }) => `${equity.toFixed(0)}`,
                },
            },
        ],
    });

    return <AgCharts options={options} />;
}
