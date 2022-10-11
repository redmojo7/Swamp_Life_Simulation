# Swamp Life Simulation
## Contents
- border.py - Boundaries: Stop the beings going beyond the grid(window).
- config.py	- Configration file initialize windows size and number of creatures.
- grid.py - Move creatures(update cells), add new creatures and remove died creartures.
- map.py - The map of this simulation, which include mountains position and all alive creatures.
- swamp.py - Definition of class Creature, Duck, Newt and Shrimp.
- grass.py - 	To reproduce soome grass(food).
- main.py - Entry point, the main function of Simulation.
- simulation.py - Show simulation info on screen, store app states for each step, and resume simulation from a CSV file.
- terrain.py - Initial terrain for the map, and draw terrain on the screen.
- tools.py - Some tools function, such as manhattan_distance().
## Test
- SwampTest.py - Unit test for swamp.py.
- ToolsTest.py - Unit test for tools.py.
- TestInteractWithFood.py - Integration test for interactions (tracking or fleet).
## Others
- png - Image directory. 				
- config - Configuration directory.
- output - Output directory, which be used to store application states and resume app from CSV file.
## Dependencies
- python3-pygame
- python-math
- numpy
## Version information
24 Sep 2022 - Initial version of Swamp Life Simulation.
## How to run the program
### Install imported libraries(python3-pygame,python-math,numpy)
```
sudo apt-get install python3-pygame
pip install python-math
pip install numpy
pip3 install pyyaml
```
### Start it by Running:
```
python3 main.py
```
