import React, { useState } from 'react';
import Link from '@docusaurus/Link';
import styles from './HotTopics.module.css';
import config from './hot-topics.config.json';

const { topics } = config;

const types = ['tool', 'concept', 'protocol', 'use'];

const categoryText = {
  tool:     'Tool',
  concept:  'Concept',
  protocol: 'Protocol',
  use:      'Use Case',
};

// Shape + border description mirrors the mermaid visual language.
// Both shape AND border pattern encode the type — never color alone (WCAG 1.4.1).
const shapeDescription = {
  tool:     'rectangle · solid border',
  concept:  'pill · dashed border',
  protocol: 'double border · dotted',
  use:      'flag shape · dashed border',
};

export default function HotTopicsPage() {
  const [activeFilters, setActiveFilters] = useState([]);

  const isFiltered = activeFilters.length > 0;

  const visibleTopics = isFiltered
    ? topics.filter(topic => activeFilters.includes(topic.type))
    : topics;

  const filterContext = isFiltered
    ? `Showing ${visibleTopics.length} of ${topics.length} topics. Filtered by: ${activeFilters.map(type => categoryText[type]).join(', ')}`
    : `Showing all ${topics.length} topics`;

  const toggleFilter = (type) => {
    setActiveFilters(prev =>
      prev.includes(type) ? prev.filter(t => t !== type) : [...prev, type]
    );
  };

  const hasActiveFilter = activeFilters.length > 0;

  return (
    <main className={styles.hotTopics} role="main" aria-label="Hot Topics in Accessibility and AI">
      <div className={styles.container}>
        {/* Breadcrumb — prevents this page from being a navigation dead-end */}
        <nav aria-label="Breadcrumb" className={styles.breadcrumb}>
          <Link to="/">← Home</Link>
        </nav>

        <h1 className={styles.header}>
          <span className={styles.hotWord}>Hot</span> Topics in Accessibility &amp; AI
        </h1>
        <p>Click a topic to learn more. Filter by category — button shape and border match the card style.</p>

        {/* Filter Buttons — also serve as the visual legend for card shapes */}
        <div role="group" aria-label="Filter topics by category" className={styles.filterGroup}>
          {types.map(type => (
            <button
              key={type}
              onClick={() => toggleFilter(type)}
              aria-pressed={activeFilters.includes(type)}
              className={[
                styles.filterButton,
                styles[`${type}Filter`],
                activeFilters.includes(type) ? styles.active : '',
                hasActiveFilter && !activeFilters.includes(type) ? styles.inactive : '',
              ].filter(Boolean).join(' ')}
              aria-label={`Filter by ${categoryText[type]} (${shapeDescription[type]})`}
            >
              {activeFilters.includes(type) && (
                <span aria-hidden="true" className={styles.filterCheck}>&#10003;</span>
              )}
              <span className={styles.filterText}>{categoryText[type]}</span>
            </button>
          ))}
        </div>

        {/* Filter status — visible to all, announced by screen readers on change */}
        <div id="filter-context" className={styles.filterStatus} aria-live="polite" aria-atomic="true">
          {filterContext}
        </div>

        {/* Topic Cards */}
        <ul
          className={styles.topicsGrid}
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
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}