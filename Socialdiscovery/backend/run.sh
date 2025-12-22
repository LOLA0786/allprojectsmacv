#!/bin/bash
export PYTHONPATH=$(pwd)
uvicorn app.main:app --port 8000
