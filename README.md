# Clara AI Agent Automation Pipeline

## Overview
This project builds an automation pipeline that converts demo call transcripts into
preliminary AI voice agents and updates them using onboarding calls.

## Architecture

Demo transcript
   → extractor
   → account memo JSON
   → prompt generator
   → agent spec v1

Onboarding transcript
   → extractor
   → diff engine
   → agent spec v2
   → changelog

## How to Run

activate environment

python -m scripts.run_pipeline

## Output Structure

outputs/accounts/<account_id>/
   v1/
   v2/
   changes.json