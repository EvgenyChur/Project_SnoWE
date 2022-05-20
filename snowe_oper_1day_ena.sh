#!/bin/bash

#-------------------------------------------------------------------------------
#
# Current code owner:
#
#   Roshydromet
#
# Authors:
#
#   Hydrometeorological Research Center of Russia, 2015-2017
#   Ekaterina Kazakova, Mikhail Chumakov, Inna Rozinkina,
#   Vladimir Kopeykin, Evgeny Churiulin
#   phone:  +7(499)795-23-59
#   email:  catherine.kazakova@mail.ru, inna.rozinkina@mail.ru,
#   v.v.kopeykin@mail.ru, evgenychur@gmail.com
#
#-------------------------------------------------------------------------------

source ~/.profile


if [ $# == 3 ]; then
    year=$1
    month=$2
    day=$3
else
    echo 'Please, set the parameter - date.'
    exit 1
fi

date="date = "${year}"."${month}"."${day}
echo $date

#=== Process for the current day ===============================================

case "$year" in
  "2011" ) db=AM11; if [ "${month}" == 01 ]&&[ "${day}" == 01 ]; then db=AM10; fi;;
  "2012" ) db=AM12; if [ "${month}" == 01 ]&&[ "${day}" == 01 ]; then db=AM11; fi;;
  "2013" ) db=AM13; if [ "${month}" == 01 ]&&[ "${day}" == 01 ]; then db=AM12; fi;;
  "2014" ) db=AM14; if [ "${month}" == 01 ]&&[ "${day}" == 01 ]; then db=AM13; fi;;
  "2015" ) db=AM15; if [ "${month}" == 01 ]&&[ "${day}" == 01 ]; then db=AM14; fi;;
  "2016" ) db=AM16; if [ "${month}" == 01 ]&&[ "${day}" == 01 ]; then db=AM15; fi;;
  "2017" ) db=AM17; if [ "${month}" == 01 ]&&[ "${day}" == 01 ]; then db=AM16; fi;;
  "2018" ) db=AM18; if [ "${month}" == 01 ]&&[ "${day}" == 01 ]; then db=AM17; fi;;
  "2019" ) db=AM19; if [ "${month}" == 01 ]&&[ "${day}" == 01 ]; then db=AM18; fi;;
  "2020" ) db=AM19; if [ "${month}" == 01 ]&&[ "${day}" == 01 ]; then db=AM19; fi;;
esac

let "dif=$(date +%s) - $(date -d${year}${month}${day} +%s)"
if (( ${dif} < 604800 )); then # 7 days
  db=SHOT
fi;

satdata=$(date +%Y%j -d${year}${month}${day}' 1 days ago') # For satellite

hour=00

#=== Settings ==================================================================
# 1) region --------------------------------------------------------------------
region='ENA'
dkm=13

# 2) Directory -----------------------------------------------------------------
DIR=/RHM-Lustre3.2/users/cosmo/vkopeikin/SNOWE_OPER/SNOWE_OPER_STATIONS
DIR_SOFTWARE=/RHM-Lustre3.2/users/cosmo/vkopeikin/SNOWE_OPER/software

DIR_ROOT=$DIR
DIR_COSMO_GRIB=$DIR/COSMO_DATA/GRIB_${region}
DIR_COSMO_DATA=$DIR/COSMO_DATA/DATA_${region}
DIR_SATELLITE=$DIR/SATELLITE_4KM
DIR_SATELLITE_RAW=/RHM-Lustre3.2/users/cosmo/vkopeikin/SNOWE_OPER/SATELLITE/RAW
DIR_INTERPOLATION=$DIR/FIELD_INTERPOLATION/COSMO-${region}
DIR_SMFE_INPUT=$DIR/SMFE/INPUT/${region}
DIR_SMFE_OUTPUT=$DIR/SMFE/OUTPUT/${region}
DIR_RESULT=$DIR/RESULT_COSMO/${region}

echo 'cd '$DIR
cd $DIR






ncrcat -h







# 3) Parameters ----------------------------------------------------------------
srcDataType=1         # Use(1)/no(0) station observations (in case of no there
                      # should be forecasts for the previous day at 24,30,36,42 UTC)
interpolationMethod=1 # 1 -interpolation from SYNOP to COSMO grid (no first guess);
                      # only for small territories with dense SYNOP network
                      # 2-calculation of relations between SYNOP and first guess,
                      # their interpolation and first guess changes
                      # 3-use calculations of SMFE at each cell of COSMO-model
                      # grid (no interpolation, only change fields in laf-file)
sweRhoLayersCount=0   # Aamount of layers for output from snow model
cosmoGridsCount=500000
stationsCount=3256
satelliteDataCount=500000
pointsCount=3256

#=== Generation namelists ======================================================

cat >$DIR/cosmo2smfe_${region}.nl <<MARKER
&cosmo2smfe
    cosmoGridsCount = $cosmoGridsCount,
    filename_COSMOLonLat = "${DIR_INTERPOLATION}/COSMO_lonlat.txt",
    filename_surfaceHeight = "${DIR_INTERPOLATION}/hsurf.txt",
    filename_snowDepth = "${DIR_COSMO_DATA}/hsnow_cosmo_${region}_${year}${month}${day}.txt",
    filename_p24Sum = "${DIR_COSMO_DATA}/prec_cosmo_${region}_${year}${month}${day}.txt",
    filename_t2m0 =" ${DIR_COSMO_DATA}/t2m_0_cosmo_${region}_${year}${month}${day}.txt",
    filename_t2m6 = "${DIR_COSMO_DATA}/t2m_6_cosmo_${region}_${year}${month}${day}.txt",
    filename_t2m12 = "${DIR_COSMO_DATA}/t2m_12_cosmo_${region}_${year}${month}${day}.txt",
    filename_t2m18 = "${DIR_COSMO_DATA}/t2m_18_cosmo_${region}_${year}${month}${day}.txt",
    filename_srcRho = "${DIR_COSMO_DATA}/rho_cosmo_${region}_${year}${month}${day}.txt",
    filename_srcSwe = "${DIR_COSMO_DATA}/swe_cosmo_${region}_${year}${month}${day}.txt",
    filename_smfeIn = "${DIR_SMFE_INPUT}/smfeIn_${year}_${month}_${day}.txt"
/
MARKER

cat >$DIR/snowmask_${region}.nl <<MARKER
&snowmask
    year = $year,
    month = $month,
    day = $day,
    hour = $hour,
    filename_satelliteRaw = "${DIR_SATELLITE_RAW}/NH.C17_${satdata}_BLND_SIM;",
    filename_satelliteData = "${DIR_SATELLITE}/DATA/sat_noaa_${region}_${year}${month}${day}.txt",
    filename_satelliteConf = "${DIR_SATELLITE}/GRID_${region}/COSMOconf.nl",
/
MARKER

cat >$DIR/db2smfe_${region}.nl <<MARKER
&db2smfe
    year = $year,
    month = $month,
    day = $day,
    hour = $hour,
    stationsCount = $stationsCount,
    dBHost = "192.168.97.72",
    dBName = $db,
    dBCode = 260601,
    filename_stationsLonLat = "${DIR_INTERPOLATION}/STATION_${region}.txt",
    filename_smfeIn = "${DIR_SMFE_INPUT}/smfeIn_${year}_${month}_${day}.txt"
/
MARKER

cat >$DIR/smfecalc_${region}.nl <<MARKER
&smfecalc
    pointsCount = $pointsCount,
    satelliteDataCount = $satelliteDataCount,
    sweRhoLayersCount = $sweRhoLayersCount,
    year = $year,
    month = $month,
    day = $day,
    hour = $hour,
    filename_history = "${DIR_SMFE_OUTPUT}/history.bin",
    filename_smfeIn = "${DIR_SMFE_INPUT}/smfeIn_${year}_${month}_${day}.txt"
    filename_smfeResult = "${DIR_SMFE_OUTPUT}/snow_${year}_${month}_${day}.txt"
    filename_satelliteData = "${DIR_SATELLITE}/data/sat_noaa_${region}_${year}${month}${day}.txt"
/
MARKER

cat >$DIR/smfe2cosmogrid_${region}.nl <<MARKER
&smfe2cosmogrid
    cosmoGridsCount = $cosmoGridsCount,
    pointsCount = $pointsCount,
    satelliteDataCount = $satelliteDataCount,
    sweRhoLayersCount = $sweRhoLayersCount,
    interpolationMethod = $interpolationMethod,
    int2gridFactor = 1.0,
    radius = 15.0,
    lonBottomPoint = -21.0,
    latBottomPoint = 9.0,
    filename_int2gridExe = "${DIR_SOFTWARE}/int2grid/int2grid.ex",
    filename_int2gridIn = "${DIR_INTERPOLATION}/synop_ex.txt",
    filename_int2gridGrid = "${DIR_INTERPOLATION}/grid.txt",
    filename_int2gridOut = "${DIR_INTERPOLATION}/result.txt",
    filename_COSMOLonLat = "${DIR_INTERPOLATION}/COSMO_lonlat.txt",
    filename_surfaceHeight = "${DIR_INTERPOLATION}/hsurf.txt",
    filename_srcRho = "${DIR_COSMO_DATA}/rho_cosmo_${region}_${year}${month}${day}.txt",
    filename_srcSwe = "${DIR_COSMO_DATA}/swe_cosmo_${region}_${year}${month}${day}.txt",
    filename_satelliteData = "${DIR_SATELLITE}/data/sat_noaa_${region}_${year}${month}${day}.txt",
    filename_smfeResult = "${DIR_SMFE_OUTPUT}/snow_${year}_${month}_${day}.txt",
    filename_result = "${DIR_RESULT}/${year}${month}${day}_snow_modif_cosmo.txt",
    filename_resultLayers = "${DIR_RESULT}/${year}${month}${day}_snow_modif_layers.txt",
    filename_pointsIntoCOSMO = "${DIR_INTERPOLATION}/stations_into.txt",
    filename_mask = "${DIR_INTERPOLATION}/mask.txt"
/
MARKER

#=== Run =======================================================================

# COSMO data preparation
if [ $srcDataType == 0 ]; then
  # t2m = 11
  grib_get_data -w indicatorOfParameter=11,table2Version=2,indicatorOfTypeOfLevel=105,level=2 ${DIR_COSMO_GRIB}/lfff01000000s > ${DIR_COSMO_DATA}/t2m_0_cosmo_${region}_${year}${month}${day}.txt
  grib_get_data -w indicatorOfParameter=11,table2Version=2,indicatorOfTypeOfLevel=105,level=2 ${DIR_COSMO_GRIB}/lfff01060000s > ${DIR_COSMO_DATA}/t2m_6_cosmo_${region}_${year}${month}${day}.txt
  grib_get_data -w indicatorOfParameter=11,table2Version=2,indicatorOfTypeOfLevel=105,level=2 ${DIR_COSMO_GRIB}/lfff01120000s > ${DIR_COSMO_DATA}/t2m_12_cosmo_${region}_${year}${month}${day}.txt
  grib_get_data -w indicatorOfParameter=11,table2Version=2,indicatorOfTypeOfLevel=105,level=2 ${DIR_COSMO_GRIB}/lfff01180000s > ${DIR_COSMO_DATA}/t2m_18_cosmo_${region}_${year}${month}${day}.txt
  # hsnow= 66
  grib_get_data -w indicatorOfParameter=66,table2Version=2 ${DIR_COSMO_GRIB}/lfff01000000s > ${DIR_COSMO_DATA}/hsnow_cosmo_${region}_${year}${month}${day}.txt
  # tot_prec= 61
  grib_get_data -w indicatorOfParameter=61,table2Version=2 ${DIR_COSMO_GRIB}/lfff01000000s > ${DIR_COSMO_DATA}/prec_cosmo_${region}_${year}${month}${day}.txt
fi

# rho = 133, swe = 65
#grib_get_data -w indicatorOfParameter=133 ${DIR_COSMO_GRIB}/laf${year}${month}${day}${hour} > ${DIR_COSMO_DATA}/rho_cosmo_${region}_${year}${month}${day}.txt
#grib_get_data -w indicatorOfParameter=65,table2Version=2 ${DIR_COSMO_GRIB}/laf${year}${month}${day}${hour} > ${DIR_COSMO_DATA}/swe_cosmo_${region}_${year}${month}${day}.txt

$DIR_SOFTWARE/snowmask/snowmask.ex $DIR/snowmask_${region}.nl

$DIR_SOFTWARE/db2smfe/db2smfe.ex $DIR/db2smfe_${region}.nl
# Control of the return code
if [ $? -ne 0 ]; then
  exit 1
fi

$DIR_SOFTWARE/smfecalc/smfecalc.ex $DIR/smfecalc_${region}.nl
# Control of the return code
if [ $? -ne 0 ]; then
  exit 1
fi

#exit 0

$DIR_SOFTWARE/smfe2cosmogrid/smfe2cosmogrid.ex $DIR/smfe2cosmogrid_${region}.nl
# Control of the return code
if [ $? -ne 0 ]; then
  exit 1
fi

#exit 0

$DIR/encode_grib/eject_fields.sh ${year}${month}${day}00 $dkm

exit 0
