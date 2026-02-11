data = readmatrix("20260205\source-g3theta_target-g4theta.csv");

phases = data(:,1);
norm1 = data(:,3);
norm2 = data(:,5);

disp(norm1 + norm2)

% norm1_13 = norm1(1:13);
% norm2_13 = norm2(1:13);
% phases_13 = phases(1:13);
% 
% ft = fittype('A*sin(B + C*x)^2 + D', ...
%     'independent', 'x', ...
%     'coefficients', {'A', 'B', 'C', 'D'});
% 
% p0 = [1, pi/4, 2, 0.5];
% 
% [f, gof] = fit(phases_13, norm2_13, ft, "StartPoint", p0);
% 
% hold on
% plot(phases_13, norm2_13, "o")
% plot(phases_13, f(phases_13))
% hold off