data = readmatrix("20260202\20260202\sweep_H1_phi_average10samples_20260202_120242.csv");
phases = data(:,1);
rawOut2 = data(:,2);
rawOut3 = data(:,4);

rawSum = rawOut2 + rawOut3;

normOut2 = rawOut2 ./ rawSum

normOut3 = rawOut3 ./ rawSum

plot(normOut2)