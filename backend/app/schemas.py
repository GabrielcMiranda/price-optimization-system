from pydantic import BaseModel, Field, field_validator
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
    cost_function: str
    demand_function: str
    
    @field_validator('cost_function', 'demand_function')
    @classmethod
    def validate_function_format(cls, v: str) -> str:
        
        v_clean = v.replace(' ', '')
        
        if not v_clean:
            raise ValueError("A função não pode estar vazia")
        
        if 'x' not in v_clean.lower():
            raise ValueError("A função deve conter a variável 'x'")
        
        #números, x, operadores matemáticos básicos, parênteses
        pattern = r'^[0-9x\+\-\*/\(\)\.\s\*\*]+$'
        if not re.match(pattern, v_clean, re.IGNORECASE):
            raise ValueError(
                "A função contém caracteres inválidos. "
                "Use apenas números, 'x', +, -, *, /, ** e parênteses"
            )
        
        if v_clean.count('(') != v_clean.count(')'):
            raise ValueError("Parênteses desbalanceados na função")
        
        return v

class OptimizationResponse(BaseModel):
    optimal_price: float
    max_profit: float
    graph_image_url: str
    profit_function: Optional[str] = None
    derivative: Optional[str] = None
    