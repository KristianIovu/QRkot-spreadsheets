"""Маршруты для работы с пожертвованиями."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.dependencies import current_user, current_superuser
from app.crud import donation_crud
from app.models.charity_project import CharityProject
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, DonationFullInfoDB
from app.services.investment import distribute_funds

router = APIRouter()


@router.get(
    "/",
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True,
    summary="Получить все пожертвования",
    description="Показать список всех пожертвований "
    "(только для суперпользователя).",
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
) -> list[DonationFullInfoDB]:
    """Получить список всех пожертвований."""
    return await donation_crud.get_all(session)


@router.get(
    "/my",
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    summary="Мои пожертвования",
    description="Показать список своих пожертвований.",
)
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
) -> list[DonationDB]:
    """Получить список пожертвований текущего пользователя."""
    donations = await donation_crud.get_by_user(
        user_id=user.id,
        session=session
    )
    return donations


@router.post(
    "/",
    response_model=DonationDB,
    response_model_exclude_none=True,
    summary="Создать пожертвование",
    description="Создать пожертвование "
    "(только для авторизованных пользователей).",
)
async def create_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
) -> DonationDB:
    """Создать новое пожертвование."""
    new_donation = await donation_crud.create(
        donation.model_dump(),
        session,
        user_id=user.id
    )

    # Получаем открытые проекты
    result = await session.execute(
        select(CharityProject).where(
            CharityProject.invested_amount < CharityProject.full_amount
        ).order_by(CharityProject.create_date)
    )
    projects = result.scalars().all()

    if projects:
        changed_projects = distribute_funds(new_donation, projects)
        if changed_projects:
            session.add_all(changed_projects)

    await session.commit()
    await session.refresh(new_donation)

    return new_donation
