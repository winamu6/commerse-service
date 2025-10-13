from .read_depends import (get_product_read_repository,
                           get_cache_service,
                           get_product_reader,
                           get_cached_product_reader)

from .write_depends import (get_product_write_repository,
                            get_cache_service,
                            get_product_writer,
                            get_cached_product_writer)

__all__ = ["get_cache_service",
           "get_cached_product_reader",
           "get_product_read_repository",
           "get_product_writer",
           "get_cached_product_writer",
           "get_product_write_repository"]