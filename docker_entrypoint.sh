#!/bin/bash

set -e

FIREBASE_EMULATOR_FUNCTIONS_DISABLED=${FIREBASE_EMULATOR_FUNCTIONS_DISABLED:-false}

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FIREBASE_FUNCTIONS_DIR="$BASE_DIR/functions/"


cd "$BASE_DIR"

if [ $FIREBASE_EMULATOR_FUNCTIONS_DISABLED != "true" ]; then
    # NOTE: when we are using mapswipe-firebase as a submodule inside docker,
    # the .git directory is not accessible. The parent .git directory is in host
    # system not accesssible by the container
    # Inside the container, pnpm install fails when we are installing packages from git repository.
    # So, we need to switch to /tmp directory as a workaround
    echo "[INFO] Installing dependencies for transpiling functions for Firebase..."
    cd /tmp/
    pnpm --dir "$FIREBASE_FUNCTIONS_DIR" install --frozen-lockfile

    echo "[INFO] Transpiling functions for Firebase..."
    cd "$FIREBASE_FUNCTIONS_DIR"
    pnpm build
fi

# PIDs
pid=0
tail_pid=0

# Signal handler for graceful shutdown
graceful_shutdown() {
  echo "[INFO] Caught termination signal. Forwarding to Firebase emulator..."

  if kill -0 "$pid" 2>/dev/null; then
    kill -TERM "$pid"
    wait "$pid"
  fi

  if kill -0 "$tail_pid" 2>/dev/null; then
    kill "$tail_pid"
    wait "$tail_pid"
  fi

  echo "[INFO] Firebase shut down gracefully, export should be complete."
  exit 0
}

# Trap SIGINT and SIGTERM for Docker shutdown

trap graceful_shutdown SIGINT SIGTERM

# Start Firebase emulator in background
echo "[INFO] Starting Firebase emulator..."
FIREBASE_EMULATOR_DATA_DIR=${FIREBASE_EMULATOR_DATA_DIR?FIREBASE_EMULATOR_DATA_DIR is required}
if [ $FIREBASE_EMULATOR_FUNCTIONS_DISABLED != "true" ]; then
    firebase emulators:start --import="$FIREBASE_EMULATOR_DATA_DIR" --export-on-exit &
    pid="$!"
else
    firebase emulators:start --only database,hosting,auth --import="$FIREBASE_EMULATOR_DATA_DIR" --export-on-exit &
    pid="$!"
fi


# Keep container alive with dummy tail
tail -f /dev/null &
tail_pid="$!"

# Wait on both Firebase and tail, exit if either ends
wait -n "$pid" "$tail_pid"

# If we got here without a signal, something ended unexpectedly
echo "[ERROR] Firebase or keep-alive process exited unexpectedly"
exit 1
