// Initialize from localStorage or default
const savedLocale = localStorage.getItem("locale") || "en-US"
document.documentElement.setAttribute("saved-locale", savedLocale)

// Emit locale change event
const emitLocaleChangeEvent = (locale: string) => {
  const event = new CustomEvent("localechange", {
    detail: { locale },
  })
  document.dispatchEvent(event)
}

document.addEventListener("nav", () => {
  const switchLanguage = (e: Event) => {
    const currentLocale = document.documentElement.getAttribute("saved-locale") || "en-US"
    const targetLocale = currentLocale === "en-US" ? "de-DE" : "en-US"
    const targetLang = targetLocale.split("-")[0] // "en" or "de"

    // Get translation mapping from button data
    const button = e.currentTarget as HTMLElement
    const translationsStr = button.getAttribute("data-translations") || "{}"
    const translations = JSON.parse(translationsStr)

    // Find target slug - only use explicit translation mapping
    const targetSlug = translations[targetLang] || `${targetLang}/index`

    // Update locale preference
    document.documentElement.setAttribute("saved-locale", targetLocale)
    localStorage.setItem("locale", targetLocale)
    emitLocaleChangeEvent(targetLocale)

    // Force page reload to rebuild Explorer with new language filter
    // SPA navigation doesn't trigger Explorer rebuild, so we use full reload
    window.location.href = new URL(targetSlug, window.location.origin).href
  }

  // Attach click handlers to all language switcher buttons
  const buttons = document.getElementsByClassName("language-switcher")
  for (const button of buttons) {
    button.addEventListener("click", switchLanguage)
    window.addCleanup(() => button.removeEventListener("click", switchLanguage))
  }
})
