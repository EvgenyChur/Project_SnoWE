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

MODULE mod_commondata

    IMPLICIT NONE

    INTEGER :: data_count
    REAL, pointer :: data_lon(:)
    REAL, pointer :: data_lat(:)
    REAL, pointer :: data_surfaceHeight(:)
    REAL, pointer :: data_snowDepth(:)
    REAL, pointer :: data_maxDayAirT(:)
    REAL, pointer :: data_averageAirT(:)
    REAL, pointer :: data_p24Sum(:)
    REAL, pointer :: data_srcRho(:)
    REAL, pointer :: data_srcSwe(:)
    REAL, pointer :: data_satelliteData(:, :)
    INTEGER, pointer :: data_id(:)

    LOGICAL :: historyExist
    LOGICAL :: satelliteDataExist

    ! For sweRhoCalculation()
    INTEGER :: snowDepth, snowDepthHistory
    REAL, pointer :: snowDepthData(:, :), snowDepthDataHistory(:, :)
    REAL :: swe, rho
    REAL, pointer :: sweByLayers(:), rhoByLayers(:)

    ! Common constants
    REAL, PARAMETER :: CONST_KELVIN_ZERO = 273.16

    INTEGER, PARAMETER :: fHistory = 50
    INTEGER, PARAMETER :: fNewHistory = 51
    INTEGER, PARAMETER :: fData1 = 52
    INTEGER, PARAMETER :: fResult = 56
    INTEGER, PARAMETER :: fDebug = 57

ENDMODULE mod_commondata