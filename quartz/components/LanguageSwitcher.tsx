// @ts-ignore
import languageSwitcherScript from "./scripts/languageSwitcher.inline"
import styles from "./styles/languageSwitcher.scss"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { i18n } from "../i18n"
import { classNames } from "../util/lang"

const LanguageSwitcher: QuartzComponent = ({
  displayClass,
  cfg,
  fileData,
}: QuartzComponentProps) => {
  const translations = fileData.frontmatter?.translations || {}
  const currentSlug = fileData.slug || ""

  return (
    <button
      class={classNames(displayClass, "language-switcher")}
      data-translations={JSON.stringify(translations)}
      data-current-slug={currentSlug}
      aria-label={i18n(cfg.locale).components.languageSwitcher.switchTo}
    >
      <span class="lang-icon lang-en" aria-label="English">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="28" height="14">
          <clipPath id="s">
            <path d="M0,0 v30 h60 v-30 z" />
          </clipPath>
          <clipPath id="t">
            <path d="M30,15 h30 v15 z v-30 h-30 z h-30 v15 z v-30 h30 z" />
          </clipPath>
          <g clip-path="url(#s)">
            <path d="M0,0 v30 h60 v-30 z" fill="#012169" />
            <path d="M0,0 L60,30 M60,0 L0,30" stroke="#fff" stroke-width="6" />
            <path d="M0,0 L60,30 M60,0 L0,30" clip-path="url(#t)" stroke="#C8102E" stroke-width="4" />
            <path d="M30,0 v30 M0,15 h60" stroke="#fff" stroke-width="10" />
            <path d="M30,0 v30 M0,15 h60" stroke="#C8102E" stroke-width="6" />
          </g>
        </svg>
      </span>
      <span class="lang-icon lang-de" aria-label="Deutsch">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 5 3" width="28" height="17">
          <rect width="5" height="3" fill="#000" />
          <rect width="5" height="2" y="1" fill="#D00" />
          <rect width="5" height="1" y="2" fill="#FFCE00" />
        </svg>
      </span>
    </button>
  )
}

LanguageSwitcher.beforeDOMLoaded = languageSwitcherScript
LanguageSwitcher.css = styles

export default (() => LanguageSwitcher) satisfies QuartzComponentConstructor
