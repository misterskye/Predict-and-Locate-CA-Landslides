# Library Imports
import os
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, box, MultiPolygon
from skimage import measure
import matplotlib.pyplot as plt
import xarray as xr

def fig_boundingboxes(astar, beginning_date, end_date, threshold, output_dir, california_shapefile):
    # Get the latitude and longitude values
    lats = astar['latitude'].values
    lons = astar['longitude'].values

    # Create a meshgrid of the coordinates
    lon_grid, lat_grid = np.meshgrid(lons, lats)

    # Find the indices corresponding to the time range
    time_indices = np.where((astar['time'].values >= np.datetime64(beginning_date)) & 
                            (astar['time'].values <= np.datetime64(end_date)))[0]

    # Segment the A* prism to the specified dates
    astar_storm = astar.isel(z=slice(time_indices[0], time_indices[-1]+1))

    # Calculate maximum value over the storm window
    astar_storm_max = astar_storm.max(dim='z')

    # Threshold the data to identify regions with values >= threshold
    binary_mask = astar_storm_max >= threshold

    # Convert binary_mask to a NumPy array
    binary_mask_np = binary_mask.values

    # Find contours of the thresholded regions
    contours = measure.find_contours(binary_mask_np, 0.5)

    # Convert contours to polygons
    polygons = []
    for contour in contours:
        # Ensure contour points are within the array bounds
        contour = np.clip(contour, 0, [binary_mask_np.shape[0]-1, binary_mask_np.shape[1]-1])
        # Get the geographic coordinates for the contour points
        poly_coords = np.column_stack((lon_grid[contour[:, 0].astype(int), contour[:, 1].astype(int)], 
                                       lat_grid[contour[:, 0].astype(int), contour[:, 1].astype(int)]))
        if poly_coords.shape[0] >= 3:  # Ensure there are at least 3 points to form a polygon
            polygons.append(Polygon(poly_coords))

    # Create bounding boxes for each polygon
    bounding_boxes = [polygon.bounds for polygon in polygons]
    bbox_polygons = [box(*bbox) for bbox in bounding_boxes]

    # Create a table for bounding box coordinates and calculate areas
    bbox_coords = []
    for bbox in bounding_boxes:
        minx, miny, maxx, maxy = bbox
        area = (maxx - minx) * (maxy - miny)
        bbox_coords.append({'min_lon': minx, 'min_lat': miny, 'max_lon': maxx, 'max_lat': maxy, 'area': area})

    # Convert to DataFrame and sort by area in descending order
    bbox_df = pd.DataFrame(bbox_coords)
    bbox_df_sorted = bbox_df.sort_values(by='area', ascending=False).reset_index(drop=True)

    # Remove the area column before saving to CSV
    bbox_df_sorted = bbox_df_sorted.drop(columns=['area'])

    # Save the bounding box coordinates to a CSV file
    bbox_csv_file = os.path.join(output_dir, 'bounding_box_coords.csv')
    bbox_df_sorted.to_csv(bbox_csv_file, index=False)

    # Create a GeoDataFrame to store the polygons and bounding boxes
    gdf_polygons = gpd.GeoDataFrame({'geometry': polygons})
    gdf_bboxes = gpd.GeoDataFrame({'geometry': bbox_polygons})

    # Define the output file paths
    output_file_polygons = os.path.join(output_dir, 'polygons.geojson')
    output_file_bboxes = os.path.join(output_dir, 'bounding_boxes.geojson')

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save the polygons and bounding boxes to GeoJSON files
    gdf_polygons.to_file(output_file_polygons, driver='GeoJSON')
    gdf_bboxes.to_file(output_file_bboxes, driver='GeoJSON')

    print(f"Polygons saved to {output_file_polygons}")
    print(f"Bounding boxes saved to {output_file_bboxes}")
    print(f"Bounding box coordinates saved to {bbox_csv_file}")

    # Load the California boundary polygon
    gdf_california = gpd.read_file(california_shapefile)

    # Check the current CRS and reproject to WGS84 if necessary
    if gdf_california.crs != 'EPSG:4326':
        gdf_california = gdf_california.to_crs('EPSG:4326')

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.imshow(astar_storm_max, extent=(lons.min(), lons.max(), lats.min(), lats.max()), vmin=1.0, vmax=1.5, cmap='viridis')
    plt.colorbar(label='Astar Values')
    plt.title('Astar Max Values with Polygons, Bounding Boxes, and California Polygon')

    # Plot the polygons
    for polygon in polygons:
        if polygon.is_valid:
            x, y = polygon.exterior.xy
            plt.plot(x, y, color='red')

    # Plot the bounding boxes
    for bbox in bbox_polygons:
        if bbox.is_valid:
            x, y = bbox.exterior.xy
            plt.plot(x, y, color='blue', linestyle='--')

    # Plot the California boundary
    for geom in gdf_california.geometry:
        if isinstance(geom, Polygon):
            x, y = geom.exterior.xy
            plt.plot(x, y, color='green', linestyle='-')
        elif isinstance(geom, MultiPolygon):
            for poly in geom.geoms:
                x, y = poly.exterior.xy
                plt.plot(x, y, color='green', linestyle='-')
                
    #plt.show()
    
    # Save the plot for preview in the current working directory
    preview_path = os.path.join(output_dir, 'bounding_boxes_preview.png')
    plt.savefig(preview_path)
    plt.show()
    
    print(f"Preview map saved at: {preview_path}")
    print(bbox_df_sorted)