from bokeh.io import output_file, show, curdoc
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource,
  CustomJS, Circle, Range1d, PanTool, WheelZoomTool, BoxSelectTool
)
from bokeh.layouts import widgetbox, column, row
from bokeh.models.widgets import RadioButtonGroup, Select
from bokeh.models.callbacks import CustomJS
from bokeh.colors import RGB
from dataProcessing import *
from bokeh.models import HoverTool
from bokeh.plotting import figure, show, output_file

severity1 = generate_severityDictionary('1', RGB(255,200,0))
severity2 = generate_severityDictionary('2', RGB(255,100,0))
severity3 = generate_severityDictionary('3', RGB(255,0,0))
general = generate_mainDictionary('color_data/restaurant_violation_percentage.pickle')

#severity2 = generate_dictionary('analyzed_data/completeSeverity2.pickle')
#severity3 = generate_dictionary('analyzed_data/completeSeverity3.pickle')
def generate_colorScale():
    """
    return a list of colors for each glyph
    """
    pass

def callback(new):
    """
    Defines the the series of events that occur
    after a radio button is clicked.
    """
    #value of the clicked radio button
    i = new
    print(i)
    source.data = general

    #example of isolating certain data points when clicked
    # data = dataSource
    # x = data['lon']
    # y = data['lat']
    # print(x,y)
    # x = x[i]
    # y = y[i]

    #example of changing the color of data points when clicked
    # plot.renderers[0].glyph.fill_color=color[i]
    # source.data = dict(lon=[x], lat=[y])

def show_severity(attr, old, new):
    print(new)
    if new == 'high':
        source.data = severity3
    elif new == 'medium':
        source.data = severity2
    else:
        source.data = severity1
#Examples of custom color scale
#define colors by RGB value
color_range = [RGB(255,0,0), RGB(255,100,0), RGB(255,200,0)]
#define colors by name
color = ['green', 'blue', 'red']

#data source containing the location and color of each glyph
dataSource = dict(lat=[42.2932, 42.2936, 42.2994],
                lon=[-71.2637, -71.3059, -71.2660], color=color_range, name=['Olin', 'Wellsley', 'Babson'])

#Converts our data points into a bokeh readable object
source = ColumnDataSource(
    data=general)

#Creates the glyphs for the map
circle = Circle(x="lon", y="lat", size=11, fill_color="color", fill_alpha=0.8, line_color=None)

#Generates geographical map of Boston
map_options = GMapOptions(lat=42.36, lng=-71.05, map_type="roadmap", zoom=12)
plot = GMapPlot(x_range=Range1d(), y_range=Range1d(), map_options=map_options, plot_width=1500, plot_height=800)
plot.title.text = "Boston"
#My personal google api key
plot.api_key = " AIzaSyBt2HETloZkCelX_XuVAXAgRkds_nBhNZQ"


#Adds glyph and tools to the map
hover = HoverTool(tooltips=[
     ("Name", "@name")])
plot.add_glyph(source, circle)
plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool(), hover)

colorScale = figure(x_range=(0,1), y_range=(0,1))#x_range=(0,1), y_range=(0,1))
colorScale.image_url(url=['CMAP.jpg'],x=1, y=1, h=600, w=100)

#Initiates the objects into the html web page
button_group = RadioButtonGroup(labels=["Amon", "Ben", "Paul"], active=0)
select = Select(title="Severity Level:", value="low", options=["high", "medium", "low"])
output_file("gmap_plot.html")
#defines the layouts of the objects
layout = column(row(plot, colorScale), button_group, select)
#defines what happpens on a button click event
button_group.on_click(callback)
select.on_change('value', show_severity)
#Begins the script
curdoc().add_root(layout)#column(plot, button_group))
