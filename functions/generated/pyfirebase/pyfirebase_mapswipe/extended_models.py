from pydantic import BaseModel

from . import models


class FbEmptyModel(BaseModel): ...


class FbProject(
    models.FbProjectCreateOnlyInput,
    models.FbProjectUpdateInput,
    models.FbProjectReadonlyType,
):
    class Config:  # type: ignore[reportIncompatibleVariableOverride]
        use_enum_values = True
        frozen = True
        extra = "forbid"


class FbMappingGroup(
    models.FbMappingGroupCreateOnlyInput,
    models.FbMappingGroupReadonlyType,
):
    class Config:  # type: ignore[reportIncompatibleVariableOverride]
        use_enum_values = True
        frozen = True
        extra = "forbid"
