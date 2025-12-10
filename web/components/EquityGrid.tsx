"use client";
import "ag-charts-enterprise";

import { AgCharts } from "ag-charts-react";
import { useQuery } from "@tanstack/react-query";
import { CircularProgress, Alert } from "@mui/material";
import * as styles from "../lib/styles";
import Box from "@mui/material/Box";
import { type AgChartOptions } from "ag-charts-community";

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

    let component = null;
    if (isPending) {
        component = <CircularProgress />;
    } else if (error) {
        component = <Alert type="error">{error.message}</Alert>;
    } else {
        const options: AgChartOptions = {
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
                            data: [
                                {
                                    label: datum.hand,
                                    value: (100 * datum.equity).toFixed(0) + "%",
                                },
                            ],
                        }),
                    },
                },
            ],
        };

        component = <AgCharts options={options} />;
    }
    return <div className={styles.centerDiv}>{component}</div>;
}
