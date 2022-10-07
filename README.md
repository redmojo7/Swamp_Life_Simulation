# Swamp Life Simulation
## Contents
- border.py - Boundaries: Stop the beings going beyond the grid(window).
- config.py	- Configration file initialize windows size and number of creatures.
- grid.py - Move creatures(update cells), add new creatures and remove died creartures.
- map.py - The map of this simulation, which include mountains position and all alive creatures
- swamp.py - Definition of class Creature, Duck, Newt and Shrimp.
- grass.py - 	To reproduce soome grass(food).
- main.py - Entry point, the main function of Simulation.
- simulation.py - Show simulation info on screen, store app states for each step, and resume simulation from a CSV file.
- terrain.py - Initial terrain for the map, and draw terrain on the screen.
- tools.py - Some tools function, such as manhattan_distance()
## others
- png - image directory 			
- test - test directory		
- config - configuration directory
- output - output directory, which be used as 
## Dependencies
- python3-pygame
- python-math
- numpy
## Version information
24 Sep 2022 - initial version of Swamp Life Simulation
## How to run the program
### Install imported libraries(python3-pygame,python-math,numpy)
```
sudo apt-get install python3-pygame
pip install python-math
pip install numpy
```
### Start it by Running:
```
python3 main.py
```
