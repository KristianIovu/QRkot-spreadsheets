"""CRUD для пожертвований."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDDonation(CRUDBase):
    """Расширенный CRUD для пожертвований с привязкой к пользователю."""

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user_id: int,
        commit: bool = True,
    ) -> Donation:
        """Создание пожертвования с привязкой к пользователю."""
        # Поддержка Pydantic v2 и v1
        if hasattr(obj_in, 'model_dump'):
            obj_in_data = obj_in.model_dump()
        elif hasattr(obj_in, 'dict'):
            obj_in_data = obj_in.dict()
        else:
            obj_in_data = obj_in

        obj_in_data["user_id"] = user_id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def get_by_user(
        self,
        user_id: int,
        session: AsyncSession,
    ) -> list[Donation]:
        """Получение всех пожертвований пользователя."""
        donations = await session.execute(
            select(self.model).where(
                self.model.user_id == user_id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
