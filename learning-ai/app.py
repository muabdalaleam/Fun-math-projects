import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

plt.style.use('dark_background')
# =================== Generating Data ===================

np.random.seed(67)
FPS = 30

W0 = 10.0
W1 = 2.78
W2 = 3.14

f = lambda X : W0 + W1*X + W2*X**2

X = np.random.randn(1000)
y = f(X) + np.random.randn(1000)*2
# ========================================================


# ===================== Boring Math ======================
EPOCHS        = 270
LEARNING_RATE = 0.01

mse_cost  = lambda y_pred : np.sum((y - y_pred)**2) / len(y)

def gradient_descent(X: np.array, y: np.array,
                    learning_rate: float, epochs: int) -> dict:

    W1 = np.random.randint(-10, 10)
    W2 = np.random.randint(-10, 10)
    W0 = np.random.randint(-10, 10)
    
    history = {
        'W0': [],
        'W1': [],
        'W2': [],
        'costs': []}

    for e in range(epochs):

        y_pred = W0 + W1*X + W2*X**2
        cost = mse_cost(y_pred)
        
        history['W0'].append(W0)
        history['W1'].append(W1)
        history['W2'].append(W2)
        history['costs'].append(cost)

        delta_W1 = (-2 / len(y)) * np.sum(X    * (y - y_pred))
        delta_W2 = (-2 / len(y)) * np.sum(X**2 * (y - y_pred))
        delta_W0 = (-2 / len(y)) * np.sum        (y - y_pred)

        W1 -= learning_rate * delta_W1
        W2 -= learning_rate * delta_W2
        W0 -= learning_rate * delta_W0

    return history

history = gradient_descent(X, y, learning_rate= LEARNING_RATE, epochs= EPOCHS)

print('Predicted Bias:           ',       history['W0'][-1])
print('Predicted slope for X: ',   history['W1'][-1])
print('Predicted slope for X^2: ', history['W2'][-1])
# ========================================================


# ================== Visualizing the model ===============
W1_vals = np.linspace(-20, 20, 200)
W2_vals = np.linspace(-20, 20, 200)

W1_grid, W2_grid = np.meshgrid(W1_vals, W2_vals)

costs = np.zeros_like(W1_grid)

for i in range(len(W1_vals)):
    for j in range(len(W2_vals)):
        costs[i, j] = mse_cost(W0 + W1_vals[i] * X + W2_vals[j] * X**2)

costs = costs.T


# --------3D surface chart---------
fig = plt.figure(figsize= (10, 5))

ax_1 = fig.add_subplot(1, 2, 1, projection='3d')

ax_1.set_position([ax_1.get_position().x0 - 0.25, ax_1.get_position().y0 - 0.1, 0.8, 0.8])
ax_1.plot_surface(W1_grid, W2_grid, costs, cmap='turbo',alpha= 0.8)
ax_1.view_init(elev= 32, azim= 32)
ax_1.grid()

ax_1.set_zticks(np.linspace(0, 2000, 5))
ax_1.set_xlabel('W1')
ax_1.set_ylabel('W2')
ax_1.set_zlabel('Loss')
# ----------------------------------

# -------- 2D scatter plot ----------
ax_2 = fig.add_subplot(1, 2, 2)

ax_2.set_position([ax_2.get_position().x0 + 0.02, ax_2.get_position().y0, 0.4, 0.6])
ax_2.scatter(X, y, s= 10, color= "grey")

ax_2.set_xlabel('Feature')
ax_2.set_ylabel('Target')

ax_2.spines['top'].set_visible(False)
ax_2.spines['right'].set_visible(False)

x_vals = np.linspace(-5, 5, 100)
# ----------------------------------

# -----Animation------
ax_1.scatter([], [], [])

text    = ax_2.text(-13, 70, '')
line,   = ax_2.plot([], [], color= 'red')
scatter = ax_1.scatter([], [], [], c='red', s=18, alpha=1, zorder= 2.5)

def init():

    scatter._offsets3d = ([], [], [])
    line.set_data([], [])

    return scatter, line

def animate(frame):
    
    x = history['W1'][frame]
    y = history['W2'][frame]
    z = history['costs'][frame]
    scatter._offsets3d = ([x], [y], [z])

    y_vals = history['W0'][frame] + history['W1'][frame] * x_vals + history['W2'][frame] * (x_vals ** 2)

    text.set_text(f'Epoch: {frame}')
    line.set_data(x_vals, y_vals)

    return line, scatter
# ----------------------------------

fig.suptitle(f'Gradient Descent Optimiztion',fontsize= 20)

num_frames = len(history['W1'])

animation = FuncAnimation(
    fig, animate, frames=num_frames, init_func=init, interval=1000 / FPS
)

writer = PillowWriter(fps=15)
animation.save('animation.gif', writer=writer)

plt.show()
# ========================================================++