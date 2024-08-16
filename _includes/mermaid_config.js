{
  startOnLoad: true,
  theme: window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'default',
  flowchart: {
    curve: 'basis',
    useMaxWidth: true,
    rankSpacing: 40,
    nodeSpacing: 40,
    padding: 5,
    htmlLabels: true
  },
  securityLevel: 'loose'
}
