import fs from 'node:fs';

const [input, output] = process.argv.slice(2);
let text = fs.readFileSync(input, 'utf8');
let removed = 0;
const re = /\n\t\t\((fp_line|fp_rect|fp_poly)\n(?:(?!\n\t\t\(fp_)[\s\S])*?\n\t\t\)/g;
const out = text.replace(re, form => {
  if (/F\.SilkS/.test(form)) { removed++; return ''; }
  return form;
});

fs.writeFileSync(output, out);
console.log(`removed ${removed} F.SilkS footprint primitives`);
