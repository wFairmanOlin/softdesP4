from bokeh.io import output_file, show, curdoc
from bokeh.models import (
    GMapPlot, GMapOptions, ColumnDataSource,
    CustomJS, Circle, Range1d, PanTool, WheelZoomTool, BoxSelectTool
)
from bokeh.layouts import widgetbox, column, row
from bokeh.models.widgets import RadioButtonGroup, Select, Button
from bokeh.models.callbacks import CustomJS
from bokeh.colors import RGB
from dataProcessing import *
from bokeh.models import HoverTool
from bokeh.plotting import figure, show, output_file
from bokeh.models import Legend

severity1 = generate_severityDictionary('1', RGB(255, 200, 0))
severity2 = generate_severityDictionary('2', RGB(255, 100, 0))
severity3 = generate_severityDictionary('3', RGB(255, 0, 0))
general = generate_mainDictionary('processed_data/restaurant_violation_percentage.pickle')
Italian = generate_foodtypeDictionary('processed_data/foodtype.pickle', 'Italian', RGB(51, 51, 255))
print('Italian Works')
Mexican = generate_foodtypeDictionary('processed_data/foodtype.pickle', 'Mexican', RGB(100, 255, 0))
Chinese = generate_foodtypeDictionary('processed_data/foodtype.pickle', 'Chinese', RGB(127, 0, 255))
Seafood = generate_foodtypeDictionary('processed_data/foodtype.pickle', 'Seafood', RGB(255, 51, 51))
Sandwiches = generate_foodtypeDictionary('processed_data/foodtype.pickle', 'Sandwiches', RGB(0, 153, 0))
Indian = generate_foodtypeDictionary('processed_data/foodtype.pickle', 'Indian', RGB(255, 102, 178))
Coffee_Tea = generate_foodtypeDictionary('processed_data/foodtype.pickle', 'Coffee & Tea', 'brown')
Pizza = generate_foodtypeDictionary('processed_data/foodtype.pickle', 'Pizza', RGB(255, 153, 51))


def callback():
    """
    Defines the the series of events that occur
    after a radio button is clicked.
    """
    source.data = general


def show_severity(attr, old, new):
    print(new)
    if new == 'high':
        source.data = severity3
    elif new == 'medium':
        source.data = severity2
    else:
        source.data = severity1


def show_food_type(attr, old, new):
    if new == 'Italian':
        source.data = Italian
    elif new == 'Mexican':
        source.data = Mexican
    elif new == 'Chinese':
        source.data = Chinese
    elif new == 'Seafood':
        source.data = Seafood
    elif new == 'Sandwiches':
        source.data = Sandwiches
    elif new == 'Indian':
        source.data = Indian
    elif new == 'Coffee&Tea':
        source.data = Coffee_Tea
    elif new == 'Pizza':
        source.data = Pizza


# Converts our data points into a bokeh readable object
source = ColumnDataSource(
    data=general)

# Creates the glyphs for the map
circle = Circle(x="lon", y="lat", size=11, fill_color="color", fill_alpha=0.8, line_color=None)

# Generates geographical map of Boston
map_options = GMapOptions(lat=42.36, lng=-71.05, map_type="roadmap", zoom=12)
plot = GMapPlot(x_range=Range1d(), y_range=Range1d(), map_options=map_options, plot_width=1200, plot_height=800)
plot.title.text = "Boston Restaurant Data"

# My personal google api key
plot.api_key = " AIzaSyBt2HETloZkCelX_XuVAXAgRkds_nBhNZQ"

# Adds glyph and tools to the map
hover = HoverTool(tooltips=[
    ("Name", "@name"),
    ("Customer Rating", "@rating")])
plot.add_glyph(source, circle)
plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool(), hover)

# Initiates the objects into the html web page
button_1 = Button(label="Show all Restaurants")
# button_group = RadioButtonGroup(labels=["Show All Restaurants"], active=-1)

#drop down menu for severity
select = Select(title="Failure Severity Level:", value="low", options=["high", "medium", "low"])
output_file("gmap_plot.html")

#drop down menu for food type
select2 = Select(title="Restaurant Food Type", value="Italian",
                 options=["Italian", "Mexican", "Chinese", "Seafood", "Sandwiches", "Indian", "Coffee&Tea", "Pizza"])
output_file("gmap_plot.html")

# defines the layouts of the objects
layout = column(plot, row(button_1, select, select2))
# defines what happpens on a button click event

button_1.on_click(callback)
select.on_change('value', show_severity)
select2.on_change('value', show_food_type)

# Begins the script
curdoc().add_root(layout)  # column(plot, button_group))
