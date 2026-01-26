---
title: Home
---

<script>
  // Redirect to language-specific homepage based on localStorage
  const savedLocale = localStorage.getItem("locale") || "en-US";
  const lang = savedLocale.split("-")[0];
  window.location.href = `/${lang}/`;
</script>

Redirecting to your language preference...

If you're not redirected:
- [English](en/)
- [Deutsch](de/)
