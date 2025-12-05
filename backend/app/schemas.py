
from pydantic import BaseModel, field_validator
from typing import Optional
import re


class LoginRequest(BaseModel):
    login: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class OptimizationRequest(BaseModel):
    optimization_name: str
    cost_function: str
    demand_function: str
    
    @field_validator('cost_function')
    @classmethod
    def validate_cost_function(cls, v: str) -> str:
        v_clean = v.replace(' ', '')
        
        if not v_clean:
            raise ValueError("A função não pode estar vazia")
        
        if 'q' not in v_clean.lower():
            raise ValueError("A função de custo deve conter a variável 'q'")
        
        # números, q, operadores matemáticos básicos, parênteses
        pattern = r'^[0-9q\+\-\*/\(\)\.\s\*\*]+$'
        if not re.match(pattern, v_clean, re.IGNORECASE):
            raise ValueError(
                "A função contém caracteres inválidos. "
                "Use apenas números, 'q', +, -, *, /, ** e parênteses"
            )
        
        if v_clean.count('(') != v_clean.count(')'):
            raise ValueError("Parênteses desbalanceados na função")
        
        return v
    
    @field_validator('demand_function')
    @classmethod
    def validate_demand_function(cls, v: str) -> str:
        v_clean = v.replace(' ', '')
        
        if not v_clean:
            raise ValueError("A função não pode estar vazia")
        
        if 'p' not in v_clean.lower():
            raise ValueError("A função de demanda deve conter a variável 'p'")
        
        # números, p, operadores matemáticos básicos, parênteses
        pattern = r'^[0-9p\+\-\*/\(\)\.\s\*\*]+$'
        if not re.match(pattern, v_clean, re.IGNORECASE):
            raise ValueError(
                "A função contém caracteres inválidos. "
                "Use apenas números, 'p', +, -, *, /, ** e parênteses"
            )
        
        if v_clean.count('(') != v_clean.count(')'):
            raise ValueError("Parênteses desbalanceados na função")
        
        return v

class OptimizationInfo(BaseModel):
    optimal_price: float
    max_profit: float
    profit_function: Optional[str] = None

class OptimizationResponse(BaseModel):
    optimization_name: str
    optimal_price: float
    cost_function: str
    demand_function: str
    max_profit: float
    graph_image_url: Optional[str] = None

class StandartOutput(BaseModel):
    status_code:int
    detail:str