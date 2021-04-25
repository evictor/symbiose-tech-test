#!/usr/bin/env bash
script_dir=$(dirname "$0")
pushd "$script_dir"/.. || exit
docker-compose up --build dev
popd || exit
