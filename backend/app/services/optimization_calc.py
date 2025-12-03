from typing import Dict, Tuple
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from app.schemas import OptimizationRequest, OptimizationResponse


class OptimizationCalc:
    
    def __init__(self):
        self.x = sp.Symbol('x')
    
    def calculate_optimal_price(self, dto: OptimizationRequest) -> OptimizationResponse:
       
        try:
          
            cost = parse_expr(dto.cost_function, local_dict={'x': self.x})
            demand = parse_expr(dto.demand_function, local_dict={'x': self.x})
            
            revenue = self.x * demand
            
            profit = revenue - cost
            
            profit_derivative = sp.diff(profit, self.x)
            
            critical_points = sp.solve(profit_derivative, self.x)
            
            valid_points = [
                float(point) for point in critical_points 
                if point.is_real and float(point) > 0
            ]
            
            if not valid_points:
                raise ValueError("Nenhum ponto crítico válido encontrado")
            
            second_derivative = sp.diff(profit_derivative, self.x)
            
            optimal_price = None
            max_profit_value = float('-inf')
            
            for point in valid_points:
                second_deriv_value = float(second_derivative.subs(self.x, point))
                if second_deriv_value < 0:
                    profit_value = float(profit.subs(self.x, point))
                    if profit_value > max_profit_value:
                        max_profit_value = profit_value
                        optimal_price = point
            
            if optimal_price is None:
              
                optimal_price = max(valid_points, key=lambda p: float(profit.subs(self.x, p)))
                max_profit_value = float(profit.subs(self.x, optimal_price))

            graph_url = self._generate_graph_mock_url(
                dto.cost_function, 
                dto.demand_function, 
                optimal_price
            )
            
            return OptimizationResponse(
                optimal_price=round(optimal_price, 2),
                max_profit=round(max_profit_value, 2),
                graph_image_url=graph_url,
                profit_function=str(profit),
                derivative=str(profit_derivative)
            )
            
        except Exception as e:
            raise ValueError(f"Erro ao calcular otimização: {str(e)}")
    
    def _generate_graph_mock_url(
        self, 
        cost_function: str, 
        demand_function: str, 
        optimal_price: float
    ) -> str:
      
        return f"https://api.placeholder.com/graph?cost={cost_function}&demand={demand_function}&optimal={optimal_price}"
    
    def validate_functions(self, cost_function: str, demand_function: str) -> bool:
     
        try:
            parse_expr(cost_function, local_dict={'x': self.x})
            parse_expr(demand_function, local_dict={'x': self.x})
            return True
        except Exception:
            return False
