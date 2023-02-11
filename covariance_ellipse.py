# Plots the uncertainty ellipse for time steps 1-5 of simulation
#
# Adapted from https://irwinsnet.github.io/probrob/nb03.html 

import math
import sympy
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

def get_eigen_data(eigenvects):
    if eigenvects[0][0] > eigenvects[1][0]:
        idx_max = 0
        idx_min = 1
    else:
        idx_max = 1
        idx_min = 0
        
    return {"eigvec_major": list(eigenvects[idx_max][2][0]),
            "eigvec_minor": list(eigenvects[idx_min][2][0]),
            "eigval_major": eigenvects[idx_max][0],
            "eigval_minor": eigenvects[idx_min][0],
            "theta_major": math.atan(eigenvects[idx_max][2][0][1]/
                               eigenvects[idx_max][2][0][0])*180/math.pi,
            "theta_minor": math.atan(eigenvects[idx_min][2][0][1]/
                               eigenvects[idx_min][2][0][0])*180/math.pi,
           }


Sigma_1 = sympy.Matrix([[0.25, 0.5], [0.5, 1]])
eigen1 = Sigma_1.eigenvects()
ed1 = get_eigen_data(eigen1)

Sigma_2 = sympy.Matrix([[2.5, 2], [2, 2]])
eigen2 = Sigma_2.eigenvects()
ed2 = get_eigen_data(eigen2)

Sigma_3 = sympy.Matrix([[3, 3], [1, 1]])
eigen3 = Sigma_3.eigenvects()
ed3 = get_eigen_data(eigen3)

Sigma_4 = sympy.Matrix([[8.75, 4.5], [4.5, 3]])
eigen4 = Sigma_4.eigenvects()
ed4 = get_eigen_data(eigen4)

Sigma_5 = sympy.Matrix([[21, 8], [8, 4]])
eigen5 = Sigma_5.eigenvects()
ed5 = get_eigen_data(eigen5)



# Setup plot
plt.clf()
fig2 = plt.figure()
ax = fig2.add_subplot(111)

# Set limits of X and Y axes
lim = 6
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_aspect('equal', adjustable='datalim')

# Add ellipse
ell1 = mpatches.Ellipse((0,0), math.sqrt(ed1["eigval_major"])*2,
                        math.sqrt(ed1["eigval_minor"])*2, ed1["theta_major"],
                        fill=False, edgecolor="orange")
ell2 = mpatches.Ellipse((0,0), math.sqrt(ed2["eigval_major"])*2,
                        math.sqrt(ed2["eigval_minor"])*2, ed2["theta_major"],
                        fill=False, edgecolor="red")
ell3 = mpatches.Ellipse((0,0), math.sqrt(ed3["eigval_major"])*2,
                        math.sqrt(ed3["eigval_minor"])*2, ed3["theta_major"],
                        fill=False, edgecolor="purple")
ell4 = mpatches.Ellipse((0,0), math.sqrt(ed4["eigval_major"])*2,
                    math.sqrt(ed4["eigval_minor"])*2, ed4["theta_major"],
                    fill=False, edgecolor="blue")      
ell5 = mpatches.Ellipse((0,0), math.sqrt(ed5["eigval_major"])*2,
                        math.sqrt(ed5["eigval_minor"])*2, ed5["theta_major"],
                        fill=False, edgecolor="green")    

ax.legend([ell1, ell2, ell3, ell4, ell5], ['Time Step 1', 'Time Step 2', 'Time Step 3', 'Time Step 4', 'Time Step 5'])                                
                    
ax.add_patch(ell1)
ax.add_patch(ell2)
ax.add_patch(ell3)
ax.add_patch(ell4)
ax.add_patch(ell5)

# Add titles and Labels
title = ("Robot Position at Time t = 5\n"
         "covariance ellipse of 1 standard deviation")
plt.title(title)
plt.xlabel("Position")
plt.ylabel("Velocity")

fig2.show()

plt.show()

