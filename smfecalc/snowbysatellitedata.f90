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

LOGICAL FUNCTION snowBySatelliteData(n)

    USE mod_settings
    USE mod_commondata

    IMPLICIT NONE

    INTEGER, INTENT(IN) :: n
    REAL, PARAMETER :: a = 1852.0 * 60.0
    INTEGER :: k, i
    INTEGER :: p_lon, p_lat
    REAL :: r_min, r, r_lon, r_lat

    IF (satelliteDataExist == .false.) THEN
        snowBySatelliteData = .false.
        RETURN
    ENDIF

    IF (satelliteDataCount == pointsCount) THEN
        k = n
    ELSE
        p_lon = data_lon(n) * a * cosd(data_lat(n))
        p_lat = data_lat(n) * a

        r_min = huge(r_min)
        DO i = 1, data_count
            r_lon = p_lon - data_satelliteData(1, i) * a * cosd(data_satelliteData(2, i))
            r_lat = p_lat - data_satelliteData(2, i) * a
            r = sqrt(r_lon**2 + r_lat**2)
            IF (r < r_min) THEN
                r_min = r
                k = i
            ENDIF
        ENDDO
    ENDIF

    snowBySatelliteData = (data_satelliteData(3, k) /= 0.0)
    RETURN
ENDFUNCTION