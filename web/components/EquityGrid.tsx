"use client";

import { useState, useEffect } from "react";
import { AgCharts } from "ag-charts-react";
import { StartingHands } from "../utils/constants";
import "ag-charts-enterprise";

interface EquityHeatmapEntry {
    rankX: string;
    rankY: string;
    equity: number;
}

function getData(): Array<EquityHeatmapEntry> {
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

async function getEquityHeatmap(): Promise<Array<EquityHeatmapEntry>> {
    try {
        const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const response = await fetch(`${API_URL}/api/equity/range-heatmap`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({}),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const heatmap = data.hands.map((hand: string, index: number) => ({
            rankX: hand[0],
            rankY: hand[1],
            equity: data.equities[index],
        }));

        console.log("Heatmap:", heatmap);
        return heatmap;
    } catch (error) {
        console.error("Error generating range heatmap:", error);
        return [];
    }
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
                    formatter: ({ datum: { rankX } }) => `${rankX}`,
                },
            },
        ],
    });

    useEffect(() => {
        getEquityHeatmap().then((data) => {
            setOptions((prev) => ({
                ...prev,
                data,
            }));
        });
    }, []);

    return <AgCharts options={options} />;
}
