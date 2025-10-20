from typing import Optional

from order_service.src.models import Order
from order_service.src.repository import WriterRepository
from order_service.src.schemas import OrderCreate, OrderRead

class ProductWriter:

    def __init__(self, repository: WriterRepository):
        self.repo = repository