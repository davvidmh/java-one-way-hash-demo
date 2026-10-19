# Prueba de ida y vuelta: Java, GPT4Free y Oracle

Este experimento comprueba un recorrido concreto: tarea pública y específica → cola privada en Oracle → worker de consola en Oracle → GPT4Free → recepción del código → revisión → compilación/pruebas en Oracle → paquete comprimido → devolución por SSH → publicación sanitizada.

**Contexto general del proyecto:** [Cerebro: procedimientos de orquestación](https://github.com/davvidmh/cerebro-procedures).

## Resultado comprobado

- El worker se ejecutó en Oracle Linux ARM64, usando GPT4Free 8.7.7 y el adaptador LLM7, con modelo solicitado `default`.
- No se suministraron claves de proveedores ni cookies personales. Solo se envió la tarea pública de este ejemplo.
- El proveedor no acreditó la identidad exacta del modelo subyacente. No atribuimos el resultado a una marca o modelo concreto.
- TeachAnything falló con estado HTTP 403 desde Oracle. LLM7 devolvió el programa y el resultado quedó completado en la cola.
- El código se revisó antes de ejecutar. Solo se retiraron las marcas de bloque Markdown de la respuesta original; el cuerpo Java no se reescribió.
- La compilación y las seis comprobaciones de entradas se realizaron en Oracle con Java 17, como usuario de servicio sin privilegios, sin red y con límites de memoria. La devolución por SSH tiene sus huellas comprobadas en el equipo receptor.
- El archivo recibido ocupa 4.365 bytes. La respuesta original, los recibos y las comprobaciones están en `evidence/` y en `oracle-java-return.zip`.

Los intentos iniciales efectuados por error desde el equipo cliente no son evidencia del recorrido de Oracle. Fallaron y no produjeron el código publicado. El único origen del programa de esta entrega es la respuesta LLM7 obtenida por el worker en Oracle.

## Programa

`OneWayHash.java` transforma texto UTF-8 en un resumen SHA-256, representado por 64 caracteres hexadecimales. Sin argumentos usa `hola`; con varios argumentos los une mediante espacios.

```sh
javac -encoding UTF-8 --release 17 -d build OneWayHash.java
java -cp build OneWayHash
java -cp build OneWayHash hola
```

Crear primero `build` si la herramienta de compilación lo necesita. No se requieren dependencias externas de Java. Para repetir las comprobaciones: `python verify.py` en un entorno con Python y las herramientas de Java disponibles.

## Trasfondo: función no inyectiva y privacidad

El objetivo educativo fue representar una transformación de una vía. **Un hash no es cifrado reversible:** no hay una clave de descifrado que recupere el mensaje.

Las salidas SHA-256 tienen 256 bits; hay muchas más entradas posibles que salidas. Por ello la transformación no es inyectiva en el conjunto general de mensajes y no admite una inversa única que recupere todas las entradas originales. Esto no demuestra, por sí solo, resistencia computacional: encontrar una preimagen o una colisión es un problema distinto de demostrar que existen colisiones.

Tampoco implica que una entrada corta quede oculta. La prueba compara el hash con los de cuatro palabras y reconoce `hola`. Es adivinación por candidatos, no descifrado ni ruptura de SHA-256. Esta demostración no sirve como almacenamiento de contraseñas, como cifrado de paquetes o como protección de propiedad intelectual que después deba recuperarse.

El programa no demuestra la existencia de una colisión concreta de SHA-256 ni afirma que el resumen identifique un mensaje original único. Para paquetes recuperables se necesitaría cifrado autenticado y custodia de claves, un trabajo separado.

Fuentes: [MessageDigest de Java 17](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/security/MessageDigest.html), [estándar SHA del NIST](https://csrc.nist.gov/pubs/fips/180-4/upd1/final).

## Alcance y limitaciones

Este piloto demuestra generación externa, validación y transferencia de una tarea pública. No demuestra una colmena autónoma completa, aislamiento de todos los workers ni confidencialidad frente al proveedor que procesa una petición. No expone direcciones, claves, configuración real o conversaciones privadas de la infraestructura.

La respuesta incluyó bloques Markdown y omitió el comentario explicativo solicitado dentro del código. La revisión humana añadió la explicación aquí y conservó la respuesta original para poder comprobar qué entregó realmente el proveedor.
