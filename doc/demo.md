Brownian Dynamics in IMP {#demo}
========================

[TOC]

In this section, we show how to setup and run a Brownian Dynamics simulation
in %IMP. To follow the tutorial, first download the data files, either by
[cloning the GitHub repository](https://github.com/salilab/imp_brownian_dynamics_tutorial)
or by [downloading the zip file](https://github.com/salilab/imp_brownian_dynamics_tutorial/archive/master.zip).

# Representing parts {#repparts}

To represent parts of the system, we use a number of Python classes provided
by %IMP:

 - [IMP.Model](@ref IMP::Model)
   A container for all of the system’s parts 

 - [IMP.Particle](@ref IMP::Particle)
   A particle is the elementary data unit  describing a system part in %IMP

 - [IMP.Decorator](@ref IMP::Decorator)
   Dynamic descriptors of the properties of %IMP particles

   - [core::XYZR](@ref IMP::core::XYZR)
   - [atom::Hierarchy](@ref IMP::atom::Hierarchy)
   - [atom::Diffusion](@ref IMP::atom::Diffusion)

 - [IMP.container](@ref IMP::container)
   Static or dynamic collections of particles, particle pairs, etc.

To see these classes used in an simulation, look at the file `pbc_simple.py`
in the `scripts` directory. First, we create an %IMP
[Model](@ref IMP::Model), and set up the root of a
[hierarchy of particles](@ref IMP::atom::Hierarchy):

\code{.py}
m = IMP.Model()
p_root= IMP.Particle(m, "root")
h_root = IMP.atom.Hierarchy.setup_particle(p_root)
\endcode

Next, we can set up a coarse-grained nucleus by calling the `create_nucleus`
function. The nucleus particle is given XYZ coordinates and a radius using
the [XYZR decorator](@ref IMP::core::XYZR). We then
[add it](@ref IMP::atom::Hierarchy::add_child) to the existing hierarchy:

\code{.py}
def create_nucleus(m, R):
    '''
    Generate a coarse-grained spherical nuclear envelope
    of radius R in model m
    '''
    p= IMP.Particle(m, "nucleus")
    xyzr = IMP.core.XYZR.setup_particle(p)
    xyzr.set_coordinates_are_optimized(True)
    xyzr.set_coordinates([0,0,0])
    xyzr.set_radius(R)
    IMP.atom.Mass.setup_particle(p, 1.0) # fake mass
    IMP.display.Colored.setup_particle(p,
                                       IMP.display.get_display_color(2))
    IMP.atom.Hierarchy.setup_particle(p)
    return p

p_nucleus= create_nucleus(m, R_NUCLEUS)
h_nucleus= IMP.atom.Hierarchy(p_nucleus)
h_root.add_child(h_nucleus)
\endcode

Next, we create a number of insulin granules at random locations in the
cytoplasm. This is done using a simple piece of code, that creates similar
XYZR particles, in `GranuleFactory.py`:

\code{.py}
        p= IMP.Particle(self.model, name)
        xyzr= IMP.core.XYZR.setup_particle(p)
        xyzr.set_coordinates_are_optimized(True)
        v= get_random_vector_in_cytoplasm(self.cell_sphere,
                                          self.nucleus_sphere)
        xyzr.set_coordinates(v)
        xyzr.set_radius(self.default_R)
        IMP.atom.Mass.setup_particle(p, 1)   # fake mass required by Hierarchy
        IMP.atom.Hierarchy.setup_particle(p) # allow inclusion in IMP hierarchies
        IMP.display.Colored.setup_particle(p,
                                           IMP.display.get_display_color(0))
\endcode

# Representing interactions {#repinteract}

Next, we need to tell %IMP the nature of the interactions in the system.
These are handled by several %IMP classes:

 - [Scores](@ref IMP::SingletonScore) evaluate some property of the system,
   for example [how far a particle is outside of a sphere](@ref IMP::core::BoundingSphere3DSingletonScore).

 - [Restraints](@ref IMP::Restraint) apply Scores to a subset of the system.

 - [Containers](@ref IMP::container) describe the subsets that the Restraints
   use.

# Representing dynamics {#repdynamics}

Finally we can tell %IMP to run Brownian Dynamics. This uses the
[IMP.atom.BrownianDynamics](@ref IMP::atom::BrownianDynamics) class. We can
set properties of the simulation, such as the temperature and number of
time steps, request output of the trajectory in RMF format (using the
[add_optimizer_state method](@ref IMP::Optimizer::add_optimizer_state)), 
and then finally run the simulation by calling
[optimize](@ref IMP::Optimizer::optimize).

# Running the script {#running}

The script can be run with Python by simply running:

\code{.sh}
python pbc_simple.py
\endcode

# Visualization {#visualization}

The final RMF trajectory can be viewed in UCSF Chimera.

# Next steps {#nextsteps}

This demonstration uses a very simple representation of the insulin
granules. See also `pbc_patches.py` and `pbc_interacting_patches.py`
for similar scripts that use a more realistic representation.
