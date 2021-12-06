<pre><code>
* d0:       crs                 Data specific   useless #dröp
* d1:       name                Data specific   shows City we're in (guess) #drop   
* d2:       streets_per_node    Node specific   Mostly unnused #drop 
* d3:       y                   Node specific   Y coord #keep for heuristic for path finding
* d4:       x                   Node specific   X coord #keep for heuristic for path finding
* d5:       osmid               Node specific   Probably osmid id #drop 
* d6:       highway             Node specific   Things of interest at this node, e.g. traffic lights, junctions, bus stop #keep for now
* d7        ref                 Node specific   Some reference no idea #drop
* d8        length              Edge specific   Length of street. #keep
* d9        oneway              Edge specific   If street is oneway. #drop
* d10       osmid               Edge specific   Probably ID on osmid #drop 
* d11:      highway             Edge specific   type of road (e.g. autobahn, residential) #keep 
only on edges
* d12       name                Edge specific   Street name # keep
* d13       key                 Edge specific   No idea always 0 #drop
* d14       geometry            Edge specific   Models street via coordinates e.g. bends #drop 
* d15       lanes               Edge specific   How many lanes. # keep
* d16:      maxspeed            Edge specific   Duh # keep
* d17       ref                 Edge specific   Probably the Highway number # drop
* d18       Bridge              Edge specific   If bridge or not. # keep
* d19:      Tunnel              Edge specific   If tunnel or not. # keep 
* d20:      access              Edge specific   General access permission:  # drop
                                                    * Yes; Public has access
                                                    * Delivery: only when delivering
                                                    * Destination: only when destination in area (Zubringerdienst)
                                                    * permissive: Open to general traffic until such time as the owner
                                                      revokes the permission which they are legally allowed to do at any time in the future.
                                                    * hov: undefined, drop it
* d21:      width               Edge specific   How wide a street is. # drop                                         
* d22:    service               Edge specific   If road is an alley or not, pretty useless and only 18 occurences #drop
</code></pre> 


<code><pre>

* d3:       y                   Node specific   Y coord #keep for heuristic for path finding
* d4:       x                   Node specific   X coord #keep for heuristic for path finding
* d6:       highway             Node specific   Things of interest at this node, e.g. traffic lights, junctions, bus stop #keep for now

* d8        length              Edge specific   Length of street. #keep
* d11:      highway             Edge specific   type of road (e.g. autobahn, residential) #keep 
* d12       name                Edge specific   Street name # keep
* d15       lanes               Edge specific   How many lanes. # keep
* d16:      maxspeed            Edge specific   Duh # keep
* d18       Bridge              Edge specific   If bridge or not. # keep
* d19:      Tunnel              Edge specific   If tunnel or not. # keep 
</code></pre>