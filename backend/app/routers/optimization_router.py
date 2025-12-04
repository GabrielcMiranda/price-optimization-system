from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
import logging

from app.schemas import OptimizationRequest, OptimizationResponse, StandartOutput
from app.services.auth_service import AuthService
from app.services.optimization_service import OptimizationService

optimization_router = APIRouter(prefix='/optimizations', tags=['Optimizations'])

@optimization_router.post('/', response_model=StandartOutput, status_code=201)
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
    
@optimization_router.put('/{optimization_name}', response_model=StandartOutput, status_code=201)
async def update_optimization(optimization_name: str, dto: OptimizationRequest, user_id: UUID = Depends(AuthService.validate_user_auth)):
    try:
        optimization = await OptimizationService.update_optimization(user_id, optimization_name, dto)
        return optimization
    except HTTPException as error:
        raise error
    except Exception as error:
        logging.error("Error in update_optimization: %s", error)
        raise HTTPException(status_code=500, detail='Something went wrong. Please try again later.')
    
@optimization_router.get('/', response_model=list[OptimizationRequest])
async def list_optimizations(user_id: UUID = Depends(AuthService.validate_user_auth)):
    try:
        optimizations = await OptimizationService.list_optimizations(user_id)
        return optimizations
    except HTTPException as error:
        raise error
    except Exception as error:
        logging.error("Error in list_optimizations: %s", error)
        raise HTTPException(status_code=500, detail='Something went wrong. Please try again later.')