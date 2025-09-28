import React from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import '../css/custom.css';

const cards = [
 {
    title: 'Full Resource Map',
    emoji: '🗺️',
    headline: 'Looking for specific topics or an overview?',
    description: 'See all the content at a glance and click to dive right into your preferred topics and tutorials.',
    link: '/docs/full-sitemap',
    bgClass: 'card-bg-blue',
  },
  {
    title: 'Accessibility Guidelines',
    emoji: '📖',
    headline: 'Best practices and standards',
    description: 'Explore WCAG, ARIA, and other accessibility guidelines to make your projects inclusive for everyone.',
    link: '/docs/resources',
    bgClass: 'card-bg-green',
  },
/*
  {
    title: 'Tools & Resources',
    emoji: '🛠️',
    headline: 'Essential tools for accessibility',
    description: 'Discover testing tools, browser extensions, and frameworks that help you build accessible applications.',
    link: '/docs/tools',
    bgClass: 'card-bg-purple',
  },
  {
    title: 'Case Studies',
    emoji: '📚',
    headline: 'Real-world accessibility in action',
    description: 'Learn from organizations and projects that have successfully implemented accessibility best practices.',
    link: '/docs/case-studies',
    bgClass: 'card-bg-yellow',
  },
*/
  {
    title: 'Learning Paths',
    emoji: '🧑‍🎓',
    headline: 'Start your accessibility journey',
    description: 'Follow curated learning paths for beginners and advanced practitioners to master accessibility.',
    link: '/docs/resources/learning-paths',
    bgClass: 'card-bg-red',
  },
    {
      title: 'Frequently Asked Topics',
      emoji: '💡',
      headline: 'Want to dive into the hot topics?',
      description: 'See the most requested topics and jump directly to neural networks, RAG, chatbots, MCP, agents, and more.',
      link: '/hot-topics',
      bgClass: 'card-bg-teal',
    },

];

export default function Home() {
  return (
    <Layout title="Accessibility Resource Hub">
      <div className="homepage">
        <main>
          <div className="homepage__container">
            <h1 className="homepage__title">Find Everything Accessibility</h1>
            <p className="homepage__subtitle">
              Explore, learn, and build inclusive digital experiences for everyone.
            </p>

            <div className="card-grid">
              {cards.map((card, idx) => (
                <Link key={idx} to={card.link} className={`card-link ${card.bgClass}`}>
                  <h2 className="card-title">
                    <div>{card.title} <span aria-hidden="true">{card.emoji}</span> </div>
                  </h2>
                  <p className="card-headline">{card.headline}</p>
                  <p className="card-desc">{card.description}</p>
                </Link>
              ))}
            </div>
          </div>
        </main>
      </div>
    </Layout>
  );
}