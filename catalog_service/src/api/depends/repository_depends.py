from fastapi import Depends
from src.api.depends.db_depends import get_session

from src.repository.write.writer_repository import WriterRepository
from src.repository.read.read_repository import ReadRepository

from src.repository import IWriterRepository, IReadRepository


def get_write_repo(
    session = Depends(get_session),
) -> IWriterRepository:
    return WriterRepository(session)


def get_read_repo(
    session = Depends(get_session),
) -> IReadRepository:
    return ReadRepository(session)
