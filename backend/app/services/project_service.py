from __future__ import annotations

from fastapi import HTTPException

from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreateRequest, ProjectResponse, ProjectStatus
from app.models.project import Project


class ProjectService:
    def __init__(self, repository: ProjectRepository) -> None:
        self.repository = repository

    def create_project(self, payload: ProjectCreateRequest) -> ProjectResponse:
        if self.repository.exists_by_name(payload.name):
            raise HTTPException(status_code=409, detail="Project name already exists")

        project = self.repository.create(payload)
        self.repository.commit()

        return ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            status=ProjectStatus(project.status),
            created_at=project.created_at,
            updated_at=project.updated_at,
        )
