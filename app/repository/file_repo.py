import os
import uuid
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.file import File, FileType
from app.models import User, ReportAttachment


UPLOAD_DIR = "uploads"


class FileRepo:
    def __init__(self, db: Session):
        self.db = db

    def save_file(self, file: UploadFile, user: User) -> File:
        ext = os.path.splitext(file.filename)[1]
        stored_name = f"{uuid.uuid4()}{ext}"

        path = os.path.join(UPLOAD_DIR, stored_name)

        with open(path, "wb") as buffer:
            content = file.file.read()
            buffer.write(content)

        file_type = self._detect_type(file.content_type)

        db_file = File(
            original_name=file.filename,
            stored_name=stored_name,
            path=path,
            size=len(content),
            content_type=file.content_type,
            file_type=file_type,
            uploaded_by=user.id,
        )

        self.db.add(db_file)
        self.db.commit()
        self.db.refresh(db_file)

        return db_file

    def _detect_type(self, content_type: str):
        if content_type.startswith("image/"):
            return FileType.IMAGE
        if content_type.startswith("video/"):
            return FileType.VIDEO
        if "pdf" in content_type or "text" in content_type:
            return FileType.DOCUMENT
        if "zip" in content_type:
            return FileType.ARCHIVE
        return FileType.OTHER
    
    def make_attachment(self, report_id: int, file_id: int):
        attachment = ReportAttachment(
                report_id=report_id,
                file_id=file_id,
            )
        
        self.db.add(attachment)
        self.db.commit()
        self.db.refresh(attachment)

        return attachment
    
    def get_file_by_id(self, file_id):
        return self.db.query(File).filter(File.id == file_id).first()
    
    def delete_file(self, file: File):
        if not file:
            return 
        
        self.db.delete(file)
        self.db.commit()
        