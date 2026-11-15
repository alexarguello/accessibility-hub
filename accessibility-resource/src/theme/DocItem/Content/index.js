import React from 'react';
import Content from '@theme-original/DocItem/Content';
import Translate from '@docusaurus/Translate';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { useDoc } from '@docusaurus/plugin-content-docs/client';

/**
 * Wraps the doc content to handle pages that have no translation yet.
 *
 * On a translated locale (for example /es/), Docusaurus serves the default-language
 * page when no translation exists, but the page still declares the locale's language.
 * A screen reader would then read English text with Spanish pronunciation
 * (WCAG 3.1.2, Language of Parts). When that happens we mark the content with the
 * default language and tell the reader, in their language, why it is not translated.
 */
export default function ContentWrapper(props) {
  const {
    i18n: { currentLocale, defaultLocale, localeConfigs },
  } = useDocusaurusContext();
  const { metadata } = useDoc();

  // Translated docs are read from the i18n folder; fallbacks come from /docs.
  const isFallback =
    currentLocale !== defaultLocale && !metadata.source.startsWith('@site/i18n/');

  if (!isFallback) {
    return <Content {...props} />;
  }

  const source = localeConfigs[defaultLocale] ?? {};
  return (
    <>
      <p className="untranslated-notice" role="note">
        <Translate
          id="a11yhub.untranslated.notice"
          description="Shown above a page that has no translation in the current language">
          This page is not available in this language yet. It is shown in English.
        </Translate>
      </p>
      <div lang={source.htmlLang ?? defaultLocale} dir={source.direction ?? 'ltr'}>
        <Content {...props} />
      </div>
    </>
  );
}
