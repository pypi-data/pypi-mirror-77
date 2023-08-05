# Welcome to elkAnalyzer

This package is useful for plotting Elk DFT output files. This is still a beta version and is distributed under the MIT license (free and openly available). 
If you run into any issues, please submit an issue. Similarly, if you identify useful features that are not included, please submit a feature request issue.

The Elk code can be found at: http://elk.sourceforge.net/

The code for plotting ELK density of states was extracted with slight modifications from the MaterialsAutomated project (session 1)
created by Prof. Tyrel McQueen at Johns Hopkins University: https://github.com/materialsautomated/materialsautomated.github.io. 
Materials Automated is a series of 9 taped lectures that walk users through writing Python code for data analysis. Its code is distributed
on Github using the MIT license.

There are currently three sub-modules in elkAnalyzer:
1. bands is useful for visualizing band structure calculations and orbital contributions to band structure.
2. DOS is useful for visualizing density of states data.
3. specialPoints is useful for calculating the coordinates of special points using the Elk basis (compared to the standard described by C. Bradley and A.P. Cracknell's (Chapter 3) "The mathematical theory of symmetry in solids: representation theory for point groups and space groups": https://www.maa.org/publications/maa-reviews/the-mathematical-theory-of-symmetry-in-solids-representation-theory-for-point-groups-and-space)

## Band plotting examples
```python
import elkAnalyzer.bands as bnds
import numpy as np
import matplotlib.pyplot as plt

f='C:\\Users\\epogue1\\Documents\\postdoc\\Calculations\\Elk\\onMARCC\\f1\\'
plt.figure(1, figsize=(3, 2))
x, y=bnds.readBandsFile(f)
mn=np.amin(y)
mx=np.amax(y)
xs=bnds.getSpecialPoints(path)
lbl=['Z', '$\Gamma$', 'B', 'D', 'E', 'A', '$\Gamma$', 'Y', 'C']
plt.ylabel('Energy (eV)', fontsize=10)
plt.title('$compound$, SG-14, no SOC', fontsize=10)
plt.xlabel('k', fontsize=10)
plt.plot(x, y, color='C0')
plt.ylim(-2, 2)
plt.xlim(min(x), max(x))
plt.xticks(xs, lbl, fontsize=8)
plt.yticks(fontsize=8)
for k in xs:
    
    plt.axvline(x=k, color='k')
plt.tight_layout(pad=0)        
plt.figure(2, figsize=(3,2))      

path='C:\\Users\\epogue1\\Documents\\postdoc\\Calculations\\Elk\\onMARCC\\compound\\'

x, y=bnds.readBandsFile(path)
mn=np.amin(y)
mx=np.amax(y)
xs=bnds.getSpecialPoints(path)
lbl=['Z', '$\Gamma$', 'B', 'D', 'E', 'A', '$\Gamma$', 'Y', 'C']
plt.ylabel('Energy (eV)', fontsize=10)
plt.title('$compound$, no SOC', fontsize=10)
plt.xlabel('k', fontsize=10)
plt.plot(x, y, color='C0')
plt.ylim(-2, 2)
plt.xlim(min(x), max(x))
plt.xticks(xs, lbl, fontsize=8)
plt.yticks(fontsize=8)
for k in xs:
    
    plt.axvline(x=k, color='k')
plt.tight_layout(pad=0)
```
To plot two dispersion relationships on top of each other useL
```python
import elkAnalyzer.bands as bnds
import matplotlib.pyplot as plt
plt.figure(figsize=(6, 3))
path='C:\\Users\\epogue1\\Documents\\postdoc\\Calculations\\Elk\\onMARCC\\compound\\'
path1='C:\\Users\\epogue1\\Documents\\postdoc\\Calculations\\Elk\\onMARCC\\compound\\wSOC\\'
lbl=['Z', '$\Gamma$', 'B', 'D', 'E', 'A', '$\Gamma$', 'Y', 'C']
bnds.plotDispersionWithLegend(path, lbl, title='', energyRange=[-1.5,1.5], figsize=(6,4), xyLblSize=10, numSize=8, alpha=0.5, label='no SOC', loc='upper right')
bnds.plotDispersionWithLegend(path1, lbl, title='', energyRange=[-1.5,1.5], figsize=(6,4), xyLblSize=10, numSize=8, color='C1', alpha=0.5, label='w/ SOC', loc='upper right')
plt.tight_layout(pad=0)
```
To just plot the dispersion relationship, highlighting the CB and VB. You can artificially adjust Eg to account for errors associated with smearing.
```python
import elkAnalyzer.bands as bnds
import matplotlib.pyplot as plt
plt.figure()
path='C:\\Users\\epogue1\\Documents\\postdoc\\Calculations\\Elk\\onMARCC\\compound\\'
lbl=['Z', '$\Gamma$', 'B', 'D', 'E', 'A', '$\Gamma$', 'Y', 'C']
x, energy=bnds.plotDispersion(path, lbl, title='', energyRange=[-3,3], figsize=(3,2), xyLblSize=10, numSize=8)

Egvect, gap, idxVBmax, idxCBmin, vb, cb=bnds.calcEg(energy, -0.05)
plt.plot(x, vb, x, cb, color='C1')
```
To plot orbital contributions with color
```python
import elkAnalyzer.bands as bnds
import matplotlib.pyplot as plt
path='C:\\Users\\epogue1\\Documents\\postdoc\\Calculations\\Elk\\onMARCC\\compound\\'
x, energy, totSp, sSp, pSp, dSp, fSp, uniqueAt, norm=bnds.importSpeciesContributions(path)

fig, a=plt.subplots()
#Ba-s contributions
fig, a=plt.subplots()
bnds.plotWeightsColor(x, energy, sSp[0], title='$compound$ Ba-s')
bnds.plotFinish(path, ['Z', '$\Gamma$', 'B', 'D', 'E', 'A', '$\Gamma$', 'Y', 'C'], energyRange=[-1.5, 1.5])
bnds.removeLegend()
```
To plot species contributions for which the width of the line corresponds to its weight
```python
import elkAnalyzer.bands as bnds
import matplotlib.pyplot as plt
path='C:\\Users\\epogue1\\Documents\\postdoc\\Calculations\\Elk\\onMARCC\\compound\\'
x, energy, totSp, sSp, pSp, dSp, fSp, uniqueAt, norm=bnds.importSpeciesContributions(path)
fig, a=plt.subplots()
bnds.plotWeightsWidth(x, energy, sSp[0], lbl='Ba-s', color='C1')
bnds.plotWeightsWidth(x, energy, pSp[1], lbl='O-p', color='C0')
bnds.plotFinish(path, ['Z', '$\Gamma$', 'B', 'D', 'E', 'A', '$\Gamma$', 'Y', 'C'], energyRange=[-1, 1])
```

## DOS plotting
The slash at the end of the path is necessary.

Plot PDOS summed over all atoms of each species
```python
import matplotlib.pyplot as plt
import elkAnalyzer.DOS as DOS
path='C:\\Users\\username\\Documents\\Calculations\\Elk\\onMARCC\\myCompound\\.'
# - lms runs over all the input blocks within the file (how many and order depends on dosmsum and dossum settings)
plt.figure()
pdos = DOS.load_pdos(path)
sdos_np = DOS.sum_atoms_np(pdos)
for s in sdos_np:
    for lms in range(0,len(sdos_np[s])):
        cols = sdos_np[s][lms].swapaxes(0,1) # index by col,row
        plt.plot(cols[0],cols[1],label= str(s)+"-"+str(lms))
plt.legend()
plt.xlabel(r'Energy (eV)')
plt.ylabel('DOS ($eV^{-1}$)')
```
Plot PDOS summed over all atoms and lms of each species
```python
import matplotlib.pyplot as plt
import elkAnalyzer.DOS as DOS
plt.figure()
path='C:\\Users\\username\\Documents\\Calculations\\Elk\\onMARCC\\myCompound\\.'
pdos = DOS.load_pdos(path)
qdos_np = DOS.sum_atoms_lms_np(pdos)
for s in qdos_np:
    cols = qdos_np[s].swapaxes(0,1) # index by col,row
    plt.plot(cols[0],cols[1],label='Species '+str(s))
plt.legend()
plt.xlabel('Energy (eV)')
plt.ylabel('DOS ($eV^{-1}$)')
```
Plot PDOS by lms summed over all atoms and species
```python
import matplotlib.pyplot as plt
import elkAnalyzer.DOS as DOS
plt.figure()
path='C:\\Users\\username\\Documents\\Calculations\\Elk\\onMARCC\\myCompound\\.'
pdos = DOS.load_pdos(path)
rdos_np = DOS.sum_species_atoms_np(pdos)
for lms in range(0,len(rdos_np)):
    cols = rdos_np[lms].swapaxes(0,1) # index by col,row
    plt.plot(cols[0],cols[1],label=str(lms))
plt.legend()
plt.xlabel('Energy (eV)')
plt.ylabel('DOS ($eV^{-1}$)')
```
## Special Points determination

This module relies on having an INFO.OUT file that lists reciprocal lattice vectors and an elk.in file that contains the spacegroup number.
The basis of a "standard" reciprocal space is defined using C. Bradley and A.P. Cracknell's (Chapter 3) "The mathematical theory of symmetry in solids: representation theory for point groups and space groups": https://www.maa.org/publications/maa-reviews/the-mathematical-theory-of-symmetry-in-solids-representation-theory-for-point-groups-and-space).
A change of basis is then performed to represent this standard basis using the reciprocal lattice vectors used in the elk calculation. The slash at the end of the path is necessary.

This may be called using:
```python
import elkAnalyzer.specialPoints as csp
d=csp.calcStandard('C:\\Users\\username\\Documents\\Calculations\\Elk\\myCompound\\')
print(d)
```
When you call csp.calcStandard(path), you will have some additional items read out as sanity checks. You first get the angles, alpha, beta, and gamma. Next, you get a, b, and c from Elk. After that is the odd angle out (treated as gamma). Next, you have the reciprocal space vectors in the "standard" basis. print(d) causes the program to export a list containing the coordinates of the special points (labeled in the 4th column) in the Elk basis.



