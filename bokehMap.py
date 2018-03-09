from bokeh.io import output_file, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, CustomJS, Circle, Range1d, PanTool, WheelZoomTool, BoxSelectTool
)
from bokeh.layouts import widgetbox, column
from bokeh.models.widgets import Button, RadioButtonGroup, Select, Slider






map_options = GMapOptions(lat=42.36, lng=-71.05, map_type="roadmap", zoom=11)

plot = GMapPlot(x_range=Range1d(), y_range=Range1d(), map_options=map_options)
plot.title.text = "Boston"

# For GMaps to function, Google requires you obtain and enable an API key:
#
#     https://developers.google.com/maps/documentation/javascript/get-api-key
#
# Replace the value below with your personal API key:
plot.api_key = " AIzaSyBt2HETloZkCelX_XuVAXAgRkds_nBhNZQ"

#42.2932° N, 71.2637° W
#42.2936° N, 71.3059° W
#data = {'olin': [42.2932, -71.2637], 'wellsley': [42.2936, -71.3059]}

source = ColumnDataSource(
    data=dict(
        lat=[42.2932, 42.2936],
        lon=[-71.2637, -71.3059],
    )
)

circle = Circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, line_color=None)

plot.add_glyph(source, circle)

plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())

callback = CustomJS(args=dict(p=circle, source=source), code="""

            dsfdgfbjhbagahgbyukabgfyu
            var radio_value = cb_obj.active;
            var data = source.data;
            x = data['lon'];
            y = data['lat'];
            x = x[radio_value]
            y = y[radio_value]
        source.change.emit();
        """)


button_group = RadioButtonGroup(labels=["Qin Mo", "Deng Qhin Mo", "Josh Deng"], active=0, callback=callback)
#output_file("gmap_plot.html")
#layout = column(plot, button_group)
show(column(plot, button_group))
#show(widgetbox(button_group))
