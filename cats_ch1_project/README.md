# 🐢 Chapter 1: CATS Tag Analysis

This repo processes and analyzes data collected from CATS biologging tags deployed on green sea turtles (*Chelonia mydas*). Dive profiles, kinematics, and behavioral metrics are explored to understand habitat use and movement patterns in a shallow, urbanized bay.

---

## 📁 Folder Structure

- `src/` — Python scripts for cleaning, parsing, and analysis
- `data/raw/` — Raw CATS tag files (untouched)
- `data/processed/` — Cleaned and structured CSVs
- `notebooks/` — Jupyter notebooks for exploration and visualization
- `outputs/` — Figures, tables, and exported results
- `metadata/` — Tag deployment logs, config files, and references

---

## ⚙️ Environment Setup

```bash
conda create -n cats python=3.11
conda activate cats
pip install -r requirements.txt
