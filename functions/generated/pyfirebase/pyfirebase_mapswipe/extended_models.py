from pydantic import BaseModel

from . import models


class FbEmptyModel(BaseModel): ...


class FbProject(
    models.FbProjectCreateOnlyInput,
    models.FbProjectUpdateInput,
    models.FbProjectReadonlyType,
):
    class Config:  # type: ignore[reportIncompatibleVariableOverride]
        use_enum_values = False
        frozen = True
        extra = "forbid"


class FbMappingGroup(
    models.FbMappingGroupCreateOnlyInput,
    models.FbMappingGroupReadonlyType,
):
    class Config:  # type: ignore[reportIncompatibleVariableOverride]
        use_enum_values = False
        frozen = True
        extra = "forbid"


class FbUser(
    models.FbUserUpdateInput,
    models.FbUserReadonlyType,
):
    class Config:  # type: ignore[reportIncompatibleVariableOverride]
        use_enum_values = False
        frozen = True
        extra = "forbid"


class FbUserGroup(
    models.FbUserGroupCreateOnlyInput,
    models.FbUserGroupUpdateInput,
    models.FbUserGroupReadOnlyType,
):
    class Config:  # type: ignore[reportIncompatibleVariableOverride]
        use_enum_values = False
        frozen = True
        extra = "forbid"


class FbFindTutorialTaskComplete(
    models.FbTileMapServiceTutorialTask,
    models.FbFindTutorialTask,
):
    class Config:  # type: ignore[reportIncompatibleVariableOverride]
        use_enum_values = True
        frozen = True
        extra = "forbid"


class FbCompareTutorialTaskComplete(
    models.FbTileMapServiceTutorialTask,
    models.FbCompareTutorialTask,
):
    class Config:  # type: ignore[reportIncompatibleVariableOverride]
        use_enum_values = True
        frozen = True
        extra = "forbid"


class FbCompletenessTutorialTaskComplete(
    models.FbTileMapServiceTutorialTask,
    models.FbCompletenessTutorialTask,
):
    class Config:  # type: ignore[reportIncompatibleVariableOverride]
        use_enum_values = True
        frozen = True
        extra = "forbid"


class FbLocateTutorialTaskComplete(
    models.FbTileMapServiceTutorialTask,
    models.FbLocateTutorialTask,
):
    class Config:  # type: ignore[reportIncompatibleVariableOverride]
        use_enum_values = True
        frozen = True
        extra = "forbid"
