from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.project import Project, ProjectStatus
from app.models.user import User
from app.models.project_members import ProjectMember
from app.models.task import Task, TaskStatus


class ProjectRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, id: int):
        return self.db.query(User).filter(User.id == id).first()

    def create_project(self, project: Project):
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_all_projects(self):
        return (
            self.db.query(Project)
            .filter(Project.status != ProjectStatus.ARCHIVED)
            .all()
        )

    def get_all_archived_projects(self):
        return (
            self.db.query(Project)
            .filter(Project.status == ProjectStatus.ARCHIVED)
            .all()
        )

    def get_projects_by_manager(self, manager_id: int):
        return (
            self.db.query(Project)
            .filter(
                Project.manager_id == manager_id,
                Project.status != ProjectStatus.ARCHIVED,
            )
            .all()
        )

    def get_projects_by_user(self, user_id: int):
        return (
            self.db.query(Project)
            .join(ProjectMember)
            .filter(
                ProjectMember.user_id == user_id,
                Project.status != ProjectStatus.ARCHIVED,
            )
            .all()
        )

    def get_project_by_id(self, project_id: int):
        return (
            self.db.query(Project)
            .filter(Project.id == project_id, Project.status != ProjectStatus.ARCHIVED)
            .first()
        )

    def is_project_member(self, project_id: int, user_id: int) -> bool:
        return (
            self.db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id, ProjectMember.user_id == user_id
            )
            .first()
            is not None
        )

    def add_member(self, project_id: int, user_id: int):
        member = ProjectMember(project_id=project_id, user_id=user_id, role="worker")

        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)

        return member

    def is_member(self, project_id: int, user_id: int):
        return (
            self.db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id, ProjectMember.user_id == user_id
            )
            .first()
        )

    def update_project(self, project):
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_project_members(self, project_id: int):
        return (
            self.db.query(ProjectMember)
            .filter(ProjectMember.project_id == project_id)
            .all()
        )

    def delete_member(self, project_id: int, user_id: int):
        member = (
            self.db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id, ProjectMember.user_id == user_id
            )
            .first()
        )

        if not member:
            return None

        self.db.delete(member)
        self.db.commit()

        return member

    def get_project_tasks_stats(self, project_id: int):
        total = (
            self.db.query(func.count(Task.id))
            .filter(Task.project_id == project_id)
            .scalar()
        )

        completed = (
            self.db.query(func.count(Task.id))
            .filter(Task.project_id == project_id, Task.status == TaskStatus.DONE)
            .scalar()
        )

        return total or 0, completed or 0

    def get_user_project_ids(self, user_id: int) -> list[int]:
        return [
            m.project_id
            for m in self.db.query(ProjectMember.project_id)
            .filter(ProjectMember.user_id == user_id)
            .all()
        ]
