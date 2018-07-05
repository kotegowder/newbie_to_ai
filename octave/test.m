printf("\nMy octave tests\n");

%Calling squareThisNumber
printf("\nCalling squareThisNumber");
num = 5;
printf("\nSquare of %d is %d\n", num, squareThisNumber(num));

%Calling squareAndCubeThisNumber
printf("\nCalling squareAndCubeThisNumber");
num = 7;
[a b] = squareAndCubeThisNumber(num); 
printf("\nSquare and cube of %d is [%d %d]\n", num, a, b);

%Calling costFunctionJ
printf("\ncalling costFunctionJ");
X     = [1 1; 1 2; 1 3];
y     = [1; 2; 3];
theta = [0; 0.5];
printf("\ncostFunctionJ(X, y, theta) : %f\n", costFunctionJ(X, y, theta));
