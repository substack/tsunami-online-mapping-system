% clear all;
% filename='xyz_files/SE08c';
[long, latg, defg, dlon, dlat]=loadXYZ([directory, filename,'.xyz']);

[c,h]=contour(long, latg, defg,[min_water_depth 1]);

id=floor(rand(1,1)*1000);

f=fopen([filename,'.kml'],'wt');


fprintf(f,'%s\n','<?xml version="1.0" encoding="UTF-8"?>');
fprintf(f,'%s\n','<kml xmlns="http://www.opengis.net/kml/2.2">');
fprintf(f,'%s\n','<Document>');

index=1;
while (index<length(c))
  if (c(1,index) == min_water_depth)
    fprintf(f,'%s\n','<Placemark>');
    fprintf(f,'%s\n','  <LineString>');
    fprintf(f,'%s\n','    <coordinates>');
    for i=index+1:index+c(2,index)
      if (c(1,i) > 180)
        fprintf(f,'    %13.5f, %13.5f, %d\n', c(1,i)-360, c(2,i), id);
      else
        fprintf(f,'    %13.5f, %13.5f, %d\n', c(1,i), c(2,i), id);
      end
    end
    fprintf(f,'%s\n','    </coordinates>');
    fprintf(f,'%s\n','  </LineString>');
    fprintf(f,'%s\n','</Placemark>');
    index=i+1;
  else
    index=index+c(2,index)+1;
  end
end
fprintf(f,'%s\n','</Document>');
fprintf(f,'%s\n','</kml>');
fclose(f);