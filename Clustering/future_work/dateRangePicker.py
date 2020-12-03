import pandas as pd
import ipywidgets as widgets
from IPython import display

class DateRangePicker(object):
    def __init__(self,start,end,freq='D',fmt='%Y-%m-%d'):
        """
        Parameters
        ----------
        start : string or datetime-like
            Left bound of the period
        freq : string or pandas.DateOffset, default='D'
            Frequency strings can have multiples, e.g. '5H' 
        fmt : string, defauly = '%Y-%m-%d'
            Format to use to display the selected period

        """
        self.date_range=pd.date_range(start=start,end=end,freq=freq)
        options = [(item.strftime(fmt),item) for item in self.date_range]
        self.slider_start = widgets.SelectionSlider(
            description='date',
            options=options,
            continuous_update=False
        )

        self.slider_start.on_trait_change(self.slider_start_changed, 'value')

        self.widget = widgets.Box(children=[self.slider_start])

    def slider_start_changed(self,key,value):
        display.clear_output()
        display.display(self.slider_start)
        self._observe(date=self.slider_start.value)

    def display(self):
        display.display(self.slider_start)

    def _observe(self,**kwargs):
        if hasattr(self,'observe'):
            self.observe(**kwargs)
