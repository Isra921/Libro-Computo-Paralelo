# Polilibro de Cómputo Paralelo

Copia adaptada de Libro-App-Com-Red. Conserva sus estilos, navegación, modales y plantillas. El proyecto original no se modifica y no se copia su historial Git.

## Estado editorial

Los títulos, subtemas, competencias, horas y prácticas se basan en assets/docs/computoParalelo_IIA2020.pdf (vigencia agosto de 2022). Las 23 lecturas, 28 actividades, glosario y diagnóstico contienen propuestas provisionales, pendientes de validación. Los videos quedan sin asignar hasta recibir material validado. Las semblanzas y créditos del proyecto base se conservan como procedencia; no acreditan autoría del nuevo contenido.

## Vista local

Solo están habilitados el tema 1.1, su cuestionario de diez preguntas y la actividad final de la unidad I (simulador de reparto de trabajo). Los demás temas y actividades muestran «Próximamente», también desde enlaces directos. En cuadrícula, las filas incompletas quedan centradas.

Desde esta carpeta ejecuta `python -m http.server 8000` y abre http://localhost:8000. Se necesita HTTP para cargar los JSON; no abrir mediante file://.

## Edición

- Inicio: index.html.
- Programa: assets/data/plan-estudios.json.
- Unidades: assets/data/unidades/unidad-XX.json.
- Lecturas y actividades: unidades/unidad-XX/.
- Diagnóstico, glosario y actividades: assets/data/.
- Paleta: assets/css/variables.css.

Los recursos heredados no usados se conservan para reutilización. No son parte del contenido validado. El script scripts/adaptar_contenido.py documenta la adaptación inicial; no ejecutarlo después de incorporar contenido docente porque sobrescribe las propuestas.
