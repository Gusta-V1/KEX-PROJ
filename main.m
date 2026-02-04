data = readmatrix("20260202\20260202\sweep_H1_phi_average10samples_20260202_120242.csv");

phases = data(:,1);
rawOut2 = data(:,2);
rawOut3 = data(:,4);

badNormOut2 = data(:,3);
badNormOut3 = data(:,5);

rawSum = rawOut2 + rawOut3;

normOut2 = rawOut2 ./ rawSum;
normOut3 = rawOut3 ./ rawSum;

hold on
plot(phases, normOut2, "o")
plot(phases, badNormOut2, "o")
hold off

