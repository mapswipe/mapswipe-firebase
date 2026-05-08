import {
    FbProjectCreateOnlyInput,
    FbProjectUpdateInput,
    FbProjectReadonlyType,
    FbMappingGroupCreateOnlyInput,
    FbMappingGroupReadonlyType,
    FbUserUpdateInput,
    FbUserReadonlyType,
    FbUserGroupCreateOnlyInput,
    FbUserGroupUpdateInput,
    FbUserGroupReadOnlyType,
    FbTileMapServiceTutorialTask,
    FbFindTutorialTask,
    FbCompareTutorialTask,
    FbCompletenessTutorialTask,
} from './models';

export type FbProject = FbProjectCreateOnlyInput & FbProjectUpdateInput & FbProjectReadonlyType;

export type FbMappingGroup = FbMappingGroupCreateOnlyInput & FbMappingGroupReadonlyType;

export type FbUser = FbUserUpdateInput & FbUserReadonlyType;

export type FbUserGroup = FbUserGroupCreateOnlyInput & FbUserGroupUpdateInput & FbUserGroupReadOnlyType;

export type FbFindTutorialTaskComplete = FbTileMapServiceTutorialTask & FbFindTutorialTask;

export type FbCompareTutorialTaskComplete = FbTileMapServiceTutorialTask & FbCompareTutorialTask;

export type FbCompletenessTutorialTaskComplete = FbTileMapServiceTutorialTask & FbCompletenessTutorialTask;
