function kaiPlotData(xList, yList, data)
%PLOTDATA Plots the data points X and y into a new figure 
%   PLOTDATA(x,y) plots the data points with + for the positive examples
%   and o for the negative examples. X is assumed to be a Mx2 matrix.
%
% Note: This was slightly modified such that it expects y = 1 or y = 0

% Find Indices of Positive and Negative Examples
mesh(xList, yList, data)
set(gca, 'xscale', 'log');
set(gca, 'yscale', 'log');

end
