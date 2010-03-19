%clear all

%      Case is an object consisting of a number of vectors that correspont to
%      different scenarios. Each vector has 3 elements: scenario name,
%      number, and the color to plot the line

%Case{1}={  'DART_21414',   'NW Pacific',     '-r'    };
%Case{2}={  'DART_46409',   'NW Pacific2',     '-r'   };

%--------------------------------------------------------------

dir='../';
dir_plots='./';

time_plot_axis_scale='min';
time_plot_interval=15*60;      %how many ticks and grid lines
time_plot_scale=1/60;
time_ticks_ratio=4;            % every 3rd tick will be labeled

tt=0;
%----opening the files with time series data---------
for c=1:length(Case)
    fname{c}=[dir,'Point_',Case{c}{1},'.ts'];
    time_series{c}=load(fname{c});
    len=length(time_series{c}(:,1));

    time=time_series{c}(2:len,1);
    time_length=length(time);

%---------------------plotting--------------------

    plot_title='Sea level';
    plot_units='m';

    tt=tt+1; 
    figure(tt)
    str='';
    plot(time,time_series{c}(2:len,2),Case{c}{3})
    str=strvcat(str, Case{c}{2});
 
    time_ticks=[0 time_plot_interval:time_plot_interval:time(time_length)];
    time_ticksLabels= num2cell(time_ticks*time_plot_scale);
    for j=2:length(time_ticksLabels)
        if( mod(j,time_ticks_ratio) ~=1)   
            time_ticksLabels{j}='';
        end
    end
     
    h = legend(str,1);
    set(h,'Interpreter','none');
    set(gca,'XTick',time_ticks);
    set(gca,'XTickLabel',time_ticksLabels);
    grid on
    
    
    xlabel(['\fontsize{14}{Time after the earthquake, ',time_plot_axis_scale,'}']);
    ylabel(['\fontsize{14}{', plot_title, ', ', plot_units, '}']);
       
    title( ['Time series of ',plot_title]);

    fname_png=[dir_plots,'Point_',Case{c}{1},'_Z.png'];
    print('-dpng', fname_png);
    
    %---------------------plotting--------------------

    plot_title='velocity';
    plot_units='m/sec';
    var='vel';
    
    vel=sqrt(time_series{c}(2:len,4).^2+time_series{c}(2:len,5).^2)./time_series{c}(2:len,3);
    index=(time_series{c}(2:len,3)<0.1);
    vel(index)=NaN;
    
    tt=tt+1;
    figure(tt)
    str='';
    plot(time,vel,Case{c}{3})
    str=strvcat(str, Case{c}{2});
 
    time_ticks=[0 time_plot_interval:time_plot_interval:time(time_length)];
    time_ticksLabels= num2cell(time_ticks*time_plot_scale);
    for j=2:length(time_ticksLabels)
        if( mod(j,time_ticks_ratio) ~=1)   
            time_ticksLabels{j}='';
        end
    end
     
    h = legend(str,1);
    set(h,'Interpreter','none');
    set(gca,'XTick',time_ticks);
    set(gca,'XTickLabel',time_ticksLabels);
    grid on
    
    
    xlabel(['\fontsize{14}{Time after the earthquake, ',time_plot_axis_scale,'}']);
    ylabel(['\fontsize{14}{', plot_title, ', ', plot_units, '}']);
       
    title( ['Time series of ',plot_title]);

    fname_png=[dir_plots,'Point_',Case{c}{1},'_V.png'];
    print('-dpng', fname_png);
end
