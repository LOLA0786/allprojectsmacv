export function loadKeys() {
  const keys = {
    openai: "",
    grok: "",
    gemini: ""
  };

  try {
    if (import.meta.env.OPENAI_KEY_B64) {
      keys.openai = atob(import.meta.env.OPENAI_KEY_B64);
    }
    if (import.meta.env.GROK_KEY_B64) {
      keys.grok = atob(import.meta.env.GROK_KEY_B64);
    }
    if (import.meta.env.GEMINI_KEY_B64) {
      keys.gemini = atob(import.meta.env.GEMINI_KEY_B64);
    }
  } catch (e) {
    console.warn("Error decoding Base64 API keys:", e);
  }

  return keys;
}
