# Technical documentation for SnoWE model

### Authors:
<p align="justify">
Чурюлин Е.<sup>1</sup>, Копейкин В.<sup>1</sup>, Розинкина И.<sup>1</sup>, Чумаков М.<sup>2</sup>, Казакова Е.<sup>1</sup>
</p>

1 - ФГБУ «Гидрометцентр России», 2 – ОАО «Газпром»
  
Москва, 2020
  
### Содержание документации:
  
1. Общие представления о модели снежного покрова SnoWE
2. Запуск и начало работы с моделью снежного покрова SnoWE
    1. Сборка модели снежного покрова SnoWE
3. Модуль препроцессинга модели SnoWE
    1. Константные конфигурационные файлы
    2. Спутниковые данные о границе снежного покрова
    3. Загрузка начальных данных о метеорологических параметрах на основе синоптической информации
    4. Загрузка начальных данных о метеорологических параметрах на основе модельной информации
    5. Контроль качества загруженных данных
4. Модуль основного расчетного ядра модели SnoWE
    1. Физические параметризации расчетного ядра SMFE
        1. Первое расчетное направление – свежевыпавший снег
        2. Второе расчетное направление – высота снежного покрова не изменилась
        3. Третье расчетное направление – высота снежного покрова увеличилась  из-за выпадения влажного снега
        4. Четвертое расчетное направление – высота снежного покрова увеличилась  из-за выпадения сухого снега
        5. Пятое расчетное направление – высота снежного покрова уменьшилась  из-за воздействия ветра
        6. Шестое расчетное направление – высота снежного покрова уменьшилась  из-за его уплотненияж
        7. Седьмое расчетное направление – высота снежного покрова уменьшилась  из-за его таяния
5. Модуль постпроцессинга модели снежного покрова SnoWE
6. Блок визуализации результатов
7. Архивная версия модели
8. Дальнейшее развитие
9. Заключение
10. Список литературы
11. Приложение
