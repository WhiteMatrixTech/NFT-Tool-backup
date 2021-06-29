#!/usr/bin/env bash

cd ..
docker build . -t renderjob
ROOT=$(pwd)
echo "Path is $ROOT/data"
cd scripts
#docker run -v $ROOT/data:/data -it renderjob bash "./scripts/test_run_pawn.sh"
docker run -v $ROOT/data:/data --env-file ../.env renderjob