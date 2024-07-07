#!/bin/bash
source $(conda info --base)/etc/profile.d/conda.sh
conda activate myenv
python gui.py
read -p "Press any key to continue..."