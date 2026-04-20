import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

# --- Parameters ---
N = 50          # Number of nodes per dimension
L = 1.0         # Domain size (1x1)
Q_val = 100.0   # Constant heat generation rate (W/m^3)
k = 1.0         # Thermal conductivity (W/mK)
source_term = -Q_val / k

# --- Grid Generation ---
dx = L / (N - 1)
dy = L / (N - 1)
x = np.linspace(0, L, N)
y = np.linspace(0, L, N)
X, Y = np.meshgrid(x, y)

# --- Matrix Assembly (A*T = B) ---
# Total nodes = N*N
A = lil_matrix((N*N, N*N))
B = np.zeros(N*N)

# Function to map 2D index (i,j) to 1D index
def idx(i, j):
    return i + j*N

# Fill matrix with finite difference scheme (5-point stencil)
for i in range(1, N-1):
    for j in range(1, N-1):
        A[idx(i,j), idx(i,j)] = -2/dx**2 - 2/dy**2 # Center
        A[idx(i,j), idx(i+1,j)] = 1/dx**2          # East
        A[idx(i,j), idx(i-1,j)] = 1/dx**2          # West
        A[idx(i,j), idx(i,j+1)] = 1/dy**2          # North
        A[idx(i,j), idx(i,j-1)] = 1/dy**2          # South
        B[idx(i,j)] = source_term

# --- Neumann Boundary Conditions (Insulated) ---
# Du/Dn = 0 means neighboring node = current node
for i in range(N):
    # Bottom Boundary (y=0, j=0)
    A[idx(i, 0), idx(i, 0)] = 1
    A[idx(i, 0), idx(i, 1)] = -1
    B[idx(i, 0)] = 0
    
    # Top Boundary (y=L, j=N-1)
    A[idx(i, N-1), idx(i, N-1)] = 1
    A[idx(i, N-1), idx(i, N-2)] = -1
    B[idx(i, N-1)] = 0

for j in range(1, N-1):
    # Left Boundary (x=0, i=0)
    A[idx(0, j), idx(0, j)] = 1
    A[idx(0, j), idx(1, j)] = -1
    B[idx(0, j)] = 0
    
    # Right Boundary (x=L, i=N-1)
    A[idx(N-1, j), idx(N-1, j)] = 1
    A[idx(N-1, j), idx(N-2, j)] = -1
    B[idx(N-1, j)] = 0

# --- Fix one point (Reference Temperature) ---
# Necessary for pure Neumann problems to make it solvable
A[0, :] = 0
A[0, 0] = 1
B[0] = 0 # Assume T(0,0) = 0

# --- Solve System ---
A = A.tocsr()
T = spsolve(A, B)
T_2d = T.reshape((N, N))

# --- Visualization ---
plt.figure(figsize=(8,6))
cp = plt.contourf(X, Y, T_2d, cmap='hot')
plt.colorbar(cp, label='Temperature')
plt.title('2D Steady State Heating (Neumann BCs)')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()
