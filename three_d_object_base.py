from logging import raiseExceptions
import numpy as np
from time import time as t
from time import sleep
from typing import overload
from functools import lru_cache
class modelbase:
    def __init__(self):
        pass
    def length(self,c1,c2):
        tem=(c1-c2)
        # print(c2)
        len=np.sqrt(tem.dot(tem))
        return len
    def normal(self,c1,c2):
        return np.array((c1-c2))/self.length(c1,c2)
    
    def displacement(self,pointforce,dt):
                return 0.5*(pointforce/self.mass)*dt**2
    # @overload
    # def indexer(self,m:int,n:int)->list((m,n,3)):...
    # @overload
    # def indexer(self,n:int,m:int,k:int)->list((n,m,k,3)):...
    # @overload
    # def func(distance:float)->float:...
    # @overload
    # def adjacent(self,i:int,j:int)-> list[int]: ...
    # @overload
    # def adjacent(self,i:int,j:int,k:int)->list[int]:...
    # @overload
    # def update_grid(self)->None:...
# class Spheregridbase(modelbase):
#     def __init__(self,r,n):
#         self.ini=t()
#         self.mass=1
#         self.a=0.000765
#         self.b=0.0025
#         self.r=r
#         self.n=n
#         self.obj=self.Spheregrid(r,n)
#         self.indarray=self.indexer(m=self.n,n=self.n)
    
#     def Spheregrid(self,r,n):
#         emgrid=np.empty((n,n,3))
#         i=0
#         j=0
#         theta=0
#         phi=0
#         div1 = np.pi/n
#         div2 = 2*div1
#         while i < n:
#             while j<n:
#                 nsphi=np.sin(phi)
#                 nctheta=np.cos(theta)
#                 nstheta=np.sin(theta)
#                 x=r*nsphi*nctheta
#                 y=r*nsphi*nstheta
#                 z=r*np.cos(phi)
#                 emgrid[i][j]=[x,y,z]
#                 theta +=div2
#                 j+=1
#             phi+=div1
#             i+=1
#             j=0
#         return np.array(emgrid,dtype=np.float64)
#     def indexer(self,m,n):
#         tem1=np.arange(m)
#         tem2=np.arange(n)
#         emgrid = np.empty((m,n,2),dtype=int)
#         for i in range(m):
#             emgrid[:,i,0]=tem1
#         for j in range(n):
#             emgrid[j,:,1]=tem2
#         return emgrid
#     def force(self,distance):
#         return -2*self.a/(distance**3)+self.b/(distance**2)
#     def adjacent(self,i,j):
#         n=self.n-1
#         if (i<n and j <n and i!=0 and j!=0):
#             return ([[i+1,j],[i-1,j],[i,j+1],[i,j-1]])
#         elif (i<n and j!=0 and j!=n):
#             return ([[1,j],[n,j],[i,j-1],[i,j+1]])
#         elif (j<n and i!=0 and i!=n):
#             return ([[i,1],[i,n],[i-1,j],[i+1,j]])
#         elif (i==0 and j==n):
#             return ([[0,n-1],[0,1],[1,n],[n,n]])
#         elif (i==n and j==0):
#             return ([[n,1],[n,n],[n-1,0],[1,0]])
#         else:
#             return ([0,1],[0,n],[1,0],[n,0])
#     def total_force(self,column,aradj):
#         pointforce=np.array([0,0,0]).astype('float64')
#         for ind in aradj:
#             pointforce+=self.force(self.length(self.obj[column[0]][column[1]],self.obj[ind[0]][ind[1]])*self.normal(self.obj[column[0]][column[1]],self.obj[ind[0]][ind[1]]))            
#         return pointforce
#     def spheregriddisplacement(self,aryforce,dt):
#         tem=np.empty((self.n,self.n,3))
#         for row in self.indarray:
#             for column in row:
#                 tem[column[0]][column[1]]=self.displacement(aryforce[column[0]][column[1]],dt)
#         return tem
#     def update_grid(self):
#         now=t()
#         dt=(now-self.ini)*1e-3
#         self.ini=now
#         aryforce=np.empty((self.n,self.n,3))
#         for row in self.indarray:
#             for column in row:
#                 aradj=self.adjacent(column[0],column[1])
#                 aryforce[column[0]][column[1]]=self.total_force(column,aradj)
#                 del aradj
#         tem=self.spheregriddisplacement(aryforce,dt)
#         self.obj=self.obj+tem
#         return self.obj
class Cube(modelbase):
    def __init__(self,n,m,k,div,a,b):
        self.ini=t()
        self.mass=1
        self.n=n
        self.m=m
        self.k=k
        self.a=a*1e4
        self.b=b*1e4
        self.obj=self.cube(n,m,k,div)
        self.indarray=self.indexer(self.n,self.m,self.k)
    def cube(self,n,m,k,div):
        i=0
        j=0
        q=0
        tem=np.empty((n,m,k,3))
        while i<n:
            while j<m:
                while q<k:
                    tem[i][j][q]=[i*div,j*div,q*div]
                    q+=1
                q=0
                j+=1
            j=0
            i+=1
        return np.array(tem).astype(np.float32)
    def permutation(self,scale=1/40):
        self.obj=self.obj+np.array([np.random.random()*scale for i in range(self.m*self.n*self.k*3)]).reshape((self.n,self.m,self.k,3))
    def force(self,distance):
            return -2*self.a/(distance**3)+self.b/(distance**2)
    def indexer(self,n,m,k):
        tem=np.empty((n,m,k,3))
        tem1=range(n)
        tem2=range(m)
        tem3=range(k)
        for i in range(m):
            for j in range(k):
                tem[:,i,j,0]=tem1
        # print(i,j)
        for i in range(n):
            for j in range(k):
                tem[i,:,j,1]=tem2
        for i in range(m):
            for j in range(k):
                tem[i,j,:,2]=tem3

        return tem.astype(int)
    @lru_cache
    def adjacent(self,i,j,q):
        n=self.n-1
        m=self.m-1
        k=self.k-1
        # if (i != (0 and n)) and (j != (0 and m)) and (q != (0 and k)):
        if i!= 0 and i != n and j != 0 and j!= m and q != 0 and q != k:
            #print(1)
            return ([[i+1,j,q],[i-1,j,q],[i,j+1,q],[i,j-1,q],[i,j,q+1],[i,j,q-1]])
        
        
        
        
        # if (i == 0 ) and (j != (0 and m)) and (q != (0 and k)):
        if i == 0 and j != 0 and j != m and q != 0 and q != k:
            #print(2)
            return ([[1,j,q],[0,j+1,q],[0,j-1,q],[0,j,q+1],[0,j,q-1]])
        # if (i != (0 and n)) and (j == 0) and (q != (0 and k)):
        if i != 0 and i != n and j==0 and q != 0 and q != k:
            #print(3)
            return ([[i,1,q],[i+1,0,q],[i-1,0,q],[i,0,q+1],[i,0,q-1]])
        # if (i != (0 and n)) and (j != (0 and m)) and (q == 0):
        if i != 0 and i != n and j != 0 and j != m and q == 0:
            #print(4)
            return ([[i,j,1],[i+1,j,0],[i-1,j,0],[i,j+1,0],[i,j-1,0]])
        # if (i == n ) and (j != (0 and m)) and (q != (0 and k)):
        if i == n and j != 0 and j != m and q != 0 and q != k:
            #print(5)
            return ([[n-1,j,q],[n,j+1,q],[n,j-1,q],[n,j,q+1],[n,j,q-1]])
        # if (i != (0 and n)) and (j == m) and (q != (0 and k)):
        if i != 0 and i != n and j == m and q != 0 and q != k:
            #print(6)
            return ([[i,m-1,q],[i+1,m,q],[i-1,m,q],[i,m,q+1],[i,m,q-1]])
        # if (i != (0 and n)) and (j != (0 and m)) and (q == k):
        if i != 0 and i != n and j != 0 and j != m and q == k:
            #print(7)
            return ([[i,j,k-1],[i+1,j,k],[i-1,j,k],[i,j+1,k],[i,j-1,k]])
        
        
        
        
        # if (i == 0 ) and (j == 0 ) and (q != (0 and k)):
        if i == n and j == m and q != 0 and q != k:
            return ([[n-1,m,q],[n,m-1,q],[n,m,q+1],[n,m,q-1]])
        if i == 0 and j == 0 and q != 0 and q != k:
            #print(8)
            return([[1,0,q],[0,1,q],[0,0,q+1],[0,0,q-1]])
        # if (i == n ) and (j == 0 ) and (q != (0 and k)):
        if i == n and j == 0 and q != 0 and q != k:
            #print(9)
            return([[n-1,0,q],[n,1,q],[n,0,q+1],[n,0,q-1]])
        # if (i == 0 ) and (j == m ) and (q != (0 and k)):
        if i == 0  and j == m  and q != 0 and q != k:
            #print(10)
            return([[1,m,q],[0,m-1,q],[0,m,q+1],[0,m,q-1]])
        # if (i != (0 and n )) and (j == 0 ) and (q == 0 ):
        if i != 0 and i != k and j == 0 and q == 0:
            #print(11)
            return([[i,1,0],[i,0,1],[i+1,0,0],[i-1,0,0]])
        # if (i !=(0 and n )) and (j == m ) and (q == 0 ):
        if i != 0 and i != n and j == m and q == 0:
            #print(12)
            return([[i+1,m,0],[i,m-1,0],[i+1,m,1],[i-1,m,0]])
        # if (i != (0 and n )) and (j == 0 ) and (q == k ):
        if i != 0 and i != n and j == 0 and q == k:
            #print(13)
            return([[i,1,k],[i,0,k-1],[i+1,0,k],[i-1,0,k]])
        # if (i != (0 and n)) and (j == m ) and (q == k):
        if i !=0 and i != n and j == m and q == k:
            #print(14)
            return([[i,m-1,k],[i,m,k-1],[i+1,m,k],[i-1,m,k]])
        # if (i == 0) and (j != (m and 0 )) and (q == 0):
        if i == 0 and j != m and j != 0 and q == 0:
            #print(15)
            return([[1,j,0],[0,j,1],[0,j+1,0],[0,j-1,0]])
        # if (i == n) and (j != (m and 0 )) and (q == 0):
        if i == n and j != m and j != 0 and q == 0:
            #print(16)
            return ([[n-1,j,0],[n,j,1],[n,j+1,0],[n,j-1,0]])
        # if (i == 0) and (j != (m and 0 )) and (q == k):
        if i == 0 and j != m and j!= 0 and q == k:
            #print(17)
            return([[1,j,k],[0,j,k-1],[0,j+1,k],[0,j-1,k]])
        if i == n and j != m and j != 0 and q == k:
            return ([[n-1,j,k],[n,j+1,k],[n,j-1,k],[n,j,k-1]])

        
        
        
        
        
        if i == 0 and j ==0 and q == 0:
            #print(18)
            return([[0,0,1],[0,1,0],[1,0,0]])
        if i == n and j ==0 and q == 0:
            #print(19)
            return([[n-1,0,0],[n,1,0],[n,0,1]])
        
        
        
      
        if i == 0 and j ==m and q == 0:
            #print(20)
            return ([[0,m-1,0],[1,m,0],[0,m,1]])
        if i == 0 and j ==0 and q == k:
            #print(21)
            return ([[0,0,k-1],[0,1,k],[1,0,k]])
        if i == 0 and j ==m and q == k:
            #print(22)
            return([[0,m-1,k],[0,m,k-1],[1,m,k]])
 
        if i == n and j ==0 and q == k:
            #print(23)
            return([[n-1,0,k],[n,0,k-1],[n,1,k]])
        if i == n and j ==m and q == 0:
            #print(24)
            return([[n-1,m,0],[n,m-1,0],[n,m,1]])
        if i == n and j ==m and q == k:
            #print(25)
            return([[n-1,m,k],[n,m-1,k],[n,m,k-1]])
    def total_force(self,third,aradj):
        pointforce=np.array([0.0,0.0,0.0]).astype("float32")
        try:
            for item in aradj:
            # #print(self.obj.shape)
            # try:
                pointforce+=self.force(self.length(self.obj[item[0]][item[1]][item[2]],self.obj[third[0]][third[1]][third[2]]))*self.normal(self.obj[item[0]][item[1]][item[2]],self.obj[third[0]][third[1]][third[2]])
            # except IndexError:
            
            #     break
        except TypeError:
            #print('arddj',aradj)
            #print('third',third)
            raise TypeError("THIS HAPPEND")
        return pointforce
    def cubegriddisplacement(self,aryforce,dt):
        return 0.5*(aryforce/self.m)*dt**2
    def update_grid(self):
        now=t()
        dt=(now-self.ini)
        self.ini=now
        aryforce=np.empty((self.n,self.m,self.k,3))
        for row in self.indarray:
            for column in row:
                for third in column:
                    aradj=self.adjacent(third[0],third[1],third[2])
                    aryforce[third[0]][third[1]][third[2]]=self.total_force(third,aradj)
                    del aradj
        tem=self.cubegriddisplacement(aryforce,dt)
        # print('tem',tem[:3][0][0])
        self.obj=self.obj+tem
        # return self.obj
        
# entity=Cube(11,11,11,0.1,1,1)
# entity.update_grid()
# tem=entity.obj
# tem=tem.reshape(1331,3)
#print(tem.shape)
# print(r.adjacent(10,1,10))