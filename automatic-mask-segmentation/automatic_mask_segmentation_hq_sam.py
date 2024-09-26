# !pip install segment-geospatial

import os
import leafmap
from samgeo.hq_sam import (
    SamGeo,
    show_image,
    download_file,
    overlay_images,
    tms_to_geotiff,
)

m = leafmap.Map(center=[37.8713, -122.2580], zoom=17, height="800px")
m.add_basemap("SATELLITE")
m

if m.user_roi_bounds() is not None:
    bbox = m.user_roi_bounds()
else:
    bbox = [-122.2659, 37.8682, -122.2521, 37.8741]

m.user_roi_bounds()

bbox = [-122.2600, 37.8700, -122.2550, 37.8720]

image = "satellite.tif"
tms_to_geotiff(output=image, bbox=bbox, zoom=17, source="Satellite", overwrite=True)

# image = '/path/to/your/own/image.tif'

m.layers[-1].visible = False
m.add_raster(image, layer_name="Image")
m

sam = SamGeo(
    model_type="vit_h",  # can be vit_h, vit_b, vit_l, vit_tiny
    sam_kwargs=None,
)

sam.generate(image, output="masks.tif", foreground=True, unique=True)

sam.show_masks(cmap="binary_r")

sam.show_anns(axis="off", alpha=1, output="annotations.tif")

leafmap.image_comparison(
    "satellite.tif",
    "annotations.tif",
    label1="Satellite Image",
    label2="Image Segmentation",
)

m.add_raster("annotations.tif", alpha=0.5, layer_name="Masks")
m

sam.tiff_to_vector("masks.tif", "masks.gpkg")

sam_kwargs = {
    "points_per_side": 32,
    "pred_iou_thresh": 0.86,
    "stability_score_thresh": 0.92,
    "crop_n_layers": 1,
    "crop_n_points_downscale_factor": 2,
    "min_mask_region_area": 100,
}

sam = SamGeo(
    model_type="vit_h",
    sam_kwargs=sam_kwargs,
)

sam.generate(image, output="masks2.tif", foreground=True)

sam.show_masks(cmap="binary_r")

sam.show_anns(axis="off", opacity=1, output="annotations2.tif")

leafmap.image_comparison(
    image,
    "annotations.tif",
    label1="Image",
    label2="Image Segmentation",
)

overlay_images(image, "annotations2.tif", backend="TkAgg")