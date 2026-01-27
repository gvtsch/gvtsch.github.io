import { pathToRoot } from "../util/path"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"
import { i18n } from "../i18n"

const PageTitle: QuartzComponent = ({ fileData, cfg, displayClass }: QuartzComponentProps) => {
  const title = cfg?.pageTitle ?? i18n(cfg.locale).propertyDefaults.title
  const baseDir = pathToRoot(fileData.slug!)

  // Determine language-specific home page
  const slug = fileData.slug!
  let homeLink = baseDir

  // Ensure baseDir ends with a slash
  const base = baseDir.endsWith("/") ? baseDir : baseDir + "/"

  if (slug.startsWith("en/") || slug === "en") {
    homeLink = base + "en/"
  } else if (slug.startsWith("de/") || slug === "de") {
    homeLink = base + "de/"
  }

  return (
    <h2 class={classNames(displayClass, "page-title")}>
      <a href={homeLink}>{title}</a>
    </h2>
  )
}

PageTitle.css = `
.page-title {
  font-size: 1.75rem;
  margin: 0;
  font-family: var(--titleFont);
}
`

export default (() => PageTitle) satisfies QuartzComponentConstructor
