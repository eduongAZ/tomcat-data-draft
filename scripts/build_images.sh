#!/bin/bash

source "$(dirname "$0")/output_requirements.sh"

docker compose build
