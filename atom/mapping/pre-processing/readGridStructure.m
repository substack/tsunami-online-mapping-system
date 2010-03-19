function tGrid=readGridStructure(filename)

p=parseXML(filename);

tGrid.bathymetry_file    =  getTagValue(p,'bathymetry','file');
tGrid.bathymetry_units   =  getTagValue(p,'bathymetry','units');

tGrid.deformation_file   =  getTagValue(p,'deformation','file');
tGrid.deformation_units  =  getTagValue(p,'deformation','units');

tGrid.name          = getTagValue(p,'id','name');
tGrid.type          = getTagValue(p,'physics','type');
tGrid.color         = getTagValue(p,'visualize','color');

rx                  = getTagNumericalValue(p,'ratio','lon');
ry                  = getTagNumericalValue(p,'ratio','lat');
tGrid.ratio         = [rx ry];

tGrid.c.west        = getTagNumericalValue(p,'corner','west');
tGrid.c.south       = getTagNumericalValue(p,'corner','south');

tGrid.friction      = getTagNumericalValue(p,'physics','friction');
tGrid.level         = getTagNumericalValue(p,'physics','level');
tGrid.bath_prepost  = getTagNumericalValue(p,'physics','bathpp');




function value=getTagData(p,tagName)

nChildren=length(p.Children);
for i=1:nChildren
  if(strcmp(p.Children(i).Name,tagName)==1)
    attr=p.Children(i).Attributes;
    nattr=length(attr);
    value=p.Children(i).Children.Data;
    return
  end
end

function value=getTagValue(p,tagName,attrName)
nChildren=length(p.Children);
for i=1:nChildren
  if(strcmp(p.Children(i).Name,tagName)==1)
    attr=p.Children(i).Attributes;
    nattr=length(attr);
    for j=1:nattr
      if(strcmp(attr(j).Name,attrName)==1)
        value=strcat(attr(j).Value);
        return
      end
    end
  end
end
value=0;


function value=getTagNumericalValue(p,tagName,attrName)
nChildren=length(p.Children);
for i=1:nChildren
  if(strcmp(p.Children(i).Name,tagName)==1)
    attr=p.Children(i).Attributes;
    nattr=length(attr);
    for j=1:nattr
      if(strcmp(attr(j).Name,attrName)==1)
        value=str2num(attr(j).Value);
        return
      end
    end
  end
end
value=0;

