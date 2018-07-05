function J = costFunctionJ(X, y, theta)

% X is the "design matrix" containing training examples.
% y is the class labels

m 		= size(X, 1);			% number of training examples
predictions	= X*theta;			% predictions of hypothesis on all m examples
squareErrors	= (predictions - y).^2;		% squared errors
J		= 1/(2*m) * sum(squareErrors);
