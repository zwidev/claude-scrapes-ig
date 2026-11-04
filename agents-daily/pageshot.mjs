// Screenshot an agent's live marketplace page for the monitor in the squint frame. Usage: node pageshot.mjs agent.json out.png
// Chromium here doesn't trust the egress proxy CA, so every request is fetched by Playwright and fulfilled.
import { chromium } from 'playwright'; import fs from 'fs';
const a = JSON.parse(fs.readFileSync(process.argv[2] || 'agent.json', 'utf8'));
const b = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium' });
const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, colorScheme: 'dark' });
await ctx.route('**/*', async r => { try { r.fulfill({ response: await r.fetch() }); } catch { r.abort(); } });
const p = await ctx.newPage();
await p.goto(a.url, { waitUntil: 'networkidle', timeout: 60000 });
await p.waitForTimeout(800);
await p.screenshot({ path: process.argv[3] || 'screen.png' });
await b.close(); console.log('screen ->', process.argv[3] || 'screen.png');
