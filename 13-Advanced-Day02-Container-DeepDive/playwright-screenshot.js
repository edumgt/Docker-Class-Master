const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  await page.setContent(`
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Playwright Docker Screenshot</title>
        <style>
          :root {
            color-scheme: light;
            --bg: linear-gradient(135deg, #0f172a 0%, #1d4ed8 45%, #93c5fd 100%);
            --card: rgba(255, 255, 255, 0.9);
            --text: #0f172a;
            --muted: #334155;
            --accent: #f59e0b;
          }
          * { box-sizing: border-box; }
          body {
            margin: 0;
            min-height: 100vh;
            display: grid;
            place-items: center;
            font-family: Arial, sans-serif;
            background: var(--bg);
          }
          .card {
            width: min(880px, calc(100vw - 48px));
            padding: 40px;
            border-radius: 24px;
            background: var(--card);
            box-shadow: 0 24px 80px rgba(15, 23, 42, 0.28);
          }
          h1 {
            margin: 0 0 12px;
            font-size: 48px;
            line-height: 1.05;
            color: var(--text);
          }
          p {
            margin: 0 0 18px;
            font-size: 20px;
            line-height: 1.6;
            color: var(--muted);
          }
          .pill {
            display: inline-block;
            padding: 10px 14px;
            border-radius: 999px;
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--text);
            background: rgba(245, 158, 11, 0.18);
            border: 1px solid rgba(245, 158, 11, 0.45);
          }
        </style>
      </head>
      <body>
        <main class="card">
          <span class="pill">Docker + Playwright</span>
          <h1>Screenshot Captured From a Container</h1>
          <p>The page was rendered inside the official Playwright Docker image.</p>
          <p>This image file is written back into the mounted project directory.</p>
        </main>
      </body>
    </html>
  `);

  await page.screenshot({
    path: '/workspace/13-Advanced-Day02-Container-DeepDive/playwright-screenshot.png',
    fullPage: true,
  });

  await browser.close();
})();
