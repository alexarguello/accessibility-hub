import React, { useState } from 'react';
import Link from '@docusaurus/Link';
import styles from './HotTopics.module.css';

const topics = [
  { label: 'Alt Text AI', type: 'tool', link: '/docs/hot-topics/alt-text-ai' },
  { label: 'Voice Navigation', type: 'tool', link: '/docs/hot-topics/voice-navigation' },
  { label: 'Real-time Captions', type: 'tool', link: '/docs/hot-topics/real-time-captions' },
  { label: 'Screen Readers', type: 'tool', link: '/docs/for-users/by-disability-type/vision/screen-readers' },
  { label: 'NLP Assist', type: 'concept', link: '/docs/hot-topics/nlp-assist' },
  { label: 'Accessibility Audit', type: 'protocol', link: '/docs/hot-topics/accessibility-audit' },
  { label: 'Color Contrast', type: 'concept', link: '/docs/hot-topics/color-contrast' },
  { label: 'ARIA Roles', type: 'concept', link: '/docs/hot-topics/aria-roles' },
  { label: 'Inclusive Design', type: 'concept', link: '/docs/hot-topics/inclusive-design' },
  { label: 'Seeing AI', type: 'tool', link: '/docs/hot-topics/seeing-ai' },
  { label: 'Otter.ai', type: 'tool', link: '/docs/hot-topics/otter-ai' },
  { label: 'GitHub Access Tools', type: 'tool', link: '/docs/hot-topics/github-access-tools' },
  { label: 'Accessibility Testing', type: 'protocol', link: '/docs/hot-topics/accessibility-testing' },
  { label: 'SpringAI Assistive', type: 'tool', link: '/docs/hot-topics/springai-assistive' },
  { label: 'LangChain4J Tools', type: 'tool', link: '/docs/hot-topics/langchain4j-tools' },
  { label: 'Smart Homes', type: 'use', link: '/docs/hot-topics/smart-homes' },
  { label: 'Dyslexia Support', type: 'concept', link: '/docs/hot-topics/dyslexia-support' },
  { label: 'Bug Bounty', type: 'protocol', link: '/docs/hot-topics/bug-bounty' },
];
const types = ['tool', 'concept', 'protocol', 'use'];

// Category emoji and label mappings
const categoryEmojis = {
  tool: '🧰',
  concept: '🎓',
  protocol: '📜',
  use: '🏠',
};
const categoryText = {
  tool: 'Tool',
  concept: 'Concept',
  protocol: 'Protocol',
  use: 'Use Case',
};

export default function HotTopicsPage() {
  const [reduceMotion, setReduceMotion] = useState(false);
  const [activeFilters, setActiveFilters] = useState([]);

  const isFiltered = activeFilters.length > 0;

  const visibleTopics = isFiltered
      ? topics.filter(topic => activeFilters.includes(topic.type))
      : topics;

  // Compose filter status — visible to all users, announced by screen readers via aria-live
  const filterContext = isFiltered
      ? `Showing ${visibleTopics.length} of ${topics.length} topics. Filtered by: ${activeFilters.map(type => categoryText[type]).join(', ')}`
      : `Showing all ${topics.length} topics`;

  const toggleFilter = (type) => {
    setActiveFilters(prev =>
        prev.includes(type) ? prev.filter(t => t !== type) : [...prev, type]
    );
  };

  return (
      <main className={styles.hotTopics} role="main" aria-label="Hot Topics in Accessibility and AI">
        <div className={styles.container}>
          <h1 className={styles.header}>
            <span className={styles.hotWord}>Hot</span> Topics in Accessibility & AI
          </h1>
          <p>Click a tag to learn more. You can also filter by category below.</p>

          {/* Legend for category types */}
          <ul className={styles.categoryLegend}>
            {types.map(type => (
                <li key={type} className={styles.categoryLegendItem}>
                  <span aria-hidden="true" className={styles.legendEmoji}>{categoryEmojis[type]}</span>
                  <span className={styles.legendText}>{categoryText[type]}</span>
                </li>
            ))}
          </ul>

          {/* Filter Buttons */}
          <div role="group" aria-label="Filter topics by category" className={styles.filterGroup}>
            {types.map(type => (
                <button
                    key={type}
                    onClick={() => toggleFilter(type)}
                    aria-pressed={activeFilters.includes(type)}
                    className={`${styles.filterButton} ${styles[`${type}Legend`]} ${activeFilters.includes(type) ? styles.active : styles.inactive}`}
                    aria-label={`Filter by category: ${categoryText[type]}`}
                >
                  {activeFilters.includes(type) && (
                      <span aria-hidden="true" style={{ textDecoration: 'underline', fontWeight: 'bold' }}>&#10003; </span>
                  )}
                  <span aria-hidden="true" className={styles.filterEmoji}>{categoryEmojis[type]}</span>{' '}
                  <span className={styles.filterText}>{categoryText[type]}</span>
                </button>
            ))}
          </div>

          {/* Filter status — visible to all, announced to screen readers on change */}
          <div id="filter-context" className={styles.filterStatus} aria-live="polite" aria-atomic="true">
            {filterContext}
          </div>

          {/* Topic Tags */}
          <ul
              className={`${styles.topicsGrid} ${reduceMotion ? styles.reduceMotion : ''}`}
              aria-describedby="filter-context"
              role="list"
          >
            {visibleTopics.map((topic, i) => (
                <li key={i} role="listitem">
                  <Link
                      to={topic.link}
                      className={`${styles.topicTag} ${styles[`topic-${topic.type}`]}`}
                      aria-label={`${categoryText[topic.type]}: ${topic.label}`}
                  >
                    <span className={styles.topicLabel}>{topic.label}</span>
                    <span aria-hidden="true" className={styles.topicEmoji}>{categoryEmojis[topic.type]}</span>
                  </Link>
                </li>
            ))}
          </ul>
        </div>
      </main>
  );
}