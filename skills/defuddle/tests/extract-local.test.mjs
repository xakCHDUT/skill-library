import test, { after } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readFile, writeFile, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { extractLocal } from '../scripts/extract-local.mjs';

const root = await mkdtemp(path.join(os.tmpdir(), 'defuddle-skill-check-'));
const here = path.dirname(fileURLToPath(import.meta.url));
const fixture = path.join(here, 'fixtures/article.html');
const runtime = process.env.DEFUDDLE_TEST_RUNTIME || path.resolve(here, '..');
const sourceUrl = 'https://example.org/research/article';
after(async () => {
  const parent = path.resolve(os.tmpdir());
  assert.equal(path.dirname(path.resolve(root)), parent);
  assert.ok(path.basename(root).startsWith('defuddle-skill-check-'));
  await rm(root, { recursive: true, force: true });
});

test('keeps Chinese body, numbers and article metadata', async () => {
  const output = path.join(root, 'article.json');
  await extractLocal({ input: fixture, output, sourceUrl, runtime, json: true });
  const article = JSON.parse(await readFile(output, 'utf8'));
  assert.equal(article.title, '合成研究资料：现金流与扩产');
  assert.equal(article.author, '合成测试作者');
  assert.equal(article.published, '2026-10-01T08:00:00Z');
  assert.equal(article.source, sourceUrl);
  assert.match(article.content, /现金流/);
  assert.match(article.content, /123\.45/);
  assert.match(article.content, /25%/);
  assert.match(article.content, /第二条合成观察/);
});
test('removes navigation and advertisements', async () => {
  const article = JSON.parse(await readFile(path.join(root, 'article.json'), 'utf8'));
  assert.doesNotMatch(article.content, /导航标记|广告标记|页脚标记/);
});
test('resolves relative article links against the source URL', async () => {
  const article = JSON.parse(await readFile(path.join(root, 'article.json'), 'utf8'));
  assert.match(article.content, /\[原始证据说明\]\(https:\/\/example\.org\/evidence\)/);
});
test('writes usable Markdown and never executes page script', async () => {
  const output = path.join(root, 'article.md');
  await extractLocal({ input: fixture, output, sourceUrl, runtime });
  assert.match(await readFile(output, 'utf8'), /## 证据与边界/);
});
test('preserves an existing output byte for byte', async () => {
  const output = path.join(root, 'existing.md');
  await writeFile(output, 'Existing note: 保留');
  await assert.rejects(extractLocal({ input: fixture, output, sourceUrl, runtime }), { code: 'EEXIST' });
  assert.equal(await readFile(output, 'utf8'), 'Existing note: 保留');
});
test('input equal to output leaves the original HTML intact', async () => {
  const input = path.join(root, 'same.html');
  const before = await readFile(fixture, 'utf8');
  await writeFile(input, before);
  await assert.rejects(extractLocal({ input, output: input, sourceUrl, runtime }), { code: 'EEXIST' });
  assert.equal(await readFile(input, 'utf8'), before);
});
test('rejects URL input instead of silently fetching it', async () => {
  await assert.rejects(extractLocal({ input: sourceUrl, output: path.join(root, 'url.md'), runtime }), /local HTML/);
});
test('disables third-party fallback even for an empty X page', async (t) => {
  let calls = 0;
  t.mock.method(globalThis, 'fetch', async () => { calls++; throw new Error('Unexpected network request'); });
  const input = path.join(root, 'empty.html');
  await writeFile(input, '<!doctype html><html><head><title>Empty</title></head><body></body></html>');
  await assert.rejects(extractLocal({ input, output: path.join(root, 'empty.md'), sourceUrl: 'https://x.com/example/status/1', runtime }), /No readable content/);
  assert.equal(calls, 0);
});
