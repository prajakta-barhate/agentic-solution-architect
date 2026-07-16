from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreateRequest


class ProjectRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, payload: ProjectCreateRequest) -> Project:
        project = Project(name=payload.name, description=payload.description, status="Draft")
        self.session.add(project)
        self.session.flush()
        return project

    def exists_by_name(self, name: str) -> bool:
        result = self.session.execute(select(Project).where(Project.name == name))
        return result.scalar_one_or_none() is not None

    def commit(self) -> None:
        try:
            self.session.commit()
        except IntegrityError as exc:
            self.session.rollback()
            raise exc
