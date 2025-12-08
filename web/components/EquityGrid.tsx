"use client";

import { AgCharts } from "ag-charts-react";
import "ag-charts-enterprise";
import { useQuery } from "@tanstack/react-query";

interface EquityHeatmapEntry {
    rankX: string;
    rankY: string;
    equity: number;
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
    const { isPending, error, data } = useQuery({
        queryKey: ["equityHeatmap"],
        queryFn: getEquityHeatmap,
    });

    if (isPending) return <div>Loading...</div>;
    if (error) return <div>Error loading data</div>;

    const options = {
        data: data,
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
    };

    return <AgCharts options={options} />;
}
