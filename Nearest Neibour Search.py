import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import voronoi_plot_2d, Voronoi, KDTree
import pandas as pd

'''
Logical intuition: cannot use linear scan because time complexity O(n^2) is far too slow for a 
large list; cannot sort also for poor time complexity.

Chosen step therefore for the 2D case is a voroni diagram based point location query algorithm.
Constructing the voroni diagram is implimented with scipy

Scipy implimentation for constructing the veroni diagram is robust, has O(2+ log(n)) time complexity for the d=2 case and 
n^(1) space complexity, liniar space is good since question suggests low memory buffer;

Traversing the point location query is done using KD trees for a time complexity of O(log(n)) time complexity as an ANN 
algorithmic approach, the intiution between not using an exact solution is to allow for subliminal solve time with general 
solutions in the case of d>2. 
'''


class ApproxNearestNeibours:
    
    def NearestSearch():
        
        x = [.22, .2, .4, .44, .42, .61, .17, .2, .63, .66]
        y = [.21, .43, .23, .41, .42, .31, .2, .17, .62, .65]
        London = [0,0]
        
        list1 = np.random.rand(10,2)
        list2= list(zip(x,y))

        #Voroni plot
        vor = Voronoi(list1)

        #KD tree
        tree = KDTree(list1)
        locs, ids = tree.query(list2)
    
        #Plotting and annotating (blue points are list1)
        fig,ax = plt.subplots(1,1)
        voronoi_plot_2d(vor,ax, show_vertices=False)
        ax.scatter(x,y,s=20,color='r', label ='list two points')
        ax.scatter(0,0, s=100, color='black', label= 'London')
    
        for i in range(0,len(x)):
            ax.annotate(ids[i], (x[i], y[i]), size = 10)
    
        plt.xlabel('X co-ordinate')
        plt.ylabel('Y co-ordinate')
        plt.legend()
        plt.show()


        print("Id of point in list 1 that is the nearest neibour of point in list 2:", ids)
        ID_Of_List1_Node = ids 

        '''
        What I could then do is write a script to put back out into whatever database I got the lists from
        to append with a third column of the #Id for the list 1 item that is closest to the given list 2 item
        '''


    if __name__ == "__main__":
        NearestSearch()
        
        
        
        
        
        
from annoy import AnnoyIndex
import numpy as np

'''Extention tasks:
    
    Can you generalise your code to n dimentions?
    
    Yes, using the annoy libary in python, I can define a metric space of all of the 
    points in list 1 of n dimentions and then perform the same KD tree search in higher 
    dimentionality. Annoy package seems to generalise on testing up to around d<2000.
    
    The use of the KD tree is to allow for subliminal complexity solves in the d>2 case,
    
    this is because exact methods such as solving the kirkpatrick point localisation 
    data structure cannot have subliminal time complexity solves in higher dimentional 
    systems along with the liniar construction complexity of the voroni diagram in higher 
    dimentions would Violate the mathmatics of complexity-theoretic conjecture (the strong 
    exponential time hypothesis.)
    
    

'''
class annoy:

    __innit__(self):
        self.f = 40 #Number dimentions operating in for the index


    #Data will have n dimentions incoming

    list1 = np.random.rand(10,f)
    list2 = np.random.rand(10,f)
    
    t = AnnoyIndex(f, 'euclidian')  #Length of item vector that will be indexed

    for i in len(list1):
        t.add_item(i, list1)    #Append the items of list 1 to the defined metric space
        

    t.build(10) # 10 trees
    t.save('test.ann')

    u = AnnoyIndex(f, 'euclidian')
    u.load('test.ann') # super fast, will just mmap the file
    
    for i in len(list2):
        print("Nearest neibour for each element in list2:", u.get_nns_by_item(0, 1)) # will find the nearest neighbor
    
    
    
'''
As for the 2d case, these could then be saved into a database to map each point in the second list to its 
closest point in the first
'''




'''
Extention task 2: 

    how would your answer change if your lists were too large to fit on a single machine?

for the 2d case using the veroni diagrams cannot be incremented to split the map of england into smaller parts
as veroni mappings to calculate require all the data in proximity. This would require a sort which would have 
poor time complexity for huge datasets.

Therefore instead I would use the annoy package again for all cases:
    
For the annoy package the indexes of the metric spaces created for the first list of points can be run on disk to deal 
with this exact issue allowing for the calculations to still be performed. Additionally, memory between multiple processes 
on the same metric space can be processed, so list 2 CAN be split into multiple sections that will load into memory and the 
ANN K-D algorithm can be applied to find their nearest neibours in any dimention. 

Also for extra joy, the process can be done in parallel computation by defining the routing of the points of list 2 to specific computers 
which each have an index on disk to allow for computational parrallelism.

'''


'''
Extention task 3:
    Would your answer change if the points were in a non metric space?
    
Yes it would- In short the question would lose all meaning. To summise, the definition
of a metric space can be put as any set space with a defining metric. Thus, any non metric 
space either has no set (so list 1 and list2 are empty and there are no points to calculate),
or there is no metric in which case the space has no concept of distance, everything is everywhere).
    
'''
