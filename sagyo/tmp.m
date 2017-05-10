close all; clear;

M = csvread('tmp.csv');
M = M(2:6,:);
M(:,1:2) = M(:,1:2)*256/9;
M(:,3) = M(:,3)*256;
M(:,4:5) = M(:,4:5)*256/80;

big = imresize(uint8(M), 256/5,'box');
imwrite(big,'./tmp.png')
% imshow(big)

return;