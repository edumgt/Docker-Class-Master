const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const targets = [
  { solution: 'odoo', port: 9000 },
  { solution: 'erpnext', port: 9001 },
  { solution: 'zulip', port: 9002 },
  { solution: 'taiga', port: 9003 },
  { solution: 'tryton', port: 9004 },
];

async function ensureDir(dirPath) {
  await fs.promises.mkdir(dirPath, { recursive: true });
}

async function captureSolution(browser, target) {
  const baseUrl = `http://127.0.0.1:${target.port}`;
  const outDir = path.join('captures', target.solution);
  await ensureDir(outDir);

  const context = await browser.newContext({ viewport: { width: 1600, height: 1000 } });
  const page = await context.newPage();

  const username = `${target.solution}_member1`;

  await page.goto(`${baseUrl}/app-ui`, { waitUntil: 'networkidle', timeout: 30000 });
  await page.locator('h1').first().waitFor({ timeout: 10000 });
  await page.screenshot({ path: path.join(outDir, '01-runtime.png'), fullPage: true });

  await page.goto(`${baseUrl}/login-ui`, { waitUntil: 'networkidle', timeout: 30000 });
  await page.locator('h1').first().waitFor({ timeout: 10000 });
  await page.screenshot({ path: path.join(outDir, '02-login.png'), fullPage: true });

  await page.fill('#username', username);
  await page.fill('#password', '123456');
  await page.click('#loginBtn');
  await page.waitForURL(/\/dashboard-ui\?username=/, { timeout: 15000 });
  await page.locator('h1').first().waitFor({ timeout: 10000 });
  await page.screenshot({ path: path.join(outDir, '03-dashboard.png'), fullPage: true });

  await context.close();

  return {
    solution: target.solution,
    runtime: path.join(outDir, '01-runtime.png'),
    login: path.join(outDir, '02-login.png'),
    dashboard: path.join(outDir, '03-dashboard.png'),
  };
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const results = [];
  try {
    for (const target of targets) {
      process.stdout.write(`[capture] ${target.solution}...\n`);
      const res = await captureSolution(browser, target);
      results.push(res);
      process.stdout.write(`[ok] ${target.solution}\n`);
    }
  } finally {
    await browser.close();
  }

  const summaryPath = path.join('captures', 'summary.json');
  await fs.promises.writeFile(summaryPath, JSON.stringify({ captured_at: new Date().toISOString(), results }, null, 2));
  process.stdout.write(`[done] summary -> ${summaryPath}\n`);
})();
