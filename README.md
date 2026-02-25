# Gateway Arch Viewshed Analysis

A comprehensive geospatial analysis pipeline for computing and visualizing the three-dimensional viewshed from the Gateway Arch monument in St. Louis, Missouri. This project combines high-resolution elevation data, line-of-sight algorithms, and modern geospatial visualization techniques to determine visibility patterns across the surrounding landscape.

## Problem Statement

Understanding visibility patterns from iconic landmarks is crucial for landscape planning, tourism management, and heritage conservation. Traditional 2D viewshed analyses fail to capture the true three-dimensional nature of visibility from elevated structures. This project solves this by implementing a robust 3D viewshed analysis pipeline that accounts for:

- Actual elevation data and terrain complexity
- Observer height (top of the Gateway Arch)
- Target identification at multiple distance intervals
- Comprehensive spatial coverage across the region

<img width="1920" height="925" alt="Good_and_great_views_arch" src="https://github.com/user-attachments/assets/a320dfaa-0924-4554-908a-9436bff9549e" />

## Methodology

### Overview
The viewshed analysis implements the following:

1. **Data Preparation**: Load and validate DEM data, establish observer coordinates and height
2. **Target Sampling**: Create a regular grid of target points across the study area
3. **Visibility Computation**: Execute line-of-sight checks between observer and each target
4. **Accumulation**: Aggregate results into a raster viewshed map
5. **Validation**: Cross-reference with known visibility landmarks

## Technical Details

### Dependencies

Key Python packages:
- `numpy` - Numerical computation
- `rasterio` - Raster data I/O
- `geopandas` - Vector data handling

See `environment.yml` for full dependency list and versions.

### Prerequisites
- Python 3.8+
- GDAL/OGR libraries
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/dander1989/million-dollar-view-validator.git
cd gateway-arch-viewshed

# Create virtual environment with dependencies
conda env create --file environment.yml
```

### Performance Considerations
- **Memory**: DEM resolution directly impacts memory usage. For large DEMs, consider processing in tiles
- **Computation Time**: Line-of-sight computation scales with DEM size and target distance
- **Optimization**: Implement spatial indexing (quadtree/R-tree) for larger analyses

## Additional Visualizations

<img width="613" height="788" alt="partial_view" src="https://github.com/user-attachments/assets/c4607453-6aa4-4594-a75b-50e6ce308fbc" />

*Basic Map showing 'partial' views that have possible less-than-ideal viewings of the Arch*

<img width="612" height="787" alt="premium_view" src="https://github.com/user-attachments/assets/731f5256-2517-4234-9622-51baffd5e57f" />

*Basic Map showing 'premium' views that have at least half or more fo the Arch in view*

<img width="613" height="787" alt="premium_partial_overlay_view" src="https://github.com/user-attachments/assets/10a05465-5072-4beb-ae7c-0c1dd5a0809e" />

*Overlay of both 'partial' and 'premium' views. Note that 'partial' views may also overlap with 'premium'*

## License
This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments
- United States Geological Service (USGS)
- Matt Forrest of the Spatial Lab for providing project idea

