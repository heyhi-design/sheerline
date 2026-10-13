#!/usr/bin/env node
// extract.mjs — HeyHi Design Bridge, Phase T1 extractor.
//
// Loads a ui-studio HTML prototype headless (Chromium via Playwright) and emits
// one schema-valid scene-graph IR per breakpoint (sm 375 / md 768 / lg 1440). The
// IR is the reviewed contract the use_figma Builder (Phase T2) consumes.
//
//   node extract.mjs --prototype <file.html> [--config <brand.json>]
//                    [--out <dir>] [--name <slug>] [--root <selector>]
//                    [--breakpoints sm,md,lg] [--settle <ms>]
//
// Defaults target the bundled golden prototype. See README.md.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright";
import { loadConfig, BrandMap } from "./lib/brand-map.mjs";
import { captureScene } from "./lib/browser-capture.mjs";
import { buildIR } from "./lib/build-ir.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SKILL_DIR = path.resolve(HERE, "..", ".."); // skill-updates/heyhi-design-bridge
const REPO_ROOT = path.resolve(SKILL_DIR, "..", ".."); // worktree root

const BREAKPOINTS = { sm: 375, md: 768, lg: 1440 };
const VIEWPORT_H = 900;

function parseArgs(argv) {
  const a = { breakpoints: "sm,md,lg", root: "body", settle: "350" };
  for (let i = 2; i < argv.length; i++) {
    const k = argv[i];
    if (k.startsWith("--")) a[k.slice(2)] = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : "true";
  }
  return a;
}

async function main() {
  const args = parseArgs(process.argv);

  const prototype = path.resolve(args.prototype || path.join(SKILL_DIR, "examples/prototypes/atlas-reader.html"));
  // Default config. A bundled golden prototype (anything under examples/prototypes/) pairs with
  // the goldens' own fixture brand-config (a neutral example palette), however it is named on
  // the command line. A caller's own prototype defaults to the instance's brand config, named in
  // ui-studio/brand-config/default-config.txt (instance-only, absent in a scaffold export);
  // without it, the same example fixture.
  const fixtureConfig = path.join(SKILL_DIR, "examples/brand-config/example.json");
  const uiStudioConfigs = path.join(REPO_ROOT, "heyhi-skills/ui-studio/brand-config");
  const instanceDefaultFile = path.join(uiStudioConfigs, "default-config.txt");
  const instanceDefault = fs.existsSync(instanceDefaultFile)
    ? path.join(uiStudioConfigs, fs.readFileSync(instanceDefaultFile, "utf8").trim())
    : null;
  const isBundledGolden = prototype.startsWith(path.join(SKILL_DIR, "examples", "prototypes") + path.sep);
  const configPath = path.resolve(
    args.config || (!isBundledGolden && instanceDefault) || fixtureConfig);
  const outDir = path.resolve(args.out || path.join(SKILL_DIR, "examples"));
  const name = args.name || path.basename(prototype).replace(/\.html?$/i, "");
  const brandConfig = args["brand-name"] || path.basename(configPath).replace(/\.json$/i, "");
  const breakpoints = args.breakpoints.split(",").map((s) => s.trim()).filter((b) => BREAKPOINTS[b]);
  const settle = parseInt(args.settle, 10) || 0;
  // meta.source: prototype path relative to the IR output dir, for portability
  const sourceRel = path.relative(outDir, prototype);

  if (!fs.existsSync(prototype)) { console.error(`prototype not found: ${prototype}`); process.exit(2); }
  if (!fs.existsSync(configPath)) { console.error(`brand-config not found: ${configPath}`); process.exit(2); }

  const config = loadConfig(configPath);
  const brandMap = new BrandMap(config, { brandName: brandConfig });
  const brandFamilies = brandMap.fontFamilies.map((f) => f.family);

  fs.mkdirSync(outDir, { recursive: true });
  console.error(`extract: ${path.relative(REPO_ROOT, prototype)} | config ${brandConfig} | breakpoints ${breakpoints.join(",")}`);

  const browser = await chromium.launch();
  const writtenAssets = new Set();
  let lastReport = null;
  try {
    for (const bp of breakpoints) {
      const page = await browser.newPage({ viewport: { width: BREAKPOINTS[bp], height: VIEWPORT_H }, deviceScaleFactor: 1 });
      await page.goto(pathToFileURL(prototype).href, { waitUntil: "networkidle", timeout: 30000 });
      // reference.md §1: await fonts.ready + a layout/network-idle settle before measuring
      await page.evaluate(async () => { try { await document.fonts.ready; } catch {} });
      // Freeze animations/transitions so computed values are sampled at a stable
      // base frame (a live @keyframes opacity/transform would read mid-cycle and
      // make the IR nondeterministic). The freeze <style> is MARKED so the capture
      // skips it when reading DECLARED values — computed values reflect the freeze,
      // but the animation flag is still recovered from the real stylesheet rule.
      await page.evaluate(() => {
        const s = document.createElement("style");
        s.dataset.extractorFreeze = "1";
        s.textContent = "*,*::before,*::after{animation:none !important;transition:none !important;}";
        document.head.appendChild(s);
      });
      if (settle) await page.waitForTimeout(settle);

      const capture = await page.evaluate(captureScene, { rootSelector: args.root, brandFamilies });
      // Gap 1: read every <img src="*.svg"> off disk so the IR builder can emit
      // them as editable VECTORs instead of grey IMAGE placeholders.
      const svgAssets = collectSvgAssets(capture.root, path.dirname(prototype));
      const { ir, assets, missingFonts } = buildIR(capture, brandMap, { source: sourceRel, breakpoint: bp, brandConfig, svgAssets, protoDir: path.dirname(prototype) });

      const irPath = path.join(outDir, `${name}.${bp}.ir.json`);
      fs.writeFileSync(irPath, JSON.stringify(ir, null, 2) + "\n");

      for (const asset of assets) {
        const assetPath = path.join(outDir, asset.file);
        if (writtenAssets.has(assetPath)) continue;
        fs.mkdirSync(path.dirname(assetPath), { recursive: true });
        fs.writeFileSync(assetPath, asset.content + (asset.content.endsWith("\n") ? "" : "\n"));
        writtenAssets.add(assetPath);
      }

      const flagCount = (ir.root.flags || []).length;
      console.error(`  ${bp.padEnd(2)} ${String(BREAKPOINTS[bp]).padStart(4)}px -> ${path.relative(REPO_ROOT, irPath)}  | nodes:${countNodes(ir.root)} tokens:${ir.tokens_used.length} flags:${flagCount} rules:${capture.meta.ruleCount}`);
      lastReport = { flags: ir.root.flags || [], missingFonts, assets };
      await page.close();
    }
  } finally {
    await browser.close();
  }

  if (lastReport) {
    const dnm = lastReport.flags.filter((f) => f.needs_human);
    const gaps = lastReport.flags.filter((f) => !f.needs_human);
    console.error(`\ndoes-not-map flags (${dnm.length}): ${[...new Set(dnm.map((f) => f.feature))].join(", ")}`);
    console.error(`schema-gap flags (${gaps.length}): ${gaps.map((f) => f.feature).join(", ") || "none"}`);
    if (lastReport.missingFonts.length) console.error(`missing fonts: ${lastReport.missingFonts.join(", ")}`);
    console.error(`vector assets: ${lastReport.assets.map((a) => a.file).join(", ") || "none"}`);
  }
}

// Gap 1: walk the capture tree for <img src="*.svg">, resolve each against the
// prototype dir, and read its SVG text. Unreadable refs are skipped (the builder
// then falls back to the IMAGE placeholder + flag, never a silent drop).
function collectSvgAssets(node, baseDir, acc = {}, seen = new Set()) {
  const src = node && node.imgSrc;
  if (src && /\.svg(\?|#|$)/i.test(src) && !seen.has(src)) {
    seen.add(src);
    try {
      const rel = src.replace(/^\.?\//, "").split(/[?#]/)[0];
      acc[src] = fs.readFileSync(path.resolve(baseDir, rel), "utf8");
    } catch { /* leave unread -> IMAGE fallback */ }
  }
  for (const c of (node && node.children) || []) collectSvgAssets(c, baseDir, acc, seen);
  return acc;
}

function countNodes(n) {
  return 1 + (n.children || []).reduce((s, c) => s + countNodes(c), 0);
}

main().catch((e) => { console.error(e); process.exit(1); });
