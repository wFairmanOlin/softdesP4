# Boston Restaurant Inspection Data Visualization

We wanted to visualize the City of Boston's data concerning the health ratings of local restaurants. This data, while providing crucial information, is only accessible in a csv file approximately half a million lines long. By implementing the Bokeh python library, we were able to display restaurants on Google maps in a format that made it easy to view the severity of their failed inspections and the percentage of failed inspections.

## Getting Started

These instructions will get you a copy of the project up and running the data visualization on your local machine.

### Prerequisites


Install yelp-python from PyPI using:

```
pip3 install yelp

```

To run Yelp Fusion API Python using the Search API to query for businesses in ```Data_Mining_sofdesmp4.py``` or ```Yelp_Data.py```, install the dependencies by running:

```
pip3 install -r requirements.txt
```

Install the Bokeh library for visualizing the data by running:
```
pip3 install bokeh
```
Install Matplotlib by running:
```
sudo apt-get install python3-matplotlib
```
Install Geopy
```
pip3 install geopy
```
## Running
### To visualize the interactive data, run:
```
bokeh serve --show bokehMap.py
```
The color scale of the data points is blue to white to red where blue represents a low failure percentage and red represent a high failure percentage. The following picture is an example of the color scale:
![colorscale](https://github.com/wFairmanOlin/softdesP4/blob/master/images/cmap.png)

If the interactive map froze, hit refresh in the browser. Hover over each data point to see the restaurant name and costumer rating.

The data analysis result bokeh map calls is stored in ```processed_data/```.

### To conduct the data analysis, follow the below steps:
Warning: the process takes hours to run due to the large amount of data in the ```.csv```
```
cd data_mining_script
mkdir analyzed_data
mkdir color_data
mkdir foodtype_data
python3 Data_Mining_sofdesmp4.py
python3 Color.py
python3 Yelp_food_type.py
python3 coordinateFinder.py
```

## Built With

* [Bokeh](https://bokeh.pydata.org/en/latest/) - Used to generate visualization of interactive data.
* [Yelp Fusion API Python](https://www.yelp.com/developers/documentation/v3/get_started) - Used to query for restaurant rating and food type.
* [Matplotlib](https://matplotlib.org/) - Used to map percentage values to colormap scale.
* [Geopy](https://geopy.readthedocs.io/en/1.10.0/) - Used to query restaurant longitude and latitude.
* [data.boston.gov](https://data.boston.gov/dataset/food-establishment-inspections) - Used to download ```.csv``` file for data source.

## Authors

* **William Fairman**
* **Sherrie Shen**

## Acknowledgments

* [Yelp Fusion API Python](https://github.com/Yelp/yelp-fusion/tree/master/fusion/python) ```sample.py``` to query restaurant costumer rating and food type.
