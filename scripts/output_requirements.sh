#!/bin/bash

cd "$(dirname "$0")/../code" && pip list --format=freeze > requirements.txt
