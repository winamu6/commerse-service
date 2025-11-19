from fastapi import Depends
from payment_service.src.api.depends.db_depends import get_session

from payment_service.src.repository.write.write_repository import WriterRepository
from payment_service.src.repository.read.read_repository import ReadRepository

from payment_service.src.repository import IWriteRepository, IReadRepository


def get_write_repo(
    session = Depends(get_session),
) -> IWriteRepository:
    return WriterRepository(session)


def get_read_repo(
    session = Depends(get_session),
) -> IReadRepository:
    return ReadRepository(session)
