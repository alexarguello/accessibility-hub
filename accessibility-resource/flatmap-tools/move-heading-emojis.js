#!/usr/bin/env node
/*
  Move leading emojis in Markdown headings (H1–H6) to the end of the heading line.
  - Processes all .md files under accessibility-hub/docs
  - Only affects headings that begin with one or more emoji clusters
  - Preserves other content and formatting
*/

import fs from 'fs';
import path from 'path';

const ROOT = process.cwd();
const DOCS_DIR = path.resolve(ROOT, 'accessibility-hub', 'docs');

// Regex to match Markdown headings (allow up to 3 leading spaces per CommonMark)
const headingLineRE = /^(\s{0,3}#{1,6}\s+)(.*)$/u;

// Define an emoji cluster that supports ZWJ sequences and variation selectors
// cluster = pictographic + optional VS16 + ( ZWJ + pictographic + optional VS16 )*
const emojiCluster = String.raw`\p{Extended_Pictographic}(?:\uFE0F)?(?:\u200D\p{Extended_Pictographic}(?:\uFE0F)?)*`;
// One or more clusters possibly separated by spaces
const leadingEmojiRE = new RegExp(
  `^(?<emoji>(?:${emojiCluster}\\s*)+)(?<text>.*)$`,
  'u'
);

function moveLeadingEmojisToEnd(line) {
  const m = line.match(headingLineRE);
  if (!m) return { line, changed: false };

  const prefix = m[1];
  const rest = m[2];

  const lm = rest.match(leadingEmojiRE);
  if (!lm) return { line, changed: false };

  const emoji = (lm.groups.emoji || '').trim();
  const text = (lm.groups.text || '').trim();

  // If nothing substantive left after removing emojis, skip
  if (!text) return { line, changed: false };

  // Avoid duplicating if the same emoji sequence is already at the end
  const textNoTrailingSpace = text.replace(/\s+$/u, '');
  if (textNoTrailingSpace.endsWith(emoji)) {
    return { line, changed: false };
  }

  const newRest = `${textNoTrailingSpace} ${emoji}`;
  const newLine = `${prefix}${newRest}`;
  if (newLine !== line) return { line: newLine, changed: true };
  return { line, changed: false };
}

function processContent(content) {
  const eol = content.includes('\r\n') ? '\r\n' : '\n';
  const lines = content.split(/\r?\n/);
  let changed = false;
  let changesInFile = 0;

  const out = lines.map((ln) => {
    const { line, changed: c } = moveLeadingEmojisToEnd(ln);
    if (c) {
      changed = true;
      changesInFile += 1;
    }
    return line;
  });

  return { content: out.join(eol), changed, count: changesInFile };
}

function* walk(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      yield* walk(full);
    } else if (e.isFile() && e.name.toLowerCase().endsWith('.md')) {
      yield full;
    }
  }
}

function main() {
  if (!fs.existsSync(DOCS_DIR)) {
    console.error(`Docs directory not found: ${DOCS_DIR}`);
    process.exit(1);
  }

  let filesScanned = 0;
  let filesChanged = 0;
  let totalChanges = 0;

  for (const file of walk(DOCS_DIR)) {
    filesScanned += 1;
    const original = fs.readFileSync(file, 'utf8');
    const { content, changed, count } = processContent(original);
    if (changed) {
      fs.writeFileSync(file, content, 'utf8');
      filesChanged += 1;
      totalChanges += count;
      console.log(`Updated: ${path.relative(ROOT, file)} (${count} heading(s))`);
    }
  }

  console.log(`\nScan complete. Files scanned: ${filesScanned}, files updated: ${filesChanged}, headings modified: ${totalChanges}`);
}

main();
