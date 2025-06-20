#!/bin/bash

set -e

# TODO: This may need another look
cd functions
yarn install --frozen-lockfile
yarn build
cd ../

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
firebase emulators:start --import="$FIREBASE_EMULATOR_DATA_DIR" --export-on-exit &
pid="$!"


# Keep container alive with dummy tail
tail -f /dev/null &
tail_pid="$!"

# Wait on both Firebase and tail, exit if either ends
wait -n "$pid" "$tail_pid"

# If we got here without a signal, something ended unexpectedly
echo "[ERROR] Firebase or keep-alive process exited unexpectedly"
exit 1
