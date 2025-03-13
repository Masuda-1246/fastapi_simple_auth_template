import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="items")