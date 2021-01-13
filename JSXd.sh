#!/bin/bash

ROOT_DIR="/home/chengtong/auto-fuzz/fuzzing_platform/static/js/react"
SOURCE_DIR="$ROOT_DIR/src"
PRODUCTION_DIR="$ROOT_DIR/prod"
npx babel --watch $SOURCE_DIR --out-dir $PRODUCTION_DIR --presets react-app/prod
