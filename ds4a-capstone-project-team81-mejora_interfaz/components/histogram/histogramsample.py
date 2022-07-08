from dash import html , dcc
import plotly.express as px

class histogramsample:    
    """A class to represent a samplemap of Montreal Elections"""        
    def __init__(self,histogram_title:str,ID:str): 
        """__init__
        Construct all the attributes for the sample map
        Args:
            map_title (str): _Title for the map_
            ID (str): _div id to specify unique #id with callbacks and css_
        Methods:
        display()
            Function to display a sample map with no arguments, uses plotly express data.
            Arguments:
                None
            Returns:
                html.Div : A Div container with a dash core component dcc.Graph() inside
        """

        self.histogram_title = histogram_title
        self.id = ID

   