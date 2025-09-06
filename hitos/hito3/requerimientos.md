# Documentación del Proyecto - Hito 3

## Requerimiento 1

Para poblar la base de datos, primero se genera un archivo JSON con la información a volcar dentro de la tabla, dependiendo de los campos del modelo. Este archivo se guarda dentro de una carpeta llamada `fixtures` dentro de la app. Una vez se tiene el archivo preparado, se ejecuta el siguiente comando utilizando `loaddata` para volcar el archivo JSON dentro de la base de datos. En este caso, el comando para las regiones y comunas es:

```bash
docker-compose exec web python manage.py loaddata locations/fixtures/comunas_regiones.json
```

Se realiza el mismo procedimiento con los inmuebles. Sin embargo, los inmuebles requieren de un propietario, por lo tanto primero se generan 10 usuarios del tipo arrendador. De igual manera, se genera la carpeta `fixtures` dentro de la app `users` con el archivo `usuarios.json` y se ejecuta:

```bash
docker-compose exec web python manage.py loaddata users/fixtures/usuarios.json
```

Con los usuarios creados, es posible crear los inmuebles utilizando los datos de los arrendadores. De igual forma, se crea la carpeta `fixtures` dentro de la app y se genera el archivo `inmuebles.json`. Acto seguido, se vuelca la información con:

```bash
docker-compose exec web python manage.py loaddata portal/fixtures/inmuebles.json
```

## Requerimiento 2

* Para obtener un listado de inmuebles para arriendo separado por comunas, usando solo los campos `nombre` y `descripcion` en un script Python que se conecta a la DB usando Django y SQL, guardando los resultados en un archivo de texto, se debe definir primero la query a la base de datos. En este caso, la query es:

```sql
SELECT c.nombre AS comuna, i.nombre AS inmueble, i.descripcion
FROM portal_inmueble i
JOIN locations_comuna c ON i.comuna_id = c.id
WHERE i.arrendado = FALSE
ORDER BY c.nombre;
```

* Acto seguido, se crea el archivo `consulta_db.py` con la configuración necesaria para conectarse a la base de datos y posteriormente volcar el resultado de la query en un archivo `.txt`, configurando el formateo línea por línea. Finalmente, se ejecuta el script y se obtiene el archivo `inmuebles_para_arriendo.txt`.

## Requerimiento 3

* Para obtener un listado de inmuebles para arriendo separado por regiones en un script Python que se conecta a la DB usando Django y SQL, guardando los resultados en un archivo de texto, se procede de igual manera que en el requerimiento anterior. La diferencia radica en la query, que para este caso es:

```sql
SELECT r.nombre AS region, i.nombre AS inmueble, i.descripcion
FROM portal_inmueble i
JOIN locations_comuna c ON i.comuna_id = c.id
JOIN locations_region r ON c.region_id = r.id
WHERE i.arrendado = FALSE
ORDER BY r.nombre, i.nombre;
```

* Los archivos se encuentran adjuntos con los nombres: `consulta_db.py`, `consulta_db_2.py`, `inmuebles_para_arriendo.txt` e `inmuebles_para_arriendo2.txt`.
