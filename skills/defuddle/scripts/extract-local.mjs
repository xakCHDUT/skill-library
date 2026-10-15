#!/usr/bin/env node
// Local-only adapter. MIT; the upstream skill attribution is in PROVENANCE.md.
import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import { parseArgs } from 'node:util';

const usage = 'node extract-local.mjs --input page.html --output page.md [--source-url https://example.org/article] [--json] [--runtime dependency-directory]';

export async function extractLocal({ input, output, sourceUrl, json = false, runtime }) {
  if (!input || !output) throw new Error('Both --input and --output are required.');
  if (/^[a-z][a-z0-9+.-]*:\/\//i.test(input)) throw new Error('--input must be a local HTML file.');
  if (sourceUrl && !['http:', 'https:'].includes(new URL(sourceUrl).protocol)) {
    throw new Error('--source-url must use http or https; it is metadata only.');
  }
  const inputPath = path.resolve(input);
  const outputPath = path.resolve(output);
  const html = await readFile(inputPath, 'utf8');
  const packageRoot = runtime || path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
  const require = createRequire(path.join(path.resolve(packageRoot), 'package.json'));
  // The pinned package exports ./node only for ESM, so require.resolve cannot
  // resolve that subpath. Resolve its main bundle and import the sibling ESM entry.
  const defuddleNode = path.join(path.dirname(require.resolve('defuddle')), 'node.js');
  const { Defuddle } = await import(pathToFileURL(defuddleNode).href);
  const { parseHTML } = await import(pathToFileURL(require.resolve('linkedom')).href);
  const { document } = parseHTML(html);
  // linkedom omits browser CSS APIs used by the parser; mirror upstream polyfills.
  document.styleSheets ??= [];
  document.defaultView.getComputedStyle ??= () => ({ display: '' });
  if (sourceUrl) document.URL = sourceUrl;
  const result = await Defuddle(document, sourceUrl, { markdown: true, useAsync: false });
  if (!result.content?.trim()) throw new Error('No readable content was extracted.');
  const data = json ? JSON.stringify({
    source: sourceUrl || null,
    title: result.title,
    author: result.author,
    published: result.published,
    description: result.description,
    content: result.content
  }, null, 2) + '\n' : result.content + '\n';
  // Exclusive creation preserves existing notes, including input=output and symlinks.
  await writeFile(outputPath, data, { encoding: 'utf8', flag: 'wx' });
  return { title: result.title, bytes: Buffer.byteLength(data), outputCreated: true };
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  try {
    const { values } = parseArgs({ options: {
      input: { type: 'string' }, output: { type: 'string' },
      'source-url': { type: 'string' }, runtime: { type: 'string' },
      json: { type: 'boolean' }, help: { type: 'boolean' }
    } });
    if (values.help) console.log(usage);
    else console.log(JSON.stringify(await extractLocal({
      input: values.input, output: values.output, sourceUrl: values['source-url'],
      json: values.json, runtime: values.runtime
    })));
  } catch (error) {
    console.error(error.code === 'EEXIST' ? 'Output already exists; choose a new filename.' : error.message);
    process.exitCode = 1;
  }
}
