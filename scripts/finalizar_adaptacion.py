from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
questions=[
('¿Qué describe un algoritmo?', ['Una secuencia de pasos para resolver un problema','Una marca de procesador','Una dirección de memoria','Un tipo de monitor'],0),
('¿Qué caracteriza a un arreglo?', ['Solo almacena instrucciones','Organiza elementos accesibles por índice','No permite recorrer datos','Siempre tiene un único elemento'],1),
('¿Qué expresa una dependencia de datos?', ['La cantidad de colores de una interfaz','El nombre de una variable','Una operación necesita un resultado de otra','La velocidad nominal de la red'],2),
('¿Qué significa ejecutar tareas en paralelo?', ['Ejecutarlas siempre una después de otra','Eliminar todas las variables','Usar un solo hilo obligatoriamente','Realizar trabajo simultáneo en varios recursos'],3),
('¿Qué es un hilo?', ['Una unidad de ejecución dentro de un proceso','Un archivo de imagen','Una memoria externa','Un protocolo de correo'],0),
('¿Cuándo puede aparecer una condición de carrera?', ['Al leer una constante','Al acceder sin coordinación a un estado compartido con escrituras','Al documentar un algoritmo','Al ejecutar tareas independientes sin estado compartido'],1),
('¿Qué busca la exclusión mutua?', ['Aumentar el tamaño del arreglo','Eliminar la memoria','Evitar accesos simultáneos a una sección crítica','Duplicar cada proceso'],2),
('¿Cómo colaboran procesos con memoria distribuida?', ['Compartiendo siempre todas las variables','Sin intercambiar información nunca','Mediante un único registro de CPU','Intercambiando mensajes'],3),
('Si T(1)=100 s y T(4)=40 s, ¿cuál es la aceleración?', ['2.5','4','40','0.4'],0),
('¿Cuál es la eficiencia si S(4)=3?', ['12','0.75','7','3'],1),
('¿Qué debe comprobarse al paralelizar un programa?', ['Solo el número de líneas','Solo el color del editor','La corrección de los resultados y el rendimiento','Solo el nombre del archivo'],2),
('¿Qué representa una arista de un grafo de tareas?', ['Una licencia de software','El tamaño de pantalla','Una tecla del equipo','Una relación o dependencia entre tareas'],3)]
p=R/'assets/data/examen-diagnostico.json'
d=json.loads(p.read_text(encoding='utf-8'))
d['descripcion']='Diagnóstico provisional de algoritmos, memoria y conceptos introductorios de cómputo paralelo. Pendiente de validación.'
d['preguntas']=[dict(id=f'diag-par-{i:02}',numero=i,tipo='opcion-multiple',enunciado=q,obligatoria=True,opciones=[dict(id=chr(97+k),texto=o) for k,o in enumerate(opts)],respuestaCorrecta=chr(97+answer)) for i,(q,opts,answer) in enumerate(questions,1)]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
p=R/'assets/data/autores.json'; d=json.loads(p.read_text(encoding='utf-8'))
d['titulo']='Créditos del proyecto base y colaboradores'
for section in d['secciones']:
    section['descripcion']='Créditos conservados del proyecto base. La autoría y revisión del contenido de Cómputo Paralelo están pendientes de confirmación.'
    if section['id']=='docentes': section['titulo']='Equipo del proyecto base'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
for path,old,new in [('assets/js/unidades-ui.js','polilibro-acr:preferencias','polilibro-paralelo:preferencias'),('assets/js/plan-estudios-modal.js','Plan_de_marketing_Plan_Estudios.pdf','Computo_Paralelo_Programa_Academico.pdf')]:
    p=R/path;p.write_text(p.read_text(encoding='utf-8').replace(old,new),encoding='utf-8')
# Las biografías originales se conservan literalmente, sin atribuirles la nueva materia.
source=R.parent/'Libro-App-Com-Red/assets/data/autores.json'
original=json.loads(source.read_text(encoding='utf-8-sig'))
p=R/'assets/data/autores.json';d=json.loads(p.read_text(encoding='utf-8'))
for section,base in zip(d['secciones'],original['secciones']):section['personas']=base['personas']
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
