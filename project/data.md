<pre><code>
* d0:       crs                 Data specific   useless
* d1:       name                Data specific   shows City we're in (guess)   
* d2:       streets_per_node    Node specific   Mostly unnused
* d3:       y                   Node specific   Y coord
* d4:       x                   Node specific   X coord
* d5:       osmid               Node specific   Probably osmid id
* d6:       highway             Node specific   Things of interest at this node, e.g. traffic lights, junctions, bus stop   
* d7        ref                 Node specific   Some reference no idea
* d8        length              Edge specific   Length of street.
* d9        oneway              Edge specific   If street is oneway.
* d10       osmid               Edge specific   Probably ID on osmid    
* d11:      highway             Edge specific   type of road (e.g. autobahn, residential) 
only on edges
* d12       name                Edge specific   Street name
* d13       key                 Edge specific   No idea always 0
* d14       geometry            Edge specific   Models street via coordinates e.g. bends
* d15       lanes               Edge specific   How many lanes. 
* d16:      maxspeed            Edge specific   Duh
* d17       ref                 Edge specific   Probably the Highway number
* d18       Bridge              Edge specific   If bridge or not.
* d19:      Tunnel              Edge specific   If tunnel or not
* d20:      access              Edge specific   General access permission:  
                                                    * Yes; Public has access
                                                    * Delivery: only when delivering
                                                    * Destination: only when destination in area (Zubringerdienst)
                                                    * permissive: Open to general traffic until such time as the owner
                                                      revokes the permission which they are legally allowed to do at any time in the future.
                                                    * hov: undefined, drop it
* d21:      width               Edge specific   How wide a street is.                                                 
* d22:    service               Edge specific   If road is an alley or not, pretty useless and only 18 occurences
</code></pre>