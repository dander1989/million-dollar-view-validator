import pdal
import rasterio
import os
import json
import requests
import numpy as np
from osgeo import gdal
from pyproj import Transformer
from rasterio.transform import rowcol

# PDAL Pipeline for Obtaining LAZ and converting it to DSM
output_path = os.path.join("data", "stl_mo_dsm_test.tif")

# Change variables to configure for specific project
pipeline_json = {
    "pipeline": [
        {
            "type": "readers.las",
            "filename": "https://rockyweb.usgs.gov/vdelivery/Datasets/Staged/Elevation/LPC/Projects/legacy/MO_STLOUIS_2012/LAZ/USGS_LPC_MO_STLOUIS_2012_000054.laz"
        },
        {
            "type": "filters.range",
            "limits": "Classification![7:7]"
        },
        {
            "type": "filters.outlier",
            "method": "statistical",
            "mean_k": 12,
            "multiplier": 2.0
        },
        {
            "type": "writers.gdal",
            "filename": output_path,
            "nodata": -9999,
            "resolution": 1.0,
            "output_type": "max",
            "override_srs": "EPSG:26915"
        }
    ]
}
try:
    pipeline = pdal.Pipeline(json.dumps(pipeline_json))
    print("Connecting to USGS servers, and converting Lidar data to DSM...This may take a few minutes.")
    pipeline.execute()
    print("DSM created successfully")
except RuntimeError as e:
    print(
        f"PDAL error: The pipeline failed. Check internet connection or URl. \nDetails: {e}")
    exit()

# Create a transformer from WGS84 to EPSG: 26915
transformer = Transformer.from_crs("EPSG:4326", "EPSG:26915", always_xy=True)

# Arch Coordinates (The 'Observer' location)
# Note while this location is the centerpoint of the arch, this value would have to be modified (Line 65) due to how Lidar scan was taken because of an offset.
lon, lat = -90.1848, 38.6247

# Transform
x, y = transformer.transform(lon, lat)

# print(f"UTM Coordinates: X={x}, Y={y}") # Optional if you want to see the UTM Coords

# Open the DSM and show the shape and bounds
with rasterio.open('data/stl_mo_dsm_test.tif') as src:
    dsm_data = src.read(1)

    transform = src.transform
    crs = src.crs
    profile = src.profile

    print(f"DSM shape: {dsm_data.shape}")
    print(f"Transform: {transform}")

# Converting arch coordinates to pixel row/column
# Arch center coords
arch_x, arch_y = 745062.40, 4278879.19  # See note on line 45.

# Convert to pixel pos
row, col = rowcol(transform, arch_x, arch_y)

print(f"The Arch is at pixel row={row}, col={col}")

# Using numpy array to create mask of 100m buffer from point
rows, cols = dsm_data.shape
row_grid, col_grid = np.ogrid[0:rows, 0:cols]

# Calculate distance from each pixel to arch center
distances = np.sqrt((row_grid - row)**2 + (col_grid - col)**2)

# Create mask: True for pixels within 100m
radius = 100
arch_mask = distances <= radius

print(f"Number of pixels in arch footprint: {arch_mask.sum()}")

# Cap arch pixels at target height. Modify original dsm
# Create copy of dsm
dsm_modified = dsm_data.copy()

# Target height (halfway up the arch)
target_height = 227.0

# Cap pixels in arch footprint where arch mask == True and elevation > target_height, set to target_height
dsm_modified[arch_mask & (dsm_modified > target_height)] = target_height

print(
    f"Modified DSM - pixels changed: {np.sum((dsm_data != dsm_modified) & arch_mask)}")

# Update the profile for the output file
output_profile = profile.copy()

# Write the modified DSM
output_filename = 'data/stl_mo_dsm_testhalf.tif'

with rasterio.open(output_filename, 'w', **output_profile) as dst:
    dst.write(dsm_modified, 1)

print(f"Modified DSM saved to {output_filename}")

# Run viewshed analysis 2m height

ds = gdal.Open('data/stl_mo_dsm_test.tif')
band = ds.GetRasterBand(1)

viewshed_result = gdal.ViewshedGenerate(
    band,
    'GTiff',
    'data/viewshed_2m_test.tif',
    [],
    arch_x,
    arch_y,
    2,  # observer height in meters
    1.7,
    255,
    0,
    0,
    -9999,
    0.85714,
    gdal.GVM_Edge,
    0
)
ds = None
print('2m Viewshed Analysis completed.')

# Run viewshed 2m height (arch half-height)
ds = gdal.Open('data/stl_mo_dsm_testhalf.tif')
band = ds.GetRasterBand(1)

viewshed_result = gdal.ViewshedGenerate(
    band,
    'GTiff',
    'data/viewshed_2m_testhalf.tif',
    [],
    arch_x,
    arch_y,
    2,  # observer height in meters
    1.7,
    255,
    0,
    0,
    -9999,
    0.85714,
    gdal.GVM_Edge,
    0
)
ds = None
print('2m (Arch Half-height) Viewshed Analysis completed. Script ended')
