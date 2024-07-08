# https://stackoverflow.com/questions/46972905/distances-on-lattices-with-periodic-boundaries
# dx = Abs(x1 - x2)
# if dx > L/2
#    dx = L - dx
# similar for dy

# copy matrix over diagonal
# https://stackoverflow.com/questions/16444930/copy-upper-triangle-to-lower-triangle-in-a-python-matrix
# import numpy as np

# X= np.array([[0., 2., 3.],
#              [0., 0., 6.],
#              [0., 0., 0.]])

# X = X + X.T - np.diag(np.diag(X))
# print(X)

# #array([[0., 2., 3.],
# #       [2., 0., 6.],
# #       [3., 6., 0.]])