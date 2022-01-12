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

INTEGER FUNCTION sweRhoCalculation(n)

    USE mod_errors
    USE mod_settings
    USE mod_commondata
    USE mod_snowdepthconst
    USE mod_constants

    IMPLICIT NONE

    INTEGER, INTENT(IN) :: n
    INTEGER :: i
    LOGICAL :: snowBySatelliteData
    INTEGER :: smfe
    INTEGER :: error

    debug_route = -2

    IF ((data_srcSwe(n) /= EMPTY).and.(data_srcRho(n) /= EMPTY)) THEN
        snowDepth = 0 ! Snow history is not formed for these cases. Swe and rho are not calculated
        swe = data_srcSwe(n)
        rho = data_srcRho(n)
        IF (swe >= 1.0) THEN
            DO i = 1, sweRhoLayersCount
                sweByLayers(i) = swe / sweRhoLayersCount
                rhoByLayers(i) = rho
            ENDDO
        ELSE
            CALL setSweRhoToZero()
        ENDIF
        sweRhoCalculation = NO_ERROR
        RETURN
    ENDIF

    debug_route = -1

    ! Контроль данных
    IF ((data_snowDepth(n) == EMPTY).or.(data_maxDayAirT(n) == EMPTY).or.(data_averageAirT(n) == EMPTY).or.(data_p24Sum(n) == EMPTY)) THEN
        snowDepth = snowDepthHistory
        ALLOCATE(snowDepthData(2, snowDepth), stat = errorCode)
        IF (errorCode /= 0) THEN
            errorMsg = "snowDepthData"
            sweRhoCalculation = ALLOCATE_ERROR
            RETURN
        ENDIF
        snowDepthData = snowDepthDataHistory
        CALL setSweRhoToZero()
        sweRhoCalculation = NO_ERROR
        RETURN
    ENDIF

    debug_route = 0

    IF (snowDepthHistory == 0) THEN ! If history does not exist
        IF ((snowDepth >= 80).and.(data_lat(n) < 70.0)) THEN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 60 - плохо! !!!!! We consider this value as an error (unreal value) and snow depth = 0
            snowDepth = 0
        ENDIF
        IF (snowDepth == 0) THEN ! Snow is not present
            CALL setSweRhoToZero()
        ELSE ! Show is present
            ALLOCATE(snowDepthData(2, snowDepth), stat = errorCode)
            IF (errorCode /= 0) THEN
                errorMsg = "snowDepthData"
                sweRhoCalculation = ALLOCATE_ERROR
                RETURN
            ENDIF           

            error = smfe(data_averageAirT(n), data_maxDayAirT(n), data_p24Sum(n), sweRhoLayersCount, &
                snowDepthHistory, snowDepth, snowDepthDataHistory, snowDepthData, swe, rho, sweByLayers, rhoByLayers)
            IF (error /= NO_ERROR) THEN
                sweRhoCalculation = error
                RETURN
            ENDIF
        ENDIF
    ELSE ! If history is present
        IF (snowDepth == 0) THEN ! Snow is not present
            IF (snowDepthHistory >= 3) THEN !!! было 5
                !IF ((satelliteDataExist == .true.).and.(snowBySatelliteData(n) == .true.)) THEN ! WARNING! TEST MODE!  
                IF (((satelliteDataExist == .true.).and.(snowBySatelliteData(n) == .true.)).or.(snowNearby(n) == .true.)) THEN ! WARNING! TEST MODE!  
                    snowDepth = snowDepthHistory
                    ALLOCATE(snowDepthData(2, snowDepth), stat = errorCode)
                    IF (errorCode /= 0) THEN
                        errorMsg = "snowDepthData"
                        sweRhoCalculation = ALLOCATE_ERROR
                        RETURN
                    ENDIF
                    snowDepthData = snowDepthDataHistory

                    swe = 0.0
                    rho = 0.0
                    DO i = 1, snowDepthHistory
                        swe = swe + snowDepthDataHistory(1, i) * SH_HEIGHT
                        rho = rho + snowDepthDataHistory(1, i)
                    ENDDO
                    rho = rho / snowDepthHistory
                    DO i = 1, sweRhoLayersCount
                        sweByLayers(i) = swe / sweRhoLayersCount
                        rhoByLayers(i) = rho
                    ENDDO
                ELSE
                    CALL setSweRhoToZero()
                ENDIF
            ELSE
                CALL setSweRhoToZero()
            ENDIF
        ELSE ! Snow is present
            IF (snowDepth - snowDepthHistory > 70) THEN ! Difference in snow depth in one day - more than 0.7 m (70 cm). consider this value as an error and take snow depth for previous day
                snowDepth = snowDepthHistory
            ENDIF

            ALLOCATE(snowDepthData(2, snowDepth), stat = errorCode)
            IF (errorCode /= 0) THEN
                errorMsg = "snowDepthData"
                sweRhoCalculation = ALLOCATE_ERROR
                RETURN
            ENDIF

            error = smfe(data_averageAirT(n), data_maxDayAirT(n), data_p24Sum(n), sweRhoLayersCount, &
                snowDepthHistory, snowDepth, snowDepthDataHistory, snowDepthData, swe, rho, sweByLayers, rhoByLayers)
            IF (error /= NO_ERROR) THEN
                sweRhoCalculation = error
                RETURN
            ENDIF
        ENDIF
    ENDIF

    IF (swe < 1.0) THEN
        CALL setSweRhoToZero()
    ENDIF

    sweRhoCalculation = NO_ERROR
    RETURN

CONTAINS

    SUBROUTINE setSweRhoToZero()
        INTEGER :: i

        swe = 0.0
        rho = 0.0
        DO i = 1, sweRhoLayersCount
            sweByLayers(i) = 0.0
            rhoByLayers(i) = 0.0
        ENDDO

        RETURN
    ENDSUBROUTINE
    
    LOGICAL FUNCTION snowNearby(n)
        INTEGER, INTENT(IN) :: n
        INTEGER :: i, j
        LOGICAL :: snow(data_count), tmp_snow
        REAL :: distance(data_count), tmp_distance
        LOGICAL :: flag

        DO i = 1, data_count
            snow(i) = (data_snowDepth(i) > 0.0)
            distance(i) = SQRT((data_lon(i) - data_lon(n))**2 + (data_lat(i) - data_lat(n))**2)
        ENDDO

        DO j = 1, data_count - 1
            flag = .false.
            DO i = 1, data_count - j
                IF (distance(i) > distance(i + 1)) THEN
                    tmp_snow = snow(i)
                    tmp_distance = distance(i)
                    snow(i) = snow(i + 1)
                    distance(i) = distance(i + 1)
                    snow(i + 1) = tmp_snow
                    distance(i + 1) = tmp_distance
                    flag = .true.
                ENDIF
            ENDDO
            IF (flag == .false.) EXIT
        ENDDO

        print*, COUNT(snow(1:10))

        snowNearby = (COUNT(snow(1:10)) > 5) ! snow > 50% of stations
        RETURN
    ENDFUNCTION

ENDFUNCTION