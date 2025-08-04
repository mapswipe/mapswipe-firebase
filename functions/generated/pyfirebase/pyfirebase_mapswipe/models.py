from __future__ import annotations

import datetime
import enum
import typing

import pydantic
from pydantic_core import core_schema


class TypesyncUndefined:
    """Do not use this class in your code. Use the `UNDEFINED` sentinel instead."""

    _instance = None

    def __init__(self):
        if TypesyncUndefined._instance is not None:
            raise RuntimeError(
                "TypesyncUndefined instances cannot be created directly. Import and use the UNDEFINED sentinel instead.",
            )
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
    def model_dump(self, **kwargs) -> dict[str, typing.Any]:
        processed = {}
        for field_name, field_value in dict(self).items():
            if isinstance(field_value, pydantic.BaseModel):
                processed[field_name] = field_value.model_dump(**kwargs)
            elif isinstance(field_value, list):
                processed[field_name] = [
                    item.model_dump(**kwargs)
                    if isinstance(item, pydantic.BaseModel)
                    else item
                    for item in field_value
                ]
            elif isinstance(field_value, dict):
                processed[field_name] = {
                    key: value.model_dump(**kwargs)
                    if isinstance(value, pydantic.BaseModel)
                    else value
                    for key, value in field_value.items()
                }
            elif field_value is UNDEFINED:
                continue
            else:
                processed[field_name] = field_value
        return processed


# Model Definitions


class FbAnnouncement(TypesyncModel):
    """Represents app announcements for the contributors."""

    url: str
    text: str

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbEnumOverlayTileServerType(enum.Enum):
    RASTER = "raster"
    VECTOR = "vector"


class FbEnumValidateInputType(enum.Enum):
    AOI_FILE = "aoi_file"
    LINK = "link"
    TMID = "TMId"


class FbEnumUserGroupMembershipAction(enum.Enum):
    JOIN = "join"
    LEAVE = "leave"


class FbEnumRasterTileServerName(enum.Enum):
    """Represents supported raster tile server"""

    CUSTOM = "custom"
    BING = "bing"
    MAPBOX = "mapbox"
    MAXAR_STANDARD = "maxarStandard"
    MAXAR_PREMIUM = "maxarPremium"
    ESRI = "esri"
    ESRI_BETA = "esriBeta"


class FbEnumVectorTileServerName(enum.Enum):
    """Represents supported vector tile server"""

    CUSTOM = "custom"
    OPEN_STREET_MAP = "openStreetMap"
    OPEN_FREE_MAP = "openFreeMap"
    VERSATILES = "versatiles"


class FbEnumProjectStatus(enum.Enum):
    """Represents project status"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    PRIVATE_INACTIVE = "private_inactive"
    PRIVATE_ACTIVE = "private_active"
    FINISHED = "finished"


class FbEnumProjectType(enum.Enum):
    """Represents project type"""

    FIND = 1
    VALIDATE = 2
    VALIDATE_IMAGE = 10
    COMPARE = 3
    COMPLETENESS = 4


class FbBaseObjCustomSubOption(TypesyncModel):
    """Represents a custom sub-option"""

    value: int
    description: str

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbObjCustomOption(TypesyncModel):
    """Represents a custom option"""

    value: int
    title: str
    description: str
    icon: str
    iconColor: str
    subOptions: list[FbBaseObjCustomSubOption] | TypesyncUndefined | None = UNDEFINED

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "subOptions" and value is None:
            raise ValueError("'subOptions' field cannot be set to None")
        super().__setattr__(name, value)


class FbObjRasterTileServer(TypesyncModel):
    """Represents a raster tile server configuration"""

    apiKey: str | TypesyncUndefined | None = UNDEFINED
    wmtsLayerName: typing.Annotated[
        str | TypesyncUndefined | None,
        pydantic.Field(deprecated=True),
    ] = UNDEFINED
    credits: str
    name: FbEnumRasterTileServerName
    url: str

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "apiKey" and value is None:
            raise ValueError("'apiKey' field cannot be set to None")
        if name == "wmtsLayerName" and value is None:
            raise ValueError("'wmtsLayerName' field cannot be set to None")
        super().__setattr__(name, value)


class FbObjVectorTileServer(TypesyncModel):
    """Represents a vector tile server configuration"""

    credits: str
    name: FbEnumVectorTileServerName
    sourceLayer: str
    url: str
    minZoom: int
    maxZoom: int

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbObjRasterTileServerOverlay(TypesyncModel):
    """Represents an overlay layer for raster layer"""

    tileServer: FbObjRasterTileServer
    opacity: float

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbObjVectorTileServerOverlay(TypesyncModel):
    """Represents an overlay layer for vector layer"""

    tileServer: FbObjVectorTileServer
    fillColor: str
    fillOpacity: float
    lineColor: str
    lineOpacity: float
    lineWidth: float
    lineDasharray: list[int]
    circleColor: str
    circleOpacity: float
    circleRadius: float

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbObjUnifiedOverlayTileServer(TypesyncModel):
    """Represents an overlay layer"""

    type: FbEnumOverlayTileServerType
    raster: FbObjRasterTileServerOverlay | TypesyncUndefined | None = UNDEFINED
    vector: FbObjVectorTileServerOverlay | TypesyncUndefined | None = UNDEFINED

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "raster" and value is None:
            raise ValueError("'raster' field cannot be set to None")
        if name == "vector" and value is None:
            raise ValueError("'vector' field cannot be set to None")
        super().__setattr__(name, value)


class FbProjectReadonlyType(TypesyncModel):
    """Represents project fields that cannot be updated from backend"""

    contributorCount: int
    progress: int
    resultCount: int

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbProjectUpdateInput(TypesyncModel):
    """Represents project fields that are valid while updating a project"""

    image: str | TypesyncUndefined | None = UNDEFINED
    isFeatured: bool
    lookFor: str
    name: str
    projectDetails: str
    projectNumber: int
    projectRegion: str
    projectTopic: str
    projectTopicKey: typing.Annotated[str, pydantic.Field(deprecated=True)]
    requestingOrganisation: str
    tutorialId: str
    language: str
    manualUrl: str | TypesyncUndefined | None = UNDEFINED
    teamId: str | TypesyncUndefined | None = UNDEFINED
    status: FbEnumProjectStatus

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "image" and value is None:
            raise ValueError("'image' field cannot be set to None")
        if name == "manualUrl" and value is None:
            raise ValueError("'manualUrl' field cannot be set to None")
        if name == "teamId" and value is None:
            raise ValueError("'teamId' field cannot be set to None")
        super().__setattr__(name, value)


class FbProjectCreateOnlyInput(TypesyncModel):
    """Represents project fields that are valid while creating a project"""

    created: datetime.datetime
    createdBy: str
    groupMaxSize: int
    groupSize: int
    maxTasksPerUser: int | TypesyncUndefined | None = UNDEFINED
    projectId: str
    projectType: FbEnumProjectType
    requiredResults: int
    verificationNumber: int

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "maxTasksPerUser" and value is None:
            raise ValueError("'maxTasksPerUser' field cannot be set to None")
        super().__setattr__(name, value)


class FbProjectFindCreateOnlyInput(TypesyncModel):
    """Represents FIND project fields that are valid while creating a project"""

    zoomLevel: int
    tileServer: FbObjRasterTileServer

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbProjectCompareCreateOnlyInput(TypesyncModel):
    """Represents COMPARE project fields that are valid while creating a project"""

    zoomLevel: int
    tileServer: FbObjRasterTileServer
    tileServerB: FbObjRasterTileServer

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbProjectCompletenessCreateOnlyInput(TypesyncModel):
    """Represents COMPLETNESS project fields that are valid while creating a project"""

    zoomLevel: int
    tileServer: FbObjRasterTileServer
    tileServerB: FbObjRasterTileServer
    overlayTileServer: FbObjUnifiedOverlayTileServer

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbProjectValidateCreateOnlyInput(TypesyncModel):
    """Represents VALIDATE project fields that are valid while creating a project"""

    customOptions: list[FbObjCustomOption] | TypesyncUndefined | None = UNDEFINED
    tileServer: FbObjRasterTileServer
    inputType: FbEnumValidateInputType
    filter: str | TypesyncUndefined | None = UNDEFINED
    TMId: str | TypesyncUndefined | None = UNDEFINED

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "customOptions" and value is None:
            raise ValueError("'customOptions' field cannot be set to None")
        if name == "filter" and value is None:
            raise ValueError("'filter' field cannot be set to None")
        if name == "TMId" and value is None:
            raise ValueError("'TMId' field cannot be set to None")
        super().__setattr__(name, value)


class FbProjectValidateImageCreateOnlyInput(TypesyncModel):
    """Represents VALIDATE_IMAGE project fields that are valid while creating a project"""

    customOptions: list[FbObjCustomOption] | TypesyncUndefined | None = UNDEFINED

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "customOptions" and value is None:
            raise ValueError("'customOptions' field cannot be set to None")
        super().__setattr__(name, value)


class FbMappingGroupReadonlyType(TypesyncModel):
    """Represents mapping group fields that cannot be updated from backend"""

    finishedCount: int
    progress: int

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbMappingGroupCreateOnlyInput(TypesyncModel):
    """Represents mapping group fields that are valid while creating a mapping group"""

    projectId: str
    numberOfTasks: int
    requiredCount: int

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbMappingGroupTileMapServiceCreateOnlyInput(TypesyncModel):
    """Represents TILE_MAP_SERVICE mapping group fields that are valid while creating a mapping group"""

    groupId: str
    xMax: int
    xMin: int
    yMax: int
    yMin: int

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbMappingGroupValidateCreateOnlyInput(TypesyncModel):
    """Represents VALIDATE mapping group fields that are valid while creating a mapping group"""

    groupId: str

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbMappingGroupValidateImageCreateOnlyInput(TypesyncModel):
    """Represents VALIDATE_IMAGE mapping group fields that are valid while creating a mapping group"""

    groupId: str

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbMappingTaskCreateOnlyInput(TypesyncModel):
    """Represents mapping task fields that are valid while creating a task"""

    projectId: str

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbMappingTaskValidateCreateOnlyInput(TypesyncModel):
    """Represents VALIDATE mapping task fields that are valid while creating a task"""

    taskId: str
    geojson: dict[str, typing.Any]

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbMappingTaskValidateImageCreateOnlyInput(TypesyncModel):
    """Represents VALIDATE_IMAGE mapping task fields that are valid while creating a task"""

    taskId: str
    question: str | TypesyncUndefined | None = UNDEFINED

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "question" and value is None:
            raise ValueError("'question' field cannot be set to None")
        super().__setattr__(name, value)


class FbMappingTaskCompareCreateOnlyInput(TypesyncModel):
    """Represents COMPARE mapping task fields that are valid while creating a task"""

    groupId: str
    taskId: str
    taskX: int | TypesyncUndefined | None = UNDEFINED
    taskY: int | TypesyncUndefined | None = UNDEFINED
    url: str | TypesyncUndefined | None = UNDEFINED
    urlB: str | TypesyncUndefined | None = UNDEFINED

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "taskX" and value is None:
            raise ValueError("'taskX' field cannot be set to None")
        if name == "taskY" and value is None:
            raise ValueError("'taskY' field cannot be set to None")
        if name == "url" and value is None:
            raise ValueError("'url' field cannot be set to None")
        if name == "urlB" and value is None:
            raise ValueError("'urlB' field cannot be set to None")
        super().__setattr__(name, value)


class FbMappingResult(TypesyncModel):
    """Represents a mapswipe project"""

    appVersion: str
    clientType: str | TypesyncUndefined | None = UNDEFINED
    endTime: datetime.datetime
    startTime: datetime.datetime
    results: dict[str, int]
    usergroups: dict[str, bool] | TypesyncUndefined | None = UNDEFINED

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "clientType" and value is None:
            raise ValueError("'clientType' field cannot be set to None")
        if name == "usergroups" and value is None:
            raise ValueError("'usergroups' field cannot be set to None")
        super().__setattr__(name, value)


class FbOrganisation(TypesyncModel):
    """Represents the requesting organisation."""

    name: str
    description: str | TypesyncUndefined | None = UNDEFINED
    nameKey: typing.Annotated[str, pydantic.Field(deprecated=True)]
    abbreviation: str | TypesyncUndefined | None = UNDEFINED
    isArchived: bool

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "description" and value is None:
            raise ValueError("'description' field cannot be set to None")
        if name == "abbreviation" and value is None:
            raise ValueError("'abbreviation' field cannot be set to None")
        super().__setattr__(name, value)


class FbTeam(TypesyncModel):
    """Represents a team to limit project visibility."""

    teamName: str
    teamToken: str
    isArchived: bool

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbEnumInformationPageBlockType(enum.Enum):
    TEXT = "text"
    IMAGE = "image"


class FbInformationPageBlock(TypesyncModel):
    blockNumber: int
    blockType: FbEnumInformationPageBlockType
    textDescription: str | TypesyncUndefined | None = UNDEFINED
    image: str | TypesyncUndefined | None = UNDEFINED

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "textDescription" and value is None:
            raise ValueError("'textDescription' field cannot be set to None")
        if name == "image" and value is None:
            raise ValueError("'image' field cannot be set to None")
        super().__setattr__(name, value)


class FbInformationPage(TypesyncModel):
    pageNumber: int
    title: str
    blocks: list[FbInformationPageBlock]

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbScreenBlock(TypesyncModel):
    title: str
    description: str
    icon: str

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbScreen(TypesyncModel):
    hint: FbScreenBlock
    instructions: FbScreenBlock
    success: FbScreenBlock

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbBaseTutorial(TypesyncModel):
    exampleImage1: typing.Annotated[
        str | TypesyncUndefined | None,
        pydantic.Field(deprecated=True),
    ] = UNDEFINED
    exampleImage2: typing.Annotated[
        str | TypesyncUndefined | None,
        pydantic.Field(deprecated=True),
    ] = UNDEFINED
    contributorCount: int
    informationPages: list[FbInformationPage]
    lookFor: str
    name: str
    progress: int
    projectDetails: str
    projectId: str
    projectTopicKey: typing.Annotated[str, pydantic.Field(deprecated=True)]
    status: typing.Literal["tutorial"]
    tutorialDraftId: typing.Annotated[str, pydantic.Field(deprecated=True)]

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "exampleImage1" and value is None:
            raise ValueError("'exampleImage1' field cannot be set to None")
        if name == "exampleImage2" and value is None:
            raise ValueError("'exampleImage2' field cannot be set to None")
        super().__setattr__(name, value)


class FbBaseTutorialGroup(TypesyncModel):
    finishedCount: int
    groupId: int
    numberOfTasks: int
    progress: int
    projectId: str
    requiredCount: int

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbCompareTutorial(TypesyncModel):
    projectType: typing.Literal[3]
    tileServer: FbObjRasterTileServer
    tileServerB: FbObjRasterTileServer
    zoomLevel: int
    screens: list[FbScreen]

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbCompareTutorialGroup(TypesyncModel):
    xMax: int
    xMin: int
    yMax: int
    yMin: int

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbCompareTutorialTask(TypesyncModel):
    geometry: str
    groupId: int
    projectId: str
    referenceAnswer: int
    screen: int
    taskId: str
    taskId_real: str
    taskX: int
    taskY: int
    url: str
    urlB: str

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbCompletenessTutorial(TypesyncModel):
    projectType: typing.Literal[4]
    tileServer: FbObjRasterTileServer
    tileServerB: FbObjRasterTileServer
    overlayTileServer: FbObjUnifiedOverlayTileServer
    zoomLevel: int
    screens: list[FbScreen]

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbCompletenessTutorialGroup(TypesyncModel):
    xMax: int
    xMin: int
    yMax: int
    yMin: int

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbCompletenessTutorialTask(TypesyncModel):
    geometry: str
    groupId: int
    projectId: str
    referenceAnswer: int
    screen: int
    taskId: str
    taskId_real: str
    taskX: int
    taskY: int
    url: str
    urlB: str

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbFindTutorial(TypesyncModel):
    projectType: typing.Literal[1]
    tileServer: FbObjRasterTileServer
    zoomLevel: int
    screens: list[FbScreen]

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbFindTutorialGroup(TypesyncModel):
    xMax: int
    xMin: int
    yMax: int
    yMin: int

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbFindTutorialTask(TypesyncModel):
    geometry: str
    groupId: int
    projectId: str
    referenceAnswer: int
    screen: int
    taskId: str
    taskId_real: str
    taskX: int
    taskY: int
    url: str

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbValidateTutorial(TypesyncModel):
    inputGeometries: str
    projectType: typing.Literal[2]
    tileServer: FbObjRasterTileServer
    zoomLevel: int
    screens: list[FbScreen]
    customOptions: list[FbObjCustomOption] | TypesyncUndefined | None = UNDEFINED

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "customOptions" and value is None:
            raise ValueError("'customOptions' field cannot be set to None")
        super().__setattr__(name, value)


class FbValidateTutorialTaskProperties(TypesyncModel):
    building: str
    description: str
    reference: str
    screen: str

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbValidateTutorialTask(TypesyncModel):
    taskId: str
    geojson: typing.Any
    properties: FbValidateTutorialTaskProperties
    screen: int
    reference: int
    geometry: str

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbUserReadonlyType(TypesyncModel):
    """Represents user fields that cannot be updated from backend"""

    created: datetime.datetime
    userName: str
    userNameKey: typing.Annotated[str, pydantic.Field(deprecated=True)]
    username: str
    usernameKey: typing.Annotated[str, pydantic.Field(deprecated=True)]
    accessibility: bool | TypesyncUndefined | None = UNDEFINED
    userGroups: dict[str, typing.Any] | TypesyncUndefined | None = UNDEFINED

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "accessibility" and value is None:
            raise ValueError("'accessibility' field cannot be set to None")
        if name == "userGroups" and value is None:
            raise ValueError("'userGroups' field cannot be set to None")
        super().__setattr__(name, value)


class FbUserUpdateInput(TypesyncModel):
    """Represents a user"""

    teamId: str | TypesyncUndefined | None = UNDEFINED

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "teamId" and value is None:
            raise ValueError("'teamId' field cannot be set to None")
        super().__setattr__(name, value)


class FbUserContribution(TypesyncModel):
    """Represents a user contribution"""

    endTime: datetime.datetime
    startTime: datetime.datetime
    timestamp: datetime.datetime

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbUserGroup(TypesyncModel):
    """Represents a usergroup"""

    createdAt: int
    createdBy: str
    description: str
    name: str
    nameKey: typing.Annotated[str, pydantic.Field(deprecated=True)]
    users: dict[str, typing.Any]

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbUserGroupObsolete(TypesyncModel):
    """Represents a usergroup"""

    name: str
    description: str

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbUserGroupMembership(TypesyncModel):
    """Represents a user contribution"""

    action: FbEnumUserGroupMembershipAction
    timestamp: datetime.datetime
    userGroupId: str
    userId: str

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


class FbBackendWait(TypesyncModel):
    """Represents if to wait for firebase."""

    ok: bool
    timestamp: datetime.datetime

    class Config:
        use_enum_values = False
        extra = "forbid"

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)
