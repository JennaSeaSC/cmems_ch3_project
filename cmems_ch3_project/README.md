## 🐢 CMEMS Chapter 3 Turtle Project

This repository contains scripts and data structure for Chapter 3 of my dissertation: modeling sea turtle strandings in relation to oceanographic data (SST, wind, etc.) from CMEMS.

## CMEMS Data Directory

This folder contains all raw and processed Copernicus Marine Environment Monitoring Service (CMEMS) data used in Chapter 3.

### Structure

- `raw/` — untouched downloaded data
- `processed/` — post-processed files used for analysis (e.g., averages, subsets, interpolated)

## 📁 Folder Overview

- `data/raw/` – Raw downloads (SST, wind)
- `data/processed/` – Cleaned datasets
- `outputs/` – Figures and model-ready data
- `notebooks/` – Exploratory data analysis (EDA) notebooks
- `src/` – Scripts and data pipelines
- `metadata/` – Download logs, notes, etc.

## 🔧 Environment Setup

```bash
conda create -n turtles python=3.11
conda activate turtles
pip install -r requirements.txt

