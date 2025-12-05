export interface OptimizationRequest {
  optimization_name: string;
  cost_function: string;
  demand_function: string;
}

export interface OptimizationResponse {
  optimization_name: string;
  optimal_price: number;
  cost_function: string;
  demand_function: string;
  max_profit: number;
  graph_image_url: string;
}

export interface StandardOutput {
  status_code: number;
  detail: string;
}
