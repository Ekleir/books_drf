# books_drf
Work with DRF <br>
<ul>
  <li>Подключаю PostgreSQL вместо SQLite.</li>
  <li>Создаю несколько моделей, одну из них использую для ManyToMany, вместо автоматического создания в БД.</li>
  <li>Для модели Book создаю UserBookRelation, чтобы перенести логику взаимодействия User с Book в отдельную таблицу.</li>
  <li>Задаю логику обработки json в ModelSerializer.</li>
  <li>Использую классы DRF вместо функций во view.</li>
  <li>Вместо стандарного urls-файла использую SimpleRouter.</li>
  <li>Дополняю логику работу с endpoint с помощию фильтров, поиска, permission_classes.</li>
  <li>Меняю логику запросов SQL к БД через annotate(select_related,prefetch_related), чтобы уменьшить количество запросов к БД.</li>
  <li>Добавлена авторизация через Git.</li>
  <li>Тесты для GET, POST, PUT, PATCH запросов, сериализатора.</li>
</ul>

