%clear all
%filename = input('Filename: ') 
%filename='test';
[long, latg, defg, dlon, dlat]=loadXYZ([filename,'.xyz']);

list1=[];
for i=1:size(long,1)
  if(max(abs(defg(i,:)))>0.1)
    list1=[list1 i];
  end
end
list1=min(list1):max(list1);

list2=[];
for i=1:size(long,2)
  if(max(abs(defg(:,i)))>0.1)
    list2=[list2 i];
  end
end
list2=min(list2):max(list2);


defg(abs(defg)<0.1)=NaN;

%rgb=load('BlWhRe.rgb');

figure(1)
contourf(long(list1,list2), latg(list1,list2), defg(list1,list2),[-100 -5:1:5 100],'LineStyle','none');
caxis([-5 5]);
%colormap(rgb/255);
hold on
[c,h]=contour(long(list1,list2), latg(list1,list2), defg(list1,list2),[-100 -5:1:5 100]);
clabel(c,h,'Rotation',0)
hold off
axis off

print('-depsc', [filename,'.eps']);

tmp=[min(min(long(list1,list2))) max(max(long(list1,list2))) min(min(latg(list1,list2))) max(max(latg(list1,list2)))];
save([filename,'.extent'],'tmp','-ASCII')

