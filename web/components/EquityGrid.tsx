"use client";

import { AgCharts } from "ag-charts-react";
import "ag-charts-enterprise";
import { useQuery } from "@tanstack/react-query";
import { CircularProgress } from "@mui/material";
import { Alert } from "@mui/material";

interface EquityHeatmapEntry {
    hand: string;
    rankX: string;
    rankY: string;
    equity: number;
}

async function getEquityHeatmap(): Promise<Array<EquityHeatmapEntry>> {
    try {
        const API_URL = process.env.NEXT_PUBLIC_API_URL;
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
            hand: hand,
            rankX: hand[hand.length - 1] == "o" ? hand[0] : hand[1],
            rankY: hand[hand.length - 1] == "o" ? hand[1] : hand[0],
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

    if (isPending) return <CircularProgress />;
    if (error) {
        return <Alert severity="error">{error}</Alert>;
    }

    const options = {
        data: data,
        width: 800,
        height: 800,
        title: {
            text: "Hand Equity",
        },
        series: [
            {
                type: "heatmap",
                xKey: "rankX",
                yKey: "rankY",
                colorKey: "equity",
                colorName: "Equity",
                label: {
                    enabled: true,
                    color: "black",
                    fontSize: 12,
                    formatter: ({ datum }) => datum.hand || "",
                },
                tooltip: {
                    enabled: true,
                    renderer: ({ datum }) => ({
                        data: [{ label: datum.hand, value: datum.equity.toFixed(2) + "%" }],
                    }),
                },
            },
        ],
    };

    return <AgCharts options={options} />;
}
