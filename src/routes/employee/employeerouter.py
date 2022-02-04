from fastapi import APIRouter, Response, status


from sqlmodel import Session
from database.models.employee import Employee
from config.database import engine
from .employeentity import EmployeeEntity


router = APIRouter(prefix="/employee", tags=["Employee"])


@router.get("/")
async def getAll():
    db = Session(engine)

    return db.query(Employee).all()


@router.get("/{id}")
async def getById(id: int):
    db = Session(engine)
    db_result = db.query(Employee).filter(Employee.id == id).first()

    return db_result


@router.post("/")
async def createEmployee(request: EmployeeEntity):
    db = Session(engine)
    db_Create = Employee(name=request.name, jobs=request.jobs, address=request.address)

    db.add(db_Create)

    db.commit()

    return Response(content="Bisa", status_code=status.HTTP_200_OK)


@router.put("/{id}")
async def updateEmployee(id: int, request: EmployeeEntity):
    db = Session(engine)
    db_update = db.query(Employee).filter(Employee.id == id).first()

    db_update.name = request.name
    db_update.jobs = request.jobs
    db_update.address = request.jobs

    db.commit()

    return Response(
        content=f"Update Employee berdasarkan {id}", status_code=status.HTTP_200_OK
    )


@router.delete("/{id}")
async def deleteEmployee(id: int):
    db = Session(engine)
    db_delete = db.query(Employee).filter(Employee.id == id).first()

    db.delete(db_delete)

    db.commit()

    return Response(
        content=f"Delete Employee berdasarkan {id}", status_code=status.HTTP_200_OK
    )
