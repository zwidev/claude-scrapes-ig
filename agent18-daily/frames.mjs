// Render the board to board.mp4 frames (30 fps, 11.5 s). Usage: node frames.mjs card.json outdir
import { chromium } from 'playwright';
import fs from 'fs'; import path from 'path';
const [cardPath, out] = [process.argv[2] || 'card.json', process.argv[3] || 'bf'];
fs.mkdirSync(out, { recursive: true });
const data = JSON.parse(fs.readFileSync(cardPath, 'utf8'));
const b = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium' });
const p = await b.newPage({ viewport: { width: 1080, height: 960 } });
await p.addInitScript(d => { window.DATA = d; }, data);
await p.goto('file://' + path.resolve(path.dirname(new URL(import.meta.url).pathname), 'board.html'));
await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
for (let f = 0; f < 345; f++) {
  await p.evaluate(t => window.render(t), f / 30);
  await p.screenshot({ path: `${out}/${String(f).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 92 });
}
await b.close(); console.log('frames 345 ->', out);
