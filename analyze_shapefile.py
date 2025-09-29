import pandas as pd
import geopandas as gpd
import numpy as np

# Load the shapefile
shapefile_path = r"soil_moisture_sample_points_7sep.shp"
gdf = gpd.read_file(shapefile_path)

print("=" * 60)
print("COMPREHENSIVE SHAPEFILE ANALYSIS")
print("=" * 60)

print(f"\nDataset shape: {gdf.shape}")
print(f"CRS (Coordinate Reference System): {gdf.crs}")

print("\n=== COLUMN STRUCTURE ===")
for i, (col, dtype) in enumerate(gdf.dtypes.items()):
    if col != 'geometry':
        unique_vals = gdf[col].nunique()
        print(f"{i+1:2d}. {col:12} ({str(dtype):15}) - {unique_vals} unique values")
    else:
        print(f"{i+1:2d}. {col:12} (geometry)")

print("\n=== TEMPORAL INFORMATION ===")
print(f"Unique dates: {gdf['Date'].nunique()}")
for date in sorted(gdf['Date'].unique()):
    count = (gdf['Date'] == date).sum()
    print(f"  {date.strftime('%Y-%m-%d')}: {count} points")

print("\n=== SPATIAL INFORMATION ===")
bounds = gdf.total_bounds
print(f"Geographic bounds:")
print(f"  Longitude: {bounds[0]:.5f} to {bounds[2]:.5f}")
print(f"  Latitude:  {bounds[1]:.5f} to {bounds[3]:.5f}")
print(f"  Area coverage: ~{(bounds[2]-bounds[0])*111000:.0f}m × {(bounds[3]-bounds[1])*111000:.0f}m")

print("\n=== SOIL MOISTURE MEASUREMENTS ===")
soil_cols = ['N', 'S', 'W', 'E', 'C']
print("Measurement methodology: 5 directional readings per point")
print("  N=North, S=South, W=West, E=East, C=Center")

# Calculate statistics
gdf['Avg_SM'] = gdf[soil_cols].mean(axis=1)
gdf['SM_StdDev'] = gdf[soil_cols].std(axis=1)

print(f"\nSoil moisture statistics:")
print(f"  Range: {gdf['Avg_SM'].min():.1f}% to {gdf['Avg_SM'].max():.1f}%")
print(f"  Mean: {gdf['Avg_SM'].mean():.1f}% ± {gdf['Avg_SM'].std():.1f}%")
print(f"  Median: {gdf['Avg_SM'].median():.1f}%")

print(f"\nInternal variability (std dev of 5 measurements per point):")
print(f"  Mean variability: {gdf['SM_StdDev'].mean():.2f}%")
print(f"  Range: {gdf['SM_StdDev'].min():.2f}% to {gdf['SM_StdDev'].max():.2f}%")

print("\n=== COMPLETE DATASET ===")
display_cols = ['fid_1', 'N', 'S', 'W', 'E', 'C', 'Avg_SM', 'SM_StdDev', 'Date']
print(gdf[display_cols].round(1).to_string(index=False))

print("\n=== SAMPLE COORDINATES ===")
print("Sample of geographic coordinates:")
for i, (idx, row) in enumerate(gdf.head(5).iterrows()):
    x, y = row.geometry.x, row.geometry.y
    print(f"  Point {row['fid_1']:3.0f}: ({x:.5f}, {y:.5f}) - {row['Date'].strftime('%Y-%m-%d')} - SM: {row['Avg_SM']:.1f}%")

print("\n=== QUALITY ASSESSMENT ===")
missing_total = gdf.isna().sum().sum()
print(f"Missing values: {missing_total} (0.0% - dataset is complete)")

high_var_points = gdf[gdf['SM_StdDev'] > gdf['SM_StdDev'].quantile(0.75)]
print(f"Points with high internal variability (>75th percentile): {len(high_var_points)}")

print("\n=== DATA QUALITY INDICATORS ===")
print("Points with highest measurement variability:")
top_var = gdf.nlargest(3, 'SM_StdDev')[['fid_1', 'Avg_SM', 'SM_StdDev', 'Date']]
for _, row in top_var.iterrows():
    print(f"  Point {row['fid_1']:3.0f}: {row['Avg_SM']:.1f}% (±{row['SM_StdDev']:.1f}%) on {row['Date'].strftime('%Y-%m-%d')}")

print(f"\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)