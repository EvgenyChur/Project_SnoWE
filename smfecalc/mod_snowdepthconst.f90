!-------------------------------------------------------------------------------
!
! Current code owner:
!
!   Roshydromet
!
! Authors:
!
!   Hydrometeorological Research Center of Russia, 2015-2017
!   Ekaterina Kazakova, Mikhail Chumakov, Inna Rozinkina,
!   Vladimir Kopeykin, Evgeny Churiulin
!   phone:  +7(499)795-23-59
!   email:  catherine.kazakova@mail.ru, inna.rozinkina@mail.ru,
!   v.v.kopeykin@mail.ru, evgenychur@gmail.com
!
!-------------------------------------------------------------------------------

MODULE mod_snowdepthconst
    REAL, PARAMETER :: SH_HEIGHT = 0.01      ! 1 cm [m]
    REAL, PARAMETER :: RHO_FIRN = 700.0      ! maximum snow density [kg/m3]
    REAL, PARAMETER :: RHO_WATER = 1000.0    ! density of water [kg/m3]
    REAL, PARAMETER :: ELEMENT_VOLUME = 0.01 ! m2*cm=0.01m3 (1cm=10**-2m) [m3]
    REAL, PARAMETER :: SLOPE_PARAM = 0.5     ! In case of water in the snow column half of its amount is removed
    REAL, PARAMETER :: SLOPE_PARAM_WET = 0.5 ! Case of wet snow
ENDMODULE
