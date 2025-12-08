"use client";
import EquityGrid from "../components/EquityGrid";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();
export default function Home() {
    return (
        <QueryClientProvider client={queryClient}>
            <EquityGrid />
        </QueryClientProvider>
    );
}
