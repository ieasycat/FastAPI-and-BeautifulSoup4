#! /bin/bash

aerich upgrade

uvicorn app:app --reload --host 0.0.0.0 --port 8000

