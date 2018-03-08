from bokeh.io import output_file, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, Range1d, PanTool, WheelZoomTool, BoxSelectTool
)

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
source = ColumnDataSource(
    data=dict(
        lat=[42.2932, 42.2936],
        lon=[-71.2637, -71.3059],
    )
)

circle = Circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, line_color=None)
plot.add_glyph(source, circle)

plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
output_file("gmap_plot.html")
show(plot)
