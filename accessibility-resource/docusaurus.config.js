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

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  // ✅ Mermaid + broken link hook (onBrokenMarkdownLinks moved here per v4 deprecation)
  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  // ✅ Mermaid theme + search plugin
  themes: [
    '@docusaurus/theme-mermaid',
    [
      '@easyops-cn/docusaurus-search-local',
      {
        hashed: true,
        language: ['en'],
        highlightSearchTermsOnTargetPage: true,
        explicitSearchResultPath: true,
        docsRouteBasePath: 'docs',
        searchBarPosition: 'right',
        indexBlog: false,
        indexPages: true,
      },
    ],
  ],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // ✅ Fixed: points to your actual repo (was pointing to facebook/docusaurus)
          editUrl:
            'https://github.com/alexarguello/accessibility-hub/edit/main/accessibility-resource/',
          showLastUpdateTime: true,
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
          // ✅ Fixed: was duplicating "A11YHub Logo" as both alt text and link text
          alt: 'A11YHub',
          src: 'img/logo.svg',
          href: '/',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'About',
          },
          // ✅ Added: primary sections now reachable from the top nav
          {
            to: '/docs/for-users',
            position: 'left',
            label: 'For Users',
          },
          {
            to: '/docs/for-developers',
            position: 'left',
            label: 'For Developers',
          },
          {
            to: '/docs/hot-topics',
            position: 'left',
            label: 'Hot Topics',
          },
          {
            to: '/docs/resources',
            position: 'left',
            label: 'Resources',
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
              { label: 'How to Contribute', to: '/docs/community-contributions/contributing' },
              { label: 'Open Issues', href: 'https://github.com/alexarguello/accessibility-hub/issues' },
              { label: 'Propose a Resource', href: 'https://github.com/alexarguello/accessibility-hub/issues/new' },
              { label: 'Frontmatter Guide', to: '/docs/community-contributions/FRONTMATTER_GUIDE' },
              { label: 'Topics Guide', to: '/docs/community-contributions/TOPICS_GUIDE' },
            ],
          },
          {
            title: 'Community',
            items: [
              // ✅ Fixed: was href="#" (dead anchor) — now points to real GitHub pages
              {
                label: 'GitHub Discussions',
                href: 'https://github.com/alexarguello/accessibility-hub/discussions',
              },
              {
                label: 'Open an Issue',
                href: 'https://github.com/alexarguello/accessibility-hub/issues/new',
              },
            ],
          },
          {
            title: 'About',
            items: [
              { label: 'Project Overview', to: '/docs' },
              { label: 'License', href: 'https://github.com/alexarguello/accessibility-hub/blob/main/LICENSE' },
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