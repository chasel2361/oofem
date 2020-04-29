# oofem
This is an object-oriented programming and Finite Element method based tool.

## Static analysis Procedure
1. Generate Nodes
2. Restrain Degree of freedoms(DOfs)
3. Generate Elements
4. Assign Nodes and Elements
5. Assign equation number
6. Set tolerance of error
7. Set External force
8. Iteratively calaulate

### Example: 
![Imgur](https://i.imgur.com/vj3PLQK.png)
```python
from Assembly import Assembly
from Node import Node, Point
from Section import Section
from Beam2D import Beam2D
from scipy.sparse import linalg, dok_matrix

"""Generate Nodes"""
n1 = Node(1, Point())
n2 = Node(2, Point(8000.0, 0.0))
n3 = Node(3, Point(13000.0, 0.0))

"""Restrain Dofs"""
n3.restrain()
for n in [n1, n2]:
    for i in [1, 2, 3, 4]:
        n.restrain_dof(i)

"""Generate elements"""
E = 200.0
G = E/(2*1.3)
A1 = 6.0e3
A2 = 4.0e3
I1 = 2.0e8
I2 = 5.0e7
J1 = 3.0e5
J2 = 1.0e5

section1 = Section(1, 0, E, G, A1, I1, I1, J1)
section2 = Section(2, 0, E, G, A2, I2, I2, J2)
b1 = Beam2D(1, n1, n2, section1, 0.0)
b2 = Beam2D(2, n2, n3, section2, 0.0)


assembly = Assembly(None)

"""Assign Nodes"""
for n in [n1, n2, n3]:
    assembly.add_node(n)

"""Assign Elements"""
for e in [b1, b2]:
    assembly.add_element(e)

"""Assign equation Number"""
assembly.assign_eq_number()
neq = assembly.eq_number

"""Set tolerance of error"""
tol = 1e-4
iteration = 0

"""Set external force"""
f = dok_matrix([[0.0], [-10670], [0.0], [-3730]])

P = assembly.assemble_internal_force('d_try', 'pos_origin')
R = f - P
conv = linalg.norm(R)
K = assembly.assemble_K('pos_origin')

"""Iterative calculation"""
while conv > tol:
    delu = linalg.inv(K) * R
    assembly.inc_d_try(delu)
    u = assembly.get_dof('d_try')
    P = assembly.assemble_internal_force('d_try', 'pos_origin')
    R = f - P
    conv = linalg.norm(R)
    K = assembly.assemble_secant_stiffness('d_try', 'pos_origin')
    iteration += 1

"""Output result"""
u = assembly.get_dof('d_try')
print(u)
```
