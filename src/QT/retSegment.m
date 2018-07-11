function a = retSegment(imagePath)

img = imread(imagePath);
    
    % error checking, get one channel from image.
    if size(img,3) > 1
        img = img(:,:,1);
        display('warning: this is probably not an oct image');
    end
    
    % make image type as double.
    img = double(img);
    
    % get size of image.
    szImg = size(img);
    
    %segment whole image if yrange/xrange is not specified.
%     if isempty(yrange) && isempty(xrange)
%         yrange = 1:szImg(1);
%         xrange = 1:szImg(2);
%     end    
%     img = img(yrange,xrange);
    
    % get retinal layers.
    [retinalLayers, params] = getRetinalLayers(img);
    
    
    % save data to struct.
    imageLayer.imagePath = imagePath;
    imageLayer.retinalLayers = retinalLayers;    
    imageLayer.params = params;
    
filename = [imageLayer.imagePath '_octSegmentation.mat'];
save(filename, 'imageLayer');
display(sprintf('segmentation saved to %s',filename));

calculateRetinalThickness