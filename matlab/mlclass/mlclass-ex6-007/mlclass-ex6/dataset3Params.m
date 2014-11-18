function [C, sigma] = dataset3Params(X, y, Xval, yval)
%EX6PARAMS returns your choice of C and sigma for Part 3 of the exercise
%where you select the optimal (C, sigma) learning parameters to use for SVM
%with RBF kernel
%   [C, sigma] = EX6PARAMS(X, y, Xval, yval) returns your choice of C and 
%   sigma. You should complete this function to return the optimal C and 
%   sigma based on a cross-validation set.
%

% You need to return the following variables correctly.

C = 1;
sigma = 0.3;

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the optimal C and sigma
%               learning parameters found using the cross validation set.
%               You can use svmPredict to predict the labels on the cross
%               validation set. For example, 
%                   predictions = svmPredict(model, Xval);
%               will return the predictions on the cross validation set.
%
%  Note: You can compute the prediction error using 
%        mean(double(predictions ~= yval))
%

cList = [0.01 0.03 0.06 0.1 0.3 0.6 0.8 1 2 3 10];
sigmaList = [0.01 0.03 0.06 0.1 0.3 0.6 0.8 1 2 3 10];

% cList = 1.5 .^[0:26] ./ 1000;
% sigmaList = 1.5 .^[0:26] ./ 1000;

cList = cList';
sigmaList = sigmaList';

dataset3ParamsResult = zeros(size(cList, 1), size(sigmaList, 1));
maxCorrect = 0;
for cIndex = 1 : size(cList, 1)
	for sigmaIndex = 1 : size(sigmaList, 1)
		model = svmTrain(X, y, cList(cIndex), @(x1, x2) gaussianKernel(x1, x2, sigmaList(sigmaIndex)));
		predictions = svmPredict(model, Xval);
		numCorrect = mean(double(predictions == yval));
		dataset3ParamsResult(cIndex, sigmaIndex) = numCorrect;
		if numCorrect > maxCorrect
			maxCorrect = numCorrect
			C = cList(cIndex)
			sigma = sigmaList(sigmaIndex)

		end
	end
end


C
sigma
maxCorrect
dataset3ParamsResult

save ('kaiPlotData.mat', 'cList', 'sigmaList', 'dataset3ParamsResult', 'maxCorrect');
kaiPlotData(cList, sigmaList, dataset3ParamsResult);

% % final answer
% C = 1;
% sigma = 0.1;

% =========================================================================

end
