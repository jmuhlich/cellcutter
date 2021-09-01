import logging

import click
import pandas as pd

from . import cut as cut_mod


@click.command()
@click.argument("image", type=click.Path(exists=True, dir_okay=False))
@click.argument("segmentation_mask", type=click.Path(exists=True, dir_okay=False))
@click.argument("cell_data", type=click.Path(exists=True, dir_okay=False))
@click.argument("destination", type=click.Path())
@click.option(
    "--window-size",
    default=None,
    type=click.INT,
    help="Size of the cell thumbnail in pixels. Defaults to size of largest cell.",
)
@click.option(
    "--mask-cells/--dont-mask-cells",
    default=True,
    help="Fill every pixel not occupied by the target cell with zeros.",
)
def cut(image, segmentation_mask, cell_data, destination, window_size, mask_cells):
    """Cut out thumbnail images of all cells.

    IMAGE - Path to image in TIFF format, potentially with multiple channels.
    Thumbnails will be created from each channel.

    SEGMENTATION_MASK - Path to segmentation mask image in TIFF format.
    Used to automatically chose window size and find cell outlines.

    CELL_DATA - Path to CSV file with a row for each cell.
    Must contain columns CellID (must correspond to the cell IDs in the segmentation mask),
    Y_Centroid, and X_Centroid.

    DESTINATION - Path to file where cell thumbnails will be stored in Zarr format
    (https://zarr.readthedocs.io/en/stable/index.html).
    """
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO
    )
    img = cut_mod.Image(image)
    segmentation_mask_img = cut_mod.Image(segmentation_mask)
    cell_data_df = pd.read_csv(cell_data)
    cut_mod.save_cells_all_channels(
        img,
        segmentation_mask_img,
        cell_data_df,
        destination,
        window_size=window_size,
        mask_cells=mask_cells,
    )