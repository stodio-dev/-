#!/usr/bin/env node
// Count real tokens with bundled OpenAI vocabularies (o200k_base, cl100k_base).
// setup: (cd tools && npm install)      usage: node tools/count_tokens.mjs FILE... | -   (- reads stdin)
// These are OpenAI tokenizers. Other model families tokenize differently; treat ratios as indicative.
import fs from "fs";
import * as o200k from "gpt-tokenizer/encoding/o200k_base";
import * as cl100k from "gpt-tokenizer/encoding/cl100k_base";

const args = process.argv.slice(2);
if (!args.length) { console.error("usage: node tools/count_tokens.mjs FILE... | -"); process.exit(2); }
const rows = args.map(f => {
  const t = f === "-" ? fs.readFileSync(0, "utf8") : fs.readFileSync(f, "utf8");
  return [f, t.length, o200k.encode(t).length, cl100k.encode(t).length];
});
const w = Math.max(5, ...rows.map(r => r[0].length));
console.log("file".padEnd(w), "chars".padStart(7), "o200k".padStart(7), "cl100k".padStart(7));
for (const r of rows) console.log(r[0].padEnd(w), ...r.slice(1).map(x => String(x).padStart(7)));
if (rows.length > 1) {
  const s = i => rows.reduce((a, r) => a + r[i], 0);
  console.log("TOTAL".padEnd(w), String(s(1)).padStart(7), String(s(2)).padStart(7), String(s(3)).padStart(7));
}
