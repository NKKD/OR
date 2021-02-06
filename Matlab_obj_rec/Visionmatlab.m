clear;
%%socket communication with robotstudio WIN cmd+netstat -an|findstr 30000
 
tc=tcpip('192.168.0.20',1025); 
%open the communication 
fopen(tc);

% recive a message from the robotstudio
message=fread(tc,7);

% Run vision progamme

 if char(message')=="Execute"
%% calibration data &  get image
clear cam ;
IntrinsicMatrix = [124280.704481015,0,0;0,127713.500683758,0;1592.23618278809,1175.85902038706,1];
radialDistortion = [-66.0119 1.1457e+05]; 
cameraParams = cameraParameters('IntrinsicMatrix',IntrinsicMatrix,'RadialDistortion',radialDistortion); 



cam = webcam(1);
cam.Resolution = '3264x2448';
preview(cam);
pause(7);
closePreview(cam);
scene = snapshot(cam);

figure;
imshow(scene);
title('Distorted Image');

[sceneImage, newOrigin] = undistortImage(scene, cameraParams, 'OutputView', 'full');
figure;
imshow(sceneImage);
title('Undistorted Image');

%% image processing

scene=rgb2gray(sceneImage);
imshow(scene);

%% target define

targetImage = imread('fanta.jpg');
figure;
imshow(targetImage);
title('target');

%% RGB TO GRAY

target = rgb2gray(targetImage);
figure;
imshow(target);

%% detect feature point

targetPoints = detectSURFFeatures(target);
scenePoints = detectSURFFeatures(scene);

%% Visualize the strongest feature points found in the reference image.

figure;
imshow(target);
title('Strongest Feature Points from target Image');
hold on;
plot(selectStrongest(targetPoints, 300));

figure;
imshow(scene);
title('Strongest Feature Points from scene Image');
hold on;
plot(selectStrongest(scenePoints, 1500));

%% Extract feature descriptors at the interest points in both images.

[targetFeatures, targetPoints] = extractFeatures(target,targetPoints);
[sceneFeatures, scenePoints] = extractFeatures(scene, scenePoints);

%% Match the features using their descriptors.

targetPairs = matchFeatures(targetFeatures, sceneFeatures);

%% Display putatively matched features.

matchedtargetPoints = targetPoints(targetPairs(:, 1), :);
matchedscenePoints = scenePoints(targetPairs(:, 2), :);
figure;
showMatchedFeatures(target, scene, matchedtargetPoints,matchedscenePoints, 'montage');
title('Putatively Matched Points (Including Outliers)');

%% estimateGeometricTransform calculates the transformation relating the matched points,while eliminating outliers. This transformation allows us to localize the object in the scene.

[tform, inliertargetPoints, inlierscenePoints] = ...
    estimateGeometricTransform(matchedtargetPoints, matchedscenePoints, 'affine');

%% Display the matching point pairs with the outliers removed

figure;
showMatchedFeatures(targetImage, sceneImage, inliertargetPoints, ...
    inlierscenePoints, 'montage');
title('Matched Points (Inliers Only)');

%% bounding polygon

targetPolygon = [1, 1;...                           % top-left
        size(target, 2), 1;...                 % top-right
        size(target, 2), size(target, 1);... % bottom-right
        1, size(target, 1);...                 % bottom-left
        1, 1];                   % top-left again to close the polygon

%% Transform the polygon into the coordinate system of the target image.

newtargetPolygon = transformPointsForward(tform, targetPolygon);
pgon = polyshape(newtargetPolygon);
[x,y] = centroid(pgon);
X=(y/2472)*344.4+1167.9;
Y=(x/3296)*440.6-243;
%  t=tfotm(T);
%  quat = tform2quat(tform);??
%% Display the detected object.

figure;
imshow(scene);
hold on;
line(newtargetPolygon(:, 1), newtargetPolygon(:, 2), 'Color', 'b');
plot(x,y, 'r+', 'MarkerSize', 30, 'LineWidth', 2);
title('Detected target');



     t=num2str(X);
     A = convertCharsToStrings(t);
     
        % return X(coordinates) to server
        fwrite(tc,A);
        
         t=num2str(Y);
     B = convertCharsToStrings(t);
     
        % return Y(coordinates) to server
        fwrite(tc,B);
 
 else
     disp('ERROR!')
 end

% Convert string to num
% T=char(message');
% t=str2num(T);
