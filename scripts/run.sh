#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

pushd $DIR/..
git pull
/home/dsuo/miniconda3/envs/provid/bin/python $DIR/../provid/source/__init__.py
git commit -am "Update data"
git push
popd
