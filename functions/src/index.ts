// The Cloud Functions for Firebase SDK to create Cloud Functions and setup triggers.
import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';

// The Firebase Admin SDK to access the Firebase Realtime Database.
admin.initializeApp();

// all functions are bundled together. It's less than ideal, but it does not
// seem possible to split them using the split system for multiple sites from
// https://firebase.google.com/docs/hosting/multisites
import {redirect, token} from './osm_auth';
import { formatProjectTopic, formatUserName } from './utils';

exports.osmAuth = {};

// expose HTTP exposed functions here so that we can pass the admin object
// to them and only instantiate/initialize it once
exports.osmAuth.redirect = functions.https.onRequest((req, res) => {
    redirect(req, res);
});

exports.osmAuth.token = functions.https.onRequest((req, res) => {
    token(req, res, admin);
});

/**
 * Log the userIds of all users who finished a group to /v2/userGroups/{projectId}/{groupId}/.
 * Gets triggered when new results of a group are written to the database.
 * This is the basis to calculate number of users who finished a group (requiredCount and finishedCount),
 * which will be handled in the groupFinishedCountUpdater function.
 *
 * This function also writes to the `contributions` section in the user profile.
 */
exports.groupUsersCounter = functions.database.ref('/v2/results/{projectId}/{groupId}/{userId}/').onCreate(async (snapshot, context) => {
    const db = admin.database();
    const { projectId, groupId, userId } = context.params;

    // these references/values will be updated by this function
    const groupUsersRef = db.ref(`/v2/groupsUsers/${projectId}/${groupId}`);
    const userRef = db.ref(`/v2/users/${userId}`);

    const thisResultRef = db.ref(`/v2/results/${projectId}/${groupId}/${userId}`);


    // Check for specific user ids which have been identified as problematic.
    // These users have repeatedly uploaded harmful results.
    // Add new user ids to this list if needed.
    const userIds: string[] = [];
    if (userIds.includes(userId)) {
        console.log('suspicious user: ' + userId);
        console.log('will remove this result and not update counters');
        return thisResultRef.remove();
    }

    const result = snapshot.val() as {
        appVersion: string | undefined | null,
        results: unknown[],
        endTime: string,
        startTime: string,
    };


    // New versions of app will have the appVersion defined (> 2.2.5)
    // appVersion: 2.2.5 (14)-dev
    const appVersionString = result.appVersion;

    // Check if the app is of older version
    // (no need to check for specific version since old app won't sent the version info)
    if (appVersionString === null || appVersionString === undefined || appVersionString.trim() === '') {
        const projectRef = db.ref(`/v2/projects/${projectId}`);
        const dataSnapshot = await projectRef.once('value');

        if (dataSnapshot.exists()) {
            const project = dataSnapshot.val() as {
                projectType: number,
                customOptions: unknown[],
            };
            // Check if project type is validate and also has
            // custom options (i.e. these are new type of projects)
            if (project.projectType === 2 && project.customOptions) {
                // We remove the results submitted from older version of app (< v2.2.6)
                console.info(`Result submitted for ${projectId} was discarded: submitted from older version of app`);
                return thisResultRef.remove();
            }
        }
    }

    // if result ref does not contain all required attributes we don't updated counters
    // e.g. due to some error when uploading from client
    if (!Object.prototype.hasOwnProperty.call(result, 'results')) {
        console.log('no results attribute for ' + snapshot.ref);
        console.log('will not update counters');
        return null;
    } else if (!Object.prototype.hasOwnProperty.call(result, 'endTime')) {
        console.log('no endTime attribute for ' + snapshot.ref);
        console.log('will not update counters');
        return null;
    } else if (!Object.prototype.hasOwnProperty.call(result, 'startTime')) {
        console.log('no startTime attribute for ' + snapshot.ref);
        console.log('will not update counters');
        return null;
    }

    // check if these results are likely to be vandalism
    // mapping speed is defined by the average time needed per task in seconds
    const numberOfTasks = Object.keys(result['results']).length;
    const startTime = Date.parse(result['startTime']) / 1000;
    const endTime = Date.parse(result['endTime']) / 1000;

    const mappingSpeed = (endTime - startTime) / numberOfTasks;
    if (mappingSpeed < 0.125) {
        // this about 8-times faster than the average time needed per task
        console.log('unlikely high mapping speed: ' + mappingSpeed);
        console.log('will remove this result and not update counters');
        return thisResultRef.remove();
    }

    /*
        Check if this user has submitted a results for this group already.
        If no result has been submitted yet, set userId in v2/groupsUsers.
        Then set this group contribution in the user profile.
        Update overall taskContributionCount and project taskContributionCount in the user profile
        based on the number of results submitted and the existing count values.
    */
    const dataSnapshot = await groupUsersRef.child(userId).once('value');
    if (dataSnapshot.exists()) {
        console.log('group contribution exists already. user: '+userId+' project: '+projectId+' group: '+groupId);
        return null;
    }

    const latestNumberOfTasks = Object.keys(result['results']).length;
    const totalTaskContributionCountRef = userRef.child('taskContributionCount');
    const totalGroupContributionCountRef = userRef.child('groupContributionCount');
    const userContributionRef = userRef.child(`contributions/${projectId}`);
    const taskContributionCountRef = userRef.child(`contributions/${projectId}/taskContributionCount`);
    await Promise.all([
        userContributionRef.child(groupId).set(true),
        groupUsersRef.child(userId).set(true),
        totalTaskContributionCountRef.transaction((currentCount) => {
            return currentCount + latestNumberOfTasks;
        }),
        totalGroupContributionCountRef.transaction((currentCount) => {
            return currentCount + 1;
        }),
        taskContributionCountRef.transaction((currentCount) => {
            return currentCount + latestNumberOfTasks;
        }),
    ]);


    // Tag userGroups of the user in the result
    const userGroupsOfTheUserSnapshot = await userRef.child('userGroups').once('value');
    if (!userGroupsOfTheUserSnapshot.exists()) {
        return null;
    }

    const userGroupsRef = db.ref('/v2/userGroups/');
    const allUserGroupsSnapshot = await userGroupsRef.once('value');
    if (!allUserGroupsSnapshot.exists()) {
        return null;
    }

    const userGroupsOfTheUserKeyList = Object.keys(userGroupsOfTheUserSnapshot.val() as object);
    if (userGroupsOfTheUserKeyList.length <= 0) {
        return null;
    }

    const allUserGroups = allUserGroupsSnapshot.val() as {
        [key: string]: { archivedAt?: unknown } | undefined,
    };
    const nonArchivedUserGroupKeys = userGroupsOfTheUserKeyList.filter((key) => {
        const currentUserGroup = allUserGroups[key];

        // User might have joined some group that was removed but not cleared from their list
        if (!currentUserGroup) {
            return false;
        }

        // Skip groups that have been archived
        if (currentUserGroup.archivedAt) {
            return false;
        }

        return true;
    });

    if (nonArchivedUserGroupKeys.length === 0) {
        return null;
    }

    const nonArchivedUserGroupsOfTheUser = nonArchivedUserGroupKeys.reduce((acc, val) => {
        acc[val] = true;
        return acc;
    }, {} as Record<string, boolean>);

    // Include userGroups of the user in the results
    return thisResultRef.child('userGroups').set(nonArchivedUserGroupsOfTheUser);
});


/**
 * Set group finishedCount and group requiredCount.
 * Gets triggered when new userId key is written to v2/groupsUsers/{projectId}/{groupId}.
 * finishedCount and requiredCount of a group are calculated based on the number of userIds
 * that are present in v2/groupsUsers/{projectId}/{groupId}.
 */
exports.groupFinishedCountUpdater = functions.database.ref('/v2/groupsUsers/{projectId}/{groupId}/').onWrite(async (_, context) => {
    // Set group finishedCount based on number of users that finished this group.
    // Calculate group requiredCount based on number of userIds and verification number.
    // Verification number can be defined on the project level or on the group level.
    // If a verification number is defined for the group,
    // this will surpass the project verification number.
    // This will allow us to either map specific groups more often
    // or less often than other groups in this project.
    const db = admin.database();
    const { projectId, groupId } = context.params;

    const groupVerificationNumberRef = db.ref(`/v2/groups/${projectId}/${groupId}/verificationNumber`);
    const groupVerificationNumberSnaphost = await groupVerificationNumberRef.once('value');

    // check if a verification number is set for this group
    if (groupVerificationNumberSnaphost.exists()) {
        console.log('using group verification number');
        const verificationNumber = groupVerificationNumberSnaphost.val() as number;
        return verificationNumber;
    }

    // use project verification number if it is not set for the group
    const projectVerificationNumberRef = db.ref(`/v2/projects/${projectId}/verificationNumber`);
    const projectVerificationNumberSnapshot = await projectVerificationNumberRef.once('value');
    const projectVerificationNumber = projectVerificationNumberSnapshot.val() as number;

    // FIXME: We should be able to use snapshot.val() instead
    const groupUsersRef = db.ref(`/v2/groupsUsers/${projectId}/${groupId}`);
    const groupUsersSnapshot = await groupUsersRef.once('value');
    const groupUsersCount = groupUsersSnapshot.numChildren();

    // FIXME: Not sure if we only set these if we are using verification number from project
    const groupFinishedCountRef = db.ref(`/v2/groups/${projectId}/${groupId}/finishedCount`);
    const groupRequiredCountRef = db.ref(`/v2/groups/${projectId}/${groupId}/requiredCount`);
    return Promise.all([
        groupFinishedCountRef.set(groupUsersCount),
        groupRequiredCountRef.set(projectVerificationNumber - groupUsersCount),
    ]);
});


/**
 * Count how many projects a users has worked on at v2/users/{userId}/projectContributionCount.
 * This is based on the number of projectIds set in the `contribution` part of the user profile.
 */
exports.projectContributionCounter = functions.database.ref('/v2/users/{userId}/contributions/').onWrite(async (snapshot, context) => {
    const db = admin.database();
    const { userId } = context.params;

    // using after here to check the data after the write operation
    const contributions = snapshot.after.val() as object;

    // these references/values will be updated by this function
    const projectContributionCountRef = db.ref(`/v2/users/${userId}/projectContributionCount`);

    // set number of projects a user contributed to
    const contributionsCount = Object.keys(contributions).length;
    return projectContributionCountRef.set(contributionsCount);
});

/**
 * Generate update commands for PSQL db?
 * Gets triggered when username is changed
 */
exports.usernameUpdate = functions.database.ref('/v2/users/{userId}/username/').onWrite(async (_, context) => {
    const db = admin.database();
    const { userId } = context.params;

    const updatesUserRef = db.ref('/v2/updates/users/');
    return updatesUserRef.child(userId).set(true);
});


/**
 * Generates update commands for PSQL db
 * Gets triggered when new user group is created, update or deleted
 */
exports.userGroupWrite = functions.database.ref('/v2/userGroups/{userGroupId}/').onWrite(async (_, context) => {
    const db = admin.database();
    const { userGroupId } = context.params;

    // FIXME: Do we need to check for undefined userGroupId here?
    if (!userGroupId) {
        return null;
    }

    const updatesUserGroupRef = db.ref('/v2/updates/userGroups/');
    return updatesUserGroupRef.child(userGroupId).set(true);
});

/**
 * Generate update commands for PSQL db?
 * Gets triggered when user joins or leaves a usergroup
 */
exports.userGroupMembershipWrite = functions.database.ref('/v2/userGroupMembershipLogs/{membershipId}').onWrite(async (_, context) => {
    // FIXME: We should use a function to leave/join a group instead
    const db = admin.database();
    const { membershipId } = context.params;

    // FIXME: Do we need to check for undefined userGroupId here?
    if (!membershipId) {
        return null;
    }

    const updatesUserGroupMembershipRef = db.ref('/v2/updates/userGroupMembershipLogs');
    return updatesUserGroupMembershipRef.child(membershipId).set(true);
});


/*

MIGRATION CODE

*/

exports.addProjectTopicKey = functions.https.onRequest(async (_, res) => {
    const db = admin.database();

    try {
        const projectsRef = db.ref('v2/projects');
        const projectsSnapshot = await projectsRef.once('value');
        const projects = projectsSnapshot.val() as { [key: string]: { name?: string } | undefined };

        const isEmptyProject = Object.keys(projects).length === 0;
        if (isEmptyProject) {
            res.status(404).send('No projects found');
        } else {
            const newProjectData: {
                [key: string]: string
            } = {};

            Object.entries(projects).forEach(([projectId, projectData]) => {
                if (projectData?.name) {
                    const projectTopicKey = formatProjectTopic(projectData.name);
                    newProjectData[`v2/projects/${projectId}/projectTopicKey`] = projectTopicKey;
                }
            });

            await db.ref().update(newProjectData);

            const updatedProjectsCount = Object.keys(newProjectData).length;
            res.status(200).send(`Updated ${updatedProjectsCount} projects.`);
        }
    } catch (error) {
        console.log(error);
        res.status(500).send('Some error occurred');
    }
});

exports.addUserNameLowercase = functions.https.onRequest(async (_, res) => {
    const db = admin.database();

    try {
        const usersRef = db.ref('v2/users');
        const usersSnapshot = await usersRef.once('value');
        const users = usersSnapshot.val() as { [key: string]: { username?: string } | undefined };

        const isEmptyUser = Object.keys(users).length === 0;
        if (isEmptyUser) {
            res.status(404).send('No users found');
        } else {
            const newUserData: {
                [key: string]: string
            } = {};

            Object.entries(users).forEach(([id, user]) => {
                if (user?.username) {
                    const usernameKey = formatUserName(user.username);
                    newUserData[`v2/users/${id}/usernameKey`] = usernameKey;
                }
            });

            await db.ref().update(newUserData);

            const updatedUserCount = Object.keys(newUserData).length;
            res.status(200).send(`Updated ${updatedUserCount} users.`);
        }
    } catch (error) {
        console.log(error);
        res.status(500).send('Some error occurred');
    }
});


/*

OLD CODE

We first adjust the functions to return null.
Then we have to manually delete the functions from firebase.
Finally, we can remove the code below.

*/


// Increments or decrements various counters of User and Group once new reults are pushed.
// Gets triggered when new results of a group are written to the database.
exports.resultCounter = functions.database.ref('/v2/results/{projectId}/{groupId}/{userId}/').onCreate(() => {
    return null;
});

// Counters to keep track of contributors and project contributions of Project and User.
// Gets triggered when User contributes to new project.
exports.contributionCounter = functions.database.ref('/v2/users/{userId}/contributions/{projectId}/').onCreate(() => {
    return null;
});

// Increment project.resultCount by group.numberOfTasks.
// Or (Depending of increase or decrease of group.RequiredCount)
// Increment project.resultCount by group.numberOfTasks
//
// project.resultCount represents at init of a project: sum of all tasks * verificationNumber
//
// Gets triggered when group.requiredCount gets changed
exports.projectCounter = functions.database.ref('/v2/groups/{projectId}/{groupId}/requiredCount/').onUpdate(() => {
    return null;
});

// Calculates group.progress
//
// Gets triggered when group.requiredCount gets changed
exports.calcGroupProgress = functions.database.ref('/v2/groups/{projectId}/{groupId}/requiredCount/').onUpdate(() => {
    return null;
});

// Calculates project.progress
//
// Gets triggered when project.resultCount gets changed.
exports.incProjectProgress = functions.database.ref('/v2/projects/{projectId}/resultCount/').onUpdate(() => {
    return null;
});

// Calculates project.progress
// Almost the same function as the previous one
//
// Gets triggered when project.requiredResults gets changed.
exports.decProjectProgress = functions.database.ref('/v2/projects/{projectId}/requiredResults/').onUpdate(() => {
    return null;
});
