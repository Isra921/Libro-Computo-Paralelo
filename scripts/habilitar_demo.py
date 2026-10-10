from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding='utf-8'))
def save(p,d):(R/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for i in range(1,6):
 p=f'assets/data/unidades/unidad-{i:02}.json';u=load(p)
 for t in u['temas']:
  if t['numero']!='1.1':
   t['url']='';t['actividad']['url']=''
 if i!=1:u['actividad_final']['url']='';u['actividad_final']['descripcion']='Próximamente. Actividad pendiente de validación académica.'
 save(p,u)
p='assets/data/actividades.json';d=load(p)
allowed={'unidades/unidad-01/actividades/actividad-1-1.html','unidades/unidad-01/actividades/actividad-final.html'}
for s in d['secciones']:
 for item in s['items']:
  if item['url'] not in allowed:item['url']='';item['descripcion']='Próximamente. Contenido pendiente de validación académica.'
  elif not item['destacada']:item.update(reactivos='10 preguntas',tiempo='10 min',descripcion='Ejemplo interactivo con retroalimentación e intentos ilimitados.')
save(p,d)
# Las rutas directas también muestran el estado pendiente.
for p in (R/'unidades').glob('*/**/*.html'):
 if p.parent.name not in {'temas','actividades'}:continue
 rel=p.relative_to(R).as_posix()
 if rel in allowed or rel=='unidades/unidad-01/temas/tema-01-01.html':continue
 uid=p.relative_to(R).parts[1]
 p.write_text(f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Próximamente | Cómputo Paralelo</title><link rel="stylesheet" href="../../../assets/css/comun.css"><link rel="stylesheet" href="../../../assets/css/unidades-base.css"></head><body class="u-body" data-root="../../../" data-unidad="{uid}"><header class="site-nav" data-componente="navegacion"></header><main class="u-page"><section class="u-hero"><div><p class="u-eyebrow">Contenido pendiente</p><h1>Próximamente</h1><p>Este contenido está bloqueado mientras se recibe la versión validada. Puedes probar el tema 1.1, su actividad y la actividad final de la unidad I.</p><a class="u-btn u-btn--primary" href="../index.html">Volver a la unidad</a> <a class="u-btn" href="../../unidad-01/temas/tema-01-01.html">Ver tema de prueba 1.1</a></div></section></main><script src="../../../assets/js/data-manager.js"></script><script src="../../../assets/js/componentes.js"></script></body></html>''',encoding='utf-8')
source=R.parent/'Libro-App-Com-Red/unidades/unidad-01/actividades/actividad-1-1.html'
s=source.read_text(encoding='utf-8-sig').replace('Aplicaciones para Comunicaciones en Red','Cómputo Paralelo').replace('Servicios definidos en la capa de transporte','Motivación, bases y alcances del cómputo paralelo').replace('comunicación de proceso a proceso, multiplexación y demultiplexación por puertos, control de flujo y control de congestión','concurrencia, paralelismo, hilos, comunicación y corrección de programas').replace('arquitectura en capas','computación paralela')
s=s.replace('<h1 class="a-title">','<p class="u-eyebrow">Ejemplo provisional · Pendiente de validación</p><h1 class="a-title">')
(R/'unidades/unidad-01/actividades/actividad-1-1.html').write_text(s,encoding='utf-8')
qs=[('¿Qué distingue al paralelismo?', ['La ejecución simultánea de trabajo en varios recursos','La ejecución obligatoria en un solo núcleo','La ausencia de tareas'],0),('¿La concurrencia requiere ejecución simultánea?', ['Sí, siempre','No; las tareas pueden alternar su avance','Solo cuando no hay memoria'],1),('¿Qué es un hilo?', ['Un archivo','Una unidad de ejecución dentro de un proceso','Una red física'],1),('¿Qué permite la comunicación entre procesos?', ['Intercambiar datos y coordinar trabajo','Eliminar dependencias automáticamente','Garantizar aceleración ilimitada'],0),('¿Qué debe conservar una versión paralela?', ['El mismo número de líneas','La corrección de los resultados','La misma duración'],1),('¿Qué puede provocar una condición de carrera?', ['Leer una constante','Actualizar un dato compartido sin coordinación','Dividir tareas independientes'],1),('¿Qué describe un sistema distribuido?', ['Componentes en distintos nodos que se comunican','Un único registro','Una secuencia sin comunicación'],0),('¿Qué limita el paralelismo de una tarea?', ['Las dependencias entre operaciones','El nombre del archivo','El color de la pantalla'],0),('¿Qué significa sincronizar tareas?', ['Coordinar su avance o acceso a recursos','Duplicar todos los datos','Eliminar todos los hilos'],0),('¿Qué conviene hacer antes de paralelizar?', ['Agregar hilos sin analizar','Identificar tareas, dependencias y resultados esperados','Cambiar únicamente el lenguaje'],1)]
save('assets/data/unidad-1/preguntas_1.1.json',[dict(type='opcion_multiple',question=q,options=opts,answer=opts[a],explicacion=opts[a]+'. Este principio ayuda a diseñar programas paralelos correctos.') for q,opts,a in qs])
p=R/'assets/js/paginas/actividad-plantilla.js';s=p.read_text(encoding='utf-8').replace('| Marketing','| Cómputo Paralelo').replace("'resultadoActividad:'","'computo-paralelo:resultadoActividad:'");p.write_text(s,encoding='utf-8')
p=R/'index.html';s=p.read_text(encoding='utf-8').replace('Cada tema incluye una lectura y una actividad de muestra para preparar la futura incorporación del contenido validado.','Solo están habilitados el tema 1.1, su actividad interactiva y la actividad final de la unidad I como ejemplos de prueba. El resto está pendiente de validación.');p.write_text(s,encoding='utf-8')
