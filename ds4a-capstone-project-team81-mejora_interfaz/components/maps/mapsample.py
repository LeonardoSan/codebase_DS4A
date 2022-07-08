from dash import html , dcc
import plotly.express as px

class mapsample:    
    """A class to represent a samplemap of Montreal Elections"""        
    def __init__(self,map_title:str,ID:str): 
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

        self.map_title = map_title
        self.id = ID

    @staticmethod
    def figura():

        df = px.data.non_nan_hurtos_año() # replace with your own data source
        # geojson = px.data.election_geojson()
        fig = px.scatter_mapbox(df, lat="latitud", lon="longitud", color="modalidad", size="Cantidad_casos",
                            size_max=25, zoom=10, center={"lat": 6.29970294, "lon": -75.58201578},
                            opacity=0.5)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_layout(autosize=True)
        fig.update_layout(height=600)
        fig.update_layout(width=600)
        fig.update_layout(title_text="Cantidad de casos de hurto en la ciudad de medellín")
        return fig
        
    
    def display(self):

        layout = html.Div(
            [
                html.H4([self.map_title]),
                html.Div([
                    dcc.Graph(figure=self.figura())
                ])

            ],id=self.id
        )
        return layout
        
        
        
        
        
        
        
        
        
        
        
        
        
