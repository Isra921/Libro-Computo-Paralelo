(() => {
 const form = document.getElementById('simulador');
 function simulate() {
  const p = Number(document.getElementById('procesadores').value);
  const balanced = document.getElementById('reparto').value === 'equilibrado';
  const correct = document.getElementById('coordinacion').value === 'local';
  const loads = Array(p).fill(120 / p);
  if (!balanced && p > 1) { loads[0] = 72; for (let i = 1; i < p; i++) loads[i] = 48 / (p - 1); }
  const time = 12 + Math.max(...loads) + 2 * (p - 1), speedup = 132 / time;
  document.getElementById('resultadoSimulacion').textContent = correct
   ? `Propuesta válida en este modelo. Tiempo: ${time.toFixed(1)} unidades. Aceleración: ${speedup.toFixed(2)}×. Eficiencia: ${(100 * speedup / p).toFixed(1)} %. ${balanced || p === 1 ? 'Trabajo equilibrado.' : 'El procesador más cargado retrasa la finalización.'}`
   : 'Revisa la corrección: un acumulador sin protección puede perder resultados por una condición de carrera. Usa resultados locales y combinación final antes de comparar el rendimiento.';
  const container = document.getElementById('cargas'); container.replaceChildren();
  loads.forEach((load, i) => {
   const row = document.createElement('div'); row.className = 'demo-load';
   const name = document.createElement('span'); name.textContent = `CPU ${i + 1}`;
   const bar = document.createElement('progress'); bar.max = 120; bar.value = load; bar.setAttribute('aria-label', `Carga CPU ${i + 1}`);
   const value = document.createElement('span'); value.textContent = `${load.toFixed(1)} bloques`;
   row.append(name, bar, value); container.append(row);
  });
 }
 form.addEventListener('submit', e => { e.preventDefault(); simulate(); });
 form.addEventListener('reset', () => { requestAnimationFrame(simulate); document.getElementById('reto').reset(); document.getElementById('feedbackReto').textContent = ''; });
 document.getElementById('reto').addEventListener('submit', e => {
  e.preventDefault();
  document.getElementById('feedbackReto').textContent = new FormData(e.currentTarget).get('decision') === 'a'
   ? 'Correcto. El reparto equilibrado reduce esperas y la combinación final evita escrituras concurrentes sin protección.'
   : 'Inténtalo de nuevo: busca reparto equilibrado y coordinación que conserve los resultados.';
 });
 simulate();
})();
