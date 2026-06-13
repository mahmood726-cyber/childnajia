#!/usr/bin/env node
/*
 * Headless smoke test for the HIDAYAH danger-detection engine.
 *
 * The shipped app (hidayah-v1.3.0.html) embeds a self-contained JS engine plus
 * an in-browser TESTS array (10 cases) that is normally run via the in-page
 * "Run Tests" button. This script extracts that single <script> block, executes
 * it in a Node `vm` sandbox with minimal DOM/Chart stubs, and runs every entry
 * of the embedded TESTS array headlessly so the suite can be checked from CI
 * without a browser. No engine logic is duplicated here.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const HTML = path.join(__dirname, 'hidayah-v1.3.0.html');

function extractMainScript(html) {
  // Find the first inline <script> with no src= attribute (the engine block).
  const re = /<script(?![^>]*\ssrc=)[^>]*>([\s\S]*?)<\/script>/gi;
  let m, body = null;
  while ((m = re.exec(html)) !== null) {
    if (m[1].includes('function computeDanger')) { body = m[1]; break; }
  }
  if (!body) throw new Error('engine <script> block not found in ' + HTML);
  return body;
}

function makeSandbox() {
  // Minimal stubs: the engine + TESTS never touch the DOM at compute time,
  // but the module body defines UI helpers that reference these globals.
  const noop = () => {};
  const fakeEl = new Proxy({}, {
    get: (t, k) => (k in t ? t[k] : (typeof k === 'string' ? noop : undefined)),
    set: () => true,
  });
  const documentStub = {
    getElementById: () => fakeEl,
    querySelector: () => fakeEl,
    querySelectorAll: () => [],
    addEventListener: noop,
    createElement: () => fakeEl,
  };
  const sandbox = {
    console,
    Math, BigInt, Number, Set, Array, Object, JSON, Error,
    document: documentStub,
    window: {},
    Chart: function () { return fakeEl; },
    setTimeout: (fn) => { try { fn(); } catch (_) {} },
  };
  sandbox.window.document = documentStub;
  sandbox.globalThis = sandbox;
  return sandbox;
}

function main() {
  const html = fs.readFileSync(HTML, 'utf8');
  const code = extractMainScript(html);
  const sandbox = makeSandbox();
  vm.createContext(sandbox);
  // Top-level `const`/`function` bindings are block-scoped and not attached to
  // the sandbox object, so export the symbols we need explicitly.
  const exportTail = '\n;globalThis.__exports = { TESTS, computeDanger, BASE_INPUTS, MODEL };';
  vm.runInContext(code + exportTail, sandbox, { filename: 'hidayah-engine.js' });
  Object.assign(sandbox, sandbox.__exports);

  const TESTS = sandbox.TESTS;
  if (!Array.isArray(TESTS) || TESTS.length === 0) {
    console.error('FAIL: TESTS array missing or empty after engine load');
    process.exit(1);
  }

  let passed = 0;
  const failures = [];
  TESTS.forEach((t, i) => {
    try {
      t.fn();
      passed++;
    } catch (e) {
      failures.push(`[${i + 1}] ${t.name}: ${e && e.message ? e.message : e}`);
    }
  });

  // Sanity check on the engine itself, independent of the embedded suite.
  const res = sandbox.computeDanger({ ...sandbox.BASE_INPUTS }, sandbox.MODEL);
  if (!(res && typeof res.P === 'number' && res.P >= 0 && res.P <= 1)) {
    failures.push('engine sanity: computeDanger returned out-of-range P');
  }

  console.log(`${passed}/${TESTS.length} embedded tests passed`);
  if (failures.length) {
    failures.forEach((f) => console.error('  FAIL ' + f));
    process.exit(1);
  }
  console.log('SMOKE OK');
}

main();
