function tree_print(n,fid)
  global oGrid

  children=oGrid(n).children;
  
  while (~isempty(children))
    i=children(1);
    children=setdiff(children, i);
    
    fprintf(fid,'%s\n',strcat(['<Grid ',oGrid(i).name,'>']));
    tree_print(i,fid)
    fprintf(fid,'%s\n',strcat(['</Grid ',oGrid(i).name,'>']));
  end