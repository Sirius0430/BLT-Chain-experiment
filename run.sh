#!/bin/bash

#SBATCH --partition=hpib 
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --account=feiteng


arr=("[0.99,0.01]" "[0.975,0.025]" "[0.95,0.05]" "[0.9,0.1]" "[0.8,0.2]" "[0.5,0.5]")

for i in "${arr[@]}"
do
echo -e "\n$i start\n"
python3 modifyPyFile.py $i
cd mapAnalog
python3 analog.py
cd ..
cd tracking
python3 track.py
cd ..
echo -e "\n$i done!\n"

done


