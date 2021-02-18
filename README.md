# ar6
Repository for code for everything I do with AR6

## Installation
clone the repo and then run

    pip install -e .

This will ensure that all required dependencies are installed. I highly recommend doing this in a virtual environment to not screw up your base python installation. Conda works well.

## Order
- run the notebooks in numerical order. Some later things depend on earlier things (historical temperature attribution requires working group 3 constrained ensemble, which relies on forcing being generated).

## Data
Small datasets ingested by the code are included (`data_input`). Small output datasets are also included (`data_output`). Most large datasets are automatically downloaded by the code into `data_input_large`, but some cannot be:
- Glossac
- Toohey & Sigl
Detailed instructions on where to download these datasets from and the version numbers will be included eventually, ping me if you need it now.

Large datasets generated (e.g. probablistic time series) are not included due to their size. They should be exactly reproducible thanks to fixed random seeds and live in `data_output_large`.

## Credits
- Glen Harris and Mark Ringer for the two layer climate model in `src/ar6/twolayermodel`, and the CMIP6 tunings
- Matt Palmer: figure 7.3
- Bill Collins: figure 7.21
