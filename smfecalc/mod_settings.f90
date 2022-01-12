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

MODULE mod_settings

USE mod_errors

IMPLICIT NONE

    INTEGER, PARAMETER :: fNamelist = 30

    ! from namelist
    INTEGER :: pointsCount
    INTEGER :: satelliteDataCount
    INTEGER :: sweRhoLayersCount
    INTEGER :: year
    INTEGER :: month
    INTEGER :: day
    INTEGER :: hour
    CHARACTER(LEN = 1024) :: filename_history
    CHARACTER(LEN = 1024) :: filename_smfeIn
    CHARACTER(LEN = 1024) :: filename_smfeResult
    CHARACTER(LEN = 1024) :: filename_satelliteData

CONTAINS

INTEGER FUNCTION loadSettings(filename_namelist)

    CHARACTER(LEN = 1024), INTENT(IN) :: filename_namelist

    NAMELIST /smfecalc/ &
        pointsCount, &
        satelliteDataCount, &
        sweRhoLayersCount, &
        year, &
        month, &
        day, &
        hour, &
        filename_history, &
        filename_smfeIn, &
        filename_smfeResult, &
        filename_satelliteData

    PRINT '(">>> Loading settings...")'

    OPEN(fNamelist, file = trim(filename_namelist), iostat = errorCode)
    IF (errorCode /= 0) THEN
        errorMsg = trim(filename_namelist)
        loadSettings = FILE_OPEN_ERROR
        RETURN
    ENDIF
    read(fNamelist, nml = smfecalc, iostat = errorCode)
    IF (errorCode /= 0) THEN
        errorMsg = trim(filename_namelist)
        loadSettings = FILE_READ_ERROR
        RETURN
    ENDIF
    CLOSE(fNamelist)

    PRINT '("pointsCount = ", i0)', pointsCount
    PRINT '("satelliteDataCount = ", i0)', satelliteDataCount
    PRINT '("sweRhoLayersCount = ", i0)', sweRhoLayersCount
    PRINT '("year = ", i4.4)', year
    PRINT '("month = ", i2.2)', month
    PRINT '("day = ", i2.2)', day
    PRINT '("hour = ", i2.2)', hour
    PRINT '("filename_history = ", a)', trim(filename_history)
    PRINT '("filename_smfeIn = ", a)', trim(filename_smfeIn)
    PRINT '("filename_smfeResult = ", a)', trim(filename_smfeResult)
    PRINT '("filename_satelliteData = ", a)', trim(filename_satelliteData)
    PRINT '("")'

    loadSettings = NO_ERROR
    RETURN
ENDFUNCTION

ENDMODULE mod_settings