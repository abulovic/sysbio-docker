#!/usr/bin/env bash

DIR=`pwd`

if [ ! -d "$DIR/models" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  mkdir $DIR/models
fi

if [ ! -d "$DIR/output" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  mkdir $DIR/output
fi

docker run -ti -v $DIR/models/:/home/user/models -v $DIR/code/:/home/user/code -v $DIR/output/:/home/user/output sysbio
