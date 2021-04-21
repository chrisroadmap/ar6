#!/bin/bash

DATADIR=/Data/Shared/ESGF/CMIP5

cmip5="ACCESS1-0 ACCESS1-3 bcc-csm1-1-m bcc-csm1-1 BNU-ESM CanESM2 CCSM4 CESM1-BGC CESM1-CAM5 CMCC-CESM CMCC-CM CMCC-CMS CNRM-CM5 CSIRO-Mk3-6-0 EC-EARTH FGOALS-g2 FIO-ESM GFDL-CM3 GFDL-ESM2G GFDL-ESM2M GISS-E2-H-CC GISS-E2-H GISS-E2-R-CC GISS-E2-R HadGEM2-AO HadGEM2-CC HadGEM2-ES inmcm4 IPSL-CM5A-LR IPSL-CM5A-MR IPSL-CM5B-LR MIROC5 MIROC-ESM-CHEM MIROC-ESM MPI-ESM-LR MPI-ESM-MR MRI-CGCM3 NorESM1-ME"

#cmip5="ACCESS1-0 ACCESS1-3"

rm CMIP5_means/*

for model in $cmip5; do
    echo $model
    ls $DATADIR/tas_Amon_${model}_piControl_r1i1p1_*.nc
    cdo cat $DATADIR/tas_Amon_${model}_piControl_r1i1p1_*.nc temp.nc
    cdo fldmean -yearmean temp.nc CMIP5_means/tas_${model}_piControl.nc
    rm temp.nc
    ls $DATADIR/tas_Amon_${model}_rcp85_r1i1p1_*.nc
    cdo cat $DATADIR/tas_Amon_${model}_rcp85_r1i1p1_*.nc temp.nc
    cdo fldmean -yearmean temp.nc CMIP5_means/tas_${model}_rcp85.nc
    rm temp.nc
    cdo sub -timmean -selyear,2081/2100 CMIP5_means/tas_${model}_rcp85.nc -timmean CMIP5_means/tas_${model}_piControl.nc CMIP5_means/dtas_${model}.nc
done

#--------------------------

DATADIR=/Data/Shared/ESGF/CMIP6

cmip6="CNRM-CM6-1-HR CNRM-CM6-1 CNRM-ESM2-1 EC-Earth3-Veg UKESM1-0-LL ACCESS-CM2 ACCESS-ESM1-5 AWI-CM-1-1-MR BCC-CSM2-MR CAMS-CSM1-0 CanESM5 CESM2 CESM2-WACCM CIESM CMCC-CM2-SR5 FIO-ESM-2-0 FGOALS-f3-L FGOALS-g3 GISS-E2-1-G INM-CM4-8 HadGEM3-GC31-LL HadGEM3-GC31-MM IITM-ESM INM-CM4-8 INM-CM5-0 IPSL-CM6A-LR KACE-1-0-G MCM-UA-1-0 MIROC-ES2L MIROC6 MPI-ESM1-2-HR MPI-ESM1-2-LR MRI-ESM2-0 NESM3 NorESM2-LM NorESM2-MM TaiESM1"

rm CMIP6_means/*

for model in $cmip6; do
    echo $model
    ls $DATADIR/tas_Amon_${model}_piControl_*.nc
    cdo cat $DATADIR/tas_Amon_${model}_piControl_*.nc temp.nc
    cdo fldmean -yearmean temp.nc CMIP6_means/tas_${model}_piControl.nc
    rm temp.nc
    ls $DATADIR/tas_Amon_${model}_ssp585_*.nc
    cdo cat $DATADIR/tas_Amon_${model}_ssp585_*.nc temp.nc
    cdo fldmean -yearmean temp.nc CMIP6_means/tas_${model}_ssp585.nc
    rm temp.nc 
    cdo sub -timmean -selyear,2081/2100 CMIP6_means/tas_${model}_ssp585.nc -timmean CMIP6_means/tas_${model}_piControl.nc CMIP6_means/dtas_${model}.nc
done

