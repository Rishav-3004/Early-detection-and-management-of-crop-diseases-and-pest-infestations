import os
import uuid
from abc import ABC, abstractmethod
from app.core.config import settings

class StorageProvider(ABC):
    @abstractmethod
    async def save_file(self, file_bytes: bytes, original_filename: str) -> str:
        """
        Saves file bytes and returns a public/accessible URL or path.
        """
        pass

    @abstractmethod
    async def delete_file(self, file_url: str) -> bool:
        """
        Deletes a stored file.
        """
        pass

class LocalStorageProvider(StorageProvider):
    def __init__(self, upload_dir: str = None):
        self.upload_dir = upload_dir or settings.UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)

    async def save_file(self, file_bytes: bytes, original_filename: str) -> str:
        ext = original_filename.split(".")[-1].lower() if "." in original_filename else "jpg"
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        file_path = os.path.join(self.upload_dir, unique_filename)
        
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        
        # Return URL relative to static mount
        return f"/uploads/{unique_filename}"

    async def delete_file(self, file_url: str) -> bool:
        filename = os.path.basename(file_url)
        file_path = os.path.join(self.upload_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

def get_storage_provider() -> StorageProvider:
    # Factory for storage providers (supports local, can be extended for S3)
    return LocalStorageProvider()
