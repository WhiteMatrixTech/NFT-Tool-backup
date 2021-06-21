#!/usr/bin/env bash

docker build . -t renderjob
docker run -it renderjob bash "./test_run_pawn.sh"
