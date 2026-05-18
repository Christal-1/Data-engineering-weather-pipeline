@echo off
cd /d C:\Users\christalhaines\Downloads\data_engineering_project

python scripts/ingest.py
python scripts/transform.py