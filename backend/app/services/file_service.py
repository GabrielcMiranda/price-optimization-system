from app.core.settings import Settings
import cloudinary
from cloudinary.uploader import upload
from app.schemas import FileUploadRequest

cloudinary.config(
    cloud_name=Settings.CLOUDINARY_CLOUD_NAME,      
    api_key=Settings.CLOUDINARY_API_KEY,
    api_secret=Settings.CLOUDINARY_API_SECRET,
    secure=True
)

class FileService:
    @staticmethod
    async def upload_graph_image(dto:FileUploadRequest):
       
        safe_name = dto.optimization_name.replace(' ', '_').replace('/', '_')
        
        result = upload(
            dto.image_buffer,
            folder=f'optimization_graphs/{dto.user_id}',
            public_id=safe_name,
            overwrite=True,
            resource_type="image",
            format="png"
        )
        
        return result['secure_url']