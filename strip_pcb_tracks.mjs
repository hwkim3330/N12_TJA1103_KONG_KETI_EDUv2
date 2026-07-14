import fs from 'node:fs';

const [input, output] = process.argv.slice(2);
if (!input || !output) throw new Error('usage: node strip_pcb_tracks.mjs input.kicad_pcb output.kicad_pcb');

const text = fs.readFileSync(input, 'utf8');
const remove = new Set(['segment', 'via']);
let out = '';
let i = 0;
let depth = 0;

while (i < text.length) {
  // KiCad's top-level board wrapper is depth 0; board items such as
  // (segment ...) and (via ...) begin at depth 1.
  if (text[i] !== '(' || depth !== 1) {
    out += text[i++];
    if (text[i - 1] === '(') depth++;
    else if (text[i - 1] === ')') depth--;
    continue;
  }

  let j = i + 1;
  while (j < text.length && /\s/.test(text[j])) j++;
  let k = j;
  while (k < text.length && !/[\s()]/.test(text[k])) k++;
  const head = text.slice(j, k);
  if (!remove.has(head)) {
    out += text[i++];
    depth++;
    continue;
  }

  let d = 0;
  let q = i;
  for (; q < text.length; q++) {
    if (text[q] === '(') d++;
    else if (text[q] === ')') {
      d--;
      if (d === 0) { q++; break; }
    }
  }
  i = q;
}

fs.writeFileSync(output, out);
console.log(`removed copper tracks and vias: ${input} -> ${output}`);
