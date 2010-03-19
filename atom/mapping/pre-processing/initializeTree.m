function [res dlist ilist]=initializeTree(filename)
global list n

list=[];
n=0;
parent=0;
t=parseXML(filename);
recursiveTree(t,parent);


index=1:n;
for i=1:n
  tmpset=[index([list(:).parent]==i)];
  if(~isempty(tmpset))
    list(i).children=tmpset;
  else
    list(i).children=-1;
  end
end
res=list;


ilist=[];
max_parent=max([list.parent]);
for p=0:max_parent
  for i=1:n
    if(list(i).parent==p)
      ilist=[i; ilist];
    end
  end
end
index=n:-1:1;
dlist=ilist(index);

ilist=ilist';
dlist=dlist';





function recursiveTree(t,parent)
global list n

if(strcmp(t.Name,'Grid')==1)
  n=n+1;
  list(n).name=t.Attributes.Value;
  list(n).parent=parent;
  p=n;
  
  nchildren=length(t.Children);
  for i=1:nchildren
    recursiveTree(t.Children(i),p);
  end
end


