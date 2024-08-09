import rioxarray
import xarray as xr

def stack_bands(stac_item, bandlist):
    '''
    Returns geocube with specified bands stacked into one multi-dimensional array.
            Parameters:
                    stac_item (dict): STAC item containing band information
                    bandlist (list): List of bands that should be stacked
            Returns:
                    bandStack (xarray.Dataset): Geocube with stacked bands
                    crs (str): Coordinate Reference System corresponding to bands
    '''
    bandStack = []
    bandS = []
    bandStack_ = []
    
    # Create a mapping from bandlist to the corresponding asset keys in the stac_item
    asset_keys = {band: key for key in stac_item['assets'] for band in bandlist if band in key}

    # Extract band URLs from the STAC item using the asset_keys mapping
    band_urls = {band: stac_item['assets'][asset_keys[band]]['href'] for band in bandlist}
    
    for i, band in enumerate(bandlist):
        url = band_urls[band]
        if i == 0:
            bandStack_ = rioxarray.open_rasterio(url)
            crs = bandStack_.rio.crs.to_string()  # Extract CRS directly
            bandStack_ = bandStack_ * bandStack_.scales[0] if hasattr(bandStack_, 'scales') else bandStack_
            bandStack = bandStack_.squeeze(drop=True)
            bandStack = bandStack.to_dataset(name='z')
            bandStack.coords['band'] = i + 1
            bandStack = bandStack.rename({'x': 'longitude', 'y': 'latitude', 'band': 'band'})
            bandStack = bandStack.expand_dims(dim='band')
        else:
            bandS = rioxarray.open_rasterio(url)
            bandS = bandS * bandS.scales[0] if hasattr(bandS, 'scales') else bandS
            bandS = bandS.squeeze(drop=True)
            bandS = bandS.to_dataset(name='z')
            bandS.coords['band'] = i + 1
            bandS = bandS.rename({'x': 'longitude', 'y': 'latitude', 'band': 'band'})
            bandS = bandS.expand_dims(dim='band')
            bandStack = xr.concat([bandStack, bandS], dim='band')
    
    return bandStack, crs


