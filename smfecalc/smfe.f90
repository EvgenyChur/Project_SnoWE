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

INTEGER FUNCTION smfe(averageAirT, maxDayAirT, p24Sum, sweRhoLayersCount, snowDepth_old, snowDepth_new, &
    snowDepthData_old, snowDepthData_new, swe_end, rho_end, sweByLayers_end, rhoByLayers_end)

    USE mod_snowdepthconst
    USE mod_errors
    USE mod_constants

    IMPLICIT NONE

    REAL, INTENT(IN) :: averageAirT                            ! Averaged value [C]
    REAL, INTENT(IN) :: maxDayAirT                             ! Maximum value [C]
    REAL, INTENT(IN) :: p24Sum                                 ! 12h precipitation [mm]
    INTEGER, INTENT(IN) :: sweRhoLayersCount                   ! Amount of needed subLayersCount in snow column
    INTEGER, INTENT(IN) :: snowDepth_old                       ! Snow depth for the previous day [cm]
    INTEGER, INTENT(INOUT) :: snowDepth_new                    ! Snow depth [cm]
    REAL, INTENT(INOUT) :: snowDepthData_old(2, snowDepth_old) ! Snow depth data
    REAL, INTENT(OUT) :: snowDepthData_new(2, snowDepth_new)   ! Snow depth data for the previous day
    REAL, INTENT(OUT) :: rho_end                               ! Averaged density of the snow column [kg/m3]
    REAL, INTENT(OUT) :: swe_end                               ! Snow water equivalent (SWE) of the snow column [kg/m2 or mm]
    REAL, INTENT(OUT) :: sweByLayers_end(sweRhoLayersCount)    ! Swe for needed subLayersCount
    REAL, INTENT(OUT) :: rhoByLayers_end(sweRhoLayersCount)    ! Rho for needed subLayersCount

    INTEGER :: deltaSnow         ! Difference between new snow depth (present) and old (previous)
    REAL :: swe                  ! Snow water equivalent (SWE) of the snow column (calculated in subroutine waterSnow) [kg/m2 or mm]
    REAL :: rho                  ! Average density of snow column (calculated in subroutine density_median). Median value [kg/m3]
    REAL :: rhoSum               ! Variable for summing snow density (utility) [kg/m3]
    REAL :: rhoExcess
    INTEGER :: subLayersCount
    INTEGER :: layer1, layer2
    INTEGER :: i, j, z, m, l, k, t
	REAL :: sweDelta

    IF (snowDepth_old == 0) THEN
        debug_route = 1
        CALL section_firstSnow
    ELSE
        deltaSnow = snowDepth_new - snowDepth_old
        IF (deltaSnow == 0) THEN
            debug_route = 2
            CALL section_snowDepthDidNotChange
        ELSE ! Snow depth changed
            IF (deltaSnow > 0) THEN ! Snow accumulation. Snow has fallen and its amount is bigger than the previous amount
                IF (averageAirT >= 0.0) THEN
                    debug_route = 3
                    CALL section_wetSnowHasFallen
                ELSE
                    debug_route = 4
                    CALL section_drySnowHasFallen
                ENDIF
            ELSE ! Snow decrease (deltaSnow < 0)
                deltaSnow = -1 * deltaSnow
                ! Snow depth changed more than 25% for 24 hours => blowing
                IF (((1.0 - float(snowDepth_new) / float(snowDepth_old)) * 100.0  > 25.0).AND.(averageAirT < 0.0)) THEN
                    debug_route = 5
                    CALL section_blowingSnow
                ELSE
                    IF (maxDayAirT < 0.0) THEN
                        debug_route = 6
                        CALL section_snowDecreaseDueToSubsidence
                    ELSE
                        debug_route = 7
                        CALL section_snowDecreaseDueToMelting
                    ENDIF
                ENDIF
            ENDIF
        ENDIF
    ENDIF

! ----------------------------------------------------------------------------------------------------------------------------------

    ! Check if we received snow density more than rho_firn=700 kg/m3. in this case reduce the value to this limit
    rhoExcess = 0.0
    DO i = snowDepth_new, 1, -1
        snowDepthData_new(1, i) = snowDepthData_new(1, i) + rhoExcess
        rhoExcess = 0.0
        IF (snowDepthData_new(1, i) > RHO_FIRN) THEN
            rhoExcess = snowDepthData_new(1, i) - RHO_FIRN
            snowDepthData_new(1, i) = RHO_FIRN
        ENDIF
    ENDDO

    ! Calculate RHI and SWE for needed amount of subLayersCount
    IF (snowDepth_new == 0) THEN
        swe_end = 0.0
        rho_end = 0.0

        IF (sweRhoLayersCount /= 0) THEN
            sweByLayers_end = 0.0
            rhoByLayers_end = 0.0
        ENDIF
    ELSE
        swe_end = waterSnow(snowDepthData_new(1, :), snowDepth_new)
        rho_end = density_average(snowDepthData_new(1, :), snowDepth_new)

        IF (sweRhoLayersCount /= 0) THEN
            sweByLayers_end = 0.0
            rhoByLayers_end = 0.0
            subLayersCount = max(floor(real(snowDepth_new) / sweRhoLayersCount), 1)

            DO i = 1, min(sweRhoLayersCount, snowDepth_new)
                layer1 = 1 + (i - 1) * subLayersCount
                IF (i < sweRhoLayersCount) THEN
                    layer2 = i * subLayersCount
                ELSE
                    layer2 = snowDepth_new
                ENDIF
                sweByLayers_end(i) = waterSnow(snowDepthData_new(1, layer1 : layer2), layer2 - layer1 + 1)
                rhoByLayers_end(i) = density_average(snowDepthData_new(1, layer1 : layer2), layer2 - layer1 + 1)
            ENDDO
        ENDIF
    ENDIF

    smfe = NO_ERROR
    RETURN

CONTAINS !==========================================================================================================================

    SUBROUTINE sort_real(n, x)
    !-------------------------------------------------------------------------------------------------------------------------------
    ! Bubble sort
    !-------------------------------------------------------------------------------------------------------------------------------
        IMPLICIT NONE

        INTEGER, INTENT(IN) :: n
        REAL, INTENT(INOUT) :: x(n)
        REAL :: tmp
        INTEGER :: i, j

        DO i = 1, n - 1
            DO j = 1, n - i - 1
                IF (x(j) > x(j + 1)) THEN
                    tmp = x(j)
                    x(j) = x(j + 1)
                    x(j + 1) = tmp
                ENDIF
            ENDDO
        ENDDO

        RETURN
    ENDSUBROUTINE

    REAL FUNCTION freshSnow(temperature)
    !-------------------------------------------------------------------------------------------------------------------------------
    ! Calculation fresh snow density according to (Bartlett P.A., MacKay m.D. and Verseghy D.l., 2006)
    !-------------------------------------------------------------------------------------------------------------------------------
        IMPLICIT NONE

        REAL, INTENT(IN) :: temperature

        IF (temperature <= 0.0) THEN
            freshSnow = 67.92 + 51.25 * exp(temperature / 2.59)
        ELSE
            freshSnow = min(200.0, 119.2 + 20.0 * temperature)
        ENDIF

        RETURN
    ENDFUNCTION

    REAL FUNCTION waterSnow(snowDepthData_rho, snowDepth)
    !-------------------------------------------------------------------------------------------------------------------------------
    ! Calculation of snow water equivalent (swe) for each layer
    ! ------------------------------------------------------------------------------------------------------------------------------
        USE mod_snowdepthconst

        IMPLICIT NONE

        INTEGER, INTENT(IN) :: snowDepth
        REAL, INTENT(IN) :: snowDepthData_rho(snowDepth)

        waterSnow = sum(snowDepthData_rho) * SH_HEIGHT ! In kg/m2 or mm

        RETURN
    ENDFUNCTION

    REAL FUNCTION density_median(snowDepthData, snowDepth)
    !-------------------------------------------------------------------------------------------------------------------------------
    ! Calculation median value of snow density
    ! ------------------------------------------------------------------------------------------------------------------------------
        IMPLICIT NONE

        INTEGER, INTENT(IN) :: snowDepth ! Snow depth
        REAL, INTENT(IN) :: snowDepthData(snowDepth) ! Array with snow elements for the present day
        REAL :: snowDepthData_tmp(snowDepth)

        IF (snowDepth == 0) THEN
            density_median = 0
            RETURN
        ENDIF

        snowDepthData_tmp = snowDepthData

        CALL sort_real(snowDepth, snowDepthData_tmp)

        IF (mod(snowDepth, 2) == 0) THEN
            rho = (snowDepthData_tmp(snowDepth / 2) + snowDepthData_tmp(snowDepth / 2 + 1)) / 2
        ELSE
            rho = snowDepthData_tmp(snowDepth / 2 + 1)
        ENDIF

        density_median = rho
        RETURN
    ENDFUNCTION

    SUBROUTINE density(snowDepthData_rho, snowDepth, temperature, rhoSum)
    !-------------------------------------------------------------------------------------------------------------------------------
    ! Calculation density according to (Yosida Z., Huzioka T., 1954)
    ! ------------------------------------------------------------------------------------------------------------------------------
        USE mod_snowdepthconst

        IMPLICIT NONE
        INTEGER, INTENT(IN) :: snowDepth ! Snow depth
        REAL, INTENT(INOUT) :: snowDepthData_rho(snowDepth) ! Array with snow elements for the present day
        REAL, INTENT(IN) :: temperature ! Averaged daily T2m
        REAL, INTENT(OUT) :: rhoSum ! Density of snow elements in the column
        INTEGER :: j

        rhoSum = snowDepthData_rho(1)
        DO j = 2, snowDepth
            IF (temperature >= -5.0) THEN
                snowDepthData_rho(j) = (rhoSum * SH_HEIGHT * CONST_G / (1000000.0 * (0.002)) + 1.86) / 0.0167   ! h in cm
            ELSE
                snowDepthData_rho(j) = (rhoSum * SH_HEIGHT * CONST_G / (1000000.0 * (0.002)) + 10.8) / 0.059    ! h in cm
            ENDIF
            rhoSum = rhoSum + snowDepthData_rho(j)
        ENDDO

        RETURN
    ENDSUBROUTINE

    SUBROUTINE density1(temperatureMode, rhoSum, rho)
    !-------------------------------------------------------------------------------------------------------------------------------
    ! One element density calculation according to (Yosida Z., Huzioka T., 1954)
    ! ------------------------------------------------------------------------------------------------------------------------------
        USE mod_snowdepthconst

        IMPLICIT NONE

        REAL, INTENT(IN) :: temperatureMode ! 0.0 or 1.0
        REAL, INTENT(IN) :: rhoSum ! Density of snow elements in the column
        REAL, INTENT(OUT) :: rho  ! Median value of snow depth column

        IF (temperatureMode == 0.0) THEN
            rho = (rhoSum * SH_HEIGHT * CONST_G / (1000000.0 * (0.002)) + 1.86) / 0.0167 ! h in cm
        ELSE
            rho = (rhoSum * SH_HEIGHT * CONST_G / (1000000.0 * (0.002)) + 10.8) / 0.059 ! h in cm
        ENDIF

        RETURN
    ENDSUBROUTINE

    REAL FUNCTION density_average(snowDepthData_rho, snowDepth)
    !-------------------------------------------------------------------------------------------------------------------------------
    ! Calculation averaged density
    ! ------------------------------------------------------------------------------------------------------------------------------
        USE mod_snowdepthconst

        IMPLICIT NONE

        INTEGER, INTENT(IN) :: snowDepth
        REAL, INTENT(IN) :: snowDepthData_rho(snowDepth) ! Array with snow elements for the present day

        density_average = sum(snowDepthData_rho) / snowDepth
        RETURN
    ENDFUNCTION

    SUBROUTINE section_firstSnow
        snowDepthData_new(1, 1) = freshSnow(averageAirT)
        CALL density(snowDepthData_new(1, :), snowDepth_new, averageAirT, rhoSum)

        IF (averageAirT >= -5.0) THEN
            snowDepthData_new(2, :) = 0.0
        ELSE
            snowDepthData_new(2, :) = 1.0
        ENDIF

        RETURN
    ENDSUBROUTINE

    SUBROUTINE section_snowDepthDidNotChange
    !-------------------------------------------------------------------------------------------------------------------------------
    ! Snow depth did not change
    !-------------------------------------------------------------------------------------------------------------------------------
        REAL :: deltaRhoWet            ! Surplus of moisture (water)  [kg/m3]
        INTEGER :: deltaRhoWetUp      ! Mass of water in wet snow [kg/m3]

        snowDepth_new = snowDepth_old

        snowDepthData_new(:, 1 : snowDepth_new) = snowDepthData_old
        IF (p24Sum > 0.0) THEN ! Case of precipitation, but snow depth didn't change
            ! Temperature limit when snow is falling(larger positive temperature ->could be snow+rain)
            snowDepthData_new(1, 1) = freshSnow(-0.01) 
            deltaRhoWet = (freshSnow(averageAirT) - snowDepthData_new(1, 1)) * SLOPE_PARAM_WET ! Surplus of moisture (water)

            ! Mass of water in wet snow          
            IF (averageAirT >= -5.0) THEN
            	deltaRhoWetUp = deltaRhoWet / (2.0 * snowDepth_new) ! Draining
        	ELSE
            	deltaRhoWetUp = deltaRhoWet / (1.0 * snowDepth_new) ! No draining
            ENDIF

            DO i = 1, snowDepth_new ! Cycle for the elements of the snow column
                snowDepthData_new(1, i) = snowDepthData_new(1, i) + deltaRhoWetUp ! Each cm-layer gets equal water quantity
            ENDDO
        ENDIF

        RETURN
    ENDSUBROUTINE

    SUBROUTINE section_wetSnowHasFallen
    !-------------------------------------------------------------------------------------------------------------------------------
    ! Wet snow has fallen (averageAirT >= 0)
    !-------------------------------------------------------------------------------------------------------------------------------
        REAL :: deltaRhoWet ! Surplus of moisture (water)  [kg/m3]

        snowDepthData_new(1, 1) = freshSnow(-0.01) ! Temperature limit when snow is falling(rho_fresh - output)

        ! Top snow, its amount - deltaSnow
        CALL density(snowDepthData_new(1, :), deltaSnow, averageAirT, rhoSum)
        DO i = 1, deltaSnow
            IF (averageAirT >= -5.0) THEN ! New values of the bottom subLayersCount (as fallen snow presses the bottom)
                snowDepthData_new(2, i) = 0.0
            ELSE
                snowDepthData_new(2, i) = 1.0
            ENDIF
        ENDDO

        deltaRhoWet = (freshSnow(averageAirT) - snowDepthData_new(1, 1)) * SLOPE_PARAM_WET ! Surplus of moisture (water)

  		IF (snowDepth_new > 10) THEN
        	deltaRhoWet = deltaRhoWet! 
		ELSE
        	deltaRhoWet = deltaRhoWet / 2.0 ! Draining
        ENDIF

      	rhoSum = rhoSum + deltaRhoWet 

        DO i = 1, deltaSnow ! Top
            snowDepthData_new(1, i) = snowDepthData_new(1, i) + deltaRhoWet / deltaSnow ! Each cm-layer gets equal water quantity
        ENDDO

        ! Bottom snow, its amount - snowDepth_old
        DO i = 1, snowDepth_old
            snowDepthData_old(1, i) = snowDepthData_old(1, i) + deltaRhoWet / snowDepth_old
        ENDDO

        DO i = 1, snowDepth_old
            CALL density1(snowDepthData_old(2, i), rhoSum, rho)
            rhoSum = rhoSum + rho
            IF (snowDepthData_old(1, i) < rho) THEN
                snowDepthData_old(1, i) = rho
            ENDIF
        ENDDO

        DO i = deltaSnow + 1, snowDepth_new ! Bottom
            snowDepthData_new(1, i) = snowDepthData_old(1, i - deltaSnow)
            snowDepthData_new(2, i) = snowDepthData_old(2, i - deltaSnow)
        ENDDO

  		IF (averageAirT >= 1.0) THEN ! дождь
			sweDelta = waterSnow(snowDepthData_new(1, :), snowDepth_new) - waterSnow(snowDepthData_old(1, :), snowDepth_old)

	        !precipitation
        	IF ((p24Sum > 0.0).AND.(p24Sum > sweDelta)) THEN
        		DO i = 1, snowDepth_new
    		        snowDepthData_new(1, i) = snowDepthData_new(1, i) + (p24Sum - sweDelta) / (snowDepth_new * sh_height)
		        ENDDO
	    	ENDIF
		ENDIF

        RETURN
    ENDSUBROUTINE

    SUBROUTINE section_drySnowHasFallen
    !-------------------------------------------------------------------------------------------------------------------------------
    ! Dry snow has fallen (averageAirT < 0)
    !-------------------------------------------------------------------------------------------------------------------------------

        ! Top snow
        snowDepthData_new(1, 1) = freshSnow(averageAirT)
        CALL density(snowDepthData_new(1, :), deltaSnow, averageAirT, rhoSum)
        DO i = 1, deltaSnow
            IF (averageAirT >= -5.0) THEN ! New values of the bottom subLayersCount (as fallen snow presses the bottom)
                snowDepthData_new(2, i) = 0.0
            ELSE
                snowDepthData_new(2, i) = 1.0
            ENDIF
        ENDDO
        ! Bottom snow
        
        ! Bottom snow can keep top snow
        CALL density1(snowDepthData_old(2, 1), rhoSum, rho)
            
        IF(rho > snowDepthData_old(1, 1)) THEN ! Calculate again new values of the bottom
            DO i = 1, snowDepth_old 
                CALL density1(snowDepthData_old(2, i), rhoSum, rho)
                snowDepthData_old(1, i) = max(snowDepthData_old(1, i), rho)
				rhoSum = rhoSum + snowDepthData_old(1, i)
            ENDDO
		ELSE
            IF (snowDepthData_old(1, 1) <= 115.0) THEN ! 110.0 ! No top-fresh snow (no 100kg/m3)
				snowDepthData_old(1, 1) = rho
      		ENDIF
		ENDIF           
        	
        DO i = deltaSnow + 1, snowDepth_new
            snowDepthData_new(1, i) = snowDepthData_old(1, i - deltaSnow)
	        snowDepthData_new(2, i) = snowDepthData_old(2, i - deltaSnow)
        ENDDO
     
        RETURN
    ENDSUBROUTINE

    SUBROUTINE section_blowingSnow
    !-------------------------------------------------------------------------------------------------------------------------------
    ! Blowing snow
    !-------------------------------------------------------------------------------------------------------------------------------
        DO i = 1, snowDepth_new
            snowDepthData_new(1, i) = snowDepthData_old(1, i + deltaSnow)
            snowDepthData_new(2, i) = snowDepthData_old(2, i + deltaSnow)
        ENDDO

        RETURN
    ENDSUBROUTINE

    SUBROUTINE section_snowDecreaseDueToSubsidence
    !-------------------------------------------------------------------------------------------------------------------------------
    ! Snow decrease due to subsidence (maxDayAirT < 0)
    !-------------------------------------------------------------------------------------------------------------------------------
    ! Inclusion is a number of elements which were formed under the same temperature conditions.
    ! We determine the amount of inclusions and the minimum element inside each inclusion. This min element is removed
    ! from the inclusion and its weight is equally distributed between other elements in this inclusion
    ! The cycle continues till snowDepth_old is equal to snowDepth_new
        REAL, ALLOCATABLE :: inclusionsRho(:, :)
        REAL, ALLOCATABLE :: inclusionsTempMode(:)
        REAL, ALLOCATABLE :: minoton(:)
        INTEGER :: inclusionsNumber, minotonsNumber, minotonCount
        REAL :: currentInclusion
        INTEGER :: i, j, k, t, iSave, jSave
        REAL :: medianSave, median, rhoSave
        REAL :: addDensity

        inclusionsNumber = 0
        minotonCount = 0
        minotonsNumber = 0 ! Maxumin minotons count
        currentInclusion = -1.0 ! Inclision by tempMode

        DO k = 1, snowDepth_old
            IF (snowDepthData_old(2, k) == currentInclusion) THEN
                minotonCount = minotonCount + 1
            ELSE
                inclusionsNumber = inclusionsNumber + 1
                currentInclusion = snowDepthData_old(2, k)
                minotonCount = 1
            ENDIF
            IF (minotonCount > minotonsNumber) minotonsNumber = minotonCount
        ENDDO

        ALLOCATE(inclusionsRho(inclusionsNumber, minotonsNumber), stat = errorCode)
        IF(errorCode /= 0) THEN
            errorMsg = "inclusionsRho"
            smfe = ALLOCATE_ERROR
            RETURN
        ENDIF

        inclusionsRho = -1.0

        ALLOCATE(inclusionsTempMode(inclusionsNumber), stat = errorCode)
        IF(errorCode /= 0) THEN
            errorMsg = "inclusionsTempMode"
            smfe = ALLOCATE_ERROR
            RETURN
        ENDIF

        i = 0
        j = 0
        currentInclusion = -1.0 ! By tempMode
        DO k = 1, snowDepth_old
            IF (snowDepthData_old(2, k) == currentInclusion) THEN
                j = j + 1
            ELSE
                i = i + 1
                j = 1
                currentInclusion = snowDepthData_old(2, k)
                inclusionsTempMode(i) = snowDepthData_old(2, k)
            ENDIF
            inclusionsRho(i, j) = snowDepthData_old(1, k)
        ENDDO

        DO t = 1, deltaSnow
            iSave = -1
            DO i = 1, inclusionsNumber
                minotonCount = 0
                DO j = 1, minotonsNumber
                    IF (inclusionsRho(i, j) > -1.0) THEN
                        minotonCount = minotonCount + 1
                    ENDIF
                ENDDO

                IF (minotonCount > 0) THEN
                    ALLOCATE(minoton(minotonCount), stat = errorCode)
                    IF (errorCode /= 0) THEN
                        errorMsg = "moniton"
                        smfe = ALLOCATE_ERROR
                        RETURN
                    ENDIF

                    k = 0
                    DO j = 1, minotonsNumber
                        IF (inclusionsRho(i, j) > -1.0) THEN
                            k = k + 1
                            minoton(k) = inclusionsRho(i, j)
                        ENDIF
                    ENDDO

                    median = density_median(minoton, minotonCount)
                    IF ((iSave == -1).or.(medianSave > median)) THEN
                        iSave = i
                        medianSave = median
                    ENDIF

                    DEALLOCATE(minoton)
                ENDIF
            ENDDO

            IF (iSave == -1) exit

            jSave = -1
            minotonCount = 0
            DO j = 1, minotonsNumber
                IF (inclusionsRho(iSave, j) > -1.0) THEN
                    IF ((jSave == -1).or.(inclusionsRho(iSave, j) < rhoSave)) THEN
                        jSave = j
                        rhoSave = inclusionsRho(iSave, j)
                    ENDIF
                    minotonCount = minotonCount + 1
                ENDIF
            ENDDO

            inclusionsRho(iSave, jSave) = -1.0

            IF (minotonCount > 1) THEN
                DO j = 1, minotonsNumber
                    IF (inclusionsRho(iSave, j) > 0.0) THEN
                        inclusionsRho(iSave, j) = inclusionsRho(iSave, j) + rhoSave / (minotonCount - 1)
                        IF (inclusionsRho(iSave, j) > RHO_FIRN ) THEN
                            inclusionsRho(iSave, j) = RHO_FIRN
                        ENDIF
                    ENDIF
                ENDDO
            ELSE
                ! Zero the value
            ENDIF
        ENDDO

        k = 0
        DO i = 1, inclusionsNumber
            DO j = 1, minotonsNumber
                IF (inclusionsRho(i, j) /= -1.0) THEN
                    k = k + 1
                    snowDepthData_new(1, k) = inclusionsRho(i, j)
                    snowDepthData_new(2, k) = inclusionsTempMode(i)
                ENDIF
            ENDDO
        ENDDO

        DEALLOCATE(inclusionsRho, inclusionsTempMode)

        addDensity = 0.0
        DO i = 1, deltaSnow
            addDensity = addDensity + snowDepthData_old(1, i)
        ENDDO
        addDensity = addDensity / float(snowDepth_new)

        DO i = 1, snowDepth_new
            snowDepthData_new(1, i) = snowDepthData_old(1, i + deltaSnow) + addDensity
            snowDepthData_new(2, i) = snowDepthData_old(2, i + deltaSnow)
        ENDDO

        RETURN
    ENDSUBROUTINE

    SUBROUTINE section_snowDecreaseDueToMelting
    !-------------------------------------------------------------------------------------------------------------------------------
    ! Snow decrease due to melting (maxDayAirT > 0)
    !-------------------------------------------------------------------------------------------------------------------------------
        REAL :: addDensity                    ! Additional density to an element .When there is case of monoton snow column (case 7022)
        REAL :: water_mass, water_volume      ! Amount of water moved to 1 element (mass and volume)

        addDensity = 0.0
        DO i = 1, deltaSnow
            addDensity = addDensity + snowDepthData_old(1, i)
        ENDDO

        addDensity = addDensity * SH_HEIGHT * SLOPE_PARAM ! Water (in kg/m2)

        water_mass = addDensity / snowDepth_new ! Amount of water moved to 1 element
        water_volume = water_mass / RHO_WATER

        DO i = 1, snowDepth_new  ! Cycle for the elements of the snow column
            snowDepthData_new(1, i) = snowDepthData_old(1, i + deltaSnow) * (ELEMENT_VOLUME - water_volume) / ELEMENT_VOLUME + &
                RHO_WATER * water_volume / ELEMENT_VOLUME
            snowDepthData_new(2, i) = snowDepthData_old(2, i + deltaSnow)
        ENDDO

        ! Precipitation
        DO i = 1, snowDepth_new ! Cycle for the elements of the snow column
            snowDepthData_new(1, i) = snowDepthData_new(1, i) + p24Sum * 0.5 / (snowDepth_new * SH_HEIGHT) ! 0.5 - half of water is removed
        ENDDO

        RETURN
    ENDSUBROUTINE

ENDFUNCTION
