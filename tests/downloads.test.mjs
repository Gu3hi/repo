import assert from 'node:assert/strict';
import { test } from 'node:test';
import { parseDownloadCounts, sumDownloads } from '../docs/assets/downloads.mjs';

test('sums only the requested assets, keeping a real zero distinct from a missing asset', () => {
  const counts = parseDownloadCounts({ assets: [
    { name: 'vela-rootless.deb', download_count: 12 },
    { name: 'vela-roothide.deb', download_count: 23 },
    { name: 'aura.deb', download_count: 0 },
  ] });
  assert.equal(sumDownloads(counts, ['vela-rootless.deb', 'vela-roothide.deb']), 35);
  assert.equal(sumDownloads(counts, ['vela-rootless.deb']), 12);
  assert.equal(sumDownloads(counts, ['aura.deb']), 0);
  assert.equal(sumDownloads(counts, ['aura.deb', 'missing.deb']), null);
  assert.equal(sumDownloads(counts, []), null);
});

test('rejects malformed, duplicate and negative counts instead of presenting them as downloads', () => {
  for (const release of [null, {}, { assets: [null] }, { assets: [{ name: 'a', download_count: -1 }] },
    { assets: [{ name: 'a', download_count: '3' }] }, { assets: [{ name: 'a', download_count: 1.5 }] },
    { assets: [{ name: 'a', download_count: 1 }, { name: 'a', download_count: 2 }] }]) {
    assert.throws(() => parseDownloadCounts(release));
  }
});
