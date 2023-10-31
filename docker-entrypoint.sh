#!/bin/bash
set -e

if [ "$1" = 'batchee' ]; then
  exec batchee "$@"
elif [ "$1" = 'batchee_harmony' ]; then
  exec batchee_harmony "$@"
else
  exec batchee_harmony "$@"
fi
