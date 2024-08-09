import numpy as np
import xarray as xr
import pandas as pd
import holoviews as hv
import panel as pn
import param
import hvplot.xarray
from bokeh.models import FixedTicker
from bokeh.plotting import show, output_notebook
import cartopy.crs as ccrs
import geoviews as gv

output_notebook()
pn.extension()

class VegDistVisualizer(param.Parameterized):
    da = param.Parameter()
    
    start_date = param.Parameter()
    max_value = param.Parameter()
    max_date = param.Parameter()
    min_date = param.Parameter()
    
    min_date_slider = param.Parameter()
    max_date_slider = param.Parameter()
    
    base = param.Parameter()
    
    def __init__(self, da, **params):
        super().__init__(**params)
        
        self.da = da
        self.start_date = pd.Timestamp('2020-12-31')
        self.max_value = da.z.sel({'band': 2}).max().item()
        self.max_date = self.start_date + pd.to_timedelta(self.max_value, unit='D')
        self.min_date = self.start_date

        self.min_date_slider = pn.widgets.DateSlider(
            name='Min Date', start=self.min_date, end=self.max_date, value=self.min_date, sizing_mode='stretch_width'
        )
        self.max_date_slider = pn.widgets.DateSlider(
            name='Max Date', start=self.min_date, end=self.max_date, value=self.max_date, sizing_mode='stretch_width'
        )

        self.base = gv.tile_sources.EsriImagery.opts(width=1000, height=1000, padding=0.1)

    @pn.depends('min_date_slider.value', 'max_date_slider.value')
    def veg_dist_date_plot(self):
        min_days = (pd.Timestamp(self.min_date_slider.value) - self.start_date).days
        max_days = (pd.Timestamp(self.max_date_slider.value) - self.start_date).days

        masked_veg_dist_date = self.da.z.sel({'band': 2}).where(
            (self.da.z.sel({'band': 2}) >= min_days) & (self.da.z.sel({'band': 2}) <= max_days), np.nan
        )

        plot = masked_veg_dist_date.hvplot.image(
            x='longitude', 
            y='latitude', 
            crs=ccrs.PlateCarree(), 
            rasterize=True, 
            dynamic=False, 
            aspect='equal', 
            cmap='hot_r', 
            alpha=0.8,
            width=400, 
            height=400
        ).opts(
            title="VEG_DIST_DATE", 
            xlabel='Longitude', 
            ylabel='Latitude', 
            clim=(min_days, max_days),
            colorbar=True,
            colorbar_opts={
                'title': 'Days',
                'ticker': FixedTicker(ticks=list(range(min_days, max_days + 1))),
                'title_standoff': 10,
                'label_standoff': 8,
                'major_label_text_font_size': '10pt',
                'title_text_font_size': '12pt'
            }
        ) * self.base

        return plot

    @pn.depends('min_date_slider.value', 'max_date_slider.value')
    def veg_dist_status_plot(self):
        min_days = (pd.Timestamp(self.min_date_slider.value) - self.start_date).days
        max_days = (pd.Timestamp(self.max_date_slider.value) - self.start_date).days

        veg_dist_date_filtered = self.da.z.sel({'band': 2}).where(
            (self.da.z.sel({'band': 2}) >= min_days) & (self.da.z.sel({'band': 2}) <= max_days)
        )

        veg_dist_date_filtered, veg_dist_status = xr.align(
            veg_dist_date_filtered, self.da.z.sel({'band': 3}), join='inner', copy=False
        )

        veg_dist_status_filtered = veg_dist_status.where(
            veg_dist_date_filtered.notnull() & ((veg_dist_status != 0) & (veg_dist_status != 255)), np.nan
        )

        plot = veg_dist_status_filtered.hvplot.image(
            x='longitude', 
            y='latitude', 
            crs=ccrs.PlateCarree(), 
            rasterize=True, 
            dynamic=False, 
            aspect='equal', 
            cmap='hot_r', 
            alpha=0.8,
            width=400, 
            height=400
        ).opts(
            title="VEG_DIST_STATUS", 
            clim=(0, 4), 
            colorbar_opts={'ticker': FixedTicker(ticks=[0, 1, 2, 3, 4])}, 
            xlabel='Longitude', 
            ylabel='Latitude'
        ) * self.base

        return plot

    @pn.depends('min_date_slider.value', 'max_date_slider.value')
    def veg_anom_max_plot(self):
        min_days = (pd.Timestamp(self.min_date_slider.value) - self.start_date).days
        max_days = (pd.Timestamp(self.max_date_slider.value) - self.start_date).days

        veg_anom_max_filtered = self.da.z.sel({'band': 1}).where(
            (self.da.z.sel({'band': 1}) != 0) & 
            (self.da.z.sel({'band': 1}) != 255) & 
            (self.da.z.sel({'band': 2}) >= min_days) & 
            (self.da.z.sel({'band': 2}) <= max_days), np.nan
        )

        plot = veg_anom_max_filtered.hvplot.image(
            x='longitude', 
            y='latitude', 
            crs=ccrs.PlateCarree(), 
            rasterize=True, 
            dynamic=False, 
            aspect='equal', 
            cmap='hot_r', 
            alpha=0.8,
            width=400, 
            height=400
        ).opts(
            title="VEG_ANOM_MAX", 
            xlabel='Longitude', 
            ylabel='Latitude',
            clim=(0, 100)
        ) * self.base

        return plot

    def panel_layout(self):
        return pn.Column(
            pn.Row(self.min_date_slider, self.max_date_slider, sizing_mode='scale_width'),
            pn.Row(
                pn.panel(self.veg_dist_date_plot, sizing_mode='scale_width'), 
                pn.panel(self.veg_dist_status_plot, sizing_mode='scale_width'),
                pn.panel(self.veg_anom_max_plot, sizing_mode='scale_width')
            )
        )




