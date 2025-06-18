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

class MappingGroup(TypesyncModel):
    """Represents a group in a mapswipe project"""
    finishedCount: int
    groupId: str
    numberOfTasks: int
    progress: int
    projectId: str
    requiredCount: int
    xMax: typing.Union[TypesyncUndefined, str] = UNDEFINED
    xMin: typing.Union[TypesyncUndefined, str] = UNDEFINED
    yMax: typing.Union[TypesyncUndefined, str] = UNDEFINED
    yMin: typing.Union[TypesyncUndefined, str] = UNDEFINED

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "xMax" and value is None:
            raise ValueError("'xMax' field cannot be set to None")
        if name == "xMin" and value is None:
            raise ValueError("'xMin' field cannot be set to None")
        if name == "yMax" and value is None:
            raise ValueError("'yMax' field cannot be set to None")
        if name == "yMin" and value is None:
            raise ValueError("'yMin' field cannot be set to None")
        super().__setattr__(name, value)

class MappingResult(TypesyncModel):
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

class MappingTask(TypesyncModel):
    """Repesents a task in a group in a project"""
    groupId: str
    projectId: str
    taskId: str
    taskX: typing.Union[TypesyncUndefined, str] = UNDEFINED
    taskY: typing.Union[TypesyncUndefined, str] = UNDEFINED
    url: str

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "taskX" and value is None:
            raise ValueError("'taskX' field cannot be set to None")
        if name == "taskY" and value is None:
            raise ValueError("'taskY' field cannot be set to None")
        super().__setattr__(name, value)

Project = typing.Union[ProjectCreateOnlyInput, ProjectUpdateInput, ProjectReadonlyType]
"""Represents a mapswipe project"""

class ProjectCreateOnlyInput(TypesyncModel):
    """Represents fields that are valid only while creating a project"""
    created: datetime.datetime
    createdBy: str
    groupMaxSize: int
    groupSize: int
    projectId: str
    projectType: ProjectTypeEnum
    project_type: ProjectTypeEnum
    requiredResults: int
    verificationNumber: int
    zoomLevel: typing.Union[TypesyncUndefined, int] = UNDEFINED
    tileServer: typing.Union[TypesyncUndefined, ProjectRasterTileServer] = UNDEFINED
    tileServerB: typing.Union[TypesyncUndefined, ProjectRasterTileServer] = UNDEFINED

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "zoomLevel" and value is None:
            raise ValueError("'zoomLevel' field cannot be set to None")
        if name == "tileServer" and value is None:
            raise ValueError("'tileServer' field cannot be set to None")
        if name == "tileServerB" and value is None:
            raise ValueError("'tileServerB' field cannot be set to None")
        super().__setattr__(name, value)

class ProjectRasterTileServer(TypesyncModel):
    """Represents a raster tile server"""
    apiKey: typing.Union[TypesyncUndefined, str] = UNDEFINED
    credits: str
    name: str
    url: str

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "apiKey" and value is None:
            raise ValueError("'apiKey' field cannot be set to None")
        super().__setattr__(name, value)

class ProjectReadonlyType(TypesyncModel):
    """Represents fields that cannot be updated from backend"""
    contributorCount: int
    progress: int
    resultCount: int
    status: ProjectStatus

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

ProjectStatus = typing.Union[typing.Literal["active"], typing.Literal["finished"]]
"""Represents a project status"""

class ProjectTypeEnum(enum.Enum):
    """Represents a project type"""
    FIND = 1
    VALIDATE = 2
    VALIDATE_IMAGE = 10
    COMPARE = 3
    COMPLETENESS = 4

class ProjectUpdateInput(TypesyncModel):
    """Represents fields that are valid while updating a project"""
    image: typing.Union[TypesyncUndefined, str] = UNDEFINED
    isFeatured: bool
    lookFor: str
    name: str
    projectDetails: str
    projectNumber: str
    projectRegion: str
    projectTopic: str
    projectTopicKey: str
    requestingOrganisation: str
    tutorialId: str

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "image" and value is None:
            raise ValueError("'image' field cannot be set to None")
        super().__setattr__(name, value)

class UserContribution(TypesyncModel):
    """Represents a user contribution"""
    endTime: datetime.datetime
    startTime: datetime.datetime
    timestamp: datetime.datetime

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class UserGroupMembershipActionEnum(enum.Enum):
    Join = "join"
    Leave = "leave"

class Announcement(TypesyncModel):
    url: str
    text: str

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class Organisation(TypesyncModel):
    name: str
    description: str
    nameKey: str

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class Team(TypesyncModel):
    """Represents a mapswipe team"""
    teamName: str
    teamToken: datetime.datetime

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class User(TypesyncModel):
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

class UserGroup(TypesyncModel):
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

class UserGroupMembership(TypesyncModel):
    """Represents a user contribution"""
    action: UserGroupMembershipActionEnum
    timestamp: datetime.datetime
    userGroupId: str
    userId: str

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

class UserGroupObsolete(TypesyncModel):
    """Represents a usergroup"""
    name: str
    description: str

    class Config:
        use_enum_values = True
        extra = 'forbid'

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)

