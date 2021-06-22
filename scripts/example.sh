#!/usr/bin/env bash

cd ..
docker build . -t renderjob
cd scripts
docker run -it renderjob bash "./scripts/test_run_pawn.sh"
