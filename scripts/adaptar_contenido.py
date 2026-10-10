"""Genera la edición provisional conservando las plantillas del proyecto base."""
from pathlib import Path
import json, re, html

ROOT = Path(__file__).resolve().parents[1]
def read(p): return (ROOT / p).read_text(encoding='utf-8-sig')
def write(p, s):
    p = ROOT / p
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding='utf-8')
def data(p): return json.loads(read(p))
def save(p, obj): write(p, json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
NOTICE = 'Contenido de muestra pendiente de validación académica. Los títulos y la organización se basan en el programa proporcionado; los desarrollos y ejercicios son provisionales.'

# Títulos, subtemas y horas del programa entregado por el usuario.
units = [
('Acercamiento al cómputo paralelo', 'Describe los tipos de arquitectura paralela con base en sus alcances, características y aplicaciones.', 6, 0, 2, [
('Motivación, bases y alcances del cómputo paralelo: características', 'Comunicación entre procesos|Programas concurrentes, paralelos y distribuidos|Hilos|Exactitud de los programas concurrentes|Sistemas distribuidos', 'El paralelismo permite repartir trabajo entre varias unidades de procesamiento. La concurrencia describe tareas cuyo avance se solapa; su ejecución no tiene que ser simultánea. Antes de acelerar un programa, se deben reconocer sus dependencias y comprobar sus resultados.'),
('Arquitecturas de computadoras paralelas', 'Procesadores multinúcleo|Arreglos de procesadores|Computadoras multiprocesadores|Clusters|Computadoras de arquitecturas no convencionales|Redes de interconexión', 'Una arquitectura paralela combina recursos de procesamiento, memoria y comunicación. Un equipo multinúcleo y un cluster pueden resolver problemas similares, pero tienen distintos costos de acceso a datos y coordinación.'),
('Taxonomía de Flynn', 'Instrucción única, flujo de datos único (SISD)|Instrucción única, flujo de datos múltiple (SIMD)|Instrucciones múltiples, flujo de datos único (MISD)|Instrucciones múltiples, flujo de datos múltiple (MIMD)|Aplicaciones', 'La taxonomía de Flynn clasifica arquitecturas según los flujos de instrucciones y datos. SIMD aplica una misma operación a varios datos, mientras que MIMD permite que distintas unidades ejecuten instrucciones diferentes.'),
('Modelos de cómputo paralelo', 'Modelos de memoria compartida|Modelos de interconexión de red, memoria distribuida o paso de mensajes|Modelo de flujo de datos|Aplicaciones', 'El modelo de programación define cómo se expresa la colaboración entre tareas. En memoria compartida se coordinan accesos a datos comunes; en memoria distribuida se intercambian mensajes; en flujo de datos la disponibilidad de entradas determina la ejecución.')]),
('Diseño y análisis de programas paralelos', 'Distingue el diseño de algoritmos paralelos a partir de los tipos de paralelización, el método de Foster y su análisis de rendimiento.', 12, 6, 4, [
('Clases de problemas solucionables usando cómputo paralelo', 'Tareas paralelizables', 'Una tarea es candidata a ejecución paralela cuando sus dependencias permiten realizar parte del trabajo de forma independiente. Sumar bloques de un arreglo ilustra una descomposición: cada bloque produce un resultado parcial y después se combinan los resultados.'),
('Tipos de paralelización', 'Paralelización funcional|Paralelización de datos|Paralelización recursiva|Paralelización exploratoria|Paralelización especulativa', 'La paralelización de datos distribuye conjuntos de elementos entre trabajadores. La funcional separa operaciones distintas. Las estrategias recursivas, exploratorias y especulativas permiten organizar otros problemas, con costos y restricciones propios.'),
('Diseño de algoritmos paralelos', 'Descomposición del problema|Granularidad de la computación|Minimización de costos del algoritmo paralelo|Asignación de tareas a las unidades de procesamiento', 'La granularidad representa el tamaño del trabajo de cada tarea. Muchas tareas pequeñas pueden mejorar el reparto, pero aumentar la coordinación. El diseño debe equilibrar trabajo útil, comunicación y sincronización.'),
('Método Foster', 'Particionamiento|Comunicación|Aglomeración|Mapeo', 'El método de Foster organiza el diseño en cuatro etapas: particionar el problema, identificar comunicaciones, agrupar tareas y asignarlas a los recursos. Separar estas decisiones ayuda a comparar alternativas antes de implementar.'),
('Análisis de rendimiento para programas paralelos', 'Métricas de desempeño|Escalabilidad de los sistemas paralelos|Función de isoeficiencia|Ley de Amdahl|Ley de Gustafson-Barsis|Métrica de Karp-Flatt', 'La aceleración se calcula como S(p) = T(1) / T(p), y la eficiencia como E(p) = S(p) / p. Por ejemplo, 80 segundos en un procesador y 25 en cuatro producen una aceleración de 3.2 y eficiencia de 0.8. Las mediciones deben comparar el mismo problema y condiciones equivalentes.')]),
('Programación paralela en sistemas de memoria compartida', 'Elabora programas paralelos con base en las políticas y la memoria compartida.', 12, 7, 4, [
('Cómputo paralelo usando memoria compartida', 'Arquitecturas multinúcleo y multisocket|Modelos de memoria compartida', 'Los trabajadores pueden acceder a un espacio de direcciones compartido. Esta facilidad exige coordinar las escrituras: dos hilos que actualizan un contador sin protección pueden perder incrementos.'),
('Caché', 'Número de cachés|Tamaños de caché|Mapeo de bloques de memoria a bloques de caché', 'La caché conserva datos próximos al procesador para reducir el costo de acceso. La localidad temporal y espacial influye en el rendimiento. Un recorrido contiguo de un arreglo puede aprovechar mejor cada bloque transferido.'),
('Política de escritura', 'Política write-through|Política write-back', 'Write-through propaga las escrituras al siguiente nivel de memoria. Write-back puede aplazarlas hasta que se reemplace un bloque modificado. Estas políticas implican distintos costos de tráfico y gestión.'),
('Coherencia de caché', 'Protocolos snooping|Protocolos basados en directorio', 'La coherencia coordina las copias de una misma ubicación de memoria en varias cachés. Los mecanismos de observación del tráfico y los directorios son enfoques para controlar qué copias permanecen válidas.'),
('Consistencia de memoria', 'Consistencia secuencial', 'La consistencia define qué órdenes de lectura y escritura pueden observar los hilos. En consistencia secuencial, el resultado equivale a un orden global que respeta el orden de cada hilo.'),
('Interfaces de programación de aplicaciones y lenguajes de programación', '', 'Las interfaces de programación permiten expresar regiones paralelas, repartir iteraciones y sincronizar trabajadores. Como ejemplo provisional, una reducción combina resultados locales para evitar que todos escriban simultáneamente en un acumulador compartido.')]),
('Programación paralela en sistemas distribuidos', 'Elabora programas paralelos con base en las políticas y la memoria distribuida.', 12, 7, 4, [
('Cómputo paralelo usando memoria distribuida', 'Arquitecturas de red|Arquitectura de memoria distribuida con acoplamiento fuerte y débil|Arquitectura de memoria distribuida con acoplamiento bajo', 'Cada proceso dispone de memoria local y comunica los datos que necesitan otros procesos. Una suma distribuida divide el arreglo, calcula sumas locales y combina sus resultados mediante comunicación.'),
('Ruteo', 'Algoritmos de ruteo para transmisión y multitransmisión|Algoritmos de estancamiento y ruteo', 'El ruteo decide por dónde viaja la información entre nodos. La topología y las rutas afectan la latencia, la congestión y la posibilidad de bloqueo. Una comunicación colectiva puede requerir varios pasos.'),
('Conmutación', 'Conmutación de conexión|Conmutación de paquetes', 'La conmutación organiza el uso de enlaces para transferir información. Reservar una conexión y dividir un mensaje en paquetes son estrategias distintas, con efectos sobre el establecimiento, el almacenamiento y la utilización de recursos.'),
('APIs y lenguajes de programación', '', 'Las interfaces de paso de mensajes ofrecen operaciones para enviar, recibir y combinar datos. El diseño debe hacer coincidir participantes, tipos de datos y orden de operaciones para evitar esperas que impidan avanzar.')]),
('Programación basada en el flujo de datos', 'Elabora programas paralelos con base en principios de aceleradores paralelos y procesadores de flujo.', 12, 7, 4, [
('Cómputo paralelo usando flujos de datos', '', 'Un grafo de flujo de datos representa operaciones y dependencias. Una operación puede comenzar cuando están disponibles sus entradas. Las ramas independientes del grafo revelan oportunidades de paralelismo.'),
('Aceleradores paralelos', 'Principios|Características|Aplicaciones', 'Un acelerador ejecuta determinadas clases de trabajo con muchos recursos paralelos. La aceleración total depende también del movimiento de datos y de la parte del programa que permanece en el procesador anfitrión.'),
('Procesadores de flujo', '', 'Los procesadores de flujo aplican operaciones a secuencias de elementos. Agrupar trabajo regular y aprovechar la localidad de datos ayuda a mantener ocupadas las unidades de ejecución.'),
('APIs y lenguajes de programación', '', 'Una interfaz para aceleradores permite preparar datos, lanzar operaciones y recuperar resultados. El ejemplo didáctico propuesto compara una transformación de un arreglo con su versión secuencial y registra el tiempo completo, incluidas las transferencias.')])]
romans = ['I','II','III','IV','V']

for p in ROOT.rglob('*'):
    if p.suffix in {'.html','.css','.js','.json','.md'} and 'scripts' not in p.parts:
        s = p.read_text(encoding='utf-8-sig')
        s = re.sub(r'Aplicaciones para Comunicaciones en\s+Red', 'Cómputo Paralelo', s)
        p.write_text(s, encoding='utf-8')

unit_template = read('unidades/unidad-01/index.html')
topic_template = read('unidades/unidad-01/temas/tema-01-01.html')
plan = data('assets/data/plan-estudios.json')
general = plan['datos_generales']
general.update(unidad_academica='UPIIC · ESCOM · UPIIT', programa_academico='Ingeniería en Inteligencia Artificial', vigencia='Agosto 2022', creditos_satca='6.0', horas_autonomo_semestre='18.0 h', plan_estudios='(vigente desde agosto de 2022)')
plan.update(archivo_pdf='assets/docs/computoParalelo_IIA2020.pdf', proposito='Diseña aplicaciones paralelas con base en el cómputo paralelo.', intencion_educativa='Desarrollo de habilidades técnicas de diseño, implementación y evaluación de algoritmos paralelos para problemas que requieren soluciones de alto desempeño; trabajo colaborativo, comunicación asertiva y toma de decisiones con responsabilidad y ética. Antecedente: Algoritmos y Estructuras de Datos.', orientacion_didactica={'metodos_ensenanza':'Inductivo, deductivo y analógico','estrategias_aprendizaje':'Aprendizaje basado en problemas y aprendizaje autónomo'}, unidades_tematicas=[], practicas=[], evaluacion=['Evaluación diagnóstica y saberes previamente adquiridos.', 'Portafolio de evidencias: organizadores gráficos, ejercicios y problemas resueltos.', 'Programas funcionando según requerimientos y reportes de prácticas.', 'Evaluaciones escritas.'], bibliografia=[], recursos_digitales=[])
for author, year, title, publisher, isbn in [
('Czech, J.',2016,'Introduction to parallel computing','Cambridge University Press','9781107174399'),
('Grama, A., Kumar, V., Gupta, A. y Karypis, G.',2003,'Introduction to Parallel Computing','Addison-Wesley','0201648652'),
('Pacheco, P.',2011,'An Introduction to Parallel Computing','Morgan Kaufmann','9780123742605'),
('Foster, I.',1995,'Designing and Building Parallel Programs: Concepts and Tools for Parallel Software Engineering','Addison-Wesley','9780201575941')]:
    plan['bibliografia'].append(dict(tipo='Complementaria' if year==1995 else 'Básica',autor=author,anio=str(year),titulo=title,editorial=publisher,isbn=isbn))
for i, name in enumerate(['Plataformas y herramientas para el cómputo paralelo','Análisis y diseño de programas paralelos','Análisis de rendimiento de programas paralelos','Programas de cómputo paralelo usando memoria compartida','Programas de cómputo paralelo usando memoria distribuida','Programas de cómputo usando aceleradores paralelos I'],1):
    plan['practicas'].append(dict(numero=i,nombre=name,horas='27 h en conjunto; sin desglose individual',lugar='Laboratorio de cómputo'))

activities = dict(titulo='Actividades de aprendizaje · Muestra provisional',boton_cerrar='Cerrar ventana',secciones=[])
glossary = data('assets/data/glosario.json'); glossary['unidades']=[]
glossary['titulo']='Glosario de términos · Muestra provisional'
generated = set()
def page(path, title, body, root, uid):
    write(path, f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)} | Cómputo Paralelo</title><link rel="stylesheet" href="{root}assets/css/comun.css"><link rel="stylesheet" href="{root}assets/css/unidades-base.css"><link rel="stylesheet" href="{root}assets/css/tema.css"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"><link rel="icon" href="{root}assets/img/ESCOMB.png"></head><body class="u-body" data-root="{root}" data-unidad="{uid}"><header class="site-nav" data-componente="navegacion"></header><main class="u-page"><article class="t-article"><p class="u-eyebrow">Cómputo Paralelo · Material provisional</p><h1 class="t-title">{html.escape(title)}</h1><p class="t-callout">{NOTICE}</p><div class="t-prose">{body}</div><a class="u-btn" href="{root}unidades/{uid}/index.html">Volver a la unidad</a></article></main><footer class="u-footer">Cómputo Paralelo · ESCOM-IPN · Material de muestra</footer><script src="{root}assets/js/data-manager.js"></script><script src="{root}assets/js/componentes.js"></script></body></html>''')
    generated.add(path)

for i,(title,goal,theory,practice,autonomous,topics) in enumerate(units,1):
    uid=f'unidad-{i:02}'
    base=f'unidades/{uid}'
    unit=dict(id=uid,numero=i,titulo=title,descripcion=goal,lema='Explora, diseña y analiza soluciones paralelas. Edición provisional.',duracion_horas=theory+practice,introduccion=[NOTICE,topics[0][2]],recorrido='Lee cada tema, consulta sus subtemas y realiza los ejercicios de muestra antes de la actividad integradora.',temas=[],objetivo=goal,competencias=[goal,'Justifica decisiones de diseño y comprueba resultados con evidencias reproducibles.'],video={'titulo':'Video pendiente de validación','url':''},material_apoyo=[{'nombre':'Referencias de la unidad','url':f'{base}/referencias.html'},{'nombre':'Programa académico (PDF)','url':plan['archivo_pdf']}],actividad_final={'nombre':f'Actividad integradora {i}: {title}','descripcion':'Propuesta de trabajo y autoevaluación provisional.','url':f'{base}/actividades/actividad-final.html'})
    write(f'{base}/index.html',unit_template.replace('unidad-01',uid).replace('Unidad 1 |',f'Unidad {i} |'))
    generated.add(f'{base}/index.html')
    section=dict(id=uid,pestana=f'Unidad {i}',titulo=f'Unidad {i}: {title}',descripcion=goal,nota=NOTICE,items=[])
    g=dict(id=uid,pestana=f'Unidad {i}',titulo=title,terminos=[])
    official_topics=[]
    for j,(name,subtopics,summary) in enumerate(topics,1):
        number=f'{i}.{j}'; subs=subtopics.split('|') if subtopics else []
        url=f'{base}/temas/tema-{i:02}-{j:02}.html'; activity=f'{base}/actividades/actividad-{i}-{j}.html'
        unit['temas'].append(dict(numero=number,nombre=name,sintesis=summary,url=url,actividad={'nombre':f'Actividad de aprendizaje {number}','url':activity}))
        official_topics.append(f'{number} {name}'+(': '+ '; '.join(subs) if subs else ''))
        article=f'<p class="u-eyebrow">Unidad {romans[i-1]} · Tema {number}</p><h1 class="t-title">{name}</h1><p class="t-callout">{NOTICE}</p><p class="t-lead" id="idea-central" data-toc="Idea central">{summary}</p><div class="t-prose"><section id="subtemas" data-toc="Subtemas del programa"><h2>Subtemas del programa</h2><ul>'+''.join(f'<li>{number}.{k} {s}</li>' for k,s in enumerate(subs,1))+'</ul>'+('' if subs else '<p>El programa no desglosa subtemas para este apartado.</p>')+f'</section><section id="ejemplo" data-toc="Exploración guiada"><h2>Exploración guiada · Texto de muestra</h2><p>Considera un sistema que procesa un conjunto de datos. Identifica cómo interviene el tema «{name}» en el reparto del trabajo, el acceso a la información y la coordinación. Dibuja una propuesta y señala qué datos necesita cada participante.</p><p>Compara tu propuesta con una ejecución secuencial. Explica qué costos aparecen al colaborar y qué evidencia permitiría comprobar que el resultado sigue siendo correcto.</p></section><section id="reflexion" data-toc="Comprueba tu comprensión"><h2>Comprueba tu comprensión</h2><p>¿Qué decisión de diseño cambiarías si aumentara el volumen de datos o el número de trabajadores? Justifica tu respuesta.</p><a class="u-btn u-btn--primary" href="../actividades/actividad-{i}-{j}.html">Realizar actividad {number}</a></section></div><nav class="t-pager" id="temaNavegacion" aria-label="Navegación entre temas"></nav>'
        s=re.sub(r'<article class="t-article">.*?</article>',lambda m:'<article class="t-article">'+article+'</article>',topic_template,flags=re.S)
        s=re.sub(r'<title>.*?</title>',f'<title>{number} {name} | Cómputo Paralelo</title>',s)
        s=re.sub(r'<meta name="description"[^>]*>',f'<meta name="description" content="{html.escape(summary,quote=True)}">',s)
        s=s.replace('data-unidad="unidad-01"',f'data-unidad="{uid}"').replace('data-tema="1.1"',f'data-tema="{number}"').replace('Unidad I</span>',f'Unidad {romans[i-1]}</span>')
        write(url,s); generated.add(url)
        body=f'<h2>Objetivo</h2><p>Explicar y aplicar: {name}.</p><h2>Consigna de muestra</h2><ol><li>Describe el concepto con tus propias palabras.</li><li>Representa una situación donde intervenga y señala datos, tareas y dependencias.</li><li>Compara dos alternativas y argumenta sus costos.</li><li>Entrega un esquema y una conclusión breve.</li></ol><details><summary>Ver orientación para autoevaluarte</summary><p>{summary}</p><p>Comprueba que tu entrega identifica el problema, explica una decisión y reconoce al menos una limitación. Esta orientación no constituye una calificación oficial.</p></details><p><a href="../temas/tema-{i:02}-{j:02}.html">Volver al tema {number}</a></p>'
        page(activity,f'Actividad {number}: {name}',body,'../../../',uid)
        section['items'].append(dict(tag=f'Tema {number}',reactivos='Ejercicio guiado',tiempo='20 min sugeridos',titulo=f'Actividad {number}: {name}',descripcion='Análisis, esquema y autoevaluación de muestra.',url=activity,icono='fa-pen-to-square',destacada=False))
        g['terminos'].append(dict(termino=name,definicion=summary))
    page(f'{base}/actividades/actividad-final.html',f'Actividad integradora {i}: {title}',f'<h2>Problema propuesto</h2><p>Diseña una solución que procese un arreglo dividido en bloques. Relaciona las decisiones con los temas de esta unidad: {", ".join(t[0] for t in topics)}.</p><h2>Evidencias</h2><ol><li>Diagrama de tareas y dependencias.</li><li>Descripción del acceso y movimiento de datos.</li><li>Comparación con una solución secuencial.</li><li>Resultados esperados y limitaciones.</li></ol><details><summary>Criterios de revisión de muestra</summary><p>Claridad del modelo, justificación del reparto, corrección del resultado y análisis de costos. La rúbrica definitiva queda pendiente de validación docente.</p></details>','../../../',uid)
    section['items'].append(dict(tag='Cierre de unidad',reactivos='Reto integrador',tiempo='45 min sugeridos',titulo=unit['actividad_final']['nombre'],descripcion=unit['actividad_final']['descripcion'],url=unit['actividad_final']['url'],icono='fa-trophy',destacada=True))
    refs='<p>Selección de bibliografía incluida en el programa académico proporcionado. El desarrollo de los temas es provisional.</p><ul>'+''.join(f'<li>{b["autor"]} ({b["anio"]}). <em>{b["titulo"]}</em>. {b["editorial"]}.</li>' for b in plan['bibliografia'])+'</ul><p><a href="../../assets/docs/computoParalelo_IIA2020.pdf">Consultar programa académico completo</a></p>'
    page(f'{base}/referencias.html',f'Referencias · Unidad {i}',refs,'../../',uid)
    save(f'assets/data/unidades/{uid}.json',unit)
    plan['unidades_tematicas'].append(dict(numero=romans[i-1],titulo=title,competencia=goal,horas_docente=f'{theory+practice}.0 h ({theory}.0 h teoría / {practice}.0 h práctica)',horas_autonomo=f'{autonomous}.0 h',temas=official_topics))
    activities['secciones'].append(section); glossary['unidades'].append(g)

save('assets/data/plan-estudios.json',plan)
save('assets/data/actividades.json',activities)
save('assets/data/glosario.json',glossary)
save('assets/data/unidades-data.json',dict(titulo='Unidades temáticas',descripcion='Cinco unidades del programa de Cómputo Paralelo. Lecturas y actividades de muestra pendientes de validación académica.',unidades=[f'unidad-{i:02}' for i in range(1,6)]))

# Rutas heredadas no incluidas en el nuevo temario conservan una salida útil.
for p in (ROOT/'unidades').rglob('*.html'):
    rel=p.relative_to(ROOT).as_posix()
    if rel not in generated:
        uid=p.relative_to(ROOT).parts[1]
        page(rel,'Contenido reorganizado','<p>El temario de Cómputo Paralelo está disponible en el índice de esta unidad.</p>','../../../',uid)

s=read('index.html')
s=s.replace('<strong>3</strong> unidades','<strong>5</strong> unidades').replace('<strong>10</strong> temas','<strong>23</strong> temas').replace('<strong>8</strong> actividades','<strong>28</strong> actividades')
s=re.sub(r'(<div aria-label="Bienvenida completa"[^>]*>).*?(</div>)',lambda m:m[1]+f'<p class="t-callout"><strong>Edición provisional.</strong> {NOTICE}</p><p>Bienvenida y bienvenido al polilibro de <strong>Cómputo Paralelo</strong> de Ingeniería en Inteligencia Artificial. Aquí explorarás cómo dividir problemas, coordinar tareas y evaluar soluciones que aprovechan varios recursos de procesamiento.</p><p>El recorrido abarca arquitecturas paralelas, diseño de algoritmos, memoria compartida, sistemas distribuidos y flujo de datos. Cada tema incluye una lectura y una actividad de muestra para preparar la futura incorporación del contenido validado.</p><p>Trabaja con ejemplos, compara alternativas y explica tus resultados. El propósito del programa es diseñar aplicaciones paralelas con base en el cómputo paralelo.</p>'+m[2],s,flags=re.S)
intro='<h3>Introducción</h3><p>Cómputo Paralelo es una unidad teórica-práctica obligatoria del sexto semestre de Ingeniería en Inteligencia Artificial.</p><h3>Propósito general</h3><p>'+plan['proposito']+'</p><h3>Organización del curso</h3><ul>'+''.join(f'<li>Unidad {romans[i]} · {u[0]}</li>' for i,u in enumerate(units))+'</ul><p>'+NOTICE+'</p>'
method='<h3>Metodología de trabajo</h3><p>El programa contempla métodos inductivo, deductivo y analógico, aprendizaje basado en problemas y aprendizaje autónomo.</p><p>Se proponen organizadores gráficos, ejercicios, solución de problemas, programas funcionando y reportes de prácticas. La evaluación incluye diagnóstico, portafolio de evidencias y evaluaciones escritas.</p><h3>Tiempos y créditos</h3><p>81 horas semestrales: 54 de teoría y 27 de práctica. Aprendizaje autónomo: 18 horas. Créditos: 7.5 TEPIC y 6.0 SATCA. Se incluyen seis prácticas de laboratorio.</p><p>'+NOTICE+'</p>'
for key,content in [('introduccion',intro),('metodologia',method)]:
    s=re.sub(r'(<div class="modal-section" id="modal-'+key+r'">).*?(?=<div class="modal-section")',lambda m:m[1]+content+'</div>\n',s,flags=re.S)
s=re.sub(r'(<div class="modal-section" id="modal-examen">).*?(<hr\s*/>)',lambda m:m[1]+'<h3>Examen diagnóstico · Muestra provisional</h3><p>Doce preguntas sobre algoritmos, memoria y nociones de paralelismo. Completa los datos de identificación para probar el instrumento. Los resultados son orientativos, sin valor en la calificación final.</p><p>'+NOTICE+'</p>'+m[2],s,flags=re.S)
write('index.html',s)

palette={'#082F42':'#10162F','#123B5A':'#192447','#184A70':'#24335B','#0B2F49':'#111B38','#2A6288':'#30436A','#34719C':'#3D5282','#0A2A40':'#0D1329','#38BDF8':'#67E8F9','#7DD3FC':'#A5F3FC','#54D6C5':'#B8A4FA','#72EBD9':'#D4C6FF','#051F2D':'#090F22','#BAE6FD':'#D4C6FF'}
s=read('assets/css/variables.css').replace('Comunicaciones en Red','Cómputo Paralelo')
for old,new in palette.items(): s=s.replace(old,new)
s+='\n:root { --gradient-unit-4: linear-gradient(135deg, var(--bg-main), var(--surface-hover)); --gradient-unit-5: linear-gradient(135deg, var(--bg-section), var(--surface)); }\n'
write('assets/css/variables.css',s)
write('README.md','''# Polilibro de Cómputo Paralelo

Copia adaptada de Libro-App-Com-Red. Conserva sus estilos, navegación, modales y plantillas. El proyecto original no se modifica y no se copia su historial Git.

## Estado editorial

Los títulos, subtemas, competencias, horas y prácticas se basan en assets/docs/computoParalelo_IIA2020.pdf (vigencia agosto de 2022). Las 23 lecturas, 28 actividades, glosario y diagnóstico contienen propuestas provisionales, pendientes de validación. Los videos quedan sin asignar hasta recibir material validado. Las semblanzas y créditos del proyecto base se conservan como procedencia; no acreditan autoría del nuevo contenido.

## Vista local

Desde esta carpeta ejecuta `python -m http.server 8000` y abre http://localhost:8000. Se necesita HTTP para cargar los JSON; no abrir mediante file://.

## Edición

- Inicio: index.html.
- Programa: assets/data/plan-estudios.json.
- Unidades: assets/data/unidades/unidad-XX.json.
- Lecturas y actividades: unidades/unidad-XX/.
- Diagnóstico, glosario y actividades: assets/data/.
- Paleta: assets/css/variables.css.

Los recursos heredados no usados se conservan para reutilización. No son parte del contenido validado. El script scripts/adaptar_contenido.py documenta la adaptación inicial; no ejecutarlo después de incorporar contenido docente porque sobrescribe las propuestas.
''')
print('Generadas 5 unidades, 23 temas y 28 actividades.')
