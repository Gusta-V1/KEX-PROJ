import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

def solve_2d_heat_steady(Nx, Ny, Lx, Ly, Q, k, top_T, bot_T, left_T, right_T):
    # Mesh generation
    dx = Lx / (Nx - 1)
    dy = Ly / (Ny - 1)
    x = np.linspace(0, Lx, Nx)
    y = np.linspace(0, Ly, Ny)
    X, Y = np.meshgrid(x, y)

    # N = total unknown nodes
    N = Nx * Ny
    A = diags([-4 * np.ones(N), np.ones(N-1), np.ones(N-1), 
               np.ones(N-Nx), np.ones(N-Nx)], [0, 1, -1, Nx, -Nx], shape=(N, N)).toarray()
    
    # Source term vector
    b = - (Q * dx * dy / k) * np.ones(N)

    # Apply Boundary Conditions (Dirichlet)
    # This requires fixing rows of A and elements of b
    for i in range(Nx):
        for j in range(Ny):
            node = i + j * Nx
            if i == 0: # Left
                A[node, :] = 0; A[node, node] = 1; b[node] = left_T
            elif i == Nx - 1: # Right
                A[node, :] = 0; A[node, node] = 1; b[node] = right_T
            if j == 0: # Bottom
                A[node, :] = 0; A[node, node] = 1; b[node] = bot_T
            elif j == Ny - 1: # Top
                A[node, :] = 0; A[node, node] = 1; b[node] = top_T

    # Solve linear system
    T = np.linalg.solve(A, b)
    T = T.reshape((Ny, Nx))
    return X, Y, T

# Parameters
Nx, Ny = 100, 100
Lx, Ly = 625.0, 625.0
Q = 1000  # Constant power/volume
k = 1.0   # Thermal conductivity
T_bound = 20 # Boundary temperature

# Solve
X, Y, T = solve_2d_heat_steady(Nx, Ny, Lx, Ly, Q, k, T_bound, T_bound, T_bound, T_bound)

# Plotting
plt.imshow(T, extent=[0, Lx, 0, Ly])
plt.colorbar(label='Temperature')
plt.title('2D Laplace')
plt.show()
