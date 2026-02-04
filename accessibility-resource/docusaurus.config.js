// @ts-check
import { themes as prismThemes } from 'prism-react-renderer';
import remarkStripHeadingEmojis from './plugins/remark-strip-heading-emojis.js';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Home',
  tagline: 'A11YHub: Accessibility resources and tools',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://alexarguello.github.io',
  baseUrl: '/accessibility-hub/',

  trailingSlash: true,

  organizationName: 'alexarguello',
  projectName: 'accessibility-hub',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  // ✅ Enable Mermaid plugin
  themes: ['@docusaurus/theme-mermaid'],

  // ✅ Enable Mermaid in Markdown
  markdown: {
    mermaid: true,
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
          remarkPlugins: [
            remarkStripHeadingEmojis,
          ],
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // ✅ Mermaid theme setup
      mermaid: {
        theme: {
          light: 'neutral',
          dark: 'forest',
        },
      },
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Home',
        logo: {
          alt: 'A11YHub Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'About',
          },
          {
            href: 'https://github.com/alexarguello/accessibility-hub',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Explore',
            items: [
              { label: 'Home', to: '/' },
              { label: 'Welcome', to: '/docs' },
              { label: 'Hot Topics', to: '/docs/hot-topics' },
              { label: 'Use Cases', to: '/docs/use-cases' },
              { label: 'Resources', to: '/docs/resources' },
            ],
          },
          {
            title: 'Contribute',
            items: [
              { label: 'How to Contribute', to: '/docs/contribute/contributing' },
              { label: 'Open Issues', href: 'https://github.com/alexarguello/accessibility-hub/issues' },
              { label: 'Propose a Resource', href: 'https://github.com/alexarguello/accessibility-hub/issues/new' },
              { label: 'Frontmatter Guide', to: '/docs/community-contributions/FORMATTER_GUIDE' },
              { label: 'Topics Guide', to: '/docs/community-contributions/TOPICS_GUIDE' },
            ],
          },
          {
            title: 'Community',
            items: [
              { label: 'Coming soon', href: '#' },
            ],
          },
          {
            title: 'About',
            items: [
              { label: 'Project Overview', to: '/docs' },
              { label: 'License', to: 'https://github.com/alexarguello/accessibility-hub/blob/main/LICENSE' },
              { label: 'GitHub', href: 'https://github.com/alexarguello/accessibility-hub' },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} A11YHub. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
