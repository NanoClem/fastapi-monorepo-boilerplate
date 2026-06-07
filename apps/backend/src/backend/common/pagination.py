from pydantic import computed_field

from .schemas import CustomBaseModel


class PaginatedResponse[T: CustomBaseModel](CustomBaseModel):
    """Generic pagination response model."""

    total: int
    page: int
    size: int
    items: list[T]

    @computed_field
    @property
    def total_pages(self) -> int:
        return (self.total + self.size - 1) // self.size

    @computed_field
    @property
    def has_next(self) -> bool:
        return self.page * self.size < self.total

    @computed_field
    @property
    def has_previous(self) -> bool:
        return self.page > 1
