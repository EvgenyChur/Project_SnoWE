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
source ~/.bashrc

#years="2012 2013"
years="2019"

for year in ${years}
do

  case "$year" in
      "2012" ) months="10 11 12";;
      "2013" ) months="01 02";;
      "2016" ) months="11 12";;
      "2018" ) months="09 10 11 12";;
      "2019" ) months="09";;
  esac

  for month in ${months}
  do
    days="01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28"
    case "$month" in
      "01" ) days=${days}" 29 30 31";;
      "02" ) let "yearDiv4 = year % 4"
             let "yearDiv100 = year % 100"
             let "yearDiv400 = year % 400"
             if [ "${yearDiv4}" == 0 ]&&[ "${yearDiv100}" <> 0 ]||[ "${yearDiv400}" == 0 ]
             then days=${days}" 29"
             else days=${days}""; fi;;
      "03" ) days=${days}" 29 30 31";;
      "04" ) days=${days}" 29 30";;
      "05" ) days=${days}" 29 30 31";;
      "06" ) days=${days}" 29 30";;
      "07" ) days=${days}" 29 30 31";;
      "08" ) days=${days}" 29 30 31";;
      "09" ) days=${days}" 29 30";;
      "10" ) days=${days}" 29 30 31";;
      "11" ) days=${days}" 29 30";;
      "12" ) days=${days}" 29 30 31";;
    esac

    for day in ${days}
    do
    
      ./snowe_oper_1day_ena.sh ${year} ${month} ${day}

      if [ "${year}${month}${day}" == "20190918" ]
      then
        exit 0
      fi
      
    done
  done
done
