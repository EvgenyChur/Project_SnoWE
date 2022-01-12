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

INTEGER FUNCTION loadSatelliteData()

    USE mod_errors
    USE mod_settings
    USE mod_commondata

    IMPLICIT NONE

    INTEGER :: count
    INTEGER :: i

    PRINT '(">>> Loading satellite data...")'

    count = satelliteDataCount

    satelliteDataExist = .false.
    OPEN(fData1, file = trim(filename_satelliteData), status = 'old', iostat = errorCode)
    IF (errorCode == 0) THEN
        IF (eof(fData1) == .false.) THEN
            satelliteDataExist = .true.
            ALLOCATE(data_satelliteData(3, count), stat = errorCode)
            IF (errorCode /= 0) THEN
                errorMsg = "data_satelliteData"
                loadSatelliteData = ALLOCATE_ERROR
                RETURN
            ENDIF
            READ(fData1, *, iostat = errorCode) ! Skip header
            IF (errorCode /= 0) THEN
                satelliteDataExist = .false.
                PRINT '("WARNING: satellite data file is corrupted!")'
                loadSatelliteData = NO_ERROR
                RETURN
            ENDIF
            do i = 1, count
               READ(fData1, *, iostat = errorCode) data_satelliteData(1, i), data_satelliteData(2, i), data_satelliteData(3, i)
               IF (errorCode /= 0) THEN
                   satelliteDataExist = .false.
                   PRINT '("WARNING: satellite data file is corrupted!")'
                   loadSatelliteData = NO_ERROR
                   RETURN
                ENDIF
             ENDDO
        ENDIF
        CLOSE(fData1)
    ENDIF

    loadSatelliteData = NO_ERROR
    RETURN
ENDFUNCTION