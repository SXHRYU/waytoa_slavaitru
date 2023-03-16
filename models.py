from pydantic import BaseModel


class Tag(BaseModel):
    id: str
    name: str

    def __hash__(self) -> int:
        return hash(id)


class Contest(BaseModel):
    id: str
    name: str

    def __hash__(self) -> int:
        return hash(self.id)


class Problem(BaseModel):
    id: str
    tag_id: str | None = None
    contest_id: str | None = None
    name: str
    difficulty: int
    passed_count: int
    url: str

    def __hash__(self) -> int:
        return hash(self.id)
