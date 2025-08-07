# NOTE: If you make any BREAKING CHANGE:
# - Update the Docker image tag in `./.github/workflows/docker-push-dev.yml`
# - Update the `mapswipe-backend` workflow to use the new image tag
FROM node:20-bullseye-slim

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        openjdk-11-jdk bash procps git \
    && corepack enable \
    && corepack prepare pnpm@10.6.1 --activate

WORKDIR /firebase

# renovate: datasource=github-tags depName=firebase/firebase-tools
ARG FIREBASE_TOOLS_VERSION=14.5.1

RUN --mount=type=cache,target=/root/.npm \
    npm install -g firebase-tools@$FIREBASE_TOOLS_VERSION \
    # Download jar files
    && firebase setup:emulators:database \
    && firebase setup:emulators:firestore \
    && firebase setup:emulators:storage \
    && firebase setup:emulators:ui
