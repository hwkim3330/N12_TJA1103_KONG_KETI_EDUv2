import fs from 'node:fs';

const [input, output, prefix] = process.argv.slice(2);
if (!input || !output || prefix === undefined) throw new Error('usage: node prefix_pcb_nets.mjs input output PREFIX');
let text = fs.readFileSync(input, 'utf8');
let count = 0;
text = text.replace(/(\(net\s+(?:\d+\s+)?")([^"]*)("\))/g, (all, open, name, close) => {
  if (!name) return all;
  count++;
  return `${open}${prefix}${name}${close}`;
});
fs.writeFileSync(output, text);
console.log(`prefixed ${count} nets with ${prefix}`);
