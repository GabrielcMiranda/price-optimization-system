from io import BytesIO
import sympy as sp
import numpy as np
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from sympy.parsing.sympy_parser import parse_expr
from app.schemas import OptimizationRequest, OptimizationInfo


class OptimizationCalc:
    
    @staticmethod
    def calculate_optimal_price(dto: OptimizationRequest) -> OptimizationInfo:
       
        x = sp.Symbol('x')
        q = sp.Symbol('q') 
        
        try:
           
            cost_expr = parse_expr(dto.cost_function, local_dict={'x': q})  # C(q)
            demand = parse_expr(dto.demand_function, local_dict={'x': x})   # Q(p)
            
            # C(Q(p))
            cost = cost_expr.subs(q, demand)
            
            # Receita: R(p) = p · Q(p)
            revenue = x * demand
            
            # Lucro: L(p) = R(p) - C(Q(p))
            profit = revenue - cost
            
            profit_derivative = sp.diff(profit, x)
            critical_points = sp.solve(profit_derivative, x)
            
            valid_points = [
                float(point) for point in critical_points 
                if point.is_real and float(point) > 0
            ]
            
            if not valid_points:
                raise ValueError("Nenhum ponto crítico válido encontrado")
            
            second_derivative = sp.diff(profit_derivative, x)
            
            optimal_price = None
            max_profit_value = float('-inf')
            
            for point in valid_points:
                second_deriv_value = float(second_derivative.subs(x, point))
                if second_deriv_value < 0:
                    profit_value = float(profit.subs(x, point))
                    if profit_value > max_profit_value:
                        max_profit_value = profit_value
                        optimal_price = point
            
            if optimal_price is None:
                optimal_price = max(valid_points, key=lambda p: float(profit.subs(x, p)))
                max_profit_value = float(profit.subs(x, optimal_price))
            
            return OptimizationInfo(
                optimal_price=optimal_price,
                max_profit=max_profit_value,
                profit_function=str(profit),
            )
        
        except Exception as e:
            raise ValueError(f"Erro ao calcular otimização: {str(e)}")
    
    @staticmethod
    def generate_graph_image(dto: OptimizationRequest, optimization: OptimizationInfo) -> BytesIO:
        
        x = sp.Symbol('x')
        try:
            cost = parse_expr(dto.cost_function, local_dict={'x': x})
            demand = parse_expr(dto.demand_function, local_dict={'x': x})
            revenue = x * demand
            profit = revenue - cost
            
            cost_func = sp.lambdify(x, cost, 'numpy')
            revenue_func = sp.lambdify(x, revenue, 'numpy')
            profit_func = sp.lambdify(x, profit, 'numpy')
            
            x_range = np.linspace(0, optimization.optimal_price * 2, 1000)
            
            cost_values = cost_func(x_range)
            revenue_values = revenue_func(x_range)
            profit_values = profit_func(x_range)
            
            plt.figure(figsize=(12, 8))
            
            plt.plot(x_range, cost_values, label='Custo', color='red', linewidth=2)
            plt.plot(x_range, revenue_values, label='Receita', color='green', linewidth=2)
            plt.plot(x_range, profit_values, label='Lucro', color='blue', linewidth=2)
            
            plt.scatter([optimization.optimal_price], [optimization.max_profit], color='gold', s=200, zorder=5, 
                       label=f'Ponto Ótimo ({optimization.optimal_price:.2f}, {optimization.max_profit:.2f})',
                       edgecolors='black', linewidth=2)
            
            plt.axvline(x=optimization.optimal_price, color='gray', linestyle='--', alpha=0.7)
            plt.axhline(y=optimization.max_profit, color='gray', linestyle='--', alpha=0.7)
            
            plt.xlabel('Preço (x)', fontsize=12, fontweight='bold')
            plt.ylabel('Valor ($)', fontsize=12, fontweight='bold')
            plt.title('Otimização de Preço - Análise de Custo, Receita e Lucro', 
                     fontsize=14, fontweight='bold')
            plt.legend(fontsize=10, loc='best')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()
            
            return img_buffer
            
        except Exception as e:
            plt.close()
            raise ValueError(f"Erro ao gerar gráfico: {str(e)}")
    
    @staticmethod
    def validate_functions(cost_function: str, demand_function: str) -> bool:
    
        x = sp.Symbol('x')
        try:
            parse_expr(cost_function, local_dict={'x': x})
            parse_expr(demand_function, local_dict={'x': x})
            return True
        except Exception:
            return False
