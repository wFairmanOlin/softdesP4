# from bokeh.models.widgets import RadioButtonGroup
# from bokeh.plotting import figure, show
#
#
# def my_radio_handler():
#     print('Radio button option selected.')
#
#
# radio_button_group = RadioButtonGroup(
#         labels=["Option 1", "Option 2", "Option 3"], active=0)
#
# radio_button_group.on_click(my_radio_handler)
# show(radio_button_group)
from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure

plot = figure(plot_width=400, tools='pan')
plot.circle([1,2,3,4,5], [2,3,4,5,6])

output_file('test.html')
curdoc().add_root(plot)
