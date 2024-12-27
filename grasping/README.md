# MIE_1075
Project Name:
Shopping Assistant Robot

#### Grasping
The simulation has been performced using Isaac Sim and Isaac Lab (https://isaac-sim.github.io/IsaacLab/main/index.html).
Please follow the instructions in the website to install Isaac Sim and Lab.


Training was performed using the provided rl_games workflow wrapper (https://isaac-sim.github.io/IsaacLab/main/source/overview/reinforcement-learning/rl_existing_scripts.html)
```
python source/standalone/workflows/rl_games/train.py --task=Isaac-Lift-Cube-Franka-v0
```
The trained model was tested using
```
python source/standalone/workflows/rl_games/play.py --task=Isaac-Lift-Cube-Franka-Play-v0 --checkpoint /home/sourabh/project/IsaacLab/logs/rl_games/franka_lift/2024-12-23_17-29-54/nn/franka_lift.pth
```