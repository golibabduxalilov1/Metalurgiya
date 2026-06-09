const puppeteer = require('puppeteer-core');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--no-sandbox', '--window-size=1440,1000'],
    defaultViewport: { width: 1440, height: 1000 },
  });
  const page = await browser.newPage();
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  page.on('pageerror', err => errors.push('pageerror: ' + err.message));

  await page.goto('http://localhost:5175/', { waitUntil: 'networkidle2' });
  await new Promise(r => setTimeout(r, 1500));

  const hasLogin = await page.$('input[type="password"]');
  if (hasLogin) {
    const userInput = await page.$('input[type="text"], input[name="username"]');
    await userInput.type('test');
    const passInput = await page.$('input[type="password"]');
    await passInput.type('Test12345');
    await Promise.all([
      page.click('button[type="submit"]'),
      page.waitForNavigation({ waitUntil: 'networkidle2' }).catch(() => {}),
    ]);
  }
  await new Promise(r => setTimeout(r, 4000));
  await page.screenshot({ path: 'dashboard.png', fullPage: true });
  console.log('URL:', page.url());
  console.log('Console/page errors:', JSON.stringify(errors, null, 2));
  await browser.close();
})();
