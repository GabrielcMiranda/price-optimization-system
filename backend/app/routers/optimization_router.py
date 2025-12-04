from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
import logging

from app.schemas import OptimizationInfo, OptimizationRequest, OptimizationResponse
from app.services.auth_service import AuthService
from app.services.optimization_service import OptimizationService

optimization_router = APIRouter(prefix='/optimizations', tags=['Optimizations'])

@optimization_router.post('/', response_model=OptimizationInfo)
async def make_optimization(dto: OptimizationRequest, user_id: UUID = Depends(AuthService.validate_user_auth)):
    try:
        optimization = await OptimizationService.make_optimization(user_id, dto)
        return optimization
    except HTTPException as error:
        raise error
    except Exception as error:
        logging.error("Error in make_optimization: %s", error)
        raise HTTPException(status_code=500, detail='Something went wrong. Please try again later.')

@optimization_router.get('/{optimization_name}', response_model=OptimizationResponse)
async def get_optimization(optimization_name: str, user_id: UUID = Depends(AuthService.validate_user_auth)):
    try:
        optimization = await OptimizationService.get_optimization(user_id, optimization_name)
        return optimization
    except HTTPException as error:
        raise error
    except Exception as error:
        logging.error("Error in get_optimization: %s", error)
        raise HTTPException(status_code=500, detail='Something went wrong. Please try again later.')