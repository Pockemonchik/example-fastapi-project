class Tag:
    def __init__(
        self,
        name: str,
        tag_id: int | None = None,
    ) -> None:
        self.id = tag_id
        self.name = name
