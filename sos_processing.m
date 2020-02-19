%% REQUIRES DATA FROM DIGILENT

% distances between receivers and source
r1 = 1.4097;
r2 = 1.4478;

% data from source
data = csvread('air_data_3.csv', 25, 0);
Fs = ceil(1/abs(data(2,1)-data(1,1)));
N = length(data(:, 1));
t = linspace(0, (N-1)/Fs, N);
c1 = data(:, 2);
c2 = data(:, 3);

% raw signals plot
figure;
plot(t, c1, 'Color', 'r');
hold on
plot(t, c2, 'Color', 'b');
xlim([0 t(end)]);
title('Raw Signals');
xlabel('time (seconds)');
ylabel('Voltage (V)');
legend('Channel 1', 'Channel 2');

k = linspace(0, (N-1), N)*Fs/N;
C1 = fft(c1.*hamming(N), N);
C2 = fft(c2.*hamming(N), N);

M = zeros(1, 2);
M(1, 1) = max(abs(C1));
M(1, 2) = max(abs(C2));

if M(1, 1) >= M(1, 2)
    M = M(1, 1);
else
    M = M(1, 2);
end

% spectral plot
figure;
subplot(2,1,1);
plot(k(1:N/2)./1e+03, 20*log10(abs(C1(1:N/2))./M), 'Color', 'r');
xlim([0, 10]);
title('Spectral Comparison');
ylabel('Magnitude (dB)');
xlabel('Frequency (kHz)');
legend('Channel 1');
subplot(2,1,2);
plot(k(1:N/2)./1e+03, 20*log10(abs(C2(1:N/2))./M), 'Color', 'b');
xlim([0, 10]);
ylabel('Magnitude (dB)');
xlabel('Frequency (kHz)');
legend('Channel 2')

% filter signals
Num = load('sos_filter.mat');
Num = Num.Num;

c1 = filter(Num, 1, c1);
c2 = filter(Num, 1, c2);

% calculate correlation
C = xcorr(c1, c2);
t = -t(end):(1/Fs):t(end);

figure;
plot(t, 20*log10(abs(C)./max(abs(C))), 'Color', 'r');
xlim([0 t(end)]);
ylim([-60 0]);
xlabel('time (seconds)');
ylabel('Magnitude (dB)');
title('Correlation of Filtered Signals');

[Cmax, Cind] = max(20*log10(abs(C(N:end))./max(abs(C(N:end)))));

t = t(N:end);
dt = t(Cind);

% calculate speed of sound
c = abs(r1-r2)/dt;

disp(['The Approximate Speed of Sound is: ' num2str(c) ' m/s'])


