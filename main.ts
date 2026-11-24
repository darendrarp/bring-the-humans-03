// Bring the humans with a TikTok ad — a make.fun entry (Node 22, standard
// library only). The entry itself is the video: my agent made an original
// vertical ad for make.fun in this session — a first-person hook ("My AI
// agent makes real money"), nine seconds of BOUNTY RUSH, a tiny arcade game
// the agent built and filmed on autopilot, what make.fun is and its $500
// prize table, and a call to action — with make.fun's brand badge from the
// first frame and the referral end card carrying the entrant's referral
// code. The video is posted publicly on TikTok; VIDEO.json at this
// repository's root names its address, and that is what the house reads
// and scores (views alone). The rendered video is
// video/bring-the-humans-03-final.mp4 (24 s, 1080x1920).
//
// This program's whole job is to hand VIDEO.json to the grader: it copies
// the file from the repository root into the output directory, byte for
// byte, and exits 0. Nothing it writes about the video is scored — the
// house reads the video itself from TikTok.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
// Outside the grader, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand in for
// the /bot and /output directories the sandbox provides.

import { copyFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = join(botDir, 'VIDEO.json');

// The video's address must be a TikTok video URL: a full
// /@<handle>/video/<digits> address, never a short link or a photo post.
const VIDEO_URL = /^https:\/\/(www\.|m\.)?tiktok\.com\/@[^/]+\/video\/\d+\/?$/;

if (!existsSync(source)) {
  console.error(`VIDEO.json not found in ${botDir}; nothing to hand in.`);
  process.exit(1);
}

const raw = readFileSync(source, 'utf8');
// The scorer's video_file check caps VIDEO.json at 16384 bytes.
if (Buffer.byteLength(raw, 'utf8') > 16384) {
  console.error('VIDEO.json is over the 16384-byte cap.');
  process.exit(1);
}
let parsed;
try {
  parsed = JSON.parse(raw);
} catch {
  console.error('VIDEO.json is not valid JSON.');
  process.exit(1);
}
if (typeof parsed !== 'object' || parsed === null || typeof parsed.url !== 'string'
    || !VIDEO_URL.test(parsed.url)) {
  console.error('VIDEO.json does not name a TikTok video URL.');
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'VIDEO.json');
copyFileSync(source, dest);
// Verify the copy is byte-identical before reporting success.
if (readFileSync(dest, 'utf8') !== raw) {
  console.error('VIDEO.json copy does not match the source.');
  process.exit(1);
}
