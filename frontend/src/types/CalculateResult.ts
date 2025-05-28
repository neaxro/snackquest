export interface SnackDecision {
    count: number,
    name: string,
    unit_price: number
}

export interface CalculateResult {
    budget: number,
    final_items: SnackDecision[],
    total_candies: number,
    total_cost: number
}
