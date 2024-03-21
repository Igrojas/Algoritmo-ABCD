# Algoritmo-ABCD

Creación del grafo: El algoritmo comienza creando un grafo a partir de los datos de entrada. Los datos de entrada representan una red de colaboración entre autores, donde los nodos son autores y las aristas representan la colaboración entre ellos. El grafo se crea considerando ciertos criterios de poda, como el número mínimo de artículos que debe tener un autor principal y el número mínimo de artículos que debe tener un coautor para ser considerado relevante.

Inicialización de nodos y aristas: Se inicializan los nodos y las aristas del grafo con valores predeterminados.

Iteración entre comunidades: El algoritmo itera entre las comunidades dentro del grafo hasta que no se produzcan cambios significativos en la estructura de la comunidad. Esto se hace mediante un bucle while que se repite hasta que se cumpla una condición de salida.

Cálculo de pesos y promedios: En cada iteración, el algoritmo calcula el peso de las aristas y el peso promedio de los nodos dentro de las comunidades.

Unión de comunidades: El algoritmo considera fusionar dos comunidades si la unión de sus nodos produce una mejora significativa en el peso promedio de la comunidad resultante.

Actualización de estructuras de datos: Si se encuentra una mejora, el algoritmo actualiza las estructuras de datos que representan las comunidades y las aristas del grafo.

Salida de resultados: Una vez que se alcanza la condición de salida del bucle while, el algoritmo devuelve las comunidades encontradas en el grafo.

En resumen, este algoritmo busca identificar y agrupar comunidades dentro de una red de colaboración entre autores, optimizando la estructura de la comunidad para mejorar la colaboración y la cohesión dentro de cada grupo de autores.

DOI: 10.1016/j.procs.2014.05.248
