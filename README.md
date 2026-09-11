# Welcome

Welcome to my Master's Dissertation repo where Physical Reservoir Computing (PRC) is investigated in controlling compliant soft bodies. 
Our goal is for the soft body and PRC controller to evolve towards autonomous locomotion. 

We use the soft body itself as the reservoir, using the displacement of springs at time step t as the input, multiply by some weight matrix, to output the updated rest length of springs for the next time step or t + 1. 
Updating the rest length of springs on the fly allows us to dynamically alter the force exerted by the springs. Reduce the rest lengths and the spring contracts, increaase the rest length and the spring expands.

# Where to start

The **main.py** file is a visual demonstration of what the entities are evolving to do. By taking the weight matrix of the "fittest" entities and plugging it into main.py, we can see how the entities are moving.

The **ga_main.py** file was my own Genetic Algorithm implementation, however, this lacked multiprocessing and thus was significantly slower than utilising the Pygad package.

The **pygad_main.py** file is where the real work happens, utilising the Pygad package for a multiprocessing Genetic Algorithm, we evolve our entities toward locomotion.

# Final Evolved Result

After 348 generations, with an initial population of 200 genotypes, the following locomotion was produced.

The genetic algorithm has found a weight matrix that allows the soft body to traverse downwards with a gait that looks disturbingly like walking.

<img width="800" height="450" alt="EvolvedGif" src="https://github.com/user-attachments/assets/bea2c75d-a32c-474e-8f43-64609776bc59" />

To introduce some kind of friction to the simulation, an alternating pattern of locking particles in place was introduced. This is depicted by the particles (typically in white) turning red, meaning they are locked in place.

The 2 particles on the right hand side of the entity are locked for 5 seconds and then the opposite particles are locked. This was a simpler alternative than introducing friction into the simulation, where different particles have different friction or resistance values.

Friction, while the ideal scenario, would add an entirely new dimension to the simulation and to the genetic algorithm that would need to be optimised. With limited time, a simple lock particles in place alternative was introduced.

Notice at the start of the simulation the soft body is disfigured into a pattern that allows the body to "walk", but does not properly maintain it's internal volume as expected when utilising the Ideal Gas Law (IGL). 

This is due to a programmatic error when initially implementing the IGL that allowed this to happen. This error was corrected later in the project, but results were not as successful.

# Reservoir Computing

The Fully Connected Square entity (see further down) forms the basis of an implementation of Reservoir Computing (RC).

Springs have an initial set rest length, should springs extend to be more than 5 times the size of this initial rest length, they "break"
- A broken spring no longer exerts a force
- Furthermore they are no longer drawn to the screen

![BreakingSpringsGIF](https://user-images.githubusercontent.com/60474698/181378437-ab06ef45-6faf-4941-9607-d721bd6c5f32.gif)

- Spring displacements are fed into a randomly initialised weight matrix
- The output becomes the springs new rest length

![InitReservoirGif](https://user-images.githubusercontent.com/60474698/181374108-58aa98d3-b655-44e1-90ae-09e2dd127a48.gif)


# Soft Body - Fully Connected Square Entity
- Simulation updated from PyGame led to mathematical basis.
- Instead of utilising pygame.clock to set the pace of the simulation, time is incremented (dt) by 0.01 per iteration
- All physics equations use this dt to calculate forces, velocity and distance moved
- Damping factor of 0.98 is used mostly, however adjusted per entity as needed

![FCSquareGif](https://user-images.githubusercontent.com/60474698/181373654-cacfdd41-6707-44cf-b6b8-42f75955e455.gif)

Damping of 0.99, Different sizes of soft bodys react differently to different damping values
Springs appear to "support" each other in larger bodies

![DifferentSizesGif](https://user-images.githubusercontent.com/60474698/181380023-59d06e53-f8c5-4374-9af9-1391c885b02e.gif)

- Square starts out stretched out, the springs attempt to return to their rest lengths.
- Particles are still present but are not being drawn to the screen for a clearer display and to save processing power.


# Mass Spring Damper Investigation
Testing Mass Spring Dampers in Python.
- PyGame is used purely to animate the calculations giving visual representation 

## Entity Investigation

![TowardEleganGif](https://user-images.githubusercontent.com/60474698/181374686-da4f568d-b4ed-4e42-93bd-1e4507fc6664.gif)

Rope like entity, springs connected in a long chain.
- First particle instantiated in the entity is labelled as the entity's "head"
- Head responds to mouse input, can be moved around and "locked" in place
- When a particle is locked in place, it is unaffected by phyics


Spring colour changing based on force being exerted.
- Simulation slowed down to 30 frames per second (FPS) and Springs drawn thicker to better show colour change.

![SpringColour2Gif](https://user-images.githubusercontent.com/60474698/174324994-8c18d11a-402b-433c-87a0-ad3003d47ed1.gif)

Square Implementation with particles losing 1% of velocity every frame / iteration.

![Square gif](https://user-images.githubusercontent.com/60474698/172199022-434b1dc7-ad2d-4cc8-a107-193531ee5eef.gif)


Square behaviour when particles maintain velocity.

![InfiniteSquareGif](https://user-images.githubusercontent.com/60474698/172199059-3622318e-ffce-4b36-a035-09a6e262402f.gif)

## Basic Spring Origins

2D Spring Implementation with some simple Gravity.

![2DSpringGravityGif](https://user-images.githubusercontent.com/60474698/172057802-787e26fa-705d-4cd3-9d14-410c531acba7.gif)

Initial spring implementation operating only on the Y axis.

![1d Spring Gif](https://user-images.githubusercontent.com/60474698/172019510-8bd3294e-d22e-4686-89ae-364b7dd9227e.gif)
