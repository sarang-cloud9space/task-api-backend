
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth import decode_access_token
from database import get_db
from models import Task, User
from schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


DbSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    "",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_data: TaskCreate,
    db: DbSession,
    current_user: CurrentUser,
):
    task = Task(
        title=task_data.title,
        description=task_data.description,
        owner_id=current_user.id,
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task


@router.get("", response_model=list[TaskRead])
async def list_tasks(
    db: DbSession,
    current_user: CurrentUser,
):
    result = await db.execute(
        select(Task)
        .where(Task.owner_id == current_user.id)
        .order_by(Task.id)
    )
    return result.scalars().all()


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    result = await db.execute(
        select(Task).where(
            Task.id == task_id,
            Task.owner_id == current_user.id,
        )
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: DbSession,
    current_user: CurrentUser,
):
    result = await db.execute(
        select(Task).where(
            Task.id == task_id,
            Task.owner_id == current_user.id,
        )
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    updates = task_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    result = await db.execute(
        select(Task).where(
            Task.id == task_id,
            Task.owner_id == current_user.id,
        )
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    await db.delete(task)
    await db.commit()
