// news-image-20261120 entrypoint (Node 22, standard library only).
//
// The entry is the broadsheet in entry.png, rendered by tools/render20.py
// from news.json and three Pexels file photos. This program checks the
// file is a whole PNG inside the competition's limits, then writes it to
// the grader's output directory as entry.png. Both runs must produce the
// same bytes, and this program writes nothing else, so they do.
//
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1024 * 1024;
const MAX_SIDE = 1024;

function fail(message) {
  throw new Error(`entry.png rejected: ${message}`);
}

function main() {
  const here = dirname(fileURLToPath(import.meta.url));
  const bytes = readFileSync(join(here, "entry.png"));

  if (bytes.length > MAX_BYTES) {
    fail(`is ${bytes.length} bytes, over the ${MAX_BYTES} byte cap`);
  }
  if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
    fail("does not start with the PNG signature");
  }
  // IHDR: width at bytes 16-19, height at 20-23, big-endian.
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width > MAX_SIDE || height > MAX_SIDE) {
    fail(`is ${width}x${height}, over the ${MAX_SIDE}x${MAX_SIDE} cap`);
  }
  if (width !== 680 || height !== 1024) {
    fail(`is ${width}x${height}, expected 680x1024`);
  }

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, "entry.png"), bytes);
}

main();
