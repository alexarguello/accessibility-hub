import React, { useState, useRef, useEffect } from 'react';
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

export default function HotTopicsPage() {
  const [reduceMotion, setReduceMotion] = useState(false);
  const [activeFilters, setActiveFilters] = useState([]);
  const topicsListRef = useRef(null);

  const isFiltered = activeFilters.length > 0;

  const visibleTopics = isFiltered
    ? topics.filter(topic => activeFilters.includes(topic.type))
    : topics;

  // Compose filter context description
  const filterContext = isFiltered
    ? `Filtered by: ${activeFilters.map(type => type.charAt(0).toUpperCase() + type.slice(1)).join(', ')}`
    : 'Showing all topics';

  // Focus management after filtering
  useEffect(() => {
    if (topicsListRef.current) {
      topicsListRef.current.focus();
    }
  }, [activeFilters]);

  const toggleFilter = (type) => {
    setActiveFilters(prev =>
      prev.includes(type) ? prev.filter(t => t !== type) : [...prev, type]
    );
  };

  return (
    <main className={styles.hotTopics} role="main" aria-label="Hot Topics in Accessibility and AI">
      <div className={styles.container}>
        <h1 className={styles.header}>
          🔥 <span className={styles.hotWord}>Hot</span> Topics in Accessibility & AI
        </h1>
        <p>Click a tag to learn more. You can also filter by category below.</p>

        <button
          onClick={() => setReduceMotion(prev => !prev)}
          aria-pressed={reduceMotion}
          aria-label="Toggle reduced motion for animations"
          className={styles.motionToggle}
        >
          {reduceMotion ? 'Enable Animations' : 'Reduce Motion'}
          <span className={styles.srOnly}>
            {reduceMotion
              ? 'Animations are currently reduced. Click to enable animations.'
              : 'Animations are currently enabled. Click to reduce motion.'}
          </span>
        </button>

        {/* 🪧 Filter Buttons */}
        <div role="group" aria-label="Filter topics by category" className={styles.filterGroup}>
          <span className={styles.srOnly} id="filter-group-desc">
            Use these buttons to filter topics by category.
          </span>
          {types.map(type => (
            <button
              key={type}
              onClick={() => toggleFilter(type)}
              aria-pressed={activeFilters.includes(type)}
              className={`${styles.filterButton} ${styles[`${type}Legend`]} ${activeFilters.includes(type) ? styles.active : styles.inactive}`}
            >
              {activeFilters.includes(type) && <span aria-hidden="true" style={{ textDecoration: 'underline', fontWeight: 'bold' }}>&#10003; </span>}
              {type === 'tool' && '🧰 Tool'}
              {type === 'concept' && '🎓 Concept'}
              {type === 'protocol' && '📜 Protocol'}
              {type === 'use' && '🏠 Use Case'}
            </button>
          ))}
        </div>

        {/* Visually hidden filter context for screen readers */}
        <div id="filter-context" className={styles.srOnly} aria-live="polite">
          {filterContext}
        </div>

        {/* 🧩 Filtered Topic Tags */}
        <ul
          className={`${styles.topicsGrid} ${reduceMotion ? styles.reduceMotion : ''}`}
          aria-describedby="filter-context"
          tabIndex="-1"
          ref={topicsListRef}
          role="list"
        >
          {visibleTopics.map((topic, i) => (
            <li key={i} role="listitem">
              <Link
                to={topic.link}
                tabIndex={0}
                className={`${styles.topicTag} ${styles[`topic-${topic.type}`]}`}
                aria-label={`Topic: ${topic.label}, Category: ${topic.type}`}
              >
                {topic.label}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}
