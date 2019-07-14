#!/usr/bin/env bash

PYTHONUNBUFFERED=1
VENV="wappuradio-scrobbler-venv"

function activate_venv {
    if [ "$OSTYPE" = "msys" ]; then
        source $VENV/Scripts/activate
    else
        source $VENV/bin/activate
    fi
}

if [ ! -d "$VENV" ]; then
    if [ "$OSTYPE" = "msys" ]; then
        python -m venv $VENV
    else
        python3 -m venv $VENV
    fi

    activate_venv
    pip install -r requirements.txt
fi

if [[ "$VIRTUAL_ENV" == "" ]]; then
    activate_venv
fi

source env.sh

if [ "$OSTYPE" = "msys" ]; then
    python main.py
else
    python3 main.py
fi
