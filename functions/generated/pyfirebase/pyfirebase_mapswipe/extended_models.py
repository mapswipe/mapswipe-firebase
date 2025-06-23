import typing

from . import models


class FbProject(
    models.FbProjectCreateOnlyInput,
    models.FbProjectUpdateInput,
    models.FbProjectReadonlyType,
):
    class Config:  # type: ignore[reportIncompatibleVariableOverride]
        use_enum_values = True
        extra = "forbid"

    @typing.override
    def __setattr__(self, name: str, value: typing.Any) -> None:
        super(models.FbProjectReadonlyType).__setattr__(name, value)
        super(models.FbProjectCreateOnlyInput).__setattr__(name, value)
        super(models.FbProjectUpdateInput).__setattr__(name, value)
