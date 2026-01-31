"""Template base para crear un router completo CRUD.

Para ejecutar el servidor:
    uv run uvicorn app.main:app --reload

Para ver la documentación interactiva:
    http://localhost:8000/docs
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
# from app.schemas.xxx import CreateSchema, UpdateSchema, ResponseSchema
# from app.crud.xxx import crud_xxx

router = APIRouter(
    prefix="/ENTIDAD",
    tags=["ENTIDAD"],
)


@router.get("/", response_model=List[dict])
def listar(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar registros con paginación."""
    # return crud_xxx.get_multi(db, skip=skip, limit=limit)
    return []


@router.post("/", status_code=status.HTTP_201_CREATED)
def crear(
    # obj_in: CreateSchema,
    db: Session = Depends(get_db)
):
    """Crear nuevo registro."""
    # return crud_xxx.create(db, obj_in=obj_in)
    return {"message": "Creado"}


@router.get("/{obj_id}")
def obtener(
    obj_id: int,
    db: Session = Depends(get_db)
):
    """Obtener registro por ID."""
    # obj = crud_xxx.get(db, id=obj_id)
    # if not obj:
    #     raise HTTPException(status_code=404, detail="No encontrado")
    # return obj
    return {"id": obj_id}


@router.put("/{obj_id}")
def actualizar(
    obj_id: int,
    # obj_in: UpdateSchema,
    db: Session = Depends(get_db)
):
    """Actualizar registro existente."""
    # db_obj = crud_xxx.get(db, id=obj_id)
    # if not db_obj:
    #     raise HTTPException(status_code=404, detail="No encontrado")
    # return crud_xxx.update(db, db_obj=db_obj, obj_in=obj_in)
    return {"id": obj_id, "message": "Actualizado"}


@router.delete("/{obj_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(
    obj_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar registro por ID."""
    # crud_xxx.remove(db, id=obj_id)
    return None
