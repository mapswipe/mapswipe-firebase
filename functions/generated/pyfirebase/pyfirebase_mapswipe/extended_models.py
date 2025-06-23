import typing

from . import models


class FbProject(
    models.FbProjectCreateOnlyInput,
    models.FbProjectUpdateInput,
    models.FbProjectReadonlyType,
):
    class Config:  # type: ignore[reportIncompatibleVariableOverride]
        use_enum_values = True
        frozen = True
        extra = "forbid"
