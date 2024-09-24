from src.core.errors import DomainError, ResourceNotFound


class NoteError(DomainError):
    @classmethod
    def invalid_id(cls) -> "NoteError":
        return cls("Invalid node id passed")


class NoteErrorNotFound(ResourceNotFound):
    pass


class ExportError(DomainError):
    pass
