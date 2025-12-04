from uuid import UUID
import asyncio
from app.schemas import OptimizationRequest, OptimizationInfo
from app.core.database.connection import async_session
from sqlalchemy.future import select
from app.models import PriceOptimization, User
from fastapi import HTTPException
from app.services.optimization_calc import OptimizationCalc
from app.services.file_service import FileService

class OptimizationService:
   
    @staticmethod
    async def make_optimization(user_id: UUID, dto: OptimizationRequest) -> OptimizationInfo:
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
            
            image_buffer = await asyncio.to_thread(
                OptimizationCalc.generate_graph_image, dto, optimization
            )
            
            graph_url = await FileService.upload_graph_image(
                image_buffer=image_buffer,
                user_id=str(user_id),
                optimization_name=dto.optimization_name
            )
            
            new_optimization = PriceOptimization(
                optimization_name=dto.optimization_name,
                user_id=user_id,
                cost_function=dto.cost_function,
                demand_function=dto.demand_function,
                optimal_price=optimization.optimal_price,
                max_profit=optimization.max_profit,
                graph_image_url=graph_url
            )

            session.add(new_optimization)
            await session.commit()
            await session.refresh(new_optimization)
            
            return optimization