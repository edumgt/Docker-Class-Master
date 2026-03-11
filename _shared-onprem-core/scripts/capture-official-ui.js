const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const OUT_ROOT = path.resolve(__dirname, '..', 'captures_official');

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

async function safeScreenshot(page, outPath) {
  ensureDir(path.dirname(outPath));
  await page.screenshot({ path: outPath, fullPage: true });
}

async function captureOdoo(browser) {
  const solution = 'odoo';
  const outDir = path.join(OUT_ROOT, solution);
  ensureDir(outDir);
  const context = await browser.newContext({ viewport: { width: 1600, height: 1000 } });
  const page = await context.newPage();
  const result = { solution, status: 'ok', notes: [] };

  try {
    await page.goto('http://127.0.0.1:9060/web', { waitUntil: 'networkidle', timeout: 60000 });
    await safeScreenshot(page, path.join(outDir, '01-runtime.png'));

    await page.goto('http://127.0.0.1:9060/web/login?db=odoo_official', { waitUntil: 'networkidle', timeout: 60000 });
    await safeScreenshot(page, path.join(outDir, '02-login.png'));

    if (await page.locator('input[name="login"]').count()) {
      await page.fill('input[name="login"]', 'admin');
      await page.fill('input[name="password"]', 'admin');
      await Promise.all([
        page.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {}),
        page.click('button[type="submit"]'),
      ]);
    } else {
      result.notes.push('Odoo login form selector not found; dashboard may be anonymous page.');
    }

    await page.waitForTimeout(3000);
    await safeScreenshot(page, path.join(outDir, '03-dashboard.png'));
  } catch (e) {
    result.status = 'partial';
    result.notes.push(`Odoo capture error: ${String(e.message || e)}`);
    try {
      await safeScreenshot(page, path.join(outDir, '03-dashboard.png'));
    } catch {}
  } finally {
    await context.close();
  }

  return result;
}

async function captureERPNext(browser) {
  const solution = 'erpnext';
  const outDir = path.join(OUT_ROOT, solution);
  ensureDir(outDir);
  const context = await browser.newContext({ viewport: { width: 1600, height: 1000 } });
  const page = await context.newPage();
  const result = { solution, status: 'ok', notes: [] };

  try {
    await page.goto('http://official.local:9061/', { waitUntil: 'networkidle', timeout: 60000 });
    await safeScreenshot(page, path.join(outDir, '01-runtime.png'));
    await safeScreenshot(page, path.join(outDir, '02-login.png'));

    if (await page.locator('#login_email').count()) {
      await page.fill('#login_email', 'Administrator');
      await page.fill('#login_password', '123456');
      await Promise.all([
        page.waitForURL(/\/app(\/|$)/, { timeout: 30000 }).catch(() => {}),
        page.click('.btn-login'),
      ]);
      await page.waitForTimeout(3000);
    } else {
      result.status = 'partial';
      result.notes.push('ERPNext login fields not found.');
    }

    await safeScreenshot(page, path.join(outDir, '03-dashboard.png'));
  } catch (e) {
    result.status = 'partial';
    result.notes.push(`ERPNext capture error: ${String(e.message || e)}`);
    try {
      await safeScreenshot(page, path.join(outDir, '03-dashboard.png'));
    } catch {}
  } finally {
    await context.close();
  }

  return result;
}

async function captureTryton(browser) {
  const solution = 'tryton';
  const outDir = path.join(OUT_ROOT, solution);
  ensureDir(outDir);
  const context = await browser.newContext({ viewport: { width: 1600, height: 1000 } });
  const page = await context.newPage();
  const result = { solution, status: 'ok', notes: [] };

  try {
    await page.goto('http://127.0.0.1:9062/', { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(4000);
    await safeScreenshot(page, path.join(outDir, '01-runtime.png'));

    await safeScreenshot(page, path.join(outDir, '02-login.png'));

    const loginField = page.locator('input[name="login"], #login');
    if (await loginField.count()) {
      await loginField.first().fill('admin');

      const submitBtn = page.locator('button[type="submit"]:has-text("LOGIN"), button[type="submit"]');
      if (await submitBtn.count()) {
        await submitBtn.first().click();
      } else {
        result.status = 'partial';
        result.notes.push('Tryton login submit button not found.');
      }

      await page.waitForSelector('input[name="password"], #ask-dialog-entry', { timeout: 15000 }).catch(() => {});
      const passField = page.locator('input[name="password"], #ask-dialog-entry');
      if (await passField.count()) {
        await passField.first().fill('123456');
        const okBtn = page.locator('button:has-text("OK"), .modal button.btn-primary');
        if (await okBtn.count()) {
          await okBtn.first().click().catch(() => {});
        } else {
          await page.keyboard.press('Enter').catch(() => {});
        }
        await page.waitForTimeout(6000);
      } else {
        const loginStillVisible = (await page.locator('input[name="login"], #login').count()) > 0;
        if (loginStillVisible) {
          result.status = 'partial';
          result.notes.push('Tryton password prompt not found after login submit.');
        }
      }
    } else {
      result.status = 'partial';
      result.notes.push('Tryton login field not found.');
    }

    await safeScreenshot(page, path.join(outDir, '03-dashboard.png'));
  } catch (e) {
    result.status = 'partial';
    result.notes.push(`Tryton capture error: ${String(e.message || e)}`);
    try {
      await safeScreenshot(page, path.join(outDir, '03-dashboard.png'));
    } catch {}
  } finally {
    await context.close();
  }

  return result;
}

async function captureTaiga(browser) {
  const solution = 'taiga';
  const outDir = path.join(OUT_ROOT, solution);
  ensureDir(outDir);
  const context = await browser.newContext({ viewport: { width: 1600, height: 1000 } });
  const page = await context.newPage();
  const result = { solution, status: 'ok', notes: [] };

  try {
    await page.goto('http://127.0.0.1:9063/', { waitUntil: 'networkidle', timeout: 60000 });
    await safeScreenshot(page, path.join(outDir, '01-runtime.png'));

    await page.goto('http://127.0.0.1:9063/login', { waitUntil: 'networkidle', timeout: 60000 });
    await safeScreenshot(page, path.join(outDir, '02-login.png'));

    const emailSel = ['input[type="email"]', 'input[name="username"]', 'input[type="text"]'];
    const passSel = ['input[type="password"]'];

    const pick = async (arr) => {
      for (const sel of arr) {
        if (await page.locator(sel).count()) return sel;
      }
      return null;
    };

    const email = await pick(emailSel);
    const pass = await pick(passSel);

    if (email && pass) {
      await page.fill(email, 'admin@example.com').catch(() => {});
      await page.fill(pass, '123456').catch(() => {});
      const btn = page.locator('button:has-text("Log"), button:has-text("Sign"), button[type="submit"]');
      if (await btn.count()) {
        await btn.first().click().catch(() => {});
        await page.waitForTimeout(3000);
      }
    } else {
      result.status = 'partial';
      result.notes.push('Taiga login form not found or backend unavailable; captured discover page as dashboard.');
    }

    await page.goto('http://127.0.0.1:9063/discover', { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
    await safeScreenshot(page, path.join(outDir, '03-dashboard.png'));
  } catch (e) {
    result.status = 'partial';
    result.notes.push(`Taiga capture error: ${String(e.message || e)}`);
    try {
      await safeScreenshot(page, path.join(outDir, '03-dashboard.png'));
    } catch {}
  } finally {
    await context.close();
  }

  return result;
}

async function captureZulip(browser) {
  const solution = 'zulip';
  const outDir = path.join(OUT_ROOT, solution);
  ensureDir(outDir);
  const context = await browser.newContext({ viewport: { width: 1600, height: 1000 } });
  const page = await context.newPage();
  const result = { solution, status: 'ok', notes: [] };

  try {
    await page.goto('http://127.0.0.1:9064/', { waitUntil: 'networkidle', timeout: 60000 });
    await safeScreenshot(page, path.join(outDir, '01-runtime.png'));

    await page.goto('http://127.0.0.1:9064/login/', { waitUntil: 'networkidle', timeout: 60000 });
    await safeScreenshot(page, path.join(outDir, '02-login.png'));

    const creds = [
      { username: 'admin@example.com', password: '123456' },
      { username: 'user9@example.com', password: '123456' },
    ];

    let loggedIn = false;
    for (const cred of creds) {
      if (await page.locator('#id_username').count()) {
        await page.fill('#id_username', cred.username).catch(() => {});
      }
      if (await page.locator('#id_password').count()) {
        await page.fill('#id_password', cred.password).catch(() => {});
      }

      const submitBtn = page.locator('form#login_form button[type="submit"], button[type="submit"]');
      if (await submitBtn.count()) {
        await Promise.all([
          page.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {}),
          submitBtn.first().click(),
        ]);
      }
      await page.waitForTimeout(4000);

      const current = page.url();
      if (!current.includes('/login') && !current.includes('/accounts/login')) {
        loggedIn = true;
        break;
      }
    }

    if (!loggedIn) {
      result.status = 'partial';
      result.notes.push('Zulip login did not transition to dashboard URL.');
    }

    await safeScreenshot(page, path.join(outDir, '03-dashboard.png'));
  } catch (e) {
    result.status = 'failed';
    result.notes.push(`Zulip capture error: ${String(e.message || e)}`);
    try {
      await safeScreenshot(page, path.join(outDir, '03-dashboard.png'));
    } catch {}
  } finally {
    await context.close();
  }

  return result;
}

(async () => {
  ensureDir(OUT_ROOT);
  const browser = await chromium.launch({ headless: true });
  const results = [];

  try {
    results.push(await captureOdoo(browser));
    results.push(await captureERPNext(browser));
    results.push(await captureTryton(browser));
    results.push(await captureTaiga(browser));
    results.push(await captureZulip(browser));
  } finally {
    await browser.close();
  }

  const summary = {
    captured_at: new Date().toISOString(),
    mode: 'official-product-ui',
    results,
  };

  fs.writeFileSync(path.join(OUT_ROOT, 'summary.json'), JSON.stringify(summary, null, 2), 'utf-8');
  console.log('[done] captures_official/summary.json');
})();
