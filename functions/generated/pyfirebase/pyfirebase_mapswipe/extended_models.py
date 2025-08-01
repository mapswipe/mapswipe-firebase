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
        # NOTE: We need to allow extra fields as FbProject
        # is not a complete project representation
        extra = "allow"


class FbMappingGroup(
    models.FbMappingGroupCreateOnlyInput,
    models.FbMappingGroupReadonlyType,
):
    class Config:  # type: ignore[reportIncompatibleVariableOverride]
        use_enum_values = True
        frozen = True
        extra = "forbid"


class FbUser(
    models.FbUserUpdateInput,
    models.FbUserReadonlyType,
):
    class Config:  # type: ignore[reportIncompatibleVariableOverride]
        use_enum_values = True
        frozen = True
        extra = "forbid"
