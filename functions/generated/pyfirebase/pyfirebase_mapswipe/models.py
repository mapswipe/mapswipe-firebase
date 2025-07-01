from __future__ import annotations

import typing
import datetime
import enum
import pydantic
from pydantic_core import core_schema
from typing_extensions import Annotated

class TypesyncUndefined:
    """Do not use this class in your code. Use the `UNDEFINED` sentinel instead."""
    _instance = None

    def __init__(self):
        if TypesyncUndefined._instance is not None:
            raise RuntimeError("TypesyncUndefined instances cannot be created directly. Import and use the UNDEFINED sentinel instead.")
        else:
            TypesyncUndefined._instance = self

    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler) -> core_schema.CoreSchema:
        return core_schema.with_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, value: typing.Any, info) -> TypesyncUndefined:
        if not isinstance(value, cls):
            raise ValueError("Undefined field type is not valid")
        return value

UNDEFINED = TypesyncUndefined()
"""A sentinel value that can be used to indicate that a value should be undefined. During serialization all values that are marked as undefined will be removed. The difference between `UNDEFINED` and `None` is that values that are set to `None` will serialize to explicit null."""

class TypesyncModel(pydantic.BaseModel):
    def model_dump(self, **kwargs) -> typing.Dict[str, typing.Any]:
        processed = {}
        for field_name, field_value in dict(self).items():
            if isinstance(field_value, pydantic.BaseModel):
                processed[field_name] = field_value.model_dump(**kwargs)
            elif isinstance(field_value, list):
                processed[field_name] = [item.model_dump(**kwargs) if isinstance(item, pydantic.BaseModel) else item for item in field_value]
            elif isinstance(field_value, dict):
                processed[field_name] = {key: value.model_dump(**kwargs) if isinstance(value, pydantic.BaseModel) else value for key, value in field_value.items()}
            elif field_value is UNDEFINED:
                continue
            else:
                processed[field_name] = field_value
        return processed

# Model Definitions

class FbBaseObjCustomSubOption(TypesyncModel):
    """Represents a custom sub option"""
    value: int
    description: str

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class FbEnumProjectStatus(enum.Enum):
    """Represents a project status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PRIVATE_INACTIVE = "private_inactive"
    PRIVATE_ACTIVE = "private_active"
    FINISHED = "finished"

class FbEnumProjectType(enum.Enum):
    """Represents a project type"""
    FIND = 1
    VALIDATE = 2
    VALIDATE_IMAGE = 10
    COMPARE = 3
    COMPLETENESS = 4

class FbEnumRasterTileServerName(enum.Enum):
    """Represents a project status"""
    CUSTOM = "custom"
    BING = "bing"
    MAPBOX = "mapbox"
    MAXAR_STANDARD = "maxarStandard"
    MAXAR_PREMIUM = "maxarPremium"
    ESRI = "esri"
    ESRI_BETA = "esriBeta"

class FbEnumUserGroupMembershipAction(enum.Enum):
    JOIN = "join"
    LEAVE = "leave"

class FbEnumValidateInputType(enum.Enum):
    AOI_FILE = "aoi_file"
    LINK = "link"
    TMID = "TMId"

class FbMappingGroupCreateOnlyInput(TypesyncModel):
    """Represents a group in a mapswipe project"""
    groupId: str
    projectId: str
    numberOfTasks: int
    requiredCount: int

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class FbMappingGroupReadonlyType(TypesyncModel):
    """Represents fields that cannot be updated from backend"""
    finishedCount: int
    progress: int

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class FbMappingResult(TypesyncModel):
    """Represents a mapswipe project"""
    appVersion: str
    clientType: typing.Union[TypesyncUndefined, str] = UNDEFINED
    endTime: datetime.datetime
    startTime: datetime.datetime
    results: typing.Dict[str, int]
    usergroups: typing.Union[TypesyncUndefined, typing.Dict[str, bool]] = UNDEFINED

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "clientType" and value is None:
            raise ValueError("'clientType' field cannot be set to None")
        if name == "usergroups" and value is None:
            raise ValueError("'usergroups' field cannot be set to None")
        super().__setattr__(name, value)

class FbMappingTaskCreateOnlyInput(TypesyncModel):
    """Repesents a task in a group in a project"""
    projectId: str
    groupId: str
    taskId: str

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class FbObjCustomOption(TypesyncModel):
    """Represents a custom option"""
    value: int
    title: str
    description: str
    icon: str
    iconColor: str
    subOptions: typing.Union[TypesyncUndefined, typing.List[FbBaseObjCustomSubOption]] = UNDEFINED

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "subOptions" and value is None:
            raise ValueError("'subOptions' field cannot be set to None")
        super().__setattr__(name, value)

class FbObjRasterTileServer(TypesyncModel):
    """Represents a raster tile server"""
    apiKey: typing.Union[TypesyncUndefined, str] = UNDEFINED
    wmtsLayerName: typing.Union[TypesyncUndefined, str] = UNDEFINED
    credits: str
    name: FbEnumRasterTileServerName
    url: str

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "apiKey" and value is None:
            raise ValueError("'apiKey' field cannot be set to None")
        if name == "wmtsLayerName" and value is None:
            raise ValueError("'wmtsLayerName' field cannot be set to None")
        super().__setattr__(name, value)

class FbProjectCompareCreateOnlyInput(TypesyncModel):
    """Represents fields that are valid only while creating a project for COMPARE"""
    zoomLevel: int
    tileServer: FbObjRasterTileServer
    tileServerB: FbObjRasterTileServer

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class FbProjectCompletenessCreateOnlyInput(TypesyncModel):
    """Represents fields that are valid only while creating a project for COMPLETENESS"""
    zoomLevel: int
    tileServer: FbObjRasterTileServer
    tileServerB: FbObjRasterTileServer

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class FbProjectCreateOnlyInput(TypesyncModel):
    """Represents fields that are valid only while creating a project"""
    created: datetime.datetime
    createdBy: str
    groupMaxSize: int
    groupSize: int
    maxTasksPerUser: typing.Union[TypesyncUndefined, int] = UNDEFINED
    projectId: str
    projectType: FbEnumProjectType
    requiredResults: int
    verificationNumber: int

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "maxTasksPerUser" and value is None:
            raise ValueError("'maxTasksPerUser' field cannot be set to None")
        super().__setattr__(name, value)

class FbProjectFindCreateOnlyInput(TypesyncModel):
    """Represents fields that are valid only while creating a project for FIND"""
    zoomLevel: int
    tileServer: FbObjRasterTileServer

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class FbProjectReadonlyType(TypesyncModel):
    """Represents fields that cannot be updated from backend"""
    contributorCount: int
    progress: int
    resultCount: int

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class FbProjectUpdateInput(TypesyncModel):
    """Represents fields that are valid while updating a project"""
    image: typing.Union[TypesyncUndefined, str] = UNDEFINED
    isFeatured: bool
    lookFor: str
    name: str
    projectDetails: str
    projectNumber: int
    projectRegion: str
    projectTopic: str
    projectTopicKey: str
    requestingOrganisation: str
    tutorialId: str
    language: str
    manualUrl: typing.Union[TypesyncUndefined, str] = UNDEFINED
    teamId: typing.Union[TypesyncUndefined, str] = UNDEFINED
    status: FbEnumProjectStatus

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "image" and value is None:
            raise ValueError("'image' field cannot be set to None")
        if name == "manualUrl" and value is None:
            raise ValueError("'manualUrl' field cannot be set to None")
        if name == "teamId" and value is None:
            raise ValueError("'teamId' field cannot be set to None")
        super().__setattr__(name, value)

class FbProjectValidateCreateOnlyInput(TypesyncModel):
    """Represents fields that are valid only while creating a project for VALIDATE"""
    customOptions: typing.Union[TypesyncUndefined, typing.List[FbObjCustomOption]] = UNDEFINED
    filter: str
    inputType: FbEnumValidateInputType
    tileServer: FbObjRasterTileServer

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "customOptions" and value is None:
            raise ValueError("'customOptions' field cannot be set to None")
        super().__setattr__(name, value)

class FbProjectValidateImageCreateOnlyInput(TypesyncModel):
    """Represents fields that are valid only while creating a project for VALIDATE"""
    customOptions: typing.Union[TypesyncUndefined, typing.List[FbObjCustomOption]] = UNDEFINED

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "customOptions" and value is None:
            raise ValueError("'customOptions' field cannot be set to None")
        super().__setattr__(name, value)

class FbUserContribution(TypesyncModel):
    """Represents a user contribution"""
    endTime: datetime.datetime
    startTime: datetime.datetime
    timestamp: datetime.datetime

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class FbAnnouncement(TypesyncModel):
    url: str
    text: str

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class FbOrganisation(TypesyncModel):
    name: str
    description: str
    nameKey: str

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class FbTeam(TypesyncModel):
    """Represents a mapswipe team"""
    teamName: str
    teamToken: datetime.datetime

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class FbUser(TypesyncModel):
    """Represents a user"""
    created: datetime.datetime
    userName: str
    userNameKey: str
    username: str
    usernameKey: str
    accessibility: typing.Union[TypesyncUndefined, bool] = UNDEFINED
    userGroups: typing.Union[TypesyncUndefined, typing.Dict[str, typing.Any]] = UNDEFINED

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "accessibility" and value is None:
            raise ValueError("'accessibility' field cannot be set to None")
        if name == "userGroups" and value is None:
            raise ValueError("'userGroups' field cannot be set to None")
        super().__setattr__(name, value)

class FbUserGroup(TypesyncModel):
    """Represents a usergroup"""
    createdAt: int
    createdBy: str
    description: str
    name: str
    nameKey: str
    users: typing.Dict[str, typing.Any]

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class FbUserGroupMembership(TypesyncModel):
    """Represents a user contribution"""
    action: FbEnumUserGroupMembershipAction
    timestamp: datetime.datetime
    userGroupId: str
    userId: str

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class FbUserGroupObsolete(TypesyncModel):
    """Represents a usergroup"""
    name: str
    description: str

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

