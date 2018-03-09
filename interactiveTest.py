from bokeh.io import show
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models.widgets import RadioButtonGroup
from bokeh.layouts import column, widgetbox
from bokeh.models.callbacks import CustomJS

dataset = {'x':[0,1,2],'y':[0,1,2],'x_filter':[0,1,2]}

source = ColumnDataSource(data=dataset)
p = figure(plot_width=600, plot_height=600,
            x_range=(-0.1, 2.1), y_range=(-0.1,2.1))
p.scatter('x', 'y', source=source,
          size=15, alpha=0.8, line_color=None)

# add callback to control
callback = CustomJS(args=dict(p=p, source=source), code="""

            var radio_value = cb_obj.active;
            var data = source.data;
            x = data['x']
            x_filter = data['x_filter']
            y = data['y']

            for (i = 0; i < x.length; i++) {
                if(x_filter[i] == radio_value) {
                    x[i] = x_filter[i];
                } else {
                    x[i] = undefined;
                }
            }
        source.change.emit();
        """)

# option
option = RadioButtonGroup(labels=["One", "Two", "Three"],
                          active=0, callback=callback)
show(column(widgetbox(option),p))
