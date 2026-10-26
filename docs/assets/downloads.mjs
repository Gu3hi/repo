const endpoint = new URL('./downloads.json', import.meta.url);

export function parseDownloadCounts(release) {
  if (!release || !Array.isArray(release.assets)) throw new Error('Missing release assets');
  const counts = new Map();
  for (const asset of release.assets) {
    if (!asset || typeof asset.name !== 'string' || !Number.isSafeInteger(asset.download_count) || asset.download_count < 0 || counts.has(asset.name)) {
      throw new Error('Invalid download count');
    }
    counts.set(asset.name, asset.download_count);
  }
  return counts;
}

export function sumDownloads(counts, names) {
  if (!names.length || names.some(name => !counts.has(name))) return null;
  return names.reduce((total, name) => total + counts.get(name), 0);
}

if (typeof document !== 'undefined') {
  const counters = document.querySelectorAll('[data-download-files]');
  if (counters.length) {
    fetch(endpoint, { signal: AbortSignal.timeout(10000) })
      .then(response => {
        if (!response.ok) throw new Error('Download statistics unavailable');
        return response.json();
      })
      .then(release => {
        const counts = parseDownloadCounts(release);
        const updated = new Date(release.updated_at);
        if (Number.isNaN(updated.getTime())) throw new Error('Invalid statistics timestamp');
        counters.forEach(counter => {
          const total = sumDownloads(counts, counter.dataset.downloadFiles.split(' '));
          counter.textContent = total === null ? '暂不可用 / Unavailable' : total.toLocaleString();
          counter.setAttribute('aria-label', total === null ? '下载次数暂不可用 / Download count unavailable' : `${total.toLocaleString()} 次下载 / downloads`);
          counter.title = `统计截至 / As of ${updated.toLocaleString()}`;
        });
        document.querySelectorAll('[data-download-updated]').forEach(element => {
          element.textContent = `统计截至 / As of ${updated.toLocaleString()} · 约每小时更新 / Updated about hourly`;
        });
      })
      .catch(() => {
        counters.forEach(counter => {
          counter.textContent = '暂不可用 / Unavailable';
          counter.setAttribute('aria-label', '下载次数暂不可用 / Download count unavailable');
        });
        document.querySelectorAll('[data-download-updated]').forEach(element => {
          element.textContent = '下载统计暂不可用 / Download statistics unavailable';
        });
      });
  }
}
