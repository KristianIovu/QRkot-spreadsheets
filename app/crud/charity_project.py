"""CRUD для целевых проектов."""

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


charity_project_crud = CRUDBase(CharityProject)
