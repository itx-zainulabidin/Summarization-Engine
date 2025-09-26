#!/bin/bash
export PYTHONPATH=./src
uvicorn src.api.main:app --reload --port 8000
