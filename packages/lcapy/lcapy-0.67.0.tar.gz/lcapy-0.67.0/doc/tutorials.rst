=========
Tutorials
=========


Noise analysis
==============


RC network
----------

Let's consider the thermal noise produced by a resistor in parallel
with a capacitor.  Now only the resistor produces thermal noise (white
Gaussian noise) but the capacitor and resistor form a filter so the
resultant noise is no longer white.  The interesting thing is that the
resultant noise voltage only depends on the capacitor value.  This can
be demonstrated using Lcapy.   Let's start by creating the circuit:

   >>> from lcapy import *
   >>> a = Circuit("""
   ... R 1 0; down
   ... W 1 2; right
   ... C 2 0_2; down
   ... W 0 0_2; right""")
   >>> a.draw()

.. image:: examples/tutorials/RCnoise/RCparallel1.png
   :width: 4cm

A noisy circuit model can be created with the `noisy()` method of the circuit object.   For every resistor in the circuit, a noisy voltage source is added in series.  For example,

   >>> b = a.noisy()
   >>> b.draw()

.. image:: examples/tutorials/RCnoise/RCparallel1noisy.png
   :width: 4cm
        
The noise voltage across the capacitor can be found using:

   >>> Vn = b.C.V.n
   >>> Vn
       2⋅√R⋅√T⋅√k   
   ─────────────────
      ______________
     ╱  2  2  2     
   ╲╱  C ⋅R ⋅ω  + 1 

Note, this is the (one-sided) amplitude spectral density with units of volts per root hertz.  Here `T` is the absolute temperature in degrees kelvin, `k` is Boltzmann's constant, and :math:`\omega` is the angular frequency.  The expression can be made a function of linear frequency using:

   >>> Vn(f)
         2⋅√R⋅√T⋅√k      
   ──────────────────────
      ___________________
     ╱    2  2  2  2     
   ╲╱  4⋅π ⋅C ⋅R ⋅f  + 1 

This expression can be plotted if we substitute the symbols with numbers.  Let's choose :math:`T = 293` K, :math:`R = 10` kohm, and :math:`C = 100` nF.

   >>> Vns = Vn.subs({'R':10e3, 'C':100e-9, 'T':293, 'k':1.38e-23})
   >>> Vns(f)
              √101085           
   ─────────────────────────────
                    ____________
                   ╱  2  2      
                  ╱  π ⋅f       
   25000000000⋅  ╱   ────── + 1 
               ╲╱    250000     

Note, Lcapy tries to approximate all numbers with integers.  A floating point representation can be found with the `evalf()` method:

   >>> Vns(f).evalf()               
                                                     -0.5
                       ⎛                     2      ⎞    
   1.27175469332729e-8⋅⎝3.94784176043574e-5⋅f  + 1.0⎠    

The amplitude spectral density of the noise can be plotted by definining a vector of frequency samples:

   >>> from numpy import linspace
   >>> vf = linspace(0, 10e3, 200)
   >>> (Vns(f) * 1e9).plot(vf, plot_type='mag', ylabel='ASD (nV/rootHz'))
 

.. image:: examples/tutorials/RCnoise/RCparallel1noiseplot1.png
   :width: 10cm   

Finally, the rms noise voltage can be found using the `rms()` method.  This integrates the square of the ASD (the power spectral density) over all frequencies and takes the square root.  For this example, the rms value does not depend on R.

   >>> Vn.rms()
   √T⋅√k
   ─────
     √C 


Opamp non-inverting amplifier
-----------------------------

This tutorial looks at the noise from an opamp non-inverting
amplifier.  It uses an ideal opamp with open-loop gain `A` augmented
with a voltage source representing the input-referred opamp voltage
noise, and current sources representing the input-referred opamp
current noise.

   >>> from lcapy import *
   >>> a = Circuit("""
   ... Rs 1 0; down
   ... Vn 1 2 noise; right
   ... W 2 3; right
   ... In1 2 0_2 noise; down, l=I_{n+}
   ... W 0 0_2; right
   ... In2 5 0_5 noise; down, l=I_{n-}
   ... W 5 4; right
   ... W 0_2 0_5; right
   ... W 4 6; down
   ... R1 6 0_6; down
   ... W 0_5 0_6; right
   ... R2 6 7; right
   ... W 8 7; down
   ... E 8 0 opamp 3 4 A; right
   ... W 8 9; right
   ... W 0_6 0_9; right
   ... P 9 0_9; down
   ... ; draw_nodes=connections, label_nodes=none""")
   >>> a.draw()

.. image:: examples/tutorials/opampnoise/opamp-noninverting-amplifier.png
   :width: 10cm

The noise ASD at the input of the opamp is
           
   >>> a[3].V.n
      ____________________________
     ╱    ⎛   2           ⎞     2 
   ╲╱  Rₛ⋅⎝Iₙ₁ ⋅Rₛ + 4⋅T⋅k⎠ + Vₙ  

This is independent of frequency and thus is white.  In practice, the voltage and current noise of an opamp has a 1/f component at low frequencies.

The noise at the output of the amplifier is

   >>> a[8].V.n   
        _____________________________________________________
       ╱    2   2          2      2   2   2     2          2 
   A⋅╲╱  Iₙ₁ ⋅Rₛ ⋅(R₁ + R₂)  + Iₙ₂ ⋅R₁ ⋅R₂  + Vₙ ⋅(R₁ + R₂)  
   ──────────────────────────────────────────────────────────
                         A⋅R₁ + R₁ + R₂                      

Assuming an infinite open-loop gain this simplifies to

   >>> a[8].V.n.limit('A', oo)
      _____________________________________________________
     ╱    2   2          2      2   2   2     2          2 
   ╲╱  Iₙ₁ ⋅Rₛ ⋅(R₁ + R₂)  + Iₙ₂ ⋅R₁ ⋅R₂  + Vₙ ⋅(R₁ + R₂)  
   ────────────────────────────────────────────────────────
                              R₁                           

This is simply the input noise scaled by the amplfier gain :math:`1 + R_2/R_1`.

So far the analysis has ignored the noise due to the feedback resistors.   The noise from these resistors can be modelled with the `noisy()` method of the circuit object.

   >>> b = a.noisy()
   >>> b.draw()

.. image:: examples/tutorials/opampnoise/opamp-noninverting-amplifier-noisy.png
   :width: 10cm


Let's choose :math:`R2 = (G - 1) R_1` where :math:`G` is the closed-loop gain:

   >>> c = b.subs({'R2':'(G - 1) * R1'})
   >>> c[8].V.n.limit('A', oo)

Unfortunately, this becomes unmanageable since SymPy has to assume that :math:`G` may be less than one.   So instead, let's choose :math:`G=10`,

   >>> c = b.subs({'R2':'(10 - 1) * R1'})
   >>> c[8].V.n.limit('A', oo)
      ________________________________________________________________
     ╱        2   2         2   2                                   2 
   ╲╱  100⋅Iₙ₁ ⋅Rₛ  + 81⋅Iₙ₂ ⋅R₁  + 360⋅R₁⋅T⋅k + 400⋅Rₛ⋅T⋅k + 100⋅Vₙ  

In practice, both noise current sources have the same ASD.  Thus

   >>> c = b.subs({'R2':'(10 - 1) * R1', 'In2':'In1'})
   >>> c[8].V.n.limit('A', oo)
      _________________________________________________________________
     ╱        2   2        ⎛     2            ⎞                      2 
   ╲╱  100⋅Iₙ₁ ⋅Rₛ  + 9⋅R₁⋅⎝9⋅Iₙ₁ ⋅R₁ + 40⋅T⋅k⎠ + 400⋅Rₛ⋅T⋅k + 100⋅Vₙ  

The noise is minimised by keeping `R1` as small as possible.  However, for high gains, the noise is dominated by the opamp noise.  Ideally, `Rs` needs to be minimised.  However, if it is large, it is imperative to choose a CMOS opamp with a low noise current.   Unfortunately, these amplifiers have a higher noise voltage than bipolar opamps.
   
