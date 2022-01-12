PROGRAM smfecalc

!-------------------------------------------------------------------------------
!
! Description:
!
!   The program "smfecalc" calculates snow water equivalent (swe) and snow density
!   values using information about meteorological elements - snow depth, T2m,
!   12-hour precipitation sums. For each pount snow is represented as a number
!   of subLayersCount (elements) with the height of 1 cm. Two main processes are
!   considered in the snow model – snow accumulation and snow decrease. Snow
!   accumulation is connected with snowfalls (fresh snow). Fresh snow density
!   is determined according to temperature dependence suggested in (Bartlett P.A.,
!   MacKay m.D. and Verseghy D.l., 2006)(SUBROUTINE snowfresh). When accumulation
!   period is, snow density can be calculated according to (Yosida Z., Huzioka T.,
!   1954) based on the dependence of Young's module on snow density (SUBROUTINE
!   density and SUBROUTINE density1). Snow decrease can be due to subsidence,
!   melting, snow blowing.
!
! Current Code Owner:
!
!   Roshydromet
!
! Authors:
!
!   Hydrometeorological Research Center of Russia, 2015-2017!
!   Ekaterina Kazakova, Mikhail Chumakov, Inna Rozinkina, Vladimir Kopeykin,
!   Evgeny Churiulin
!   phone:  +7(499)795-23-59
!   email:  catherine.kazakova@mail.ru, inna.rozinkina@mail.ru,
!   v.v.kopeykin@mail.ru, evgenychur@gmail.com
!
!-------------------------------------------------------------------------------

    USE mod_errors
    USE mod_settings
    USE mod_commondata

    IMPLICIT NONE

    CHARACTER(LEN = 1024) :: filename_namelist
    INTEGER :: error
    INTEGER :: loadMeteoData
    INTEGER :: loadSatelliteData
    INTEGER :: sweRhoCalculation
    INTEGER :: n, layer
    CHARACTER(LEN = 1024) :: filename_debug
    CHARACTER(LEN = 1024) :: yearMonthDay

    PRINT '("")'
    PRINT '(">>> smfecalc is started! v.0.115")'
    PRINT '("")'

    IF (iargc() == 0) THEN
        filename_namelist = "./smfecalc.nl"
    ELSE
        CALL getarg(1, filename_namelist)
    ENDIF

    ! Load settings from namelist
    error = loadSettings(filename_namelist)
    IF (error /= NO_ERROR) THEN
        CALL printErrorInfo(error)
        CALL exit(error)
    ENDIF

    ! READ initial data
    error = loadMeteoData()
    IF (error /= NO_ERROR) THEN
        CALL printErrorInfo(error)
        CALL exit(error)
    ENDIF

    ! READ satellite data, if it exists
    error = loadSatelliteData()
    IF (error /= NO_ERROR) THEN
        CALL printErrorInfo(error)
        CALL exit(error)
    ENDIF

    ! OPEN history file, if it exists
    historyExist = .false.
    OPEN(fHistory, file = trim(filename_history), form = 'binary', status = 'old', iostat = errorCode)
    IF (errorCode == 0) THEN
        IF (eof(fHistory) == .false.) THEN
            historyExist = .true.
        ENDIF
    ENDIF
    IF (historyExist == .true.) THEN
        PRINT '("History exists!")'
    ELSE
        PRINT '("History is empty!")'
    ENDIF
    PRINT '("")'

    ! OPEN file for new history
    OPEN(fNewHistory, file = trim(filename_history)//".tmp", form='binary', status = 'new', iostat = errorCode)
    IF (errorCode /= 0) THEN
        errorMsg = trim(filename_history)//".tmp"
        error = FILE_OPEN_ERROR
        CALL printErrorInfo(error)
        CALL exit(error)
    ENDIF

    IF (sweRhoLayersCount > 0) THEN
        ALLOCATE(rhoByLayers(sweRhoLayersCount), stat = errorCode)
        IF (errorCode /= 0) THEN
            errorMsg = "rhoByLayers"
            error = ALLOCATE_ERROR
            CALL printErrorInfo(error)
            CALL exit(error)
        ENDIF
        ALLOCATE(sweByLayers(sweRhoLayersCount), stat = errorCode)
        IF (errorCode /= 0) THEN
            errorMsg = "sweByLayers"
            error = ALLOCATE_ERROR
            CALL printErrorInfo(error)
            CALL exit(error)
        ENDIF
    ENDIF

    ! OPEN file for result
    OPEN(fResult, file = trim(filename_smfeResult), status = 'unknown', iostat = errorCode)
    IF (errorCode /= 0) THEN
        errorMsg = trim(filename_smfeResult)
        error = FILE_OPEN_ERROR
        CALL printErrorInfo(error)
        CALL exit(error)
    ENDIF
    ! WRITE result header to file
    WRITE(fResult ,'(3(a10),2(a10),:10(2(a8,i2.2)))') &
        "id", "lon", "lat", "swe", "rho", (("swe", layer, "rho", layer), layer = 1, sweRhoLayersCount)

    PRINT '(">>> Swe, rho calculation...")'

    do n = 1, data_count

        snowDepth = nint(data_snowDepth(n))

        ! READ history, if it exists
        IF (historyExist == .false.) THEN
            snowDepthHistory = 0
        ELSE
            READ(fHistory, iostat = errorCode) snowDepthHistory
            IF (errorCode /= 0) THEN
                errorMsg =  trim(filename_history)
                error = FILE_READ_ERROR
                CALL printErrorInfo(error)
                CALL exit(error)
            ENDIF
        ENDIF
        ALLOCATE(snowDepthDataHistory(2, snowDepthHistory), stat = errorCode)
        IF (errorCode /= 0) THEN
            errorMsg = "snowDepthData_old"
            error = ALLOCATE_ERROR
            CALL exit(error)
        ENDIF
        IF (snowDepthHistory > 0) THEN
            READ(fHistory, iostat = errorCode) snowDepthDataHistory
            IF (errorCode /= 0) THEN
                errorMsg =  trim(filename_history)
                error = FILE_READ_ERROR
                CALL printErrorInfo(error)
                CALL exit(error)
            ENDIF
        ENDIF

        ! Swe, rho calculation
        error = sweRhoCalculation(n)
        IF (error /= NO_ERROR) THEN
            CALL printErrorInfo(error)
            CALL exit(error)
        ENDIF

        ! WRITE new history to file
        WRITE(fNewHistory) snowDepth
        IF (snowDepth /= 0) THEN
            WRITE(fNewHistory) snowDepthData
        ENDIF

        IF (ASSOCIATED(snowDepthDataHistory)) DEALLOCATE(snowDepthDataHistory)
        IF (ASSOCIATED(snowDepthData)) DEALLOCATE(snowDepthData)

        ! WRITE result to file
        WRITE(fResult ,'(i10,2(f10.4),2(f10.3),:10(2(f10.3)))') &
            data_id(n), data_lon(n), data_lat(n), swe, rho, &
            ((sweByLayers(layer), rhoByLayers(layer)), layer = 1, sweRhoLayersCount)

!===================================================================================================================================
       ! WRITE DEBUG DATA (SERIES)
       IF ((data_id(n) == 25563).or.(data_id(n) == 32379).or.(data_id(n) == 25503).or.(data_id(n) == 24143).or.&
           (data_id(n) == 24871).or.(data_id(n) == 30385).or.(data_id(n) == 20982).or.(data_id(n) == 23982).or.&
           (data_id(n) == 36104).or.(data_id(n) == 36022).or.(data_id(n) == 28748).or.(data_id(n) == 34146).or.&
           (data_id(n) == 27242).or.(data_id(n) == 23701).or.(data_id(n) == 23662).or.(data_id(n) == 22213).or.&
           (data_id(n) == 23073).or.(data_id(n) == 23274).or.(data_id(n) == 23884).or.(data_id(n) == 22349).or.&
           (data_id(n) == 23179).or.(data_id(n) == 23472).or.(data_id(n) == 23867).or.(data_id(n) == 22204).or.&
           (data_id(n) == 24219).or.(data_id(n) == 23426).or.(data_id(n) == 23226).or.(data_id(n) == 34356).or.&
           (data_id(n) == 23912).or.(data_id(n) == 28264).or.(data_id(n) == 23632).or.(data_id(n) == 28216).or.&
           (data_id(n) == 29023).or.(data_id(n) == 23804).or.(data_id(n) == 26094).or.(data_id(n) == 27242).or.&
           (data_id(n) == 23708).or.(data_id(n) == 22619).or.(data_id(n) == 22408)) THEN
!       IF ((data_lon(n) >= 44.5).and.(data_lon(n) <= 64.5).and.(data_lat(n) >= 50.0).and.(data_lat(n) <= 61.0)) THEN
           WRITE(filename_debug, '("DEBUG/",i8.8,".txt")') data_id(n)

           OPEN(fDebug, file = trim(filename_debug), status = 'old', access = 'append', iostat = errorCode)
           IF (errorCode /= 0) THEN
               OPEN(fDebug, file = trim(filename_debug), status = 'new', iostat = errorCode)
               IF (errorCode /= 0) THEN
                   errorMsg = trim(filename_debug)
                   error = FILE_OPEN_ERROR
                   CALL printErrorInfo(error)
                   CALL exit(error)
               ENDIF
               WRITE(fDebug ,'(a8,a6,2(a10),2(a10),a10,2(a10),:10(2(a8,i2.2)))') &
                   "date", "route", "lon", "lat", "maxT", "aveT", "depth", "swe", "rho", &
                   (("swe", layer, "rho", layer), layer = 1, sweRhoLayersCount)
           ENDIF

           WRITE(yearMonthDay, '(i4.4,i2.2,i2.2)') year, month, day
           WRITE(fDebug ,'(a8,i6,2(f10.4),2(f10.3),i10,:10(2(f10.3)))') &
               trim(yearMonthDay), debug_route, data_lon(n), data_lat(n), data_maxDayAirT(n), data_averageAirT(n), snowDepth, &
               swe, rho, ((sweByLayers(layer), rhoByLayers(layer)), layer = 1, sweRhoLayersCount)
           CLOSE(fDebug)
       ENDIF
!===================================================================================================================================

    ENDDO

    CLOSE(fHistory)
    CLOSE(fNewHistory)
    CLOSE(fResult)
    CALL rename(trim(filename_history)//".tmp", filename_history)

    PRINT '("")'
    PRINT '(">>> smfecalc completed successfully!")'
    PRINT '("")'

    CALL EXIT(NO_ERROR)

ENDPROGRAM
