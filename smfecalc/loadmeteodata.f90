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

INTEGER FUNCTION loadMeteoData()

    USE mod_errors
    USE mod_settings
    USE mod_commondata

    IMPLICIT NONE

    INTEGER :: i

    PRINT '(">>> Loading meteo data...")'

    data_count = pointsCount

    ALLOCATE(data_id(data_count), stat = errorCode)
    IF (errorCode /= 0) THEN
        errorMsg = "data_stationNumbers"
        loadMeteoData = ALLOCATE_ERROR
        RETURN
    ENDIF
    ALLOCATE(data_lon(data_count), stat = errorCode)
    IF (errorCode /= 0) THEN
        errorMsg = "data_lon"
        loadMeteoData = ALLOCATE_ERROR
        RETURN
    ENDIF
    ALLOCATE(data_lat(data_count), stat = errorCode)
    IF (errorCode /= 0) THEN
        errorMsg = "data_lat"
        loadMeteoData = ALLOCATE_ERROR
        RETURN
    ENDIF
    ALLOCATE(data_surfaceHeight(data_count), stat = errorCode)
    IF (errorCode /= 0) THEN
        errorMsg = "data_surfaceHeight"
        loadMeteoData = ALLOCATE_ERROR
        RETURN
    ENDIF
    ALLOCATE(data_snowDepth(data_count), stat = errorCode)
    IF (errorCode /= 0) THEN
        errorMsg = "data_snowDepth"
        loadMeteoData = ALLOCATE_ERROR
        RETURN
    ENDIF
    ALLOCATE(data_maxDayAirT(data_count), stat = errorCode)
    IF (errorCode /= 0) THEN
        errorMsg = "data_maxDayAirT"
        loadMeteoData = ALLOCATE_ERROR
        RETURN
    ENDIF
    ALLOCATE(data_averageAirT(data_count), stat = errorCode)
    IF (errorCode /= 0) THEN
        errorMsg = "data_averageAirT"
        loadMeteoData = ALLOCATE_ERROR
        RETURN
    ENDIF
    ALLOCATE(data_p24Sum(data_count), stat = errorCode)
    IF (errorCode /= 0) THEN
        errorMsg = "data_p24Sum"
        loadMeteoData = ALLOCATE_ERROR
        RETURN
    ENDIF
    ALLOCATE(data_srcSwe(data_count), stat = errorCode)
    IF (errorCode /= 0) THEN
        errorMsg = "data_srcSwe"
        loadMeteoData = ALLOCATE_ERROR
        RETURN
    ENDIF
    ALLOCATE(data_srcRho(data_count), stat = errorCode)
    IF (errorCode /= 0) THEN
        errorMsg = "data_srcRho"
        loadMeteoData = ALLOCATE_ERROR
        RETURN
    ENDIF

    OPEN(fData1, file = trim(filename_smfeIn), status = 'old', iostat = errorCode)
    IF (errorCode /= 0) THEN
        errorMsg = trim(filename_smfeIn)
        loadMeteoData = FILE_OPEN_ERROR
        RETURN
    ENDIF

    READ(fData1, *, iostat = errorCode) ! Skip header
    IF (errorCode /= 0) THEN
        errorMsg = trim(filename_smfeIn)
        loadMeteoData = FILE_READ_ERROR
        RETURN
    ENDIF

    DO i = 1, data_count
        READ(fData1, *, iostat = errorCode) data_id(i), data_lon(i), data_lat(i), data_surfaceHeight(i), &
            data_snowDepth(i), data_maxDayAirT(i), data_averageAirT(i), data_p24Sum(i), data_srcSwe(i), data_srcRho(i)
        IF (errorCode /= 0) THEN
            errorMsg = trim(filename_smfeIn)
            loadMeteoData = FILE_READ_ERROR
            RETURN
        ENDIF
    ENDDO

    CLOSE(fData1)

    loadMeteoData = NO_ERROR
    RETURN
ENDFUNCTION