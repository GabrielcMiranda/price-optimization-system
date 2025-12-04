from typing import List
from uuid import UUID
import asyncio
from app.schemas import OptimizationInfo, OptimizationRequest, OptimizationResponse, StandartOutput
from app.core.database.connection import async_session
from sqlalchemy.future import select
from app.models import PriceOptimization, User
from fastapi import HTTPException
from app.services.optimization_calc import OptimizationCalc
from app.services.file_service import FileService

class OptimizationService:
   
    @staticmethod
    async def make_optimization(user_id: UUID, dto: OptimizationRequest) -> StandartOutput:
        async with async_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            existing_optimization = await session.execute(
                select(PriceOptimization).where(
                    PriceOptimization.optimization_name == dto.optimization_name,
                    PriceOptimization.user_id == user_id
                )
            )
            
            if existing_optimization.scalar_one_or_none():
                raise HTTPException(status_code=400, detail="Optimization name already exists for this user")
            
            optimization = await asyncio.to_thread(
                OptimizationCalc.calculate_optimal_price, dto
            )
            
            new_optimization = PriceOptimization(
                optimization_name=dto.optimization_name,
                user_id=user_id,
                cost_function=dto.cost_function,
                demand_function=dto.demand_function,
                optimal_price=optimization.optimal_price,
                max_profit=optimization.max_profit
            )

            session.add(new_optimization)
            await session.flush() 
            
            image_buffer = await asyncio.to_thread(
                OptimizationCalc.generate_graph_image, dto, optimization
            )
            
            graph_url = await FileService.upload_graph_image(
                image_buffer=image_buffer,
                user_id=str(user_id),
                optimization_id=str(new_optimization.id)
            )
            
            new_optimization.graph_image_url = graph_url
            await session.commit()
            await session.refresh(new_optimization)

            return StandartOutput(status_code=201, detail="Optimization created successfully.")
        
    @staticmethod
    async def get_optimization(user_id: UUID, optimization_name:str) -> OptimizationResponse:
        async with async_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))         

            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            optimization_result = await session.execute(
                select(PriceOptimization).where(
                    PriceOptimization.optimization_name == optimization_name,
                    PriceOptimization.user_id == user_id
                ))
            
            optimization = optimization_result.scalar_one_or_none()
            
            if not optimization:
                raise HTTPException(status_code=404, detail="Optimization not found")

            return OptimizationResponse(
                optimization_name=optimization.optimization_name,
                optimal_price=optimization.optimal_price,
                cost_function=optimization.cost_function,
                demand_function=optimization.demand_function,
                max_profit=optimization.max_profit,
                graph_image_url=optimization.graph_image_url
            )
    
    @staticmethod
    async def update_optimization(user_id: UUID, optimization_name: str, dto: OptimizationRequest) -> StandartOutput:
        async with async_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            optimization_result = await session.execute(
                select(PriceOptimization).where(
                    PriceOptimization.optimization_name == optimization_name,
                    PriceOptimization.user_id == user_id
                ))
            
            optimization = optimization_result.scalar_one_or_none()
            
            if not optimization:
                raise HTTPException(status_code=404, detail="Optimization not found")
            
            available_name_result = await session.execute(
                select(PriceOptimization).where(PriceOptimization.optimization_name == dto.optimization_name,
                PriceOptimization.user_id == user_id)
            )

            available_name_optimization = available_name_result.scalar_one_or_none()

            if dto.optimization_name != optimization_name and available_name_optimization:
                raise HTTPException(status_code=400, detail="Optimization name already exists for this user")
            
            if dto.cost_function != optimization.cost_function or dto.demand_function != optimization.demand_function:
            
                updated_optimization = await asyncio.to_thread(
                    OptimizationCalc.calculate_optimal_price, dto
                )
                
                image_buffer = await asyncio.to_thread(
                    OptimizationCalc.generate_graph_image, dto, updated_optimization
                )
                
                graph_url = await FileService.upload_graph_image(
                    image_buffer=image_buffer,
                    user_id=str(user_id),
                    optimization_id=str(optimization.id)
                )

                optimization.cost_function = dto.cost_function
                optimization.demand_function = dto.demand_function
                optimization.optimal_price = updated_optimization.optimal_price
                optimization.max_profit = updated_optimization.max_profit
                optimization.graph_image_url = graph_url
            
            optimization.optimization_name = dto.optimization_name
            
            session.add(optimization)
            await session.commit()
            await session.refresh(optimization)
            
            return StandartOutput(
                status_code=200,
                detail="Optimization updated successfully"
            )
        
    @staticmethod
    async def list_optimizations(user_id: UUID) -> List[OptimizationRequest]:
        async with async_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            optimizations_result = await session.execute(
                select(PriceOptimization).where(PriceOptimization.user_id == user_id)
            )
            
            optimizations = optimizations_result.scalars().all()
            
            optimization_list = [
                OptimizationRequest(
                    optimization_name=opt.optimization_name,
                    cost_function=opt.cost_function,
                    demand_function=opt.demand_function
                ) for opt in optimizations
            ]
            
            return optimization_list