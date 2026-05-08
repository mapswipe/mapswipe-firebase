#!/bin/bash

set -xe

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FIREBASE_FUNCTIONS_DIR="$BASE_DIR/functions/"

cd "$BASE_DIR"

echo "[INFO] Installing dependencies for transpiling functions for Firebase..."
cd /tmp/

pnpm --dir "$FIREBASE_FUNCTIONS_DIR" install --frozen-lockfile

echo "[INFO] Transpiling functions for Firebase..."
cd "$FIREBASE_FUNCTIONS_DIR"

cd "$BASE_DIR"

firebase use "${FIREBASE_PROJECT?error}"

firebase target:apply hosting auth "$FIREBASE_AUTH_SITE"

firebase functions:config:set \
  osm.redirect_uri="$OSM_OAUTH_REDIRECT_URI" \
  osm.redirect_uri_web="$OSM_OAUTH_REDIRECT_URI_WEB" \
  osm.app_login_link="$OSM_OAUTH_APP_LOGIN_LINK" \
  osm.app_login_link_web="$OSM_OAUTH_APP_LOGIN_LINK_WEB" \
  osm.api_url="$OSM_OAUTH_API_URL" \
  osm.client_id="$OSM_OAUTH_CLIENT_ID" \
  osm.client_id_web="$OSM_OAUTH_CLIENT_ID_WEB" \
  osm.client_secret="$OSM_OAUTH_CLIENT_SECRET" \
  osm.client_secret_web="$OSM_OAUTH_CLIENT_SECRET_WEB"

if [ "${SKIP_HOSTING:-false}" != "true" ]; then
  firebase deploy --only hosting
fi

firebase deploy --only database

export FIREBASE_CLI_IMAGE_CLEANUP_DAYS=${FIREBASE_CLI_IMAGE_CLEANUP_DAYS:-30}
firebase deploy --only functions --non-interactive
