#!/bin/bash

#SBATCH --partition=hpxg     #申请分区 `hpxg` 的计算资源   
#SBATCH --ntasks=8

cd mapAnalog
python3 analog.py
cd ..
cd tracking
python3 track.py
