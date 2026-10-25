/* Plot controls and accessible tables. Data is generated from the same JSON as the SVGs. */
(() => {
  'use strict';
  const tabs = Array.from(document.querySelectorAll('.plot-tabs [role="tab"]'));
  function selectPlot(tab, focus = false) {
    tabs.forEach(item => {
      const selected = item === tab;
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
      const panel = document.getElementById(item.getAttribute('aria-controls'));
      if (panel) panel.hidden = !selected;
    });
    if (focus) tab.focus();
  }
  if (tabs.length) {
    selectPlot(tabs[0]);
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => selectPlot(tab));
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        else if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = tabs.length - 1;
        else return;
        event.preventDefault();
        selectPlot(tabs[next], true);
      });
    });
  }

  const data = window.NRSFM_PAPER_DATA;
  if (!data) return;
  const fixed = (value, digits = 2) => typeof value === 'number'
    ? value.toLocaleString('en-US', {minimumFractionDigits:digits, maximumFractionDigits:digits})
    : '—';

  function addTable(name, headings, rows, highlightedColumn = -1) {
    const details = document.querySelector('[data-table="' + name + '"]');
    if (!details || !rows.length) return;
    const table = document.createElement('table');
    const thead = table.createTHead();
    const header = thead.insertRow();
    headings.forEach(label => {
      const cell = document.createElement('th');
      cell.scope = 'col';
      cell.textContent = label;
      header.appendChild(cell);
    });
    const body = table.createTBody();
    rows.forEach(values => {
      const row = body.insertRow();
      values.forEach((value, index) => {
        const cell = index === 0 ? document.createElement('th') : document.createElement('td');
        if (index === 0) cell.scope = 'row';
        if (index === highlightedColumn) cell.className = 'ours-value';
        cell.textContent = String(value);
        row.appendChild(cell);
      });
    });
    details.querySelector('.data-table-scroll').replaceChildren(table);
    details.hidden = false;
  }

  // Field names are taken from the verified dataset, with no interpolated values.
  const dense = data.dense || [];
  const sequences = [...new Set(dense.map(row => row.sequence))];
  for (const metric of ['runtime_seconds', 'error_e3d']) {
    const rows = sequences.map(sequence => {
      const group = dense.filter(row => row.sequence === sequence);
      return [sequence, group[0].frames, ...['Ours','OPM','TSM'].map(method =>
        fixed(group.find(row => row.method === method)?.[metric], metric === 'error_e3d' ? 4 : 2))];
    });
    addTable(metric === 'runtime_seconds' ? 'dense-runtime' : 'dense-accuracy',
      ['Sequence','Frames',metric === 'runtime_seconds' ? 'Ours (s)' : 'Ours e₃d',
       metric === 'runtime_seconds' ? 'OPM (s)' : 'OPM e₃d',metric === 'runtime_seconds' ? 'TSM (s)' : 'TSM e₃d'],rows,2);
  }

  const shape = data.mocap_shape || [];
  const means = ['Ours','OPM','R-BMM','TSM','BMM'].map(method => {
    const group = shape.filter(row => row.method === method);
    if (!group.length) return null;
    return [method,group.length,fixed(group.reduce((sum,row)=>sum+row.runtime_seconds,0)/group.length,5),
      fixed(group.reduce((sum,row)=>sum+row.error_e3d,0)/group.length,7)];
  }).filter(Boolean);
  addTable('mocap-means',['Method','Sequences','Mean shape time (s)','Mean e₃d'],means);

  const stage = data.stage_breakdown || [];
  const stageRows = stage.filter(row => row.benchmark === 'CMU MoCap')
    .map(row => [row.sequence,row.frames,row.points,fixed(row.rotation_seconds),fixed(row.shape_seconds),fixed(row.total_seconds)]);
  addTable('stage-times',['Sequence','Frames','Points','Rotation (s)','Shape (s)','Total (s)'],stageRows);
})();
