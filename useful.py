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

# rotate 90 degrees
# https://stackoverflow.com/questions/45701615/how-can-i-rotate-a-line-segment-around-its-center-by-90-degrees
# //find the center
# cx = (x1+x2)/2;
# cy = (y1+y2)/2;

# //move the line to center on the origin
# x1-=cx; y1-=cy;
# x2-=cx; y2-=cy;

# //rotate both points
# xtemp = x1; ytemp = y1;
# x1=-ytemp; y1=xtemp; 

# xtemp = x2; ytemp = y2;
# x2=-ytemp; y2=xtemp; 

# //move the center point back to where it was
# x1+=cx; y1+=cy;
# x2+=cx; y2+=cy;