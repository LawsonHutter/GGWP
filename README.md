## Shit we need to figure out:
* State structure
  * Position
  * Health bars and Nexus (generalized to one-shot, medium, full)
  * Do we need to consider projectiles?
  
* How will we handle concurrent time steps?
 
* Assume random policy for user, create MDP optimal policy for cpu based on random user policy

## Goals
* 2 player reachability with mdp model to predict user movement from cpu perspective.  Just nexus and 2 players.  3x8 grid.
  * Action Space:  Auto-melee attack, ranged ability, flash

* Larger grid, tune cpu ai.  Potentially look at the concurrent time game optimal policy papers.  Or, tune action policy.
  * Maybe have it learn player movements as time goes on

## L Hutt:
* Sprite structure / state structure
* Pygame
* Player input

## K-Slayer:
* ggsolver stuff
* cpu player
