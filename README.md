# IPCC AR6 WG1 Chapter 7 and friends multi-purpose repository

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5211357.svg)](https://doi.org/10.5281/zenodo.5211357)

In this repository is the code, data and figures that I (Chris Smith) was responsible for creating. Many of the figures and datasets relate to Chapter 7 and the Chapter 7 Supplementary Material, but there are other datasets used in other chapters (e.g. the effective radiative forcing time series used in fig. 2.10; attribution of future warming for SPM fig. 4).

Included here also is the calibration and constraining of the FaIRv1.6.2 simple climate model that will later get used by the IPCC's Working Group 3 to determine the climate response to integrated assessment modelling pathways.

## Key output datasets

- Effective radiative forcing: historical 1750-2019 time series [best estimate](data_output/AR6_ERF_1750-2019.csv) | [minor greenhouse gases](data_output/AR6_ERF_minorGHGs_1750-2019.csv) | [5th percentile](data_output/AR6_ERF_1750-2019_pc05.csv) | [95th percentile](data_output/AR6_ERF_1750-2019_pc95.csv)
  - CMIP6 Shared Socioeconomic Pathways, [1750-2500](https://github.com/chrisroadmap/ar6/tree/main/data_output/SSPs)
  - CMIP5 Representative Concentration Pathways, [1750-2500](https://github.com/chrisroadmap/ar6/tree/main/data_output/RCPs)
- Greenhouse gas concentrations: historical 1750-2019 [time series](data_input/observations/LLGHG_history_AR6_v9_for_archive.xlsx?raw=true) (coordinator: Bradley Hall)
- [Metrics (e.g. GWP and GTP) for greenhouse gases](data_output/7sm/metrics_supplement_cleaned.csv) (coordinator: Bill Collins). **NOTE** Table 7.SM.7 has incorrect values for CFC-11 and CFC-12, and occasionally rounding errors differ in the third significant figure for AWGP and AGTP compared to Table 7.SM.7.

For \*.csv files, you can click the "Raw" button to view a plain text version of each file. Alternatively, clone the repo to download all of the files.

## Figure plotting code locations

| Figure        | Code                                 | Authors        |
| ------------- | ------------------------------------ | -------------- |
| Box 7.2 Fig 1 | [notebooks/350_chapter7_box7.2_fig1.ipynb](notebooks/350_chapter7_box7.2_fig1.ipynb) | Matthew Palmer, Chris Smith |
| 7.3           | [notebooks/300_chapter7_fig7.3.ipynb](notebooks/300_chapter7_fig7.3.ipynb)  | Matthew Palmer, Chris Smith |
| 7.4           | [notebooks/270_chapter7_fig7.4.ipynb](notebooks/270_chapter7_fig7.4.ipynb)  | Chris Smith |
| 7.5           | [notebooks/060_chapter7_fig7.5_SPM_fig15.ipynb](notebooks/060_chapter7_fig7.5_SPM_fig15.ipynb) | Chris Smith |
| 7.6           | [notebooks/100_chapter7_fig7.6.ipynb](notebooks/100_chapter7_fig7.6.ipynb) | Chris Smith |
| 7.7           | [notebooks/220_chapter7_fig7.7.ipynb](notebooks/220_chapter7_fig7.7.ipynb) | Chris Smith |
| 7.8           | [notebooks/230_chapter7_fig7.8.ipynb](notebooks/230_chapter7_fig7.8.ipynb) | Chris Smith |
| 7.10          | https://github.com/mzelinka/AR6_figure <br> [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5218854.svg)](https://doi.org/10.5281/zenodo.5218854) | Mark Zelinka |
| 7.11          | https://github.com/danlunt1976/ipcc_ar6/blob/master/nonlin/nonlin_fgd.pro | Dan Lunt |
| 7.13          | https://github.com/danlunt1976/ipcc_ar6/blob/master/patterns/fgd/plot_all_fgd.pro | Dan Lunt |
| 7.16          | [notebooks/020_chapter7_fig7.16.ipynb](notebooks/020_chapter7_fig7.16.ipynb) | Chris Smith, Masa Watanabe |
| 7.17          | [contributed/fig7.17/tcr_fgd.f](contributed/fig7.17/tcr_fgd.f) | Masa Watanabe |
| 7.18          | [notebooks/330_chapter7_fig7.18.ipynb](notebooks/330_chapter7_fig7.18.ipynb) | Piers Forster, Chris Smith |
| 7.19          | https://github.com/danlunt1976/ipcc_ar6/blob/master/patterns/fgd/plot_all_fgd.pro | Dan Lunt |
| 7.21          | [notebooks/320_chapter7_fig7.21.ipynb](notebooks/320_chapter7_fig7.21.ipynb) | Bill Collins, Chris Smith |
| 7.22          | [notebooks/310_chapter7_fig7.22.ipynb](notebooks/310_chapter7_fig7.22.ipynb) | Piers Forster, Michelle Cain, Chris Smith |
| FAQ 7.3 Fig 1 | [contributed/faq7.3_fig1/Redo_Grose_figure.py](contributed/faq7.3_fig1/Redo_Grose_figure.py) | Sophie Berger |
| 7.SM.1        | [notebooks/115_chapter7_fig7.SM.1.ipynb](notebooks/115_chapter7_fig7.SM.1.ipynb) | Chris Smith |

## Reproduction
The figures above where I am one of the listed authors can be reproduced. Data and figures are produced by the Jupyter Notebooks that live inside the `notebooks` directory. Also listed are external GitHub repositories and locations within the `contributed` directory where code for figures have been supplied by other authors. These are provided "as-is" and are not guaranteed to be reproducible within this environment. For external GitHub locations, check out the relevant repository READMEs.

Within my processing chain, every notebook is prefixed by a number. To reproduce all results in the chapter, the notebooks should be run in numerical order, because some later things depend on earlier things (historical temperature attribution requires a constrained ensemble of the two layer climate model, which relies on the generation of the radiative forcing time series). This being said, most notebooks should run standalone, as input data is provided where the datasets are small enough (see below).

### Installation
I recommend using a virtual environment such as `venv` or `conda`. This repository was built inside a `conda` environment using `python 3.7`.

First, set up your virtual environment. For example, if using `conda`:

    $ conda create -n ar6-wg1-ch7 python=3.7
    $ conda activate ar6-wg1-ch7

Once this is done, clone the repo from GitHub and then run

    (ar6-wg1-ch7) $ cd ar6  # or if you have used the IPCC-WG1 fork, this will be "Chapter-7"
    (ar6-wg1-ch7) $ pip install -e .

This will ensure that all required dependencies are installed inside the virtual environment named `ar6-wg1-ch7`.


### Input datasets
Small ancillary datasets that are ingested by the code are included in this repository (`data_input`). TODO: [#17](/../../issues/17)

Most large input ancillary datasets are automatically downloaded when required into `data_input_large`, with two exceptions where public APIs were not found to be available. The following files should be downloaded and placed into the `data_input_large` directory:

#### Glossac v2.0 stratospheric aerosol optical depth time series
- Obtained from https://asdc.larc.nasa.gov/project/GloSSAC/GloSSAC_2.0 (registration required).

    $ cksum GloSSAC_V2.0.nc<br>
    938562794 482976764 GloSSAC_V2.0.nc


#### eVolv v3 stratospheric optical depth, 500 BCE to 1900 CE
- Obtained from https://cera-www.dkrz.de/WDCC/ui/cerasearch/entry?acronym=eVolv2k_v3 (registration required).

    $ cksum eVolv2k_v3_EVA_AOD_-500_1900_1.nc<br>
    3663959754 22244500 eVolv2k_v3_EVA_AOD_-500_1900_1.nc

### Output datasets
Small output datasets of general interest that are generated by the code, such as the ERF time series, are included in the repository (`data_output`).

Large datasets generated by the code (e.g. probablistic time series) are not included in the GitHub repository due to their size. They should be exactly reproducible thanks to fixed random seeds and live in `data_output_large`. The most likely reason for a notebook not running out of the box is that it requires a dataset that lives in `data_output_large` and generated by an earlier notebook.

## Contributed code
In the `contributed` directory is code that I did not produce or co-produce that is used in Chapter 7 figures, this being the most appropriate place to put it. A number of Chapter 7 figures are externally hosted on repositories belonging to other authors, which have been linked above.

## Playlist
I often work listening to music, and every notebook has an associated theme song. Some are related to the contents of the notebook, but most are just a reflection of what I was listening to at the time or what mood I was in. Hopefully you might discover something new.

## Anything broken?
This notebook was pieced together in stages, over a period of nearly two years, in the face of conflicting priorities and changing assessments. It's highly likely that one or two links in the chain are broken. [Please raise an issue](https://github.com/chrisroadmap/ar6/issues) if something isn't working.

## Credits
- Matt Palmer: box 7.2 figure 1 and figure 7.3
- Mark Zelinka: figure 7.10 (externally hosted)
- Dan Lunt: figures 7.11, 7.13, 7.19 (externally hosted)
- Masa Watanabe: figure 7.17 (contributed)
- Piers Forster: figures 7.18 and 7.22
- Bill Collins: figure 7.21, greenhouse gas metrics
- Michelle Cain: figure 7.22
- Sophie Berger: figure 1, FAQ 7.3 (contributed)
- Nick Leach: FaIR calibrations for the carbon cycle
- Glen Harris and Mark Ringer for the two layer climate model in `src/ar6/twolayermodel`, and the CMIP6 tunings
- Brad Hall: greenhouse gas concentrations

If I forgot you, please [raise an issue](https://github.com/chrisroadmap/ar6/issues).

## Suggested citations

**This repository:** Smith C.J., P.M. Forster, S. Berger, W. Collins, B. Hall, D. Lunt, M.D. Palmer, M. Watanabe, M. Cain, G. Harris, N.J. Leach, M. Ringer, M. Zelinka, 2021. Figure and data generation for Chapter 7 of the IPCC's Sixth Assessment Report, Working Group 1 (plus assorted other contributions). Version 1.0. https://doi.org/10.5281/zenodo.5211357

**Figure 7.10:** Zelinka, M., 2021. mzelinka/AR6_figure: Aug 18, 2021 Release (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.5218854

Please also consider citing, if appropriate:

**[Chapter 7](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter_07.pdf):** Forster, P., T. Storelvmo, K. Armour, W. Collins, J. L. Dufresne, D. Frame, D. J. Lunt, T. Mauritsen, M. D. Palmer, M. Watanabe, M. Wild, H. Zhang, 2021, The Earth’s Energy Budget, Climate Feedbacks, and Climate Sensitivity. In: Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change [Masson-Delmotte, V., P. Zhai, A. Pirani, S. L. Connors, C. Péan, S. Berger, N. Caud, Y. Chen, L. Goldfarb, M. I. Gomis, M. Huang, K. Leitzell, E. Lonnoy, J.B.R. Matthews, T. K. Maycock, T. Waterfield, O. Yelekçi, R. Yu and B. Zhou (eds.)]. Cambridge University Press. In Press.

**[Chapter 7 Supplementary Material](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter_07_Supplementary_Material.pdf):** Smith, C., Z.R.J. Nicholls, K. Armour, W. Collins, P. Forster, M. Meinshausen, M. D. Palmer, M. Watanabe, 2021, The Earth’s Energy Budget, Climate Feedbacks, and Climate Sensitivity Supplementary Material. In: Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change [Masson-Delmotte, V., P. Zhai, A. Pirani, S. L. Connors, C. Péan, S. Berger, N. Caud, Y. Chen, L. Goldfarb, M. I. Gomis, M. Huang, K. Leitzell, E. Lonnoy, J.B.R. Matthews, T. K. Maycock, T. Waterfield, O. Yelekçi, R. Yu and B. Zhou (eds.)]. Available from https://ipcc.ch/static/ar6/wg1.

**[Annex III](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Annex_III.pdf) (GHG concentrations, radiative forcing time series):** IPCC, 2021: Annex III: Tables of historical and projected well-mixed greenhouse gas mixing ratios and effective radiative forcing of all climate forcers [Dentener F. J., B. Hall, C. Smith (eds.)]. In: Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change [Masson-Delmotte, V., P. Zhai, A. Pirani, S. L. Connors, C. Péan, S. Berger, N. Caud, Y. Chen, L. Goldfarb, M. I. Gomis, M. Huang, K. Leitzell, E. Lonnoy, J.B.R. Matthews, T. K. Maycock, T. Waterfield, O. Yelekçi, R. Yu and B. Zhou (eds.)]. Cambridge University Press. In Press.
