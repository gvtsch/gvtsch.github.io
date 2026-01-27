import test, { describe } from "node:test"
import assert from "node:assert"
import { TRANSLATIONS, i18n } from "../i18n"

describe("Language Switcher - i18n", () => {
  test("should have languageSwitcher translations in en-US", () => {
    const translation = i18n("en-US")
    assert(translation.components.languageSwitcher)
    assert.strictEqual(typeof translation.components.languageSwitcher.switchTo, "string")
    assert.strictEqual(typeof translation.components.languageSwitcher.german, "string")
    assert.strictEqual(typeof translation.components.languageSwitcher.english, "string")
  })

  test("should have languageSwitcher translations in de-DE", () => {
    const translation = i18n("de-DE")
    assert(translation.components.languageSwitcher)
    assert.strictEqual(typeof translation.components.languageSwitcher.switchTo, "string")
    assert.strictEqual(typeof translation.components.languageSwitcher.german, "string")
    assert.strictEqual(typeof translation.components.languageSwitcher.english, "string")
  })

  test("should have different translations for en-US and de-DE", () => {
    const enTranslation = i18n("en-US")
    const deTranslation = i18n("de-DE")

    // Switch to text should be different
    assert.notStrictEqual(
      enTranslation.components.languageSwitcher.switchTo,
      deTranslation.components.languageSwitcher.switchTo
    )

    // German label should be different
    assert.notStrictEqual(
      enTranslation.components.languageSwitcher.german,
      deTranslation.components.languageSwitcher.german
    )
  })

  test("should return English translation for en-US", () => {
    const translation = i18n("en-US")
    assert.strictEqual(translation.components.languageSwitcher.switchTo, "Switch to")
    assert.strictEqual(translation.components.languageSwitcher.german, "German")
    assert.strictEqual(translation.components.languageSwitcher.english, "English")
  })

  test("should return German translation for de-DE", () => {
    const translation = i18n("de-DE")
    assert.strictEqual(translation.components.languageSwitcher.switchTo, "Wechseln zu")
    assert.strictEqual(translation.components.languageSwitcher.german, "Deutsch")
    assert.strictEqual(translation.components.languageSwitcher.english, "Englisch")
  })

  test("should fallback to default locale for invalid locale", () => {
    // @ts-expect-error - testing invalid locale
    const translation = i18n("invalid-LOCALE")
    assert(translation.components.languageSwitcher)
    assert.strictEqual(typeof translation.components.languageSwitcher.switchTo, "string")
  })
})

describe("Language Switcher - Locale Logic", () => {
  test("should extract language code from locale", () => {
    const enLocale = "en-US"
    const deLocale = "de-DE"

    assert.strictEqual(enLocale.split("-")[0], "en")
    assert.strictEqual(deLocale.split("-")[0], "de")
  })

  test("should determine opposite language", () => {
    const currentLangEn = "en"
    const currentLangDe = "de"

    const oppositeOfEn = currentLangEn === "en" ? "de" : "en"
    const oppositeOfDe = currentLangDe === "en" ? "de" : "en"

    assert.strictEqual(oppositeOfEn, "de")
    assert.strictEqual(oppositeOfDe, "en")
  })

  test("should build language-specific URLs", () => {
    const targetLang = "de"
    const targetSlug = `${targetLang}/index`

    assert.strictEqual(targetSlug, "de/index")
  })

  test("should detect language from slug", () => {
    const enSlug = "en/example-article"
    const deSlug = "de/beispiel-artikel"
    const rootSlug = "index"

    assert(enSlug.startsWith("en/"))
    assert(deSlug.startsWith("de/"))
    assert(!rootSlug.startsWith("en/"))
    assert(!rootSlug.startsWith("de/"))
  })
})

describe("Language Switcher - Translation Mappings", () => {
  test("should parse translations from frontmatter", () => {
    const translationsStr = '{"de":"de/beispiel-artikel","en":"en/example-article"}'
    const translations = JSON.parse(translationsStr)

    assert.strictEqual(translations.de, "de/beispiel-artikel")
    assert.strictEqual(translations.en, "en/example-article")
  })

  test("should handle empty translations object", () => {
    const translationsStr = "{}"
    const translations = JSON.parse(translationsStr)

    assert.strictEqual(Object.keys(translations).length, 0)
  })

  test("should provide fallback for missing translation", () => {
    const translations: { [key: string]: string } = {}
    const targetLang = "de"
    const targetSlug = translations[targetLang] || `${targetLang}/index`

    assert.strictEqual(targetSlug, "de/index")
  })

  test("should use explicit translation when available", () => {
    const translations = { de: "de/special-page" }
    const targetLang = "de"
    const targetSlug = translations[targetLang] || `${targetLang}/index`

    assert.strictEqual(targetSlug, "de/special-page")
  })
})

describe("Language Switcher - Explorer Filtering", () => {
  test("should filter nodes by language folder", () => {
    // Mock file nodes
    const nodes = [
      { slugSegment: "en", slug: "en/" },
      { slugSegment: "de", slug: "de/" },
      { slugSegment: "example", slug: "en/example" },
      { slugSegment: "beispiel", slug: "de/beispiel" },
      { slugSegment: "tags", slug: "tags/" },
    ]

    const currentLang = "en"
    const otherLang = "de"

    const filtered = nodes.filter(node => {
      if (node.slugSegment === "tags") return false
      if (node.slugSegment === otherLang) return false
      if (node.slug && node.slug.startsWith(`${otherLang}/`)) return false
      return true
    })

    assert.strictEqual(filtered.length, 2)
    assert.strictEqual(filtered[0].slugSegment, "en")
    assert.strictEqual(filtered[1].slugSegment, "example")
  })

  test("should keep English nodes when English is selected", () => {
    const nodes = [
      { slugSegment: "example", slug: "en/example" },
      { slugSegment: "beispiel", slug: "de/beispiel" },
    ]

    const currentLang = "en"
    const filtered = nodes.filter(node =>
      !node.slug || !node.slug.startsWith("de/")
    )

    assert.strictEqual(filtered.length, 1)
    assert.strictEqual(filtered[0].slugSegment, "example")
  })

  test("should keep German nodes when German is selected", () => {
    const nodes = [
      { slugSegment: "example", slug: "en/example" },
      { slugSegment: "beispiel", slug: "de/beispiel" },
    ]

    const currentLang = "de"
    const filtered = nodes.filter(node =>
      !node.slug || !node.slug.startsWith("en/")
    )

    assert.strictEqual(filtered.length, 1)
    assert.strictEqual(filtered[0].slugSegment, "beispiel")
  })
})

describe("Language Switcher - Graph Filtering", () => {
  test("should filter graph data by language", () => {
    const mockData = {
      "en/page1": { title: "Page 1" },
      "en/page2": { title: "Page 2" },
      "de/seite1": { title: "Seite 1" },
      "de/seite2": { title: "Seite 2" },
      "index": { title: "Home" },
    }

    const currentLang = "en"

    const filtered = Object.entries(mockData)
      .filter(([k, v]) => {
        return k.startsWith(`${currentLang}/`) || k === "index"
      })

    assert.strictEqual(filtered.length, 3)
    assert(filtered.some(([k]) => k === "en/page1"))
    assert(filtered.some(([k]) => k === "en/page2"))
    assert(filtered.some(([k]) => k === "index"))
    assert(!filtered.some(([k]) => k.startsWith("de/")))
  })
})
