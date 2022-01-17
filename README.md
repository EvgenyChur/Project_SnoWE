# Technical documentation for SnoWE model

### Authors:
<p align="justify">
Churiulin E.<sup>1</sup>, Kopeikin V.<sup>1</sup>, Rozinkina I.<sup>1</sup>, Chumakov M.<sup>2</sup>, Kazakova E.<sup>1</sup>
</p>

1 - [Hydrometcenter of Russia][3], 2 – Ltd. [Gazprom][4]
  
Moscow, 2020

### Description
The “snow technology” – SMFE is used for work with snow cover on territory of the Russian Federation. There are two the most interesting output characteristics of snow cover: snow density (RHO) and snow water equivalent (SWE). The “snow technology” is based on a variety of input parameters and involves a different complex of assimilation initial information. The main feature “snow technology” is work with model data (output data of COSMO-Ru model), satellite data and initial data from a meteorological network (SYNOP-code). We are using “snow technology” for two schemes of calculations: calculating snow parameters on real a meteorological network and calculating it for COSMO grid points. For the territory of Russian Federation, we are applying “snow technology” for three areas of investigation with different model step of special resolution: COSMO-Ru-13-ENA – model step 13 km; area of investigation – all territory of country; COSMO-Ru-ETR – model step 7 km; area of investigation – Europe part of country; COSMORu-2-CFO – model step 2 km; area of investigation – central part of country. Technology has been applied in semi-operational mode for forecasts of spring flood since 2016.

### Documentation content:
  
1. General overview of SnoWE
2. First run of SnoWE
    1. Model assembly
3. Preprocessing of SnoWE 
    1. Constant configuration files
    2. Get satellite data
    3. Get SINOP data
    4. Get COSMO-Ru data
    5. Quality control
4. Main core of SnoWE
    1. Physical parameterizations of the calculation kernel SMFE
        1. First software branch: Case of first snow
        2. Second software branch: Case of snow depth don’t change
        3. Third software branch: Case of wet snow falling
        4. Fourth software branch: Case of dry snow falling
        5. Fifth software branch: Case of snow blown
        6. Sixth software branch: Case of snow subsidence
        7. Seventh software branch: Case of snow melting
5. Postprocessing of SnoWE
6. Visualisation of results
7. Archive version of SnoWE
8. Future plans
9. Conclusions
10. List of references
11. Appendix


![image](https://user-images.githubusercontent.com/51716145/149184448-f2aab45f-f32a-4a93-bb31-ea8efab5cf4a.png)

**Figure 1.** Blockdiagram of SnoWE structure

### Documentation languages
[Russian][1] (full vesion), [English][2] (general topics)


[1]: https://github.com/EvgenyChur/Project_SnoWE/blob/master/SnoWE.pdf
[2]: https://github.com/EvgenyChur/Project_SnoWE/blob/master/SnoWE%20-%20Eng.pdf
[3]: https://meteoinfo.ru/en/about-us-eng
[4]: https://www.gazprom.com/
