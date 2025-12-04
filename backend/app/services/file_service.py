from io import BytesIO
from app.core.settings import Settings
import cloudinary
from cloudinary.uploader import upload

cloudinary.config(
    cloud_name=Settings.CLOUDINARY_CLOUD_NAME,      
    api_key=Settings.CLOUDINARY_API_KEY,
    api_secret=Settings.CLOUDINARY_API_SECRET,
    secure=True
)

class FileService:
    @staticmethod
    async def upload_graph_image(image_buffer: BytesIO, user_id: str, optimization_id: str) -> str:

        result = upload(
            image_buffer,
            folder=f'optimization_graphs/{user_id}',
            public_id=optimization_id,  
            overwrite=True,
            resource_type="image",
            format="png"
        )
        
        return result['secure_url']