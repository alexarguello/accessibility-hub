/* File: /src/components/PageBreak.jsx */
import React from 'react';

/**
 * PageBreak component: Use <PageBreak /> in your Markdown/MDX.
 * When printing, this will force a page break.
 */
export default function PageBreak() {
  return <div className="pagebreak" aria-hidden="true" />;
}