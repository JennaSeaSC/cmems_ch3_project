## 🐢 CMEMS Chapter 3 Turtle Project

This repository contains scripts and data structure for Chapter 3 of my dissertation: modeling sea turtle strandings in relation to oceanographic data (SST, wind, etc.) from CMEMS.

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

