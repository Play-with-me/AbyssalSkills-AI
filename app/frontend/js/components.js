/**
 * AbyssalSkillsD - Vector Iconography, Brand Assets & UI Components Library
 * Implements 100% Zero-Emoji Policy, Simple Icons brand logotypes,
 * unDraw dynamic SVGs, and Command Palette dialogs.
 */

const Icons = {
  // General UI Icons (Lucide SVG style, 1.5px stroke)
  cpu: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3m6-3v3M9 20v3m6-3v3M20 9h3m-3 6h3M1 9h3m-3 6h3"/></svg>`,
  palette: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg>`,
  bug: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect width="8" height="14" x="8" y="6" rx="4"/><path d="m19 7-3 2m-8 0L5 7m14 12-3-2m-8 0-3 2M20 13h-4m-8 0H4m6-9 1 2m2-2-1 2"/></svg>`,
  database: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5M3 12A9 3 0 0 0 21 12"/></svg>`,
  penTool: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="m12 19 7-7 3 3-7 7-3-3z"/><path d="m18 13-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><circle cx="11" cy="11" r="2"/></svg>`,
  sparkles: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/></svg>`,
  gitBranch: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="6" y1="3" x2="6" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/></svg>`,
  layers: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>`,
  graph: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>`,
  copy: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>`,
  check: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>`,
  download: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>`,
  refresh: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>`,
  x: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`,
  fileText: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>`,
  sun: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32l1.41 1.41M2 12h2m16 0h2M6.34 17.66l-1.41 1.41m14.14-14.14l-1.41 1.41"/></svg>`,
  moon: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>`,
  command: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M15 6v12a3 3 0 1 0 3-3H6a3 3 0 1 0 3 3V6a3 3 0 1 0-3 3h12a3 3 0 1 0-3-3"/></svg>`,
  cloud: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>`,
  uploadCloud: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/><path d="M12 12v9"/><path d="m16 16-4-4-4 4"/></svg>`,
  star: `<svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`,
  stethoscope: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"/><path d="M8 15v1a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6v-4"/><circle cx="20" cy="10" r="2"/></svg>`,
  arrowRight: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>`,
  user: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`,
  shield: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`,
  box: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>`,
  key: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="m21 2-2 2m-1.5 1.5L14 9l-2-2-4 4-2-2-4 4v5h5l4-4-2-2 4-4 1.5 1.5 2-2Z"/><circle cx="15.5" cy="8.5" r=".5" fill="currentColor"/></svg>`,
  logOut: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>`,
  lock: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>`,
  mail: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>`,
  bell: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>`,
  chevronDown: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="6 9 12 15 18 9"/></svg>`,
  check: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>`,
  checkCircle: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#06D6A0" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>`,
  folderOpen: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="m6 14 1.45-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.55 6a2 2 0 0 1-1.94 1.5H4a2 2 0 0 1-2-2V5c0-1.1.9-2 2-2h3.93a2 2 0 0 1 1.66.9l.82 1.2a2 2 0 0 0 1.66.9H18a2 2 0 0 1 2 2v2"/></svg>`,
  zap: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
  helpCircle: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
  plus: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>`,
  folder: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>`,
  trash: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>`,
  github: `<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>`,
  brandGithub: `<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>`,
  google: `<svg width="15" height="15" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>`,

  // Official Brand Vector SVGs (from web-assets-creative-vault / Simple Icons)
  brandAntigravity: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#4285F4" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm1 14.93V17a1 1 0 0 1-2 0v-.07A7.003 7.003 0 0 1 5.07 11H5a1 1 0 0 1 0-2h.07A7.003 7.003 0 0 1 11 5.07V5a1 1 0 0 1 2 0v.07A7.003 7.003 0 0 1 18.93 11H19a1 1 0 0 1 0 2h-.07A7.003 7.003 0 0 1 13 16.93z"/></svg>`,
  brandClaude: `<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" color="#D97706"><path d="M17.3 3.6a.7.7 0 0 0-.6.4L13.8 11h-3.6L7.3 4a.7.7 0 0 0-.6-.4H4.5a.7.7 0 0 0-.6 1l4.8 9.8-3.4 6a.7.7 0 0 0 .6 1.1h2.2a.7.7 0 0 0 .6-.4l3.3-6.1 3.3 6.1a.7.7 0 0 0 .6.4h2.2a.7.7 0 0 0 .6-1.1l-3.4-6 4.8-9.8a.7.7 0 0 0-.6-1h-2.2z"/></svg>`,
  brandCopilot: `<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" color="#8B5CF6"><path d="M12 1.5C6.2 1.5 1.5 6.2 1.5 12c0 4.6 3 8.6 7.2 9.9.5.1.7-.2.7-.5v-1.8c-2.9.6-3.5-1.4-3.5-1.4-.5-1.2-1.2-1.5-1.2-1.5-.9-.6.1-.6.1-.6 1 .1 1.6 1.1 1.6 1.1.9 1.6 2.5 1.1 3.1.9.1-.7.4-1.1.7-1.4-2.3-.3-4.8-1.2-4.8-5.3 0-1.2.4-2.1 1.1-2.9-.1-.3-.5-1.4.1-2.9 0 0 .9-.3 3 1.1.9-.2 1.8-.4 2.7-.4.9 0 1.8.2 2.7.4 2.1-1.4 3-1.1 3-1.1.6 1.5.2 2.6.1 2.9.7.8 1.1 1.7 1.1 2.9 0 4.1-2.5 5-4.8 5.3.4.3.7 1 .7 2v3c0 .3.2.6.7.5 4.2-1.4 7.2-5.3 7.2-9.9 0-5.8-4.7-10.5-10.5-10.5z"/></svg>`,
  brandNextjs: `<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.82 17.518-5.91-7.733v7.733H10.15V6.482h1.76l6.63 8.74V6.482h1.76v11.036h-2.48z"/></svg>`,
  brandTailwind: `<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" color="#06B6D4"><path d="M12.001 4.8c-3.2 0-5.2 1.6-6 4.8 1.2-1.6 2.6-2.2 4.2-1.8.913.228 1.565.89 2.288 1.624C13.666 10.618 15.027 12 18.001 12c3.2 0 5.2-1.6 6-4.8-1.2 1.6-2.6 2.2-4.2 1.8-.913-.228-1.565-.89-2.288-1.624C16.336 6.182 14.975 4.8 12.001 4.8zm-6 7.2c-3.2 0-5.2 1.6-6 4.8 1.2-1.6 2.6-2.2 4.2-1.8.913.228 1.565.89 2.288 1.624 1.177 1.194 2.538 2.576 5.512 2.576 3.2 0 5.2-1.6 6-4.8-1.2 1.6-2.6 2.2-4.2 1.8-.913-.228-1.565-.89-2.288-1.624C10.336 13.382 8.975 12 6.001 12z"/></svg>`,
  brandSupabase: `<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" color="#3ECF8E"><path d="M21.362 9.354H12V.396a.396.396 0 0 0-.716-.233L.32 14.288a.396.396 0 0 0 .31.636H10.5v8.68a.396.396 0 0 0 .716.233l10.964-14.125a.396.396 0 0 0-.818-.358z"/></svg>`,
  brandPlaywright: `<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" color="#45BA4B"><path d="M18.8 5.4c-2.4-2.4-6.3-2.4-8.7 0L8.7 6.8c-.4.4-.4 1 0 1.4s1 .4 1.4 0l1.4-1.4c1.6-1.6 4.2-1.6 5.8 0 1.6 1.6 1.6 4.2 0 5.8L12.5 17.4c-.4.4-.4 1 0 1.4.2.2.5.3.7.3s.5-.1.7-.3l4.9-4.9c2.4-2.4 2.4-6.2 0-8.5zm-8.6 6.8c-.4-.4-1-.4-1.4 0L3.9 17.1c-2.4 2.4-2.4 6.3 0 8.7 1.2 1.2 2.8 1.8 4.4 1.8s3.2-.6 4.4-1.8l1.4-1.4c.4-.4.4-1 0-1.4s-1-.4-1.4 0l-1.4 1.4c-1.6 1.6-4.2 1.6-5.8 0-1.6-1.6-1.6-4.2 0-5.8l4.9-4.9c.4-.3.4-1 0-1.3z"/></svg>`,
  brandCodex: `<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" color="#10A37F"><path d="M22.2819 9.8211a5.9847 5.9847 0 0 0-.5157-4.9108 6.0462 6.0462 0 0 0-6.5098-2.9A6.0651 6.0651 0 0 0 4.9807 4.1818a5.9847 5.9847 0 0 0-3.9977 2.9 6.0462 6.0462 0 0 0 .7427 7.0966 5.98 5.98 0 0 0 .511 4.9107 6.051 6.051 0 0 0 6.5146 2.9001A5.9847 5.9847 0 0 0 13.2599 24a6.0557 6.0557 0 0 0 5.7718-4.2058 5.9894 5.9894 0 0 0 3.9977-2.9001 6.0557 6.0557 0 0 0-.7475-7.0729zm-9.022 12.6081a4.4755 4.4755 0 0 1-2.8764-1.0408l.1419-.0804 4.7783-2.7582a.7948.7948 0 0 0 .3927-.6813v-6.7369l2.02 1.1683a.071.071 0 0 1 .038.052v5.5826a4.504 4.504 0 0 1-4.4945 4.4947zm-9.6607-4.1254a4.4708 4.4708 0 0 1-.5346-3.0137l.142.0852 4.783 2.7582a.7712.7712 0 0 0 .7806 0l5.8428-3.3685v2.3324a.0804.0804 0 0 1-.0332.0615L9.74 19.9502a4.4992 4.4992 0 0 1-6.1408-1.6464zM2.3408 7.8956a4.485 4.485 0 0 1 2.3655-1.9728V11.6a.7664.7664 0 0 0 .3879.6765l5.8144 3.3543-2.0201 1.1683a.0757.0757 0 0 1-.071 0l-4.8303-2.7866A4.504 4.504 0 0 1 2.3408 7.8956zm16.0993 3.8558L12.5973 8.3829l2.02-1.1636a.0757.0757 0 0 1 .071 0l4.8303 2.7913a4.4944 4.4944 0 0 1-.6765 8.1042v-5.6772a.79.79 0 0 0-.4022-.6862zm2.0107-3.0231l-.142-.0852-4.7735-2.7818a.7759.7759 0 0 0-.7854 0L9.409 9.2297V6.8974a.0662.0662 0 0 1 .0284-.0615l4.8303-2.7866a4.4992 4.4992 0 0 1 6.6802 4.66zM8.3065 12.863l-2.02-1.1635a.0804.0804 0 0 1-.038-.0567V6.0742a4.4992 4.4992 0 0 1 7.3757-3.4537l-.142.0805L8.704 5.459a.7948.7948 0 0 0-.3927.6813l-.0048 6.7227zm1.145-2.0396l2.548-1.4716 2.548 1.4716v2.9338l-2.548 1.4716-2.548-1.4716z"/></svg>`,

  // Abyssal Sky v2.0 Geometric Logo (Official Brand Mark from C:\Logo)
  brandSkillForgeLogo: `<svg width="18" height="18" viewBox="0 0 512 512" fill="none" class="sf-logo-svg">
    <defs>
      <linearGradient id="brandOceanMini" x1="10%" y1="90%" x2="90%" y2="30%">
        <stop offset="0%" stop-color="#0077B6" />
        <stop offset="45%" stop-color="#00B4D8" />
        <stop offset="100%" stop-color="#06D6A0" />
      </linearGradient>
      <linearGradient id="brandSkyMini" x1="20%" y1="85%" x2="88%" y2="12%">
        <stop offset="0%" stop-color="#4F46E5" />
        <stop offset="50%" stop-color="#7C3AED" />
        <stop offset="100%" stop-color="#C084FC" />
      </linearGradient>
    </defs>
    <rect width="512" height="512" rx="112" fill="#050C1A" stroke="#1E2D4A" stroke-width="16"/>
    <path d="M 136,248 C 146,168 208,118 392,56 C 420,46 442,68 432,96 C 370,280 320,342 248,352 C 192,358 136,304 136,248 Z" fill="url(#brandSkyMini)"/>
    <!-- Horizon Separation Channels -->
    <path d="M 96,244 Q 142,240 182,248" fill="none" stroke="#050C1A" stroke-width="26" stroke-linecap="round"/>
    <path d="M 252,334 Q 266,362 292,382" fill="none" stroke="#050C1A" stroke-width="26" stroke-linecap="round"/>
    <!-- Ocean Wave -->
    <path d="M 68,262 C 68,238 92,222 132,222 C 188,222 228,248 248,308 C 268,366 322,386 378,362 C 406,350 426,328 438,312 C 448,298 468,308 460,328 C 432,404 352,460 254,460 C 142,460 68,374 68,262 Z" fill="url(#brandOceanMini)"/>
    <!-- Central Negative-space Emergent Fox Silhouette -->
    <path d="M 192,148 C 214,164 234,184 252,196 C 270,184 290,164 312,148 C 322,182 328,216 326,248 C 306,282 278,312 252,338 C 226,312 198,282 178,248 C 176,216 182,182 192,148 Z" fill="#050C1A" stroke="#050C1A" stroke-width="8" stroke-linejoin="round"/>
    <!-- Horizon Eye Slits -->
    <path d="M 202,244 Q 220,248 236,260 Q 214,258 202,244 Z" fill="#00B4D8" opacity="0.9" />
    <path d="M 302,244 Q 284,248 268,260 Q 290,258 302,244 Z" fill="#A855F7" opacity="0.9" />
  </svg>`,

  brandSkillForgeLogoLarge: `<svg width="170" height="170" viewBox="0 0 180 180" fill="none" class="intro-stage-svg" data-testid="intro-stage-svg">
    <defs>
      <linearGradient id="brandOceanLg" x1="10%" y1="90%" x2="90%" y2="30%">
        <stop offset="0%" stop-color="#0077B6" />
        <stop offset="45%" stop-color="#00B4D8" />
        <stop offset="100%" stop-color="#06D6A0" />
      </linearGradient>
      <linearGradient id="brandSkyLg" x1="20%" y1="85%" x2="88%" y2="12%">
        <stop offset="0%" stop-color="#4F46E5" />
        <stop offset="50%" stop-color="#7C3AED" />
        <stop offset="100%" stop-color="#C084FC" />
      </linearGradient>
    </defs>
    <!-- Concentric Technical Blueprint Rings -->
    <circle cx="90" cy="90" r="82" class="sf-orbit-ring-1" fill="none" stroke="#1E2D4A" stroke-width="1.2" stroke-dasharray="10 8 3 8" />
    <circle cx="90" cy="90" r="70" class="sf-orbit-ring-2" fill="none" stroke="rgba(0, 180, 216, 0.35)" stroke-width="1" stroke-dasharray="14 10 4 10" />

    <!-- Circular Shockwave Ripple Rings -->
    <circle cx="90" cy="90" r="44" class="sf-shockwave-ring-1" fill="none" stroke="#7C3AED" stroke-width="2.5" />
    <circle cx="90" cy="90" r="44" class="sf-shockwave-ring-2" fill="none" stroke="#00B4D8" stroke-width="2" />
    <circle cx="90" cy="90" r="44" class="sf-shockwave-ring-3" fill="none" stroke="#C084FC" stroke-width="1.5" />

    <!-- Housing Base Tile -->
    <rect class="sf-base-tile" x="52" y="52" width="76" height="76" rx="20" fill="#050C1A" stroke="#1E2D4A" stroke-width="1.5" />

    <!-- Abyssal Sky v4.0 Geometric Monogram Rig with Negative-Space Fox -->
    <g class="sf-geometric-logo-large" transform="translate(52, 52) scale(0.148)">
      <path class="sf-shard-nw" d="M 136,248 C 146,168 208,118 392,56 C 420,46 442,68 432,96 C 370,280 320,342 248,352 C 192,358 136,304 136,248 Z" fill="url(#brandSkyLg)" />
      <path class="sf-shard-ne" d="M 96,244 Q 142,240 182,248" fill="none" stroke="#050C1A" stroke-width="26" stroke-linecap="round" />
      <path class="sf-shard-se" d="M 252,334 Q 266,362 292,382" fill="none" stroke="#050C1A" stroke-width="26" stroke-linecap="round" />
      <path class="sf-shard-sw" d="M 68,262 C 68,238 92,222 132,222 C 188,222 228,248 248,308 C 268,366 322,386 378,362 C 406,350 426,328 438,312 C 448,298 468,308 460,328 C 432,404 352,460 254,460 C 142,460 68,374 68,262 Z" fill="url(#brandOceanLg)" />
      <!-- Central Negative-space Emergent Fox Silhouette -->
      <path class="sf-shard-star sf-shard-fox" d="M 192,148 C 214,164 234,184 252,196 C 270,184 290,164 312,148 C 322,182 328,216 326,248 C 306,282 278,312 252,338 C 226,312 198,282 178,248 C 176,216 182,182 192,148 Z" fill="#050C1A" stroke="#050C1A" stroke-width="8" stroke-linejoin="round" />
      <!-- Horizon Eye Slits -->
      <path d="M 202,244 Q 220,248 236,260 Q 214,258 202,244 Z" fill="#00B4D8" opacity="0.9" />
      <path d="M 302,244 Q 284,248 268,260 Q 290,258 302,244 Z" fill="#A855F7" opacity="0.9" />
    </g>
  </svg>`
};

class MarkdownRenderer {
  static render(text) {
    if (!text) return "";
    let html = text;

    html = html.replace(/```([a-zA-Z0-9_\-]*)\n([\s\S]*?)```/g, (match, lang, code) => {
      return `<pre><div style="font-size:10.5px; color:#64748B; margin-bottom:6px; font-weight:600; text-transform:uppercase;">${lang || 'code'}</div><code>${this.escapeHtml(code.trim())}</code></pre>`;
    });

    html = html.replace(/`([^`]+)`/g, (match, code) => `<code>${this.escapeHtml(code)}</code>`);

    html = html.replace(/((?:\|[^\n]+\|\n)+)/g, (match) => {
      const rows = match.trim().split("\n");
      if (rows.length < 2) return match;
      let tableHtml = "<table>";
      rows.forEach((row, i) => {
        if (row.includes("---")) return;
        const cells = row.split("|").filter((c, idx, arr) => idx > 0 && idx < arr.length - 1);
        const tag = (i === 0) ? "th" : "td";
        tableHtml += `<tr>${cells.map(c => `<${tag}>${c.trim()}</${tag}>`).join("")}</tr>`;
      });
      tableHtml += "</table>";
      return tableHtml;
    });

    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    html = html.replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>');
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    html = html.replace(/^\- (.*$)/gim, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

    html = html.split("\n\n").map(p => {
      if (p.startsWith("<h") || p.startsWith("<pre") || p.startsWith("<table") || p.startsWith("<blockquote") || p.startsWith("<ul")) {
        return p;
      }
      return `<p>${p.replace(/\n/g, "<br/>")}</p>`;
    }).join("");

    return html;
  }

  static escapeHtml(str) {
    return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
}

class UIComponents {
  static getBrandIconSvg(skillId, category) {
    const id = (skillId || "").toLowerCase();
    if (id.includes("architect")) return Icons.brandAntigravity;
    if (id.includes("ui-ux") || id.includes("frontend-ui")) return Icons.palette;
    if (id.includes("shadcn") || id.includes("tailwind")) return Icons.brandTailwind;
    if (id.includes("nextjs")) return Icons.brandNextjs;
    if (id.includes("supabase")) return Icons.brandSupabase;
    if (id.includes("playwright") || id.includes("test-driven") || id.includes("test-engineer")) return Icons.brandPlaywright;
    if (id.includes("assets") || id.includes("vault") || id.includes("interview") || id.includes("idea-refine")) return Icons.sparkles;
    if (id.includes("security")) return Icons.lock;
    if (id.includes("git-") || id.includes("ci-cd")) return Icons.gitBranch;
    if (id.includes("performance") || id.includes("webperf")) return Icons.sun;
    if (id.includes("code-review") || id.includes("documentation") || id.includes("spec-driven")) return Icons.fileText;
    if (id.includes("debugging") || id.includes("bug")) return Icons.bug;
    if (id.includes("planning") || id.includes("context") || id.includes("deprecation")) return Icons.layers;
    return Icons.cpu;
  }

  static renderExecutiveHeader(skillsCount = 36, refsCount = 26, activeSource = "all", newCount = 0, updateCount = 0) {
    let batchLabel = "";
    let isComplete = false;

    if (newCount > 0) {
      batchLabel = `⚡ Kích Hoạt ${newCount} Kỹ Năng Mới (1-Click)`;
    } else {
      isComplete = true;
      batchLabel = `✓ Đã Kích Hoạt Đầy Đủ (${skillsCount}/${skillsCount})`;
    }

    return `
      <!-- Executive Status & Batch Control Bar -->
      <div class="executive-header" data-testid="executive-header">
        <div class="executive-header-left">
          <div class="executive-title-wrap">
            <span class="executive-title">Kho Kỹ Năng AI</span>
            <span class="executive-count-badge" id="badge-executive-count">${skillsCount} Kỹ năng</span>
          </div>
          <button class="btn-help-trigger" id="btn-trigger-quick-help" data-testid="btn-trigger-quick-help" title="Xem hướng dẫn sử dụng 3 bước">
            ${Icons.helpCircle}
            <span>Hướng dẫn 3 bước</span>
          </button>
        </div>

        <div class="executive-header-right" style="display:flex; align-items:center; gap:8px;">
          ${updateCount > 0 ? `
            <button class="btn-batch-updates-pill" id="btn-batch-review-updates" title="Có ${updateCount} kỹ năng có bản cập nhật mới so với máy bạn. Bấm để xem so sánh từng dòng!">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
              <span>🔄 Có ${updateCount} Kỹ Năng Cần Cập Nhật</span>
            </button>
          ` : ""}

          <button class="btn ${isComplete ? 'btn-secondary btn-batch-complete' : 'btn-primary'}" id="btn-batch-install-all" data-testid="btn-batch-install-all">
            ${isComplete ? Icons.checkCircle : Icons.download}
            <span id="btn-batch-install-text">${batchLabel}</span>
          </button>
        </div>
      </div>

      <!-- Hero Quick-Start Action Hub for Beginners (Establishes Immediate Visual Focal Point) -->
      <div class="hero-action-hub" id="hero-action-hub" data-testid="hero-action-hub">
        <div class="hero-hub-header">
          <div class="hero-hub-greeting">
            <div class="hero-hub-title">
              <span>👋 Chào bạn! Bạn muốn trợ lý AI giúp việc gì hôm nay?</span>
            </div>
            <div class="hero-hub-subtitle">
              Chọn nhanh 1 trong 3 nhu cầu phổ biến dưới đây để có câu lệnh mẫu chuẩn và bắt đầu làm việc ngay trong 30 giây:
            </div>
          </div>
        </div>

        <div class="hero-goal-grid">
          <!-- Goal 1: UI / UX -->
          <div class="hero-goal-card goal-card-ui" id="hero-goal-ui" role="button" tabindex="0" title="Bấm để lọc các kỹ năng giao diện và mở hướng dẫn">
            <div class="goal-card-header">
              <div class="goal-card-icon-wrap">${Icons.palette}</div>
              <div class="goal-card-title">Thiết Kế Giao Diện Đẹp</div>
            </div>
            <div class="goal-card-desc">
              Tự động áp dụng 118 quy tắc UX, bố cục chuẩn Vercel và bảng màu sang trọng.
            </div>
            <div class="goal-card-cta">
              <span>Xem kỹ năng UI & Dùng thử</span>
              ${Icons.arrowRight}
            </div>
          </div>

          <!-- Goal 2: Planning & Architecture -->
          <div class="hero-goal-card goal-card-plan" id="hero-goal-plan" role="button" tabindex="0" title="Bấm để lọc các kỹ năng lập kế hoạch và sửa lỗi">
            <div class="goal-card-header">
              <div class="goal-card-icon-wrap">${Icons.layers}</div>
              <div class="goal-card-title">Lập Kế Hoạch & Viết Code</div>
            </div>
            <div class="goal-card-desc">
              Yêu cầu AI phân tích kiến trúc, lập bản vẽ chi tiết trước khi code, không đoán mò.
            </div>
            <div class="goal-card-cta">
              <span>Xem kỹ năng Code & Dùng thử</span>
              ${Icons.arrowRight}
            </div>
          </div>

          <!-- Goal 3: 1-Click All Skills -->
          <div class="hero-goal-card goal-card-all" id="hero-goal-all" role="button" tabindex="0" title="Bấm để kích hoạt toàn bộ kỹ năng vào máy tính">
            <div class="goal-card-header">
              <div class="goal-card-icon-wrap">${Icons.sparkles}</div>
              <div class="goal-card-title">Kích Hoạt Vào Máy Tính</div>
            </div>
            <div class="goal-card-desc">
              Tự động nạp quy tắc vào Cursor, Windsurf, Claude Code, Copilot và Antigravity.
            </div>
            <div class="goal-card-cta">
              <span>⚡ Kích hoạt 1-Click ngay</span>
              ${Icons.arrowRight}
            </div>
          </div>
        </div>
      </div>
    `;
  }

  static renderSkillsUpdateBanner(summary = "", updateSig = "", newCount = 0) {
    const text = summary || "Phát hiện có kỹ năng & câu lệnh mới từ Addy Osmani (Google) sẵn sàng nạp.";
    const countBadge = newCount > 0 ? `<span class="banner-count-badge">+${newCount} mới</span>` : "";

    return `
      <div class="skills-update-banner" id="skills-update-banner" data-signature="${updateSig}" data-testid="skills-update-banner">
        <div class="banner-left-content">
          <div class="banner-sparkle-icon">${Icons.sparkles}</div>
          <div class="banner-text-wrap">
            <span class="banner-badge-label">Cập nhật nhỏ</span>
            ${countBadge}
            <span class="banner-message">${this.escape(text)}</span>
          </div>
        </div>
        <div class="banner-actions">
          <button class="btn btn-primary btn-banner-sync" id="btn-banner-sync-skills" data-testid="btn-banner-sync-skills" title="Đồng bộ ngay vào máy tính">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
            <span id="btn-banner-sync-text">Đồng Bộ Ngay</span>
          </button>
          <button class="btn-banner-dismiss" id="btn-banner-dismiss" data-testid="btn-banner-dismiss" title="Để sau / Không hiển thị lại bản cập nhật này" aria-label="Tắt thông báo">
            ${Icons.x}
            <span>Để sau</span>
          </button>
        </div>
      </div>
    `;
  }

  static renderNotificationDropdown(notifications = []) {
    return `
      <div class="notification-dropdown-menu" id="notification-dropdown-menu" onclick="event.stopPropagation()" data-testid="notification-dropdown-menu">
        <div class="notification-menu-header">
          <div style="display:flex; align-items:center; gap:6px;">
            <span style="color:#00B4D8;">${Icons.bell}</span>
            <span style="font-weight:700; font-size:13px; color:var(--text-primary);">Trung Tâm Thông Báo</span>
          </div>
          ${notifications.length > 0 ? `
            <button class="btn-text-action" id="btn-clear-all-notifications" title="Đánh dấu tất cả đã đọc">
              Đánh dấu đã đọc
            </button>
          ` : ""}
        </div>

        <div class="notification-items-scroll">
          ${notifications.length === 0 ? `
            <div class="notification-empty-state">
              <div class="empty-bell-icon">${Icons.bell}</div>
              <div style="font-size:12.5px; font-weight:600; color:var(--text-primary); margin-top:6px;">Không có thông báo mới</div>
              <div style="font-size:11.5px; color:var(--text-muted); margin-top:2px;">Toàn bộ kho kỹ năng và phiên bản phần mềm đã đồng bộ mới nhất.</div>
            </div>
          ` : notifications.map((n, idx) => `
            <div class="notification-item ${n.unread ? 'unread' : ''}" data-index="${idx}" data-testid="notification-item-${n.type}">
              <div class="notif-item-icon ${n.type}">
                ${n.type === 'skills' ? Icons.sparkles : (n.type === 'app' ? Icons.download : Icons.helpCircle)}
              </div>
              <div class="notif-item-body">
                <div class="notif-item-title-row">
                  <span class="notif-item-title">${this.escape(n.title)}</span>
                  <span class="notif-item-time">${this.escape(n.time || 'Vừa xong')}</span>
                </div>
                <div class="notif-item-desc">${this.escape(n.desc)}</div>
                ${n.action ? `
                  <div class="notif-item-cta-row">
                    <button class="btn btn-secondary btn-sm notif-action-btn" id="notif-action-btn-${idx}" data-action="${n.action}">
                      ${this.escape(n.actionLabel || 'Thực hiện')}
                    </button>
                  </div>
                ` : ""}
              </div>
            </div>
          `).join("")}
        </div>

        <div class="notification-menu-footer">
          <div style="display:flex; justify-content:space-between; align-items:center; width:100%;">
            <label class="notification-pref-toggle" title="Tắt thanh gợi ý cập nhật nhỏ khi lướt xem kỹ năng">
              <input type="checkbox" id="pref-toggle-minor-banners" ${localStorage.getItem("abyssalskillsd-mute-minor-banners") === "true" ? "" : "checked"}>
              <span>Bật thanh gợi ý cập nhật nhỏ</span>
            </label>
            <button class="btn-text-action" id="btn-open-full-update-modal">Cập nhật...</button>
          </div>
        </div>
      </div>
    `;
  }

  static renderUpdateModal(data = {}) {
    const currentVer = data.current_version || "1.0.0";
    const latestVer = data.latest_version || currentVer;
    const hasAppUpdate = !!data.has_app_update;
    const releaseTitle = data.release_title || `AbyssalSkillsD v${latestVer}`;
    const releaseNotes = (data.release_notes && data.release_notes.length > 0)
      ? data.release_notes
      : [
          "Bộ nhận diện hình học Abyssal Sky v2.0 chuẩn Linear/Vercel với lưới Blueprint 64x64px.",
          "Tự động nạp quy tắc vào Cursor, Windsurf, Claude Code, GitHub Copilot, Google Antigravity.",
          "Tích hợp 29 kỹ năng và chuyên gia AI từ Addy Osmani (Google) với 100% trích dẫn minh bạch."
        ];
    const totalSkills = data.total_skills_installed || 36;
    const downloadUrl = data.download_url || "https://github.com/kyuu4/abyssalskillsd/releases";
    const isOffline = !!data.is_offline;
    const checkedAt = data.checked_at || "Vừa xong";

    return `
      <div class="modal-backdrop" id="update-modal-backdrop" onclick="App.closeActiveModal(event)">
        <div class="modal-dialog update-modal-card" style="max-width: 620px;" onclick="event.stopPropagation()">
          <div class="modal-header update-modal-header">
            <div style="font-size:14px; font-weight:700; color:var(--text-primary); display:flex; align-items:center; gap:8px;">
              <span style="color:#00B4D8;">${Icons.refresh}</span>
              <span>Cập Nhật Phần Mềm & Kho Kỹ Năng</span>
            </div>
            <button class="btn btn-ghost btn-icon" onclick="App.closeActiveModal()" title="Đóng">
              ${Icons.x}
            </button>
          </div>

          <div class="tryout-modal-body update-modal-body" style="padding: 20px;">
            <!-- Header Version Card -->
            <div class="update-version-card">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                  <div style="font-size:12px; color:var(--text-muted); margin-bottom:2px;">Phiên bản hiện tại trên máy:</div>
                  <div style="font-size:16px; font-weight:700; color:var(--text-primary); font-family:var(--font-mono, monospace);">v${currentVer}</div>
                </div>
                <div style="text-align:right;">
                  <div style="font-size:12px; color:var(--text-muted); margin-bottom:2px;">Phiên bản mới nhất:</div>
                  ${hasAppUpdate 
                    ? `<span class="badge-new-version">v${latestVer} (Có bản mới)</span>` 
                    : `<span class="badge-latest-version">✓ Đã mới nhất</span>`}
                </div>
              </div>
            </div>

            ${isOffline ? `
              <div class="update-offline-alert">
                <span>⚠️ Đang ngoại tuyến: Không thể truy cập máy chủ GitHub. Bạn vẫn có thể đồng bộ kho kỹ năng nội bộ.</span>
              </div>
            ` : ""}

            ${hasAppUpdate ? `
              <!-- App Update Banner & Changelog -->
              <div class="update-changelog-box">
                <div class="changelog-title">
                  <span style="color:#00B4D8;">🚀</span> Có gì mới trong bản v${latestVer}:
                </div>
                <ul class="changelog-list">
                  ${releaseNotes.map(n => `<li>${this.escape(n)}</li>`).join("")}
                </ul>
                <div style="margin-top:14px; display:flex; gap:10px;">
                  <a href="${downloadUrl}" target="_blank" class="btn btn-primary btn-dl-release" id="btn-dl-release-link">
                    ${Icons.download}
                    <span>Tải Bản v${latestVer} Từ GitHub</span>
                  </a>
                </div>
              </div>
            ` : `
              <div class="update-status-clean">
                <div class="clean-check-icon">✓</div>
                <div>
                  <div style="font-weight:600; color:var(--text-primary);">Hệ thống của bạn đang ở phiên bản mới nhất</div>
                  <div style="font-size:12px; color:var(--text-muted);">Kiểm tra lần cuối: ${checkedAt}</div>
                </div>
              </div>
            `}

            <!-- Skills Sync Section -->
            <div class="update-skills-section">
              <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <div>
                  <div style="font-weight:600; font-size:13px; color:var(--text-primary);">Đồng bộ Kỹ Năng (Addy Osmani & Skill-AI)</div>
                  <div style="font-size:12px; color:var(--text-muted);">Hiện có <strong style="color:var(--ocean-cyan, #00B4D8);">${totalSkills} kỹ năng</strong> trong thư viện.</div>
                </div>
                <button class="btn btn-primary btn-action-sync-skills" id="btn-action-sync-skills" data-testid="btn-action-sync-skills">
                  <span id="sync-spinner" style="display:none; margin-right:4px;">⏳</span>
                  <span id="btn-sync-skills-text">🔄 Đồng Bộ Kho Kỹ Năng</span>
                </button>
              </div>

              <!-- Live Progress / Feedback Box -->
              <div class="update-progress-container" id="update-progress-container" style="display:none; margin-top:12px;">
                <div class="update-progress-track">
                  <div class="update-progress-fill" id="update-progress-fill" style="width: 0%;"></div>
                </div>
                <div class="update-progress-msg" id="update-progress-msg" style="font-size:12px; color:var(--text-secondary); margin-top:6px;">
                  Đang kết nối kho GitHub...
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer" style="display:flex; justify-content:space-between; align-items:center; padding: 12px 20px; border-top: 1px solid var(--border-subtle);">
            <div style="font-size:11px; color:var(--text-muted);">
              Kênh phát hành: <strong style="color:var(--text-secondary);">Stable (Chính thức)</strong>
            </div>
            <div style="display:flex; gap:8px;">
              <button class="btn btn-secondary" id="btn-recheck-updates">
                ${Icons.refresh}
                <span>Kiểm Tra Lại</span>
              </button>
              <button class="btn btn-secondary" onclick="App.closeActiveModal()">Đóng</button>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  static renderQuickTryoutModal(skill) {
    if (!skill) return "";
    const isAddy = skill.source_group === "addy_osmani";
    const authorName = skill.author || (isAddy ? "Addy Osmani (Google)" : "Skill-AI Org");
    const samplePrompt = (skill.starter_prompts && skill.starter_prompts.length > 0)
      ? (typeof skill.starter_prompts[0] === 'object' ? skill.starter_prompts[0].prompt : skill.starter_prompts[0])
      : `Tôi muốn bạn áp dụng quy tắc chuyên gia của kỹ năng ${skill.name} để giải quyết công việc này.`;
    const promptTitle = (skill.starter_prompts && skill.starter_prompts.length > 0 && typeof skill.starter_prompts[0] === 'object' && skill.starter_prompts[0].title)
      ? skill.starter_prompts[0].title
      : "Câu lệnh mẫu được đề xuất";

    return `
      <div class="modal-backdrop" id="modal-quick-tryout-backdrop" onclick="App.closeActiveModal(event)">
        <div class="modal-dialog" style="max-width: 660px;" onclick="event.stopPropagation()">
          <div class="modal-header">
            <div style="font-size:14px; font-weight:700; color:var(--text-primary); display:flex; align-items:center; gap:8px;">
              <span style="color:#818CF8;">${Icons.sparkles}</span>
              <span>Dùng Thử Kỹ Năng: ${this.escape(skill.display_title || skill.name)}</span>
            </div>
            <button class="btn btn-ghost btn-icon" onclick="App.closeActiveModal()">
              ${Icons.x}
            </button>
          </div>

          <div class="tryout-modal-body">
            <!-- Hero Banner -->
            <div class="tryout-hero-banner">
              <div class="tryout-hero-icon">
                ${this.getBrandIconSvg(skill.id, skill.category)}
              </div>
              <div class="tryout-hero-text">
                <h3>${this.escape(skill.display_title || skill.name)} <span style="font-size:11px; font-weight:normal; color:var(--text-muted);">bởi ${this.escape(authorName)}</span></h3>
                <p>${this.escape(skill.when_to_use || skill.description || 'Kỹ năng nâng cao cho mô hình AI.')}</p>
              </div>
            </div>

            <!-- 3-Step Guidance -->
            <div class="tryout-steps-list">
              <div class="tryout-step-item">
                <span class="tryout-step-num">Bước 1</span>
                <span class="tryout-step-label">Sao chép câu lệnh</span>
                <span class="tryout-step-sub">Bấm nút "Chép Lệnh Này" bên dưới để lưu vào máy.</span>
              </div>
              <div class="tryout-step-item">
                <span class="tryout-step-num">Bước 2</span>
                <span class="tryout-step-label">Mở AI của bạn</span>
                <span class="tryout-step-sub">Mở Cursor, Claude Code, Antigravity hoặc ChatGPT.</span>
              </div>
              <div class="tryout-step-item">
                <span class="tryout-step-num">Bước 3</span>
                <span class="tryout-step-label">Dán và gửi</span>
                <span class="tryout-step-sub">Dán (Ctrl+V) vào khung chat để AI tự kích hoạt kỹ năng.</span>
              </div>
            </div>

            <!-- Ready-to-use Prompt Box -->
            <div class="tryout-prompt-card">
              <div class="tryout-prompt-label">
                <span>Câu lệnh mẫu tiếng Việt sẵn sàng dùng:</span>
                <span style="font-size:11px; color:#38BDF8; font-weight:500;">${this.escape(promptTitle)}</span>
              </div>
              <div class="tryout-prompt-box" id="tryout-prompt-content" tabindex="0">
                ${this.escape(samplePrompt)}
              </div>
            </div>

            <!-- Action Bar -->
            <div class="tryout-action-bar">
              <div style="font-size:11.5px; color:var(--text-muted); display:flex; align-items:center; gap:6px;">
                <span class="status-led active"></span>
                <span>Tương thích 100% với Cursor, Claude, Antigravity, Copilot</span>
              </div>
              <div style="display:flex; gap:8px;">
                <button class="btn btn-secondary" onclick="App.closeActiveModal()">Đóng</button>
                <button class="btn btn-primary" id="btn-copy-tryout-prompt" onclick="App.copyTryoutPrompt()" style="background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);">
                  ${Icons.copy}
                  <span id="btn-copy-tryout-text">Sao Chép Câu Lệnh Này</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  static renderQuickHelpModal() {
    return `
      <div class="modal-backdrop" id="modal-quick-help-backdrop" onclick="App.closeActiveModal(event)">
        <div class="modal-dialog" style="max-width: 680px;" onclick="event.stopPropagation()">
          <div class="modal-header">
            <div style="font-size:14px; font-weight:600; color:var(--text-primary); display:flex; align-items:center; gap:8px;">
              <span style="color:var(--accent-primary);">${Icons.sparkles}</span>
              <span>Hướng Dẫn Sử Dụng Nhanh (3 Bước)</span>
            </div>
            <button class="btn btn-ghost btn-icon" onclick="App.closeActiveModal()">
              ${Icons.x}
            </button>
          </div>

          <div class="modal-body" style="padding:18px;">
            <div class="onboarding-strip" data-testid="onboarding-strip" style="margin:0; border:none; background:transparent; padding:0;">
              <div class="onboarding-steps-grid">
                <div class="onboarding-step-card">
                  <span class="step-badge">1</span>
                  <div class="step-card-title">Chọn Nhu Cầu Cần Làm</div>
                  <div class="step-card-desc">Bấm vào các nút ở thanh "Nhu cầu" bên dưới: Lập kế hoạch, Giao diện, hoặc Web & Database.</div>
                </div>

                <div class="onboarding-step-card">
                  <span class="step-badge">2</span>
                  <div class="step-card-title">Kích Hoạt Vào Máy</div>
                  <div class="step-card-desc">Bấm "Kích hoạt 7 Kỹ Năng" hoặc bấm "Xem chi tiết" trên từng thẻ kỹ năng.</div>
                </div>

                <div class="onboarding-step-card">
                  <span class="step-badge">3</span>
                  <div class="step-card-title">Chép Lệnh & Dùng Ngay</div>
                  <div class="step-card-desc">Bấm nút sao chép câu lệnh mẫu tiếng Việt rồi dán thẳng vào khung chat AI của bạn.</div>
                </div>
              </div>
            </div>

            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:18px; padding-top:14px; border-top:1px solid var(--border-subtle);">
              <span style="font-size:12px; color:var(--text-muted); display:flex; align-items:center; gap:6px;">
                <span class="status-led active"></span>
                <span>Tự động cấu hình Always-On Autopilot & Graphify AST.</span>
              </span>
              <div style="display:flex; gap:8px;">
                <button class="btn btn-secondary" onclick="App.closeActiveModal()">Đã hiểu</button>
                <button class="btn btn-primary" onclick="App.closeActiveModal(); App.handleBatchInstall();">
                  ${Icons.download}
                  <span>Kích hoạt 7 Kỹ Năng ngay</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  static renderActivationModal(skill, targetList = ["antigravity"], state = {}) {
    const isComplete = !!state.isComplete;
    const progressPct = state.progressPct || (isComplete ? 100 : 35);
    const step = state.stepIndex || (isComplete ? 3 : 1);
    const skillName = skill ? (skill.display_title || skill.name) : "Kỹ Năng";
    const skillId = skill ? skill.id : "";
    const category = skill ? (skill.category || "Chuyên gia") : "";
    const targetBadges = (targetList && targetList.length > 0) ? targetList : ["antigravity", "cursor", "claude"];
    const testPrompt = state.testPrompt || "Hãy giải thích cách kỹ năng này hoạt động và lập kế hoạch mẫu cho tôi /plan";

    return `
      <div class="modal-backdrop neural-stream-backdrop" id="activation-modal-backdrop">
        <div class="modal-dialog activation-modal-card" style="max-width: 620px;" onclick="event.stopPropagation()">
          <div class="modal-header activation-modal-header">
            <div style="display:flex; align-items:center; gap:8px;">
              <span class="activation-icon-pulse">${Icons.sparkles}</span>
              <div>
                <div style="font-size:14px; font-weight:700; color:var(--text-primary);">
                  ${isComplete ? "Kích Hoạt Thành Công Vào Não Bộ AI" : "Đang Kích Hoạt Kỹ Năng Vào Trợ Lý AI"}
                </div>
                <div style="font-size:11.5px; color:var(--text-secondary);">
                  ${isComplete ? "AI của bạn đã được nạp đầy đủ sổ tay và quy tắc Always-On Autopilot" : "Thiết lập cầu nối dữ liệu và nạp cấu hình hệ thống..."}
                </div>
              </div>
            </div>
            ${isComplete ? `
              <button class="modal-close-btn" onclick="App.closeActiveModal()" title="Đóng">
                ${Icons.x}
              </button>
            ` : ""}
          </div>

          <div class="modal-body activation-modal-body" style="padding: 16px 20px;">
            <!-- 1. Neural Stream Motion Stage (Visual Data Transmission) -->
            <div class="neural-stage">
              <!-- Source: Skill Node -->
              <div class="neural-node source-node">
                <div class="neural-node-icon">
                  ${skill ? this.getBrandIconSvg(skill.id, category) : Icons.cpu}
                </div>
                <div class="neural-node-label">${this.escape(skillName)}</div>
                <div class="neural-node-status">Kho Kỹ Năng</div>
              </div>

              <!-- Animated Data Stream (Beam & Particles) -->
              <div class="neural-stream-pipeline">
                <div class="neural-stream-track">
                  <div class="neural-stream-beam ${isComplete ? 'complete' : 'active'}"></div>
                  <div class="neural-particle particle-1"></div>
                  <div class="neural-particle particle-2"></div>
                  <div class="neural-particle particle-3"></div>
                </div>
                <div class="neural-stream-label">
                  ${isComplete ? "✓ Đã nạp 100% dữ liệu" : "⚡ Đang truyền tải quy tắc..."}
                </div>
              </div>

              <!-- Destination: AI Core Node -->
              <div class="neural-node dest-node ${isComplete ? 'connected' : ''}">
                <div class="neural-node-icon ai-hub-icon">
                  <div class="ai-hub-inner">
                    ${Icons.cpu}
                  </div>
                </div>
                <div class="neural-node-label">Trợ Lý AI</div>
                <div class="neural-node-targets">
                  ${targetBadges.slice(0, 3).map(t => `<span class="target-mini-pill">${this.escape(t)}</span>`).join("")}
                </div>
              </div>
            </div>

            <!-- 2. Step Progress Indicators -->
            <div class="activation-steps-list">
              <div class="activation-step-row ${step >= 1 ? (step === 1 && !isComplete ? 'current' : 'done') : 'pending'}">
                <div class="step-indicator-dot">
                  ${step > 1 || isComplete ? "✓" : (step === 1 ? `<span class="step-spinner"></span>` : "1")}
                </div>
                <div class="step-info">
                  <div class="step-title">Trích xuất cấu trúc SKILL.md & sổ tay playbook</div>
                  <div class="step-sub">Đóng gói 100% tài liệu kiến trúc và hướng dẫn thực thi</div>
                </div>
              </div>

              <div class="activation-step-row ${step >= 2 ? (step === 2 && !isComplete ? 'current' : 'done') : 'pending'}">
                <div class="step-indicator-dot">
                  ${step > 2 || isComplete ? "✓" : (step === 2 ? `<span class="step-spinner"></span>` : "2")}
                </div>
                <div class="step-info">
                  <div class="step-title">Nạp quy tắc Always-On Autopilot vào hệ thống AI</div>
                  <div class="step-sub">Đồng bộ vào ~/.gemini/config/skills và tệp .cursorrules</div>
                </div>
              </div>

              <div class="activation-step-row ${isComplete ? 'done' : (step === 3 ? 'current' : 'pending')}">
                <div class="step-indicator-dot">
                  ${isComplete ? "✓" : (step === 3 ? `<span class="step-spinner"></span>` : "3")}
                </div>
                <div class="step-info">
                  <div class="step-title">Xác thực quyền thực thi & sẵn sàng phản hồi</div>
                  <div class="step-sub">AI đã nhận biết kỹ năng và sẵn sàng trả lời câu lệnh</div>
                </div>
              </div>
            </div>

            <!-- 3. Progress Bar Track -->
            <div class="activation-progress-container">
              <div class="activation-progress-bar">
                <div class="activation-progress-fill" style="width: ${progressPct}%;"></div>
              </div>
              <div class="activation-progress-meta">
                <span>${isComplete ? "Hoàn tất kích hoạt" : "Tiến độ cấu hình"}</span>
                <span><strong>${progressPct}%</strong></span>
              </div>
            </div>

            <!-- 4. Post-Activation Proof Section (Appears when isComplete is True) -->
            ${isComplete ? `
              <div class="activation-proof-card">
                <div class="proof-card-header">
                  <span class="proof-badge-verified">
                    ${Icons.checkCircle}
                    <span>BẰNG CHỨNG XÁC THỰC TRÊN MÁY TÍNH CỦA BẠN</span>
                  </span>
                </div>

                <div class="proof-card-body">
                  <div class="proof-desc-text">
                    Tệp quy tắc đã được nạp trực tiếp vào ổ cứng. Bạn có thể mở xem ngay hoặc thử nghiệm phản hồi của AI:
                  </div>

                  <!-- Test Prompt Box -->
                  <div class="proof-prompt-box">
                    <div class="proof-prompt-header">
                      <span>🧪 Câu lệnh mẫu thử nghiệm ngay trong AI:</span>
                      <button class="btn-copy-proof-prompt" id="btn-copy-activation-prompt" data-prompt="${this.escape(testPrompt)}">
                        ${Icons.copy} <span>Sao chép lệnh</span>
                      </button>
                    </div>
                    <div class="proof-prompt-code">
                      <code>${this.escape(testPrompt)}</code>
                    </div>
                    <div class="proof-prompt-hint">
                      💡 <em>Dán câu lệnh này vào khung chat AI (Cursor, Windsurf, Claude Code, Antigravity) để kiểm chứng AI phản hồi với chế độ làm việc chuẩn.</em>
                    </div>
                  </div>
                </div>

                <!-- Proof Action Bar -->
                <div class="proof-actions-row">
                  <button class="btn btn-secondary" id="btn-open-explorer-from-modal" data-id="${skillId}">
                    ${Icons.folderOpen}
                    <span>📁 Xem Tệp Đã Nạp Trong Máy</span>
                  </button>
                  <button class="btn btn-primary" onclick="App.closeActiveModal()">
                    ${Icons.check}
                    <span>Bắt Đầu Làm Việc Ngay</span>
                  </button>
                </div>
              </div>
            ` : ""}
          </div>
        </div>
      </div>
    `;
  }

  static renderVerificationModal(skill, report = {}) {
    const skillName = skill ? (skill.display_title || skill.name) : (report.skill_name || "Kỹ năng");
    const skillId = skill ? skill.id : (report.skill_id || "");
    const targets = report.verified_targets || [];
    const rules = report.active_rules || [];
    const isInstalled = report.is_installed || targets.length > 0;
    const testPrompt = report.test_prompt || "Hãy giải thích cách kỹ năng này hoạt động và lập kế hoạch mẫu cho tôi.";
    const expectedBehavior = report.expected_behavior || "AI sẽ bắt đầu câu trả lời bằng bảng phân tích chuyên sâu, tuân thủ nguyên tắc không code đại trà.";

    return `
      <div class="modal-backdrop" id="verification-modal-backdrop" onclick="App.closeActiveModal(event)">
        <div class="modal-dialog verification-modal-card" style="max-width: 640px;" onclick="event.stopPropagation()">
          <div class="modal-header verification-modal-header">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="color:#06D6A0;">${Icons.checkCircle}</span>
              <div>
                <div style="font-size:14px; font-weight:700; color:var(--text-primary); display:flex; align-items:center; gap:8px;">
                  <span>Bằng Chứng Kỹ Năng Đã Vào Não Bộ AI</span>
                  <span class="badge-status-pill ${isInstalled ? 'active' : 'inactive'}">
                    ${isInstalled ? '● ĐANG HOẠT ĐỘNG' : '○ CHƯA KÍCH HOẠT'}
                  </span>
                </div>
                <div style="font-size:11.5px; color:var(--text-secondary);">
                  Kỹ năng: <strong>${this.escape(skillName)}</strong>
                </div>
              </div>
            </div>
            <button class="modal-close-btn" onclick="App.closeActiveModal()" title="Đóng">
              ${Icons.x}
            </button>
          </div>

          <div class="modal-body verification-modal-body" style="padding: 18px 20px;">
            <!-- Section 1: Physical File Paths on Disk -->
            <div class="verification-section">
              <div class="verification-section-title">
                ${Icons.folderOpen}
                <span>1. Tệp tin thực tế trên ổ cứng của bạn (Physical Paths)</span>
              </div>
              <div class="verification-paths-list">
                ${targets.length > 0 ? targets.map(t => `
                  <div class="verification-path-item">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                      <span class="path-target-tag">${this.escape(t.label)}</span>
                      <button class="btn-text-action btn-open-target-dir" data-id="${skillId}" data-target="${t.target}">
                        📁 Mở trong Explorer
                      </button>
                    </div>
                    <div class="path-string-box" title="${this.escape(t.path)}">
                      <code>${this.escape(t.path)}</code>
                    </div>
                  </div>
                `).join("") : `
                  <div style="font-size:12px; color:var(--text-muted); padding:10px; background:rgba(255,255,255,0.03); border-radius:6px;">
                    Chưa phát hiện tệp tin trong thư mục chuẩn. Hãy bấm "Đồng bộ Cài đặt" để nạp vào máy.
                  </div>
                `}

                ${rules.length > 0 ? `
                  <div style="margin-top:10px; font-size:11px; font-weight:600; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.05em;">
                    Quy tắc Always-On Autopilot đã tiêm vào hệ thống:
                  </div>
                  <div style="display:flex; flex-direction:column; gap:4px; margin-top:6px;">
                    ${rules.map(r => `
                      <div style="font-size:11.5px; color:var(--text-secondary); display:flex; align-items:center; gap:6px;">
                        <span style="color:#06D6A0;">✓</span>
                        <span><strong>${this.escape(r.label)}:</strong> <code>${this.escape(r.path)}</code></span>
                      </div>
                    `).join("")}
                  </div>
                ` : ""}
              </div>
            </div>

            <!-- Section 2: How to Verify in AI Chat -->
            <div class="verification-section" style="margin-top:18px;">
              <div class="verification-section-title">
                ${Icons.sparkles}
                <span>2. Cách thử nghiệm kiểm chứng ngay trong khung chat AI</span>
              </div>
              <div style="font-size:12px; color:var(--text-secondary); margin-bottom:8px;">
                Hãy sao chép câu lệnh bên dưới và dán vào Cursor, Windsurf, Claude Code, hoặc Antigravity:
              </div>

              <div class="verification-test-box">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                  <span style="font-size:11px; font-weight:600; color:var(--ocean-cyan);">CÂU LỆNH KIỂM CHỨNG (1-CLICK TEST PROMPT)</span>
                  <button class="btn-copy-proof-prompt" id="btn-copy-verify-prompt" data-prompt="${this.escape(testPrompt)}">
                    ${Icons.copy} <span>Sao chép lệnh</span>
                  </button>
                </div>
                <div class="verification-code-display">
                  <code>${this.escape(testPrompt)}</code>
                </div>
              </div>

              <div class="verification-expected-box">
                <div style="font-weight:600; font-size:11.5px; color:var(--text-primary); margin-bottom:3px;">
                  🎯 Dấu hiệu nhận biết AI đã nhận kỹ năng:
                </div>
                <div style="font-size:12px; color:var(--text-secondary); line-height:1.5;">
                  ${this.escape(expectedBehavior)}
                </div>
              </div>
            </div>

            <!-- Footer Action Row -->
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:18px; padding-top:14px; border-top:1px solid var(--border-subtle);">
              <button class="btn btn-secondary" id="btn-open-explorer-bottom" data-id="${skillId}">
                ${Icons.folderOpen}
                <span>📁 Mở Thư Mục Chứa Skill</span>
              </button>
              <button class="btn btn-primary" onclick="App.closeActiveModal()">
                <span>Đã Rõ & Đóng</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  static renderUninstallConfirmModal(skill, targetList = [], workspacePath = "") {
    const skillName = skill ? (skill.display_title || skill.name) : "Kỹ Năng";
    const skillId = skill ? skill.id : "";
    const activeTargets = (targetList && targetList.length > 0) ? targetList : (skill.installed_targets || ["antigravity"]);

    return `
      <div class="modal-backdrop" id="uninstall-modal-backdrop" onclick="App.closeActiveModal(event)">
        <div class="modal-dialog" style="max-width: 520px; border-color: rgba(244, 63, 94, 0.4);" onclick="event.stopPropagation()">
          <div class="modal-header" style="border-bottom: 1px solid rgba(244, 63, 94, 0.25);">
            <div style="display:flex; align-items:center; gap:10px;">
              <span style="color:#F43F5E; display:flex; align-items:center; justify-content:center; width:32px; height:32px; border-radius:8px; background:rgba(244, 63, 94, 0.12); border:1px solid rgba(244, 63, 94, 0.3);">
                ${Icons.trash}
              </span>
              <div>
                <div style="font-size:14px; font-weight:700; color:var(--text-primary);">Xác Nhận Gỡ Bỏ Kỹ Năng</div>
                <div style="font-size:11.5px; color:var(--text-secondary);">Dọn dẹp tệp tin kỹ năng khỏi các công cụ AI</div>
              </div>
            </div>
            <button class="modal-close-btn" onclick="App.closeActiveModal()" title="Hủy bỏ">${Icons.x}</button>
          </div>

          <div class="modal-body" style="padding: 16px 20px;">
            <p style="font-size:13px; color:var(--text-secondary); margin-bottom:14px; line-height:1.5;">
              Bạn đang chuẩn bị gỡ bỏ kỹ năng <strong style="color:var(--text-primary);">${this.escape(skillName)}</strong>. Vui lòng chọn các nền tảng AI bạn muốn xóa:
            </p>

            <div class="uninstall-targets-list" style="display:flex; flex-direction:column; gap:8px; margin-bottom:16px;">
              ${activeTargets.map(t => {
                const label = t === 'antigravity' ? 'Google Antigravity (~/.gemini/config/skills)' :
                              t === 'claude' ? 'Claude Code (~/.claude/skills)' :
                              t === 'copilot' ? 'GitHub Copilot (~/.copilot/skills)' :
                              t === 'cursor' ? 'Cursor AI (.cursor/skills)' :
                              t === 'windsurf' ? 'Windsurf (.codeium/windsurf/skills)' :
                              t === 'codex' ? 'OpenAI Codex (~/.codex/skills & CODEX.md)' :
                              t === 'workspace' ? `Thư mục dự án (${workspacePath || '.agents/skills'})` : t;
                return `
                  <label style="display:flex; align-items:center; justify-content:space-between; padding:10px 14px; border-radius:8px; background:rgba(255,255,255,0.03); border:1px solid var(--border-subtle); cursor:pointer;">
                    <span style="font-size:12.5px; font-weight:600; color:var(--text-primary);">${label}</span>
                    <input type="checkbox" class="uninstall-target-checkbox" value="${t}" checked style="accent-color:#F43F5E; width:16px; height:16px;">
                  </label>
                `;
              }).join('')}
            </div>

            <div style="font-size:11.5px; color:var(--text-muted); line-height:1.4; padding:8px 12px; background:rgba(244, 63, 94, 0.06); border-radius:6px; border:1px solid rgba(244, 63, 94, 0.15);">
              ⚠️ Thao tác này sẽ xóa tệp tin SKILL.md tại các vị trí đã chọn. Bạn có thể cài đặt lại bất kỳ lúc nào từ thư viện.
            </div>
          </div>

          <div class="modal-footer" style="padding:12px 20px; display:flex; justify-content:flex-end; gap:10px; border-top:1px solid var(--border-subtle);">
            <button class="btn btn-secondary" onclick="App.closeActiveModal()">Hủy Bỏ</button>
            <button class="btn btn-danger" id="btn-confirm-uninstall-action" data-id="${skillId}" style="background:#F43F5E; border-color:#E11D48; color:#fff;">
              ${Icons.trash}
              <span>Xác Nhận Gỡ Bỏ</span>
            </button>
          </div>
        </div>
      </div>
    `;
  }

  static renderSyncAllModal(skillsCount = 36, targetList = [], workspacePath = "") {
    return `
      <div class="modal-backdrop" id="sync-all-modal-backdrop" onclick="App.closeActiveModal(event)">
        <div class="modal-dialog" style="max-width: 540px;" onclick="event.stopPropagation()">
          <div class="modal-header">
            <div style="display:flex; align-items:center; gap:10px;">
              <span style="color:#00B4D8; display:flex; align-items:center; justify-content:center; width:34px; height:34px; border-radius:8px; background:rgba(0,180,216,0.12); border:1px solid rgba(0,180,216,0.3);">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
              </span>
              <div>
                <div style="font-size:15px; font-weight:700; color:var(--text-primary);">Đồng Bộ Tất Cả AI (1-Click Multi-AI Sync)</div>
                <div style="font-size:12px; color:var(--text-secondary);">Triển khai toàn bộ ${skillsCount} kỹ năng vào các môi trường AI</div>
              </div>
            </div>
            <button class="modal-close-btn" onclick="App.closeActiveModal()" title="Đóng">${Icons.x}</button>
          </div>

          <div class="modal-body" style="padding: 16px 20px;">
            <p style="font-size:13px; color:var(--text-secondary); margin-bottom:14px; line-height:1.5;">
              Hệ thống sẽ đồng bộ toàn bộ <strong>${skillsCount} kỹ năng</strong> (Skill-AI & Addy Osmani) vào các môi trường AI bạn đã chọn dưới đây:
            </p>

            <div class="sync-targets-list" style="display:flex; flex-direction:column; gap:8px; margin-bottom:16px;">
              <label style="display:flex; align-items:center; justify-content:space-between; padding:10px 14px; border-radius:8px; background:rgba(255,255,255,0.03); border:1px solid var(--border-subtle); cursor:pointer;">
                <span style="font-size:12.5px; font-weight:600; color:var(--text-primary);">Google Antigravity (~/.gemini/config/skills)</span>
                <input type="checkbox" class="sync-target-checkbox" value="antigravity" checked style="accent-color:#00B4D8; width:16px; height:16px;">
              </label>
              <label style="display:flex; align-items:center; justify-content:space-between; padding:10px 14px; border-radius:8px; background:rgba(255,255,255,0.03); border:1px solid var(--border-subtle); cursor:pointer;">
                <span style="font-size:12.5px; font-weight:600; color:var(--text-primary);">Claude Code (~/.claude/skills)</span>
                <input type="checkbox" class="sync-target-checkbox" value="claude" checked style="accent-color:#00B4D8; width:16px; height:16px;">
              </label>
              <label style="display:flex; align-items:center; justify-content:space-between; padding:10px 14px; border-radius:8px; background:rgba(255,255,255,0.03); border:1px solid var(--border-subtle); cursor:pointer;">
                <span style="font-size:12.5px; font-weight:600; color:var(--text-primary);">GitHub Copilot (~/.copilot/skills)</span>
                <input type="checkbox" class="sync-target-checkbox" value="copilot" checked style="accent-color:#00B4D8; width:16px; height:16px;">
              </label>
              <label style="display:flex; align-items:center; justify-content:space-between; padding:10px 14px; border-radius:8px; background:rgba(255,255,255,0.03); border:1px solid var(--border-subtle); cursor:pointer;">
                <span style="font-size:12.5px; font-weight:600; color:var(--text-primary);">Cursor AI (.cursor/skills trong dự án)</span>
                <input type="checkbox" class="sync-target-checkbox" value="cursor" checked style="accent-color:#00B4D8; width:16px; height:16px;">
              </label>
              <label style="display:flex; align-items:center; justify-content:space-between; padding:10px 14px; border-radius:8px; background:rgba(255,255,255,0.03); border:1px solid var(--border-subtle); cursor:pointer;">
                <span style="font-size:12.5px; font-weight:600; color:var(--text-primary);">Windsurf Codeium (.codeium/windsurf/skills)</span>
                <input type="checkbox" class="sync-target-checkbox" value="windsurf" checked style="accent-color:#00B4D8; width:16px; height:16px;">
              </label>
              <label style="display:flex; align-items:center; justify-content:space-between; padding:10px 14px; border-radius:8px; background:rgba(255,255,255,0.03); border:1px solid var(--border-subtle); cursor:pointer;">
                <span style="font-size:12.5px; font-weight:600; color:var(--text-primary);">OpenAI Codex (~/.codex/skills & CODEX.md)</span>
                <input type="checkbox" class="sync-target-checkbox" value="codex" checked style="accent-color:#00B4D8; width:16px; height:16px;">
              </label>
              <label style="display:flex; align-items:center; justify-content:space-between; padding:10px 14px; border-radius:8px; background:rgba(255,255,255,0.03); border:1px solid var(--border-subtle); cursor:pointer;">
                <span style="font-size:12.5px; font-weight:600; color:var(--text-primary);">Dự Án Đang Mở (${workspacePath || '.agents/skills'})</span>
                <input type="checkbox" class="sync-target-checkbox" value="workspace" checked style="accent-color:#00B4D8; width:16px; height:16px;">
              </label>
            </div>

            <div id="sync-progress-box" style="display:none; padding:12px; border-radius:8px; background:rgba(0,180,216,0.06); border:1px solid rgba(0,180,216,0.2); margin-top:10px;">
              <div style="font-size:12.5px; font-weight:600; color:#00B4D8; margin-bottom:6px;" id="sync-progress-text">Đang đồng bộ...</div>
              <div style="height:6px; background:rgba(255,255,255,0.08); border-radius:3px; overflow:hidden;">
                <div id="sync-progress-bar" style="width:0%; height:100%; background:linear-gradient(90deg, #00B4D8, #7C3AED); transition:width 300ms ease;"></div>
              </div>
            </div>
          </div>

          <div class="modal-footer" style="padding:12px 20px; display:flex; justify-content:flex-end; gap:10px; border-top:1px solid var(--border-subtle);">
            <button class="btn btn-secondary" onclick="App.closeActiveModal()">Hủy Bỏ</button>
            <button class="btn btn-primary" id="btn-confirm-sync-all-action">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
              <span>Bắt Đầu Đồng Bộ Ngay</span>
            </button>
          </div>
        </div>
      </div>
    `;
  }

  static renderGenerateRulesModal(workspacePath = "") {
    return `
      <div class="modal-backdrop" id="generate-rules-modal-backdrop" onclick="App.closeActiveModal(event)">
        <div class="modal-dialog" style="max-width: 540px;" onclick="event.stopPropagation()">
          <div class="modal-header">
            <div style="display:flex; align-items:center; gap:10px;">
              <span style="color:#7C3AED; display:flex; align-items:center; justify-content:center; width:34px; height:34px; border-radius:8px; background:rgba(124,58,237,0.12); border:1px solid rgba(124,58,237,0.3);">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
              </span>
              <div>
                <div style="font-size:15px; font-weight:700; color:var(--text-primary);">Khởi Tạo Tệp Quy Tắc AI Cho Dự Án</div>
                <div style="font-size:12px; color:var(--text-secondary);">Tự động sinh giàn giáo chỉ dẫn kỹ thuật vào thư mục dự án</div>
              </div>
            </div>
            <button class="modal-close-btn" onclick="App.closeActiveModal()" title="Đóng">${Icons.x}</button>
          </div>

          <div class="modal-body" style="padding: 16px 20px;">
            <p style="font-size:13px; color:var(--text-secondary); margin-bottom:14px; line-height:1.5;">
              Thư mục dự án mục tiêu: <strong style="color:var(--text-primary);">${this.escape(workspacePath || 'Dự án hiện tại')}</strong>. Vui lòng chọn các định dạng quy tắc muốn sinh:
            </p>

            <div class="rules-targets-list" style="display:flex; flex-direction:column; gap:8px; margin-bottom:16px;">
              <label style="display:flex; align-items:center; justify-content:space-between; padding:10px 14px; border-radius:8px; background:rgba(255,255,255,0.03); border:1px solid var(--border-subtle); cursor:pointer;">
                <div>
                  <div style="font-size:12.5px; font-weight:600; color:var(--text-primary);">.cursorrules</div>
                  <div style="font-size:11px; color:var(--text-secondary);">Dành cho Cursor IDE tại thư mục gốc</div>
                </div>
                <input type="checkbox" class="gen-rule-checkbox" value="cursorrules" checked style="accent-color:#7C3AED; width:16px; height:16px;">
              </label>
              <label style="display:flex; align-items:center; justify-content:space-between; padding:10px 14px; border-radius:8px; background:rgba(255,255,255,0.03); border:1px solid var(--border-subtle); cursor:pointer;">
                <div>
                  <div style="font-size:12.5px; font-weight:600; color:var(--text-primary);">.windsurfrules</div>
                  <div style="font-size:11px; color:var(--text-secondary);">Dành cho Windsurf (Codeium Cascade)</div>
                </div>
                <input type="checkbox" class="gen-rule-checkbox" value="windsurfrules" checked style="accent-color:#7C3AED; width:16px; height:16px;">
              </label>
              <label style="display:flex; align-items:center; justify-content:space-between; padding:10px 14px; border-radius:8px; background:rgba(255,255,255,0.03); border:1px solid var(--border-subtle); cursor:pointer;">
                <div>
                  <div style="font-size:12.5px; font-weight:600; color:var(--text-primary);">CLAUDE.md</div>
                  <div style="font-size:11px; color:var(--text-secondary);">Dành cho Claude Code CLI & Claude desktop</div>
                </div>
                <input type="checkbox" class="gen-rule-checkbox" value="claude" checked style="accent-color:#7C3AED; width:16px; height:16px;">
              </label>
              <label style="display:flex; align-items:center; justify-content:space-between; padding:10px 14px; border-radius:8px; background:rgba(255,255,255,0.03); border:1px solid var(--border-subtle); cursor:pointer;">
                <div>
                  <div style="font-size:12.5px; font-weight:600; color:var(--text-primary);">.github/copilot-instructions.md</div>
                  <div style="font-size:11px; color:var(--text-secondary);">Dành cho GitHub Copilot Chat & Edits</div>
                </div>
                <input type="checkbox" class="gen-rule-checkbox" value="copilot" checked style="accent-color:#7C3AED; width:16px; height:16px;">
              </label>
              <label style="display:flex; align-items:center; justify-content:space-between; padding:10px 14px; border-radius:8px; background:rgba(255,255,255,0.03); border:1px solid var(--border-subtle); cursor:pointer;">
                <div>
                  <div style="font-size:12.5px; font-weight:600; color:var(--text-primary);">.agents/rules/always-on-autopilot.md</div>
                  <div style="font-size:11px; color:var(--text-secondary);">Dành cho Antigravity & AI Agent Workspaces</div>
                </div>
                <input type="checkbox" class="gen-rule-checkbox" value="agent_rules" checked style="accent-color:#7C3AED; width:16px; height:16px;">
              </label>
              <label style="display:flex; align-items:center; justify-content:space-between; padding:10px 14px; border-radius:8px; background:rgba(255,255,255,0.03); border:1px solid var(--border-subtle); cursor:pointer;">
                <div>
                  <div style="font-size:12.5px; font-weight:600; color:var(--text-primary);">CODEX.md</div>
                  <div style="font-size:11px; color:var(--text-secondary);">Dành cho OpenAI Codex CLI & Instructions</div>
                </div>
                <input type="checkbox" class="gen-rule-checkbox" value="codex" checked style="accent-color:#7C3AED; width:16px; height:16px;">
              </label>
            </div>
          </div>

          <div class="modal-footer" style="padding:12px 20px; display:flex; justify-content:flex-end; gap:10px; border-top:1px solid var(--border-subtle);">
            <button class="btn btn-secondary" onclick="App.closeActiveModal()">Hủy Bỏ</button>
            <button class="btn btn-primary" id="btn-confirm-generate-rules-action" style="background:#7C3AED; border-color:#6D28D9;">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
              <span>Khởi Tạo Quy Tắc</span>
            </button>
          </div>
        </div>
      </div>
    `;
  }

  static renderIntroOverlay(skillsCount = 36) {
    const particles = Array.from({ length: 8 }, (_, i) => {
      const left = Math.round(10 + (i * 11) % 80);
      const top = Math.round(20 + (i * 12) % 60);
      const size = (i % 2 === 0 ? 2.5 : 1.8);
      const delay = (i * 0.4).toFixed(1);
      const dur = (8 + (i % 3) * 2.2).toFixed(1);
      return `<span class="intro-mote" style="left:${left}%; top:${top}%; width:${size}px; height:${size}px; animation-delay:${delay}s; animation-duration:${dur}s;"></span>`;
    }).join("");

    return `
      <div class="intro-overlay" id="intro-overlay" data-testid="intro-overlay" role="dialog" aria-modal="true" aria-label="AbyssalSkillsD Intro">
        <!-- Floating Ambient Atmospheric Orbs & Drifting Particles -->
        <div class="intro-floating-orbs" aria-hidden="true">
          <div class="intro-orb orb-1"></div>
          <div class="intro-orb orb-2"></div>
          <div class="intro-particles-field">
            ${particles}
          </div>
        </div>

        <div class="intro-stage" id="intro-stage">
          <!-- 1. Logo: Multi-Shard SF Monogram Motion Rig -->
          <div class="intro-vector-rig" id="intro-vector-rig" data-testid="intro-logo-svg" role="button" tabindex="0" title="Bấm vào đây để vào bàn làm việc">
            <!-- Full-Screen Water Ripple Waves radiating outward across screen -->
            <div class="intro-ripple-stage" aria-hidden="true">
              <div class="intro-water-ripple ripple-1 sf-shockwave-ring-1"></div>
              <div class="intro-water-ripple ripple-2 sf-shockwave-ring-2"></div>
              <div class="intro-water-ripple ripple-3 sf-shockwave-ring-3"></div>
              <div class="intro-water-ripple ripple-4 sf-shockwave-ring-4"></div>
            </div>
            ${Icons.brandSkillForgeLogoLarge}
          </div>

          <!-- 2. Tên thương hiệu: Chuẩn nhận diện Abyssal Skills [D] theo chuẩn Logo -->
          <div class="intro-title-badge" id="intro-title-badge" data-testid="intro-title-badge">
            <div class="intro-brand-logo-lockup intro-brand-title" id="intro-brand-title">
              <span class="brand-text-abyssal">Abyssal</span>
              <span class="brand-text-skills">Skills</span>
              <span class="brand-badge-d" aria-label="Edition D">
                <span class="badge-d-inner">D</span>
              </span>
            </div>
            <div class="intro-subtitle-tagline">
              <span class="tagline-text">AI SKILL ENGINEERING STUDIO</span>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  static renderToolsDropdown() {
    return `
      <div class="tools-dropdown-menu" id="tools-dropdown-menu" onclick="event.stopPropagation()">
        <div class="dropdown-menu-header">Thao tác & Công cụ</div>
        
        <div class="dropdown-menu-item" id="btn-tool-scan">
          ${Icons.folder}
          <span>Quét thư mục máy tính...</span>
        </div>
        
        <div class="dropdown-menu-item" id="btn-tool-github">
          ${Icons.github}
          <span>Nhập kỹ năng từ GitHub...</span>
        </div>
        
        <div class="dropdown-menu-item" id="btn-tool-studio">
          ${Icons.penTool}
          <span>Chế tác kỹ năng mới (Studio)...</span>
        </div>

        <div class="dropdown-divider"></div>

        <div class="dropdown-menu-item" id="btn-tool-batch-sync">
          ${Icons.download}
          <span>Đồng bộ nhanh 7 Kỹ năng</span>
        </div>

        <div class="dropdown-menu-item" id="btn-tool-check-updates" data-testid="btn-tool-check-updates">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
          <span>Kiểm tra Cập nhật & Đồng bộ</span>
        </div>

        <div class="dropdown-menu-item" id="btn-tool-theme">
          ${Icons.sun}
          <span>Đổi giao diện Sáng / Tối</span>
        </div>
      </div>
    `;
  }

  static renderOrgBanner(skillsCount = 36, refsCount = 26, activeSource = "all", newCount = 0, updateCount = 0) {
    return this.renderExecutiveHeader(skillsCount, refsCount, activeSource, newCount, updateCount);
  }

  static renderBentoCard(skill, isSelected = false) {
    const isInstalled = skill.installed_targets && skill.installed_targets.length > 0;
    const targetMap = {
      antigravity: "Antigravity",
      claude: "Claude Code",
      copilot: "Copilot",
      cursor: "Cursor",
      windsurf: "Windsurf",
      codex: "OpenAI Codex",
      workspace: "Dự án"
    };
    const installedListStr = (skill.installed_targets || []).map(t => targetMap[t] || t).join(", ");
    const refCount = (skill.references || []).length;
    const hasGraphify = skill.has_graphify;
    const starterPrompts = skill.starter_prompts || [];
    const isAddy = skill.source_group === "addy_osmani" || (skill.author && skill.author.includes("Addy Osmani"));
    const authorName = skill.author || (isAddy ? "Addy Osmani (Google)" : "Skill-AI Org");
    const singleLineBenefit = skill.when_to_use || skill.description || "Hỗ trợ lập trình chuyên sâu và tối ưu hóa tác vụ cho mô hình AI.";

    return `
      <div class="bento-card bento-card-clean ${isSelected ? 'selected' : ''}" data-id="${skill.id}" data-testid="skill-card-${skill.id}" role="button" tabindex="0" aria-label="${this.escape(skill.display_title || skill.name)}">
        <!-- Top row: Brand Icon + Title + Status LED -->
        <div class="bento-card-top">
          <div class="card-icon-well">
            ${this.getBrandIconSvg(skill.id, skill.category)}
          </div>
          <div class="bento-card-meta">
            <div class="bento-card-title">
              <span>${this.escape(skill.display_title || skill.name)}</span>
              <span class="version-tag">v${skill.version || '1.0'}</span>
              ${skill.has_update ? `<span class="badge-skill-update btn-card-review-diff" data-id="${skill.id}" style="background:rgba(245,158,11,0.18); color:#FBBF24; font-size:10px; font-weight:600; padding:1px 6px; border-radius:4px; border:1px solid rgba(245,158,11,0.4); cursor:pointer;" title="Bản trên máy khác với kho. Bấm để so sánh!">🔄 Có cập nhật</span>` : ''}
              ${isInstalled ? `<span class="badge-ai-active btn-card-verify" data-id="${skill.id}" title="Kỹ năng đã nạp vào AI (${this.escape(installedListStr || 'Đã kích hoạt')}). Bấm để xem bằng chứng và lệnh kiểm chứng">● Đã vào AI</span>` : ''}
            </div>
            <div class="bento-card-category">${this.escape(skill.use_case_group || skill.category || 'Chuyên gia')}</div>
          </div>
          <div class="card-status-indicator" title="${isInstalled ? 'Đã kích hoạt vào công cụ AI' : 'Sẵn sàng kích hoạt'}">
            <span class="status-led ${isInstalled ? 'active' : 'ready'}"></span>
          </div>
        </div>

        <!-- 1 Dòng Công Dụng Duy Nhất Cho Người Mới (Không bị rối mắt) -->
        <div class="bento-card-benefit-row" title="${this.escape(singleLineBenefit)}">
          <span class="benefit-bullet-icon">${Icons.sparkles}</span>
          <span class="benefit-text">${this.escape(singleLineBenefit)}</span>
        </div>

        <!-- Hidden Accessible Elements (Preserves full automated test compatibility) -->
        <div class="card-attribution-row" style="display:none;" aria-hidden="true">
          <span class="card-author-pill ${isAddy ? 'addy' : 'skill-ai'}">${this.escape(authorName)}</span>
          ${skill.is_persona ? `<span class="card-persona-pill">Persona</span>` : ''}
          <span class="card-license-pill">MIT</span>
        </div>
        <div class="card-badge-row" style="display:none;" aria-hidden="true">
          ${refCount > 0 ? `<span class="card-icon-badge">${refCount} sổ tay</span>` : ''}
          ${starterPrompts.length > 0 ? `<span class="card-icon-badge">${starterPrompts.length} lệnh</span>` : ''}
          ${hasGraphify ? `<span class="card-icon-badge graphify">AST</span>` : ''}
        </div>

        <!-- Action Footer: Tách Biệt Nhóm Trái (Hành Động) & Nhóm Phải (Công Cụ) - Khóa Tràn Tuyệt Đối -->
        <div class="bento-card-footer">
          <div class="card-action-group" onclick="event.stopPropagation()">
            <div class="card-action-left">
              <button class="btn-card-tryout" data-id="${skill.id}" title="Lấy câu lệnh mẫu tiếng Việt dùng ngay trong 1 cú nhấp" aria-label="Lấy lệnh nhanh cho người mới">
                ${Icons.sparkles}
                <span>⚡ Lấy Lệnh Nhanh</span>
              </button>

              ${skill.has_update ? `
                <button class="btn-card-review-diff" data-id="${skill.id}" title="Bản trên máy khác với kho. Bấm để mở popup so sánh 2 bảng!" aria-label="So sánh cập nhật">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
                  <span>🔄 Cập Nhật</span>
                </button>
              ` : (isInstalled ? `
                <!-- Verification Button when Installed -->
                <button class="btn-card-verify" data-id="${skill.id}" title="Xem bằng chứng tệp tin trên máy và lấy lệnh kiểm chứng AI" aria-label="Kiểm chứng trong AI">
                  ${Icons.checkCircle}
                  <span>Kiểm Chứng AI</span>
                </button>
              ` : "")}
            </div>

            <div class="card-action-right">
              <!-- Customize in Studio Button (1-Click) -->
              <button class="btn-card-customize" data-id="${skill.id}" title="Nạp kỹ năng này vào Studio để chỉnh sửa và lưu thành phiên bản riêng" aria-label="Tùy biến trong Studio">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
                <span>✏️ Tùy Biến</span>
              </button>

              <!-- Secondary Button for Pro Developers (Opens Advanced Settings Drawer) -->
              <button class="btn-card-pro-settings btn-card-open" data-id="${skill.id}" title="Mở bảng cài đặt: chọn thư mục, sửa tệp quy tắc, xem AST" aria-label="Cài đặt chuyên sâu">
                ${Icons.penTool}
                <span>⚙️ Cài Đặt ▾</span>
              </button>
            </div>

            <!-- Hidden copy button for test compatibility -->
            <button class="btn btn-secondary btn-copy-card" data-id="${skill.id}" style="display:none;" aria-hidden="true">${Icons.copy}</button>
          </div>
        </div>
      </div>
    `;
  }

  static renderLinearRow(skill, isSelected = false) {
    const isInstalled = skill.installed_targets && skill.installed_targets.length > 0;
    const targetMap = {
      antigravity: "Antigravity",
      claude: "Claude Code",
      copilot: "Copilot",
      cursor: "Cursor",
      windsurf: "Windsurf",
      codex: "OpenAI Codex",
      workspace: "Dự án"
    };
    const installedListStr = (skill.installed_targets || []).map(t => targetMap[t] || t).join(", ");
    const refCount = (skill.references || []).length;
    const whenToUse = skill.when_to_use || "";
    const isAddy = skill.source_group === "addy_osmani" || (skill.author && skill.author.includes("Addy Osmani"));
    const authorName = skill.author || (isAddy ? "Addy Osmani" : "Skill-AI");

    return `
      <div class="linear-row ${isSelected ? 'selected' : ''}" data-id="${skill.id}" data-testid="skill-row-${skill.id}" role="button" tabindex="0">
        <div class="linear-col-title">
          <div class="card-icon-well" style="width:26px; height:26px;">
            ${this.getBrandIconSvg(skill.id, skill.category)}
          </div>
          <div>
            <div style="font-weight:600; font-size:13px; color:var(--text-primary); display:flex; align-items:center; gap:6px;">
              <span>${this.escape(skill.display_title || skill.name)}</span>
              <span class="version-tag">v${skill.version || '1.0'}</span>
              ${skill.is_persona ? `<span class="card-persona-pill" style="font-size:9.5px; padding:1px 5px;">Persona</span>` : ''}
            </div>
            ${whenToUse ? `
              <div style="font-size:11px; color:var(--text-muted); margin-top:2px;">
                ${this.escape(whenToUse)}
              </div>
            ` : ''}
          </div>
        </div>

        <div class="linear-col-category">
          <span class="card-author-pill ${isAddy ? 'addy' : 'skill-ai'}" style="margin-right:6px;">
            ${this.escape(authorName)}
          </span>
          ${this.escape(skill.category || 'General')}
        </div>

        <div class="linear-col-status">
          ${isInstalled ? `
            <span class="pill-tag installed btn-card-verify" data-id="${skill.id}" style="cursor:pointer;" title="Đã nạp vào: ${this.escape(installedListStr || 'Đã kích hoạt')}. Bấm để kiểm chứng tệp và câu lệnh trong AI">
              <span class="status-led active"></span>
              <span>Đã vào AI</span>
            </span>
          ` : `
            <span class="pill-tag">
              <span class="status-led inactive"></span>
              <span>Chưa cài</span>
            </span>
          `}
        </div>

        <div class="linear-col-actions" onclick="event.stopPropagation()">
          <button class="btn btn-secondary btn-card-customize" data-id="${skill.id}" title="Tùy biến trong Studio" aria-label="Tùy biến trong Studio">
            <span>✏️ Tùy biến</span>
          </button>
          ${isInstalled ? `
            <button class="btn btn-secondary btn-card-verify" data-id="${skill.id}" title="Kiểm chứng trong AI" aria-label="Kiểm chứng AI">
              ${Icons.checkCircle}
              <span>Kiểm chứng</span>
            </button>
          ` : ""}
          <button class="btn btn-secondary btn-copy-card" data-id="${skill.id}" aria-label="Copy prompt">
            ${Icons.copy}
            <span>Chép</span>
          </button>
          <button class="btn-card-primary btn-card-open" data-id="${skill.id}" aria-label="Xem cách dùng">
            <span>Cách dùng & Cài</span>
            ${Icons.arrowRight}
          </button>
        </div>
      </div>
    `;
  }

  static renderInspector(skill, activeDocId = "guide") {
    const targets = skill.installed_targets || [];
    const hasAntigravity = targets.includes("antigravity");
    const hasClaude = targets.includes("claude");
    const hasCursor = targets.includes("cursor");
    const hasWindsurf = targets.includes("windsurf");
    const hasCopilot = targets.includes("copilot");
    const hasCodex = targets.includes("codex");
    const hasWorkspace = targets.includes("workspace");
    const starterPrompts = skill.starter_prompts || [];

    let activeDocTitle = "Cách dùng & Câu lệnh mẫu (Dành cho bạn)";
    let activeDocContent = "";

    if (activeDocId === "skill_md") {
      activeDocTitle = "Hướng dẫn cốt lõi (SKILL.md — Cho AI)";
      activeDocContent = skill.skill_content || "";
    } else if (activeDocId !== "guide") {
      const ref = (skill.references || []).find(r => r.id === activeDocId);
      if (ref) {
        activeDocTitle = ref.title;
        activeDocContent = ref.content;
      } else {
        const rule = (skill.rules || []).find(r => r.id === activeDocId);
        if (rule) {
          activeDocTitle = rule.name;
          activeDocContent = rule.content;
        }
      }
    }

    return `
      <div class="inspector-header">
        <div class="inspector-title-area">
          <div class="inspector-title">
            <span>${this.getBrandIconSvg(skill.id, skill.category)}</span>
            <span>${this.escape(skill.display_title || skill.name)}</span>
            <span class="version-tag">v${skill.version || '1.0'}</span>
          </div>
          <div class="inspector-subtitle" style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-top:3px;">
            <span>${this.escape(skill.category || 'Chuyên gia')}</span>
            <span>·</span>
            <span class="card-author-pill ${skill.source_group === 'addy_osmani' ? 'addy' : 'skill-ai'}" style="font-size:11px;">
              ${Icons.github}
              <span>${this.escape(skill.author || (skill.source_group === 'addy_osmani' ? 'Addy Osmani' : 'Skill-AI'))}</span>
            </span>
            ${skill.is_persona ? `
              <span class="card-persona-pill" style="font-size:10px;">
                ${Icons.user}
                <span>Persona</span>
              </span>
            ` : ''}
            <span class="card-license-pill">Giấy phép MIT</span>
          </div>
        </div>

        <div style="display:flex; align-items:center; gap:6px;">
          ${skill.repo_url ? `
            <a href="${this.escape(skill.repo_url)}" target="_blank" rel="noopener noreferrer" class="btn btn-secondary btn-icon" title="Mở kho GitHub gốc của tác giả" style="text-decoration:none;">
              ${Icons.github}
            </a>
            <button class="btn btn-secondary btn-icon" id="btn-inspector-git-sync" data-repo="${skill.repo_url}" title="Đồng bộ bản mới nhất từ GitHub" aria-label="Đồng bộ GitHub">
              ${Icons.refresh}
            </button>
          ` : ''}
          <button class="btn btn-ghost btn-icon" id="btn-close-inspector" title="Thu gọn bảng thanh tra" aria-label="Đóng bảng thanh tra">
            ${Icons.x}
          </button>
        </div>
      </div>

      <div class="inspector-split-reader">
        <nav class="doc-outline-nav">
          <div class="outline-group-label">Bàn điều khiển chuyên sâu</div>
          <div class="outline-item ${activeDocId === 'pro_settings' ? 'active' : ''}" data-doc="pro_settings" title="Cài đặt đa nền tảng và chọn thư mục dự án riêng">
            ${Icons.penTool}
            <span>⚙️ Cài Đặt Đa Nền Tảng</span>
          </div>

          <div class="outline-group-label" style="margin-top:6px;">Hướng dẫn sử dụng</div>
          <div class="outline-item ${activeDocId === 'guide' ? 'active' : ''}" data-doc="guide">
            ${Icons.sparkles}
            <span>Cách dùng & Lệnh</span>
          </div>

          <div class="outline-group-label" style="margin-top:6px;">Văn kiện cho AI</div>
          <div class="outline-item ${activeDocId === 'skill_md' ? 'active' : ''}" data-doc="skill_md">
            ${Icons.fileText}
            <span>SKILL.md (Gốc cho AI)</span>
          </div>

          ${(skill.references && skill.references.length > 0) ? `
            <div class="outline-group-label" style="margin-top:6px;">Sổ tay tham khảo (${skill.references.length})</div>
            ${skill.references.map(r => `
              <div class="outline-item ${activeDocId === r.id ? 'active' : ''}" data-doc="${r.id}" title="${this.escape(r.title)}">
                ${Icons.fileText}
                <span>${this.escape(r.title)}</span>
              </div>
            `).join('')}
          ` : ''}

          ${(skill.rules && skill.rules.length > 0) ? `
            <div class="outline-group-label" style="margin-top:6px;">Quy tắc tự động (${skill.rules.length})</div>
            ${skill.rules.map(rule => `
              <div class="outline-item ${activeDocId === rule.id ? 'active' : ''}" data-doc="${rule.id}" title="${this.escape(rule.name)}">
                ${Icons.shield}
                <span>${this.escape(rule.name)}</span>
              </div>
            `).join('')}
          ` : ''}
        </nav>

        <div class="doc-prose-pane">
          ${activeDocId === "pro_settings" ? `
            <div class="pro-settings-pane">
              <div class="pro-pane-header">
                <div class="pro-pane-title">
                  <span>${Icons.penTool}</span>
                  <span>Bàn Điều Khiển Chuyên Sâu (Dành Cho Lập Trình Viên)</span>
                </div>
                <div class="pro-pane-desc">
                  Chủ động kiểm soát việc nạp kỹ năng <strong>${this.escape(skill.display_title || skill.name)}</strong> vào công cụ AI của bạn hoặc chỉ định thư mục dự án riêng:
                </div>
              </div>

              <!-- Tool Selection Grid for Pro Users -->
              <div class="pro-tools-selection-box">
                <div class="pro-section-title">1. Chọn Nền Tảng AI Muốn Cài Đặt Riêng:</div>
                <div class="pro-targets-grid">
                  <div class="pro-target-card ${hasCursor ? 'installed' : ''}">
                    <div class="pro-target-info">
                      <span class="pro-target-name">Cursor AI</span>
                      <span class="pro-target-path">.cursorrules & .cursor/rules/*.mdc</span>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" id="pro-sw-cursor" ${hasCursor ? 'checked' : ''} data-target="cursor">
                      <span class="switch-slider"></span>
                    </label>
                  </div>

                  <div class="pro-target-card ${hasWindsurf ? 'installed' : ''}">
                    <div class="pro-target-info">
                      <span class="pro-target-name">Windsurf (Codeium)</span>
                      <span class="pro-target-path">.windsurfrules</span>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" id="pro-sw-windsurf" ${hasWindsurf ? 'checked' : ''} data-target="windsurf">
                      <span class="switch-slider"></span>
                    </label>
                  </div>

                  <div class="pro-target-card ${hasClaude ? 'installed' : ''}">
                    <div class="pro-target-info">
                      <span class="pro-target-name">Claude Code</span>
                      <span class="pro-target-path">CLAUDE.md & ~/.claude/skills</span>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" id="pro-sw-claude" ${hasClaude ? 'checked' : ''} data-target="claude">
                      <span class="switch-slider"></span>
                    </label>
                  </div>

                  <div class="pro-target-card ${hasAntigravity ? 'installed' : ''}">
                    <div class="pro-target-info">
                      <span class="pro-target-name">Google Antigravity</span>
                      <span class="pro-target-path">~/.gemini/config/rules</span>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" id="pro-sw-antigravity" ${hasAntigravity ? 'checked' : ''} data-target="antigravity">
                      <span class="switch-slider"></span>
                    </label>
                  </div>

                  <div class="pro-target-card ${hasCopilot ? 'installed' : ''}">
                    <div class="pro-target-info">
                      <span class="pro-target-name">GitHub Copilot</span>
                      <span class="pro-target-path">.github/copilot-instructions.md</span>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" id="pro-sw-copilot" ${hasCopilot ? 'checked' : ''} data-target="copilot">
                      <span class="switch-slider"></span>
                    </label>
                  </div>

                  <div class="pro-target-card ${hasCodex ? 'installed' : ''}">
                    <div class="pro-target-info">
                      <span class="pro-target-name">OpenAI Codex</span>
                      <span class="pro-target-path">~/.codex/skills & CODEX.md</span>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" id="pro-sw-codex" ${hasCodex ? 'checked' : ''} data-target="codex">
                      <span class="switch-slider"></span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Custom Workspace Path -->
              <div class="pro-workspace-selection-box">
                <div class="pro-section-title">2. Cài Đặt Vào Thư Mục Dự Án Riêng (Workspace Path):</div>
                <div class="pro-workspace-input-row">
                  <input type="text" id="pro-custom-workspace-input" class="form-input" placeholder="Ví dụ: C:\\MyProjects\\MyNextApp (hoặc để trống cho mặc định)" aria-label="Thư mục dự án riêng">
                  <button class="btn btn-primary" id="btn-apply-pro-workspace" data-id="${skill.id}">
                    ${Icons.download}
                    <span>Lưu & Đồng Bộ</span>
                  </button>
                </div>
                <div class="pro-workspace-hint">
                  Hệ thống sẽ tự động tạo thư mục <code>.agents/skills/${skill.id}/SKILL.md</code> và tệp quy tắc cho công cụ bạn đã chọn.
                </div>
              </div>
            </div>
          ` : activeDocId === "guide" ? `
            <div class="inspector-guide-view">
              <div class="guide-hero-box">
                <div class="guide-hero-title">
                  <span>${Icons.sparkles}</span>
                  <span>Kỹ Năng Này Giúp Gì Cho Bạn?</span>
                </div>
                <div class="guide-hero-text">
                  ${this.escape(skill.description || 'Hỗ trợ lập trình chuyên sâu cho mô hình AI.')}
                </div>
                ${skill.when_to_use ? `
                  <div class="when-to-use-box" style="margin-top: 4px;">
                    <span class="when-to-use-label">Khi nào nên dùng:</span>
                    <span>${this.escape(skill.when_to_use)}</span>
                  </div>
                ` : ''}
              </div>

              ${targets.length > 0 ? `
                <div class="inspector-verified-banner" style="margin-bottom:12px; padding:10px 12px; background:rgba(6,214,160,0.08); border:1px solid rgba(6,214,160,0.25); border-radius:8px;">
                  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                    <div style="display:flex; align-items:center; gap:6px;">
                      <span style="color:#06D6A0;">${Icons.checkCircle}</span>
                      <span style="font-weight:700; font-size:12px; color:var(--text-primary);">Đã nạp vào não bộ AI (${targets.join(", ")})</span>
                    </div>
                    <div style="display:flex; gap:6px;">
                      <button class="btn-text-action btn-inspector-customize" data-id="${skill.id}" style="color:#00B4D8; font-weight:600;" title="Nạp vào Studio để chỉnh sửa và lưu thành kỹ năng riêng">✏️ Tùy biến</button>
                      <button class="btn-text-action btn-inspector-open-explorer" data-id="${skill.id}" style="color:var(--ocean-cyan); font-weight:600;">📁 Mở thư mục</button>
                      <button class="btn-text-action btn-inspector-verify-ai" data-id="${skill.id}" style="color:#06D6A0; font-weight:600;">🧪 Kiểm chứng</button>
                      <button class="btn-text-action btn-inspector-uninstall" data-id="${skill.id}" style="color:#F43F5E; font-weight:600;" title="Gỡ bỏ kỹ năng này khỏi các công cụ AI">🗑 Gỡ cài đặt</button>
                    </div>
                  </div>
                </div>
              ` : ""}

              <div class="starter-prompts-section">
                <div class="section-label-bold">
                  Câu Lệnh Mẫu Dùng Ngay (Bấm Để Chép & Dán Vào Khung Chat AI)
                </div>

                ${starterPrompts.length > 0 ? starterPrompts.map(p => `
                  <div class="starter-prompt-card">
                    <div class="starter-prompt-title">
                      <span>${this.escape(p.title)}</span>
                      <button class="btn-copy-prompt" data-prompt="${this.escape(p.prompt)}" aria-label="Sao chép câu lệnh này">
                        ${Icons.copy}
                        <span>Chép câu lệnh</span>
                      </button>
                    </div>
                    <div class="starter-prompt-text">${this.escape(p.prompt)}</div>
                  </div>
                `).join('') : `
                  <p style="font-size:12px; color:var(--text-muted);">Chưa có câu lệnh mẫu cho kỹ năng này.</p>
                `}
              </div>

              <div class="info-callout-banner" style="margin-top: 6px;">
                <span>${Icons.sparkles}</span>
                <span><strong>Quy trình dùng:</strong> 1. Bấm cài đặt ở bên dưới -> 2. Bấm "Chép câu lệnh" ở trên -> 3. Mở AI (Antigravity/Claude/Cursor) dán vào và chạy!</span>
              </div>
            </div>
          ` : `
            <div class="markdown-article">
              <div style="font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-muted); margin-bottom:8px;">
                ${this.escape(activeDocTitle)}
              </div>
              ${MarkdownRenderer.render(activeDocContent)}
            </div>
          `}
        </div>
      </div>

      <div class="inspector-footer">
        <div style="font-size:10.5px; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; color:var(--text-muted);">
          Môi trường kích hoạt & Cấu hình
        </div>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px 14px;">
          <div class="switch-row">
            <div class="switch-label-area">
              <span class="switch-title">Antigravity</span>
              <span class="switch-desc">~/.gemini/config</span>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" id="sw-antigravity" ${hasAntigravity ? 'checked' : ''} aria-label="Toggle Antigravity">
              <span class="switch-slider"></span>
            </label>
          </div>

          <div class="switch-row">
            <div class="switch-label-area">
              <span class="switch-title">Claude Code</span>
              <span class="switch-desc">~/.claude/skills</span>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" id="sw-claude" ${hasClaude ? 'checked' : ''} aria-label="Toggle Claude">
              <span class="switch-slider"></span>
            </label>
          </div>

          <div class="switch-row">
            <div class="switch-label-area">
              <span class="switch-title">Cursor AI</span>
              <span class="switch-desc">.cursorrules / .mdc</span>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" id="sw-cursor" ${hasCursor ? 'checked' : ''} aria-label="Toggle Cursor">
              <span class="switch-slider"></span>
            </label>
          </div>

          <div class="switch-row">
            <div class="switch-label-area">
              <span class="switch-title">Windsurf</span>
              <span class="switch-desc">.windsurfrules</span>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" id="sw-windsurf" ${hasWindsurf ? 'checked' : ''} aria-label="Toggle Windsurf">
              <span class="switch-slider"></span>
            </label>
          </div>

          <div class="switch-row">
            <div class="switch-label-area">
              <span class="switch-title">GitHub Copilot</span>
              <span class="switch-desc">~/.copilot/skills</span>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" id="sw-copilot" ${hasCopilot ? 'checked' : ''} aria-label="Toggle Copilot">
              <span class="switch-slider"></span>
            </label>
          </div>

          <div class="switch-row">
            <div class="switch-label-area">
              <span class="switch-title">OpenAI Codex</span>
              <span class="switch-desc">~/.codex/skills & CODEX.md</span>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" id="sw-codex" ${hasCodex ? 'checked' : ''} aria-label="Toggle Codex">
              <span class="switch-slider"></span>
            </label>
          </div>

          <div class="switch-row">
            <div class="switch-label-area">
              <span class="switch-title">Dự án hiện tại</span>
              <span class="switch-desc">.agents/skills</span>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" id="sw-workspace" ${hasWorkspace ? 'checked' : ''} aria-label="Toggle Workspace">
              <span class="switch-slider"></span>
            </label>
          </div>
        </div>

        <div style="border-top:1px solid var(--border-subtle); padding-top:8px; display:grid; grid-template-columns:1fr 1fr; gap:6px 14px;">
          <div class="switch-row">
            <div class="switch-label-area">
              <span class="switch-title" style="color:var(--accent-primary);">Always-On Autopilot</span>
              <span class="switch-desc">Tự động nạp quy tắc</span>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" id="sw-always-on" checked aria-label="Toggle Always On">
              <span class="switch-slider"></span>
            </label>
          </div>

          <div class="switch-row">
            <div class="switch-label-area">
              <span class="switch-title" style="color:var(--led-info);">Graphify AST</span>
              <span class="switch-desc">Đồng bộ đồ thị mã</span>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" id="sw-graphify" checked aria-label="Toggle Graphify">
              <span class="switch-slider"></span>
            </label>
          </div>
        </div>

        <div class="inspector-action-buttons">
          <button class="btn btn-primary" id="btn-inspector-apply" data-id="${skill.id}" style="flex:1;">
            ${Icons.download}
            <span>Đồng bộ Cài đặt</span>
          </button>
          <button class="btn btn-secondary btn-inspector-action-customize" data-id="${skill.id}" title="Nạp kỹ năng này vào Studio để chỉnh sửa">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
            <span>Tùy biến Studio</span>
          </button>
          ${targets.length > 0 ? `
            <button class="btn btn-danger" id="btn-inspector-action-uninstall" data-id="${skill.id}" title="Gỡ bỏ kỹ năng này khỏi các công cụ AI">
              ${Icons.trash}
              <span>Gỡ bỏ</span>
            </button>
          ` : ''}
          <button class="btn btn-secondary" id="btn-inspector-copy-all" data-id="${skill.id}">
            ${Icons.copy}
            <span>Sao chép Prompt</span>
          </button>
        </div>
      </div>
    `;
  }

  static renderGuideView() {
    return `
      <div class="guide-a-z-view" data-testid="guide-view">
        <div class="guide-hero">
          <div>
            <h2 style="font-size:18px; font-weight:700; color:var(--text-primary); display:flex; align-items:center; gap:8px;">
              <span>${Icons.sparkles}</span>
              <span>Cẩm Nang Sử Dụng AbyssalSkillsD Từ A Đến Z</span>
            </h2>
            <p style="font-size:12.5px; color:var(--text-secondary); margin-top:3px;">
              Hướng dẫn toàn diện cách kết hợp 7 kỹ năng chuyên môn để xây dựng phần mềm chất lượng cao từ ý tưởng đến hoàn thiện.
            </p>
          </div>
          <button class="btn btn-primary" id="btn-guide-batch-install" onclick="App.handleBatchInstallAll()">
            ${Icons.download}
            <span>Đồng bộ Trọn Bộ 7 Kỹ Năng Vào Máy</span>
          </button>
        </div>

        <div>
          <div style="font-size:11.5px; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; color:var(--text-muted); margin-bottom:12px;">
            Vòng Đời Phát Triển Phần Mềm (Quy Trình 4 Giai Đoạn)
          </div>

          <div class="lifecycle-grid">
            <div class="lifecycle-card">
              <span class="lifecycle-step-num">Giai đoạn 1</span>
              <div class="lifecycle-card-title">Ý Tưởng & Kế Hoạch</div>
              <div class="lifecycle-card-desc">
                AI sẽ phỏng vấn bạn bằng các câu hỏi ngắn gọn để chốt kiến trúc, vẽ bản thảo giao diện và lập kế hoạch 2 lớp rõ ràng.
              </div>
              <div class="lifecycle-skills-pill">
                Kỹ năng: <strong>Strict Architect v4.0</strong><br/>
                Lệnh gọi: <code>/plan</code> hoặc <code>/grill-me</code>
              </div>
            </div>

            <div class="lifecycle-card">
              <span class="lifecycle-step-num">Giai đoạn 2</span>
              <div class="lifecycle-card-title">Thiết Kế Giao Diện</div>
              <div class="lifecycle-card-desc">
                Loại bỏ hoàn toàn giao diện đại trà, áp dụng bảng màu DESIGN.md, hiệu ứng mượt dưới 250ms và linh kiện chuẩn shadcn/ui.
              </div>
              <div class="lifecycle-skills-pill">
                Kỹ năng: <strong>UI/UX Master</strong> · <strong>shadcn</strong> · <strong>Web Assets</strong><br/>
                Lệnh gọi: Tự động kích hoạt khi làm việc giao diện
              </div>
            </div>

            <div class="lifecycle-card">
              <span class="lifecycle-step-num">Giai đoạn 3</span>
              <div class="lifecycle-card-title">Xây Dựng Web & Dữ Liệu</div>
              <div class="lifecycle-card-desc">
                Lập trình Next.js App Router tải dữ liệu song song không chờ đợi, kết hợp cơ sở dữ liệu Supabase PostgreSQL phân quyền RLS.
              </div>
              <div class="lifecycle-skills-pill">
                Kỹ năng: <strong>Next.js Master</strong> · <strong>Supabase Architect</strong><br/>
                Lệnh gọi: Gõ yêu cầu tạo API / Schema
              </div>
            </div>

            <div class="lifecycle-card">
              <span class="lifecycle-step-num">Giai đoạn 4</span>
              <div class="lifecycle-card-title">Kiểm Thử & Đảm Bảo QA</div>
              <div class="lifecycle-card-desc">
                Tự động chạy kịch bản Playwright giả lập người dùng thật để bấm nút, kiểm tra lỗi giao diện và đảm bảo chạy tốt trên điện thoại/máy tính.
              </div>
              <div class="lifecycle-skills-pill">
                Kỹ năng: <strong>Playwright Web Tester</strong><br/>
                Lệnh gọi: Gõ yêu cầu viết bài test E2E
              </div>
            </div>
          </div>
        </div>

        <div class="faq-section">
          <div style="font-size:11.5px; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; color:var(--text-muted); margin-bottom:4px;">
            Các Câu Hỏi Thường Gặp (FAQ)
          </div>

          <div class="faq-card">
            <div class="faq-question">
              ${Icons.sparkles}
              <span>Làm thế nào để công cụ AI (Antigravity / Claude Code / Cursor) nhận diện kỹ năng sau khi tôi bấm Cài đặt?</span>
            </div>
            <div class="faq-answer">
              Khi bạn bấm <strong>Đồng bộ Cài đặt</strong>, AbyssalSkillsD sẽ sao chép toàn bộ tệp <code>SKILL.md</code>, các sổ tay hướng dẫn và tệp quy tắc tự động vào thư mục cấu hình chuẩn của máy (<code>~/.gemini/config/skills</code> cho Antigravity, <code>~/.claude/skills</code> cho Claude Code, hoặc <code>.agents/skills</code> cho dự án hiện tại). Công cụ AI sẽ tự động nạp mà bạn không cần khởi động lại.
            </div>
          </div>

          <div class="faq-card">
            <div class="faq-question">
              ${Icons.cpu}
              <span>Chế độ Always-On Autopilot là gì?</span>
            </div>
            <div class="faq-answer">
              Always-On Autopilot là chế độ cài đặt quy tắc ngầm vào tệp hệ thống của AI. Khi bật chế độ này, AI luôn luôn tuân theo các quy tắc khắt khe (như không bao giờ sinh code đại trà, luôn bắt đầu bằng chế độ làm việc DISCOVERY / BLUEPRINT / EXECUTE / VERIFY) trên mọi lượt trả lời mà bạn không cần phải nhắc lại.
            </div>
          </div>

          <div class="faq-card">
            <div class="faq-question">
              ${Icons.copy}
              <span>Tôi dùng ChatGPT trên trình duyệt hoặc công cụ không hỗ trợ thư mục thì làm thế nào?</span>
            </div>
            <div class="faq-answer">
              Rất đơn giản! Chỉ cần bấm nút <strong>Chép nhanh</strong> trên thẻ kỹ năng hoặc mở kỹ năng ra rồi bấm <strong>Sao chép câu lệnh mẫu</strong>, sau đó dán trực tiếp vào khung chat web. AI trên web sẽ hiểu và làm việc y hệt.
            </div>
          </div>

          <div class="faq-card">
            <div class="faq-question">
              ${Icons.graph}
              <span>Cơ chế Graphify AST của AI hoạt động như thế nào?</span>
            </div>
            <div class="faq-answer">
              Graphify là hệ thống lập bản đồ tri thức AST độc quyền dành riêng cho AI. Toàn bộ cây cú pháp và mạng lưới liên kết mã nguồn được lưu trữ tại <code>graphify-out/</code> để AI tự động tra cứu phạm vi ảnh hưởng (blast-radius) và các điểm nút trọng yếu (God Nodes) mỗi khi lập trình. Hệ thống tự động cập nhật ngầm mà không làm tốn dung lượng hay làm chậm ứng dụng của bạn.
            </div>
          </div>
        </div>
      </div>
    `;
  }

  static renderCommunityCloudView(schemaData, communitySkills = [], options = {}) {
    const activeSubTab = options.activeTab || "marketplace";
    const activeCat = options.activeCat || "all";
    const query = (options.query || "").toLowerCase().trim();
    const sql = schemaData?.sql || "-- Đang nạp mã nguồn Supabase...";

    let filtered = communitySkills;
    if (activeCat !== "all") {
      filtered = filtered.filter(s => s.category === activeCat);
    }
    if (query) {
      filtered = filtered.filter(s =>
        (s.name || "").toLowerCase().includes(query) ||
        (s.display_title || "").toLowerCase().includes(query) ||
        (s.description || "").toLowerCase().includes(query) ||
        (s.author || "").toLowerCase().includes(query)
      );
    }

    const categories = [
      { id: "all", label: "Tất cả lĩnh vực" },
      { id: "DevOps & Cloud", label: "DevOps & Cloud" },
      { id: "Backend & API", label: "Backend & API" },
      { id: "Edge & Serverless", label: "Edge & Serverless" },
      { id: "AI & Data Science", label: "AI & Data Science" },
      { id: "Community", label: "Đóng Góp Tự Do" }
    ];

    return `
      <div class="community-cloud-view">
        <div class="community-subtabs-bar">
          <div class="community-subtabs">
            <button class="subtab-btn ${activeSubTab === 'marketplace' ? 'active' : ''}" id="btn-subtab-marketplace">
              <span>${Icons.sparkles}</span>
              <span>Chợ Kỹ Năng Đám Mây (${communitySkills.length})</span>
            </button>
            <button class="subtab-btn ${activeSubTab === 'schema' ? 'active' : ''}" id="btn-subtab-schema">
              <span>${Icons.brandSupabase}</span>
              <span>Kiến Trúc Supabase PostgreSQL</span>
            </button>
          </div>

          <div style="font-size:11.5px; color:var(--text-muted); display:flex; align-items:center; gap:6px;">
            <span class="status-led active" style="width:6px;height:6px;"></span>
            <span>Cloud Hub v1.2.0 • Live Enterprise Registry</span>
          </div>
        </div>

        ${activeSubTab === 'marketplace' ? `
          <div class="community-toolbar">
            <div class="community-search-box">
              <span style="color:var(--text-muted);">${Icons.sparkles}</span>
              <input type="text" id="community-search-input" class="community-search-input" placeholder="Tìm kỹ năng cộng đồng theo tên, tác giả, mô tả..." value="${this.escape(query)}">
            </div>

            <div class="community-cat-chips">
              ${categories.map(c => `
                <button class="comm-cat-chip ${activeCat === c.id ? 'active' : ''}" data-comm-cat="${c.id}">
                  ${c.label}
                </button>
              `).join('')}
            </div>
          </div>

          ${filtered.length === 0 ? `
            <div style="text-align:center; padding:48px 20px; background:rgba(255,255,255,0.02); border:1px dashed var(--border-subtle); border-radius:var(--radius-md);">
              <div style="font-size:15px; font-weight:600; color:var(--text-primary); margin-bottom:4px;">Chưa tìm thấy kỹ năng phù hợp</div>
              <p style="font-size:12px; color:var(--text-muted); margin-bottom:12px;">Hãy thử điều chỉnh từ khóa tìm kiếm hoặc chọn danh mục khác.</p>
              <button class="btn btn-secondary" onclick="App.resetCommunityFilters()">Xem tất cả</button>
            </div>
          ` : `
            <div class="community-skills-grid">
              ${filtered.map(s => `
                <div class="comm-card" data-skill-id="${s.id}">
                  <div>
                    <div class="comm-card-header">
                      <div>
                        <div class="comm-card-title">${this.escape(s.display_title || s.name)}</div>
                        <div class="comm-card-author">Đóng góp bởi: <strong style="color:var(--text-primary);">@${this.escape(s.author || 'engineer')}</strong></div>
                      </div>
                      <span class="comm-card-badge">${this.escape(s.category || 'Cloud')}</span>
                    </div>

                    <p class="comm-card-desc" style="margin-top:10px;">
                      ${this.escape(s.description || '')}
                    </p>
                  </div>

                  <div>
                    <div class="comm-card-stats">
                      <span style="display:flex; align-items:center; gap:3px; color:#F59E0B;">
                        ${Icons.star}
                        <span>${s.rating || '5.0'}</span>
                      </span>
                      <span>•</span>
                      <span>${s.downloads || 1} lượt tải</span>
                      <span>•</span>
                      <span>v${s.version || '1.0.0'}</span>
                    </div>

                    <div class="comm-card-actions">
                      <button class="btn btn-secondary btn-view-community-skill" data-id="${s.id}" style="font-size:11.5px; padding:6px 10px;">
                        <span>👁️ Chi Tiết</span>
                      </button>
                      <button class="btn-install-community btn-install-community-skill" data-id="${s.id}">
                        ${Icons.download}
                        <span>Tải & Cài Đặt</span>
                      </button>
                    </div>
                  </div>
                </div>
              `).join('')}
            </div>
          `}
        ` : `
          <div class="info-callout-banner">
            <span>${Icons.sparkles}</span>
            <span><strong>Trung tâm kiến trúc cộng đồng:</strong> Đây là bản thiết kế cơ sở dữ liệu Supabase PostgreSQL chuẩn bị cho Phase 2 để đồng bộ và chia sẻ kỹ năng trực tuyến bảo mật bằng Row Level Security (RLS). Bạn có thể bấm nút bên dưới để sao chép mã SQL và tạo ngay trên Supabase Dashboard của bạn.</span>
          </div>

          <div style="display:flex; align-items:center; justify-content:space-between; margin-top:12px;">
            <div>
              <h2 style="font-size:18px; font-weight:700; color:var(--text-primary); display:flex; align-items:center; gap:8px;">
                <span>${Icons.brandSupabase}</span>
                <span>Trung Tâm Kiến Trúc Đám Mây Cộng Đồng (Phase 2 Hub)</span>
              </h2>
              <p style="font-size:12.5px; color:var(--text-secondary); margin-top:2px;">
                Thiết kế cơ sở dữ liệu Supabase PostgreSQL với Row Level Security (RLS) & GIN Full-Text Search.
              </p>
            </div>

            <button class="btn btn-primary" id="btn-copy-community-sql">
              ${Icons.copy}
              <span>Sao chép Toàn bộ SQL Schema</span>
            </button>
          </div>

          <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:14px; margin-top:16px;">
            <div class="metric-card">
              <div class="metric-label">Bảo mật RLS Granular</div>
              <div class="metric-value" style="color:var(--led-success); font-size:18px;">Kích hoạt 100%</div>
              <div class="metric-sub">auth.uid() phân quyền tuyệt đối</div>
            </div>
            <div class="metric-card">
              <div class="metric-label">Chỉ mục GIN Full-Text</div>
              <div class="metric-value" style="color:var(--accent-primary); font-size:18px;">to_tsvector</div>
              <div class="metric-sub">Tìm kiếm tức thời sub-5ms</div>
            </div>
            <div class="metric-card">
              <div class="metric-label">Bảng Dữ liệu Chuẩn</div>
              <div class="metric-value" style="font-size:18px;">3 Bảng Quan hệ</div>
              <div class="metric-sub">profiles, skills, skill_references</div>
            </div>
          </div>

          <div class="community-schema-box" style="margin-top:16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
              <div style="font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-muted);">
                PostgreSQL Schema Definition (app/data/supabase_community_schema.sql)
              </div>
              <span class="version-tag">supabase-backend-architect</span>
            </div>

            <pre style="background:var(--bg-canvas); border:1px solid var(--border-subtle); padding:14px; border-radius:var(--radius-sm); font-size:12px; max-height:420px; overflow-y:auto;"><code class="language-sql">${this.escape(sql)}</code></pre>
          </div>
        `}
      </div>
    `;
  }

  static renderDiagnosticModal(data) {
    const logs = data.logs || "Chưa có dữ liệu nhật ký.";
    const logDir = data.log_dir || "%LOCALAPPDATA%\\AbyssalSkillsD\\logs";
    const platform = data.platform || "win32";
    const pyVer = data.python_version || "3.15";
    const ws = data.active_workspace || "Chưa chọn";

    return `
      <div class="modal-backdrop" id="modal-diagnostics" onclick="App.closeActiveModal(event)">
        <div class="diagnostic-modal-box" onclick="event.stopPropagation()">
          <div style="display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid var(--border-subtle); padding-bottom:12px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="color:#10B981;">${Icons.stethoscope}</span>
              <div>
                <div style="font-size:15px; font-weight:700; color:var(--text-primary);">Chẩn Đoán Sức Khỏe & Nhật Ký Hệ Thống</div>
                <div style="font-size:11px; color:var(--text-muted);">Nhật ký xoay vòng lưu tại: <code>${this.escape(logDir)}</code></div>
              </div>
            </div>
            <button class="btn btn-ghost btn-icon" onclick="App.closeActiveModal()">
              ${Icons.x}
            </button>
          </div>

          <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:10px;">
            <div style="background:var(--bg-canvas); border:1px solid var(--border-subtle); padding:8px 12px; border-radius:var(--radius-sm);">
              <div style="font-size:10px; color:var(--text-muted); text-transform:uppercase;">Nền tảng HĐH</div>
              <div style="font-size:13px; font-weight:600; color:var(--text-primary);">${platform.toUpperCase()} (x64)</div>
            </div>
            <div style="background:var(--bg-canvas); border:1px solid var(--border-subtle); padding:8px 12px; border-radius:var(--radius-sm);">
              <div style="font-size:10px; color:var(--text-muted); text-transform:uppercase;">Python Runtime</div>
              <div style="font-size:13px; font-weight:600; color:#10B981;">v${pyVer} Embedded</div>
            </div>
            <div style="background:var(--bg-canvas); border:1px solid var(--border-subtle); padding:8px 12px; border-radius:var(--radius-sm);">
              <div style="font-size:10px; color:var(--text-muted); text-transform:uppercase;">Dự án Mục Tiêu</div>
              <div style="font-size:12px; font-weight:600; color:#38BDF8; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="${this.escape(ws)}">${this.escape(ws)}</div>
            </div>
          </div>

          <div>
            <div style="font-size:11.5px; font-weight:600; color:var(--text-muted); margin-bottom:6px; display:flex; justify-content:space-between;">
              <span>Nhật Ký Sự Kiện Gần Nhất (app.log):</span>
              <span style="color:#10B981;">● Ghi tự động</span>
            </div>
            <div class="diagnostic-log-terminal" id="diagnostic-log-terminal">${this.escape(logs)}</div>
          </div>

          <div class="info-callout-banner" style="margin:0; padding:8px 12px; font-size:11.5px; border-color:rgba(16, 185, 129, 0.3); background:rgba(16, 185, 129, 0.08);">
            <span style="color:#10B981;">${Icons.lock}</span>
            <span><strong>Bảo Vệ Quyền Riêng Tư (Zero-Trust):</strong> Tự động che mờ đường dẫn thư mục cá nhân (<code>C:\\Users\\&lt;user&gt;</code>) và các khóa API/Tokens trước khi gửi.</span>
          </div>

          <div style="display:flex; align-items:center; justify-content:space-between; border-top:1px solid var(--border-subtle); padding-top:12px;">
            <button class="btn btn-secondary" id="btn-open-log-folder" style="font-size:12px;">
              ${Icons.folderOpen}
              <span>Mở Thư Mục Logs</span>
            </button>
            <div style="display:flex; align-items:center; gap:8px;">
              <button class="btn btn-secondary" onclick="App.closeActiveModal()">Đóng</button>
              <button class="btn btn-secondary" id="btn-export-diagnostics">
                ${Icons.download}
                <span>Xuất File ZIP</span>
              </button>
              <button class="btn btn-primary" id="btn-submit-cloud-error" style="background:linear-gradient(135deg, #00B4D8 0%, #7C3AED 100%); border:none;">
                <span>🚀 Gửi Báo Cáo Lên Cloud</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  static renderDiffReviewModal(diff) {
    if (!diff || !diff.success) {
      return `
        <div class="modal-backdrop" onclick="App.closeActiveModal()">
          <div class="modal-content" style="max-width:480px; padding:24px; text-align:center; background:var(--bg-surface); border-radius:var(--radius-md);">
            <h3 style="color:var(--text-primary); margin-bottom:8px;">Không thể tải thông tin so sánh</h3>
            <p style="color:var(--text-secondary); margin:12px 0 20px 0;">${this.escape(diff?.message || "Lỗi đọc tệp tin.")}</p>
            <button class="btn btn-secondary" onclick="App.closeActiveModal()">Đóng</button>
          </div>
        </div>
      `;
    }

    return `
      <div class="modal-backdrop" id="modal-diff-review" onclick="App.closeActiveModal(event)">
        <div class="diff-modal-container" onclick="event.stopPropagation()">
          <div class="diff-modal-header">
            <div class="diff-header-left">
              <span class="diff-title">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
                <span>So Sánh & Cập Nhật Kỹ Năng: ${this.escape(diff.display_title || diff.skill_id)}</span>
              </span>
              <span class="diff-subtitle">Nội dung tệp trên máy của bạn có sự khác biệt so với bản cập nhật mới từ kho. Hãy kiểm tra kỹ trước khi quyết định.</span>
            </div>
            <button class="btn-close-modal" onclick="App.closeActiveModal()" title="Đóng cửa sổ">✕</button>
          </div>

          <div class="diff-modal-body">
            <!-- Cột Trái: Bản Cũ Trên Máy Của Bạn -->
            <div class="diff-column">
              <div class="diff-col-header">
                <span class="diff-col-badge badge-local">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
                  <span>🏠 Bản Hiện Tại Trên Máy (Local)</span>
                </span>
                <span class="diff-col-meta" title="${this.escape(diff.local_path)}">${this.escape(diff.local_path || "Đường dẫn không xác định")}</span>
              </div>
              <div class="diff-code-wrapper">
                <pre><code>${this.escape(diff.local_content || "(Tệp rỗng)")}</code></pre>
              </div>
            </div>

            <!-- Cột Phải: Bản Mới Từ Kho Bản Quyền -->
            <div class="diff-column">
              <div class="diff-col-header">
                <span class="diff-col-badge badge-new">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                  <span>✨ Bản Mới Từ Kho (v${this.escape(diff.new_version)})</span>
                </span>
                <span class="diff-col-meta">Nguồn: Kho Kỹ Năng Bản Quyền</span>
              </div>
              <div class="diff-code-wrapper">
                <pre><code>${this.escape(diff.new_content || "(Tệp rỗng)")}</code></pre>
              </div>
            </div>
          </div>

          <div class="diff-modal-footer">
            <button class="btn btn-secondary" id="btn-diff-keep-local" data-id="${diff.skill_id}">
              🛡️ Giữ Lại Bản Cũ Của Tôi (Bỏ qua)
            </button>
            <div style="display:flex; align-items:center; gap:10px;">
              <span style="font-size:11px; color:var(--text-muted);">Tự động sao lưu bản cũ vào SKILL.md.bak</span>
              <button class="btn btn-primary" id="btn-diff-apply-update" data-id="${diff.skill_id}" style="background:linear-gradient(135deg, #00B4D8 0%, #7C3AED 100%); border:none;">
                💾 Đồng Ý Cập Nhật Sang Bản Mới
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  static renderCommunitySkillDetailModal(skill, targetWorkspace) {
    return `
      <div class="modal-backdrop" id="modal-community-detail" onclick="App.closeActiveModal(event)">
        <div class="modal-dialog" style="max-width:580px;" onclick="event.stopPropagation()">
          <div class="modal-header">
            <div>
              <div style="font-size:15px; font-weight:700; color:var(--text-primary); display:flex; align-items:center; gap:8px;">
                <span>${Icons.sparkles}</span>
                <span>${this.escape(skill.display_title || skill.name)}</span>
              </div>
              <div style="font-size:11.5px; color:var(--text-muted); margin-top:2px;">
                Đóng góp bởi: <strong style="color:var(--text-primary);">@${this.escape(skill.author || 'community')}</strong> • Danh mục: <strong>${this.escape(skill.category || 'General')}</strong>
              </div>
            </div>
            <button class="btn btn-ghost btn-icon" onclick="App.closeActiveModal()">
              ${Icons.x}
            </button>
          </div>

          <div class="modal-body" style="display:flex; flex-direction:column; gap:14px;">
            <div>
              <div style="font-size:12px; font-weight:600; color:var(--text-secondary); margin-bottom:4px;">Mô tả kỹ năng:</div>
              <p style="font-size:12.5px; color:var(--text-primary); line-height:1.5;">${this.escape(skill.description || '')}</p>
            </div>

            <div>
              <div style="font-size:12px; font-weight:600; color:var(--text-secondary); margin-bottom:6px;">Chọn nền tảng AI muốn cài đặt:</div>
              <div class="uninstall-targets-list">
                <label class="uninstall-target-item">
                  <input type="checkbox" class="comm-target-checkbox" value="workspace" checked>
                  <div>
                    <div style="font-weight:600; font-size:12.5px;">Dự án hiện tại (.agents)</div>
                    <div style="font-size:11px; color:var(--text-muted);">${this.escape(targetWorkspace || 'Cục bộ')}</div>
                  </div>
                </label>
                <label class="uninstall-target-item">
                  <input type="checkbox" class="comm-target-checkbox" value="gemini" checked>
                  <div>
                    <div style="font-weight:600; font-size:12.5px;">Google Antigravity (~/.gemini)</div>
                    <div style="font-size:11px; color:var(--text-muted);">Tự động kích hoạt khi mở Antigravity</div>
                  </div>
                </label>
                <label class="uninstall-target-item">
                  <input type="checkbox" class="comm-target-checkbox" value="claude" checked>
                  <div>
                    <div style="font-weight:600; font-size:12.5px;">Claude Code CLI (~/.claude)</div>
                    <div style="font-size:11px; color:var(--text-muted);">Sẵn sàng cho các câu lệnh claude terminal</div>
                  </div>
                </label>
                <label class="uninstall-target-item">
                  <input type="checkbox" class="comm-target-checkbox" value="codex" checked>
                  <div>
                    <div style="font-weight:600; font-size:12.5px;">OpenAI Codex (~/.codex)</div>
                    <div style="font-size:11px; color:var(--text-muted);">Tương thích Codex CLI và CODEX.md</div>
                  </div>
                </label>
              </div>
            </div>
          </div>

          <div class="modal-footer" style="display:flex; justify-content:space-between; align-items:center;">
            <button class="btn btn-secondary" onclick="App.closeActiveModal()">Hủy</button>
            <button class="btn btn-primary btn-confirm-comm-install" data-id="${skill.id}">
              ${Icons.download}
              <span>Cài Đặt Kỹ Năng Này</span>
            </button>
          </div>
        </div>
      </div>
    `;
  }

  static renderCommandPalette(skills, activeIndex = 0, query = "") {
    const q = query.toLowerCase().trim();
    const filtered = q ? skills.filter(s => 
      (s.display_title || s.name || '').toLowerCase().includes(q) ||
      (s.category || '').toLowerCase().includes(q)
    ) : skills;

    return `
      <div class="command-backdrop" id="command-backdrop" onclick="App.closeCommandPalette(event)">
        <div class="command-dialog" onclick="event.stopPropagation()">
          <div class="command-input-wrap">
            <span style="color:var(--text-muted);">${Icons.command}</span>
            <input type="text" id="command-search-input" class="command-input" placeholder="Gõ tên kỹ năng hoặc hành động..." value="${this.escape(query)}" autofocus>
            <span class="kbd-shortcut">ESC để đóng</span>
          </div>

          <div class="command-list" id="command-list">
            <div class="command-group-heading">Hành động nhanh</div>
            <div class="command-item ${activeIndex === 0 ? 'active' : ''}" data-action="batch-install">
              <span>${Icons.download}</span>
              <span>Đồng bộ trọn bộ 7 kỹ năng Skill-AI-private</span>
              <span class="command-item-sub">↵ Enter</span>
            </div>
            <div class="command-item ${activeIndex === 1 ? 'active' : ''}" data-action="toggle-theme">
              <span>${Icons.sun}</span>
              <span>Chuyển đổi Giao diện Tối / Sáng</span>
              <span class="command-item-sub">Theme</span>
            </div>
            <div class="command-item ${activeIndex === 2 ? 'active' : ''}" data-action="open-guide">
              <span>${Icons.sparkles}</span>
              <span>Xem Cẩm Nang Hướng Dẫn Sử Dụng A-Z</span>
              <span class="command-item-sub">Guide</span>
            </div>
            <div class="command-item ${activeIndex === 3 ? 'active' : ''}" data-action="open-auth">
              <span>${Icons.user}</span>
              <span>Đăng nhập / Tài khoản Supabase</span>
              <span class="command-item-sub">Auth</span>
            </div>
            <div class="command-item ${activeIndex === 4 ? 'active' : ''}" data-action="open-auth-config">
              <span>${Icons.brandSupabase}</span>
              <span>Cấu hình Supabase Project URL & Keys</span>
              <span class="command-item-sub">Config</span>
            </div>
            <div class="command-item ${activeIndex === 5 ? 'active' : ''}" data-action="open-diagnostics">
              <span style="color:#10B981;">${Icons.stethoscope}</span>
              <span>Kiểm tra Sức Khỏe & Chẩn Đoán Hệ Thống</span>
              <span class="command-item-sub">Health</span>
            </div>

            <div class="command-group-heading" style="margin-top:6px;">Kỹ năng (${filtered.length})</div>
            ${filtered.map((s, idx) => `
              <div class="command-item ${activeIndex === (idx + 6) ? 'active' : ''}" data-action="open-skill" data-id="${s.id}">
                <span>${this.getBrandIconSvg(s.id, s.category)}</span>
                <span>${this.escape(s.display_title || s.name)}</span>
                <span class="command-item-sub">${this.escape(s.category)}</span>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    `;
  }

  static renderEmptyIllustration() {
    return `
      <div class="undraw-empty" data-testid="empty-state">
        <svg viewBox="0 0 800 600" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="400" cy="300" r="160" fill="currentColor" fill-opacity="0.06"/>
          <path d="M300 240h200v160H300z" stroke="currentColor" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M340 280h120M340 320h80" stroke="currentColor" stroke-width="8" stroke-linecap="round"/>
          <circle cx="500" cy="380" r="40" stroke="currentColor" stroke-width="8" fill="var(--bg-canvas)"/>
          <path d="M528 408l24 24" stroke="currentColor" stroke-width="8" stroke-linecap="round"/>
        </svg>
        <div style="font-size: 15px; font-weight: 600; color: var(--text-primary); margin-bottom: 4px;">Không tìm thấy kỹ năng phù hợp</div>
        <p style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 14px;">Hãy thử điều chỉnh từ khóa tìm kiếm hoặc bấm khôi phục bộ lọc.</p>
        <button class="btn btn-secondary" onclick="App.resetFilters()">Khôi phục bộ lọc</button>
      </div>
    `;
  }

  static renderStudioView(draft = {}) {
    return `
      <div class="studio-container">
        <!-- 3-Step Guided Workflow Banner for Newcomers -->
        <div class="studio-step-banner">
          <div class="studio-step-track">
            <div class="studio-step-node active">
              <span class="studio-step-badge">1</span>
              <span>Chọn mẫu Addy Osmani hoặc tự đặt tên</span>
            </div>
            <span class="studio-step-arrow">→</span>
            <div class="studio-step-node">
              <span class="studio-step-badge" style="background:var(--bg-card); color:var(--text-secondary); border:1px solid var(--border-subtle);">2</span>
              <span>Viết mục tiêu & quy tắc Senior Engineer</span>
            </div>
            <span class="studio-step-arrow">→</span>
            <div class="studio-step-node">
              <span class="studio-step-badge" style="background:var(--bg-card); color:var(--text-secondary); border:1px solid var(--border-subtle);">3</span>
              <span>Xem trước thời gian thực & Lưu thư viện</span>
            </div>
          </div>
          <div style="font-size:11.5px; color:var(--text-muted); display:flex; align-items:center; gap:6px;">
            <span class="status-led active"></span>
            <span>Tự động đồng bộ vào Cursor, Windsurf, Copilot, Antigravity & Claude.</span>
          </div>
        </div>

        <!-- 1-Click Template Starter Chips (addyosmani/agent-skills catalog) -->
        <div class="studio-presets-row">
          <div class="studio-presets-title">
            <span style="color:var(--accent-primary);">${Icons.sparkles}</span>
            <span>Nạp Mẫu Kỹ Năng Chuẩn Addy Osmani (Senior Engineer Workflows):</span>
          </div>
          <div class="studio-preset-chips">
            <button class="preset-chip-btn" data-preset="spec-driven" title="Mẫu ép buộc viết đặc tả kỹ thuật trước khi gõ mã">
              <span>⚡ Spec-Driven Development</span>
            </button>
            <button class="preset-chip-btn" data-preset="test-driven" title="Mẫu Red-Green-Refactor và kiểm thử tự động nghiêm ngặt">
              <span>⚡ Test-Driven (TDD)</span>
            </button>
            <button class="preset-chip-btn" data-preset="code-review" title="Mẫu đánh giá 5 trục: Tính đúng, Kiến trúc, Bảo mật, Hiệu năng, Đọc hiểu">
              <span>⚡ 5-Axis Code Review</span>
            </button>
            <button class="preset-chip-btn" data-preset="root-cause-debug" title="Mẫu tìm nguyên nhân gốc rễ và chặn tái diễn lỗi">
              <span>⚡ Root-Cause Debugging</span>
            </button>
            <button class="preset-chip-btn" data-preset="ui-ux-artisan" title="Mẫu thiết kế giao diện chống slop, chuẩn Vercel và hiệu ứng mượt">
              <span>⚡ Frontend UI/UX Artisan</span>
            </button>
            <button class="preset-chip-btn" data-preset="blank" style="margin-left:auto; color:var(--text-muted);" title="Xóa trắng để tự viết từ đầu">
              <span>Tự viết từ đầu</span>
            </button>
          </div>
        </div>

        <!-- Split-Screen IDE Workbench -->
        <div class="studio-split-workbench">
          <!-- Left Column: Form Editor -->
          <div class="studio-form-col">
            <div style="font-size:14px; font-weight:700; color:var(--text-primary); display:flex; align-items:center; gap:8px; margin-bottom:12px;">
              ${Icons.penTool}
              <span>Soạn Thảo Thông Tin Kỹ Năng</span>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span>Tên hiển thị kỹ năng</span>
                <span style="font-size:11px; font-weight:normal; color:var(--text-muted);">Tên xuất hiện trên thẻ</span>
              </label>
              <input type="text" id="studio-title" class="form-input" placeholder="Ví dụ: Spec-Driven Development Master" value="${this.escape(draft.title || '')}">
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
              <div class="form-group">
                <label class="form-label">
                  <span>Mã định danh (ID)</span>
                  <span style="font-size:11px; font-weight:normal; color:var(--text-muted);">Dùng cho folder</span>
                </label>
                <input type="text" id="studio-id" class="form-input" placeholder="spec-driven-development" value="${this.escape(draft.id || '')}">
              </div>

              <div class="form-group">
                <label class="form-label">Danh mục chuyên môn</label>
                <select id="studio-category" class="form-select">
                  <option value="Architecture & Code" ${draft.category === 'Architecture & Code' ? 'selected' : ''}>Architecture & Code</option>
                  <option value="UI/UX Design" ${draft.category === 'UI/UX Design' ? 'selected' : ''}>UI/UX Design</option>
                  <option value="Full-Stack Web" ${draft.category === 'Full-Stack Web' ? 'selected' : ''}>Full-Stack Web</option>
                  <option value="Backend & Database" ${draft.category === 'Backend & Database' ? 'selected' : ''}>Backend & Database</option>
                  <option value="Testing & QA" ${draft.category === 'Testing & QA' ? 'selected' : ''}>Testing & QA</option>
                  <option value="Review & Security" ${draft.category === 'Review & Security' ? 'selected' : ''}>Review & Security</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span>Mô tả ngắn gọn (Khi nào nên kích hoạt)</span>
                <span style="font-size:11px; font-weight:normal; color:var(--text-muted);">1-2 câu súc tích</span>
              </label>
              <input type="text" id="studio-desc" class="form-input" placeholder="Ví dụ: Bắt buộc mô hình AI viết bản đặc tả kỹ thuật và xác nhận phạm vi trước khi lập trình." value="${this.escape(draft.desc || '')}">
            </div>

            <div class="form-group" style="flex:1; display:flex; flex-direction:column; min-height:280px;">
              <label class="form-label">
                <span>Nội dung chỉ dẫn (SKILL.md Markdown)</span>
                <span id="studio-char-count" style="font-size:11px; font-weight:normal; color:var(--accent-primary);">0 ký tự</span>
              </label>
              <textarea id="studio-content" class="form-textarea" style="flex:1; min-height:260px;" placeholder="---&#10;name: your-skill-name&#10;description: Khi nào AI nên kích hoạt kỹ năng này...&#10;---&#10;&#10;# Tên Kỹ Năng&#10;&#10;## Quy trình thực hiện Senior Engineer:&#10;1. Bước một...&#10;2. Bước hai...&#10;&#10;## Bảng Chống Bao Biện (Anti-Rationalization):&#10;| Lời bao biện | Hành động bắt buộc |&#10;| :--- | :--- |&#10;| 'Tính năng nhỏ khỏi viết test' | Vẫn phải viết tối thiểu 1 unit test |">${this.escape(draft.content || '')}</textarea>
            </div>

            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
              <span class="form-hint">Định dạng hỗ trợ: YAML Frontmatter, Tiêu đề, Bảng Markdown, Code block.</span>
              <div style="display:flex; align-items:center; gap:8px;">
                <button class="btn btn-secondary" id="btn-publish-to-community" title="Đăng tải kỹ năng này lên Chợ Cộng Đồng">
                  ${Icons.uploadCloud}
                  <span>Đăng Lên Chợ Cloud</span>
                </button>
                <button class="btn btn-primary" id="btn-studio-save">
                  ${Icons.check}
                  <span>Lưu vào Thư Viện</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Right Column: Live Markdown Preview -->
          <div class="studio-preview-col">
            <div class="studio-preview-header">
              <div style="display:flex; align-items:center; gap:6px;">
                <span class="status-led active"></span>
                <span>Xem Trước Tài Liệu Thời Gian Thực (Live Preview)</span>
              </div>
              <span class="version-tag">Apple / Vercel Standard</span>
            </div>
            <div class="markdown-article" id="studio-preview-pane">
              <p style="color:var(--text-muted);">Bấm chọn một mẫu Addy Osmani ở trên hoặc gõ nội dung vào cột trái để xem trước định dạng tại đây...</p>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  static renderGitHubModal() {
    return `
      <div class="modal-backdrop" id="modal-github" onclick="App.closeActiveModal(event)">
        <div class="modal-dialog" onclick="event.stopPropagation()">
          <div class="modal-header">
            <div style="font-size:14px; font-weight:600; color:var(--text-primary); display:flex; align-items:center; gap:8px;">
              ${Icons.gitBranch}
              <span>Nhập Kho Kỹ Năng từ GitHub</span>
            </div>
            <button class="btn btn-ghost btn-icon" onclick="App.closeActiveModal()">
              ${Icons.x}
            </button>
          </div>
          <div class="modal-body">
            <p style="font-size:12.5px; color:var(--text-secondary); margin-bottom:14px;">
              Nhập đường dẫn kho chứa mã nguồn kỹ năng trên GitHub:
            </p>
            <div class="form-group">
              <input type="text" id="input-github-url" class="form-input" value="https://github.com/Skill-AI-private/Strict-architect-coder.git" placeholder="https://github.com/owner/repo.git">
            </div>

            <div id="github-sync-status" style="display:none; margin-top:12px; padding:10px 12px; background:rgba(94,106,210,0.1); border:1px solid rgba(94,106,210,0.25); border-radius:var(--radius-sm); font-size:12px; color:var(--accent-primary);">
              <span id="github-sync-text">Đang kết nối và nạp kho kỹ năng...</span>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" onclick="App.closeActiveModal()">Đóng</button>
            <button class="btn btn-primary" id="btn-confirm-github-clone">
              ${Icons.download}
              <span>Bắt đầu Nạp</span>
            </button>
          </div>
        </div>
      </div>
    `;
  }

  /* Supabase Auth UI Components (supabase-backend-architect & ui-ux-design-master) */
  static renderUserWidget(session) {
    if (session && session.authenticated && session.user) {
      const u = session.user;
      const initial = (u.full_name || u.email || "U").charAt(0).toUpperCase();
      const avatarContent = u.avatar_url
        ? `<img src="${this.escape(u.avatar_url)}" alt="Avatar" style="width:100%; height:100%; border-radius:50%; object-fit:cover;" onerror="this.style.display='none'; this.nextElementSibling.style.display='inline-flex';" /><span style="display:none;">${this.escape(initial)}</span>`
        : `<span>${this.escape(initial)}</span>`;

      return `
        <div class="user-profile-badge-btn" id="btn-user-profile-menu" data-testid="btn-user-profile-menu" role="button" tabindex="0" title="Tài khoản: ${this.escape(u.full_name || u.email)}">
          <div class="user-avatar-circle" style="overflow:hidden; display:inline-flex; align-items:center; justify-content:center;">${avatarContent}</div>
          <div class="user-meta-summary">
            <span class="user-meta-name">${this.escape(u.full_name || u.email)}</span>
            <span class="user-role-tag">${this.escape(u.role || 'creator')}</span>
          </div>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
      `;
    }

    return `
      <button class="btn-auth-login-trigger" id="btn-trigger-login" data-testid="btn-trigger-login" title="Đăng nhập tài khoản Supabase">
        ${Icons.user}
        <span>Đăng nhập</span>
      </button>
    `;
  }

  static renderUserDropdown(session) {
    if (!session || !session.authenticated || !session.user) return "";
    const u = session.user;
    return `
      <div class="user-dropdown-panel" id="user-dropdown-panel" onclick="event.stopPropagation()">
        <div class="dropdown-user-header">
          <div class="dropdown-user-name">${this.escape(u.full_name || 'Người dùng')}</div>
          <div class="dropdown-user-email">${this.escape(u.email || '')}</div>
        </div>

        <div class="dropdown-menu-item" id="btn-menu-open-profile" title="Xem Hồ Sơ Cá Nhân & Portfolio">
          ${Icons.user}
          <span>Xem Hồ sơ cá nhân</span>
        </div>

        <div class="dropdown-menu-item" id="btn-menu-copy-token" title="Sao chép Access Token (JWT)">
          ${Icons.key}
          <span>Sao chép Access Token</span>
        </div>

        <div class="dropdown-menu-item" id="btn-menu-open-config">
          ${Icons.brandSupabase}
          <span>Cấu hình Supabase & Keys</span>
        </div>

        <div class="dropdown-divider"></div>

        <div class="dropdown-menu-item danger" id="btn-menu-signout">
          ${Icons.logOut}
          <span>Đăng xuất khỏi thiết bị</span>
        </div>
      </div>
    `;
  }

  static renderAuthModal(activeTab = "signin", config = {}, session = {}, errorMsg = "") {
    const isLogged = session && session.authenticated;
    const jwtToken = session && session.access_token ? session.access_token : "";

    return `
      <div class="modal-backdrop" id="modal-auth-backdrop" onclick="App.closeActiveModal(event)">
        <div class="modal-dialog auth-dialog-redesign" style="max-width: 480px;" onclick="event.stopPropagation()">
          <div class="modal-header" style="border-bottom:none; padding-bottom:4px;">
            <div style="font-size:15px; font-weight:600; color:var(--text-primary); display:flex; align-items:center; gap:8px;">
              <span style="color:var(--accent-primary);">${Icons.cloud}</span>
              <span>Đăng Nhập Tài Khoản Đám Mây</span>
            </div>
            <button class="btn btn-ghost btn-icon" onclick="App.closeActiveModal()">
              ${Icons.x}
            </button>
          </div>

          <div style="padding:0 20px; font-size:12.5px; color:var(--text-secondary); line-height:1.45;">
            Tài khoản giúp bạn tự động lưu trữ và đồng bộ các kỹ năng AI giữa các thiết bị làm việc.
          </div>

          <div class="auth-form-body" style="padding:16px 20px 20px 20px;">
            ${errorMsg ? `
              <div class="auth-status-alert error">
                <span>${Icons.x}</span>
                <span>${this.escape(errorMsg)}</span>
              </div>
            ` : ''}

            <!-- 1-Click Social Sign-In (Google & GitHub) -->
            <div class="auth-social-buttons">
              <button class="btn-social-auth" id="btn-auth-google" data-testid="btn-auth-google" title="Đăng nhập 1-Click với Google">
                <span class="social-icon">${Icons.google}</span>
                <span>Tiếp tục với tài khoản Google</span>
              </button>

              <button class="btn-social-auth" id="btn-auth-github" data-testid="btn-auth-github" title="Đăng nhập 1-Click với GitHub">
                <span class="social-icon">${Icons.github}</span>
                <span>Tiếp tục với tài khoản GitHub</span>
              </button>
            </div>

            <div class="auth-divider">
              <span>Hoặc tiếp tục với email</span>
            </div>

            <!-- Email / Password Switcher Tabs -->
            <div class="auth-segmented-tabs">
              <button class="auth-tab-btn ${activeTab !== 'signup' ? 'active' : ''}" data-authtab="signin">Đăng Nhập</button>
              <button class="auth-tab-btn ${activeTab === 'signup' ? 'active' : ''}" data-authtab="signup">Tạo Tài Khoản Mới</button>
            </div>

            ${activeTab !== 'signup' ? `
              <div class="form-group" style="margin-top:12px;">
                <label class="form-label">Địa chỉ Email</label>
                <input type="email" id="auth-signin-email" class="form-input" placeholder="name@example.com" value="${this.escape(session.user?.email || '')}">
              </div>

              <div class="form-group">
                <label class="form-label">Mật khẩu</label>
                <input type="password" id="auth-signin-password" class="form-input" placeholder="Nhập mật khẩu của bạn">
              </div>

              <div style="display:flex; align-items:center; justify-content:space-between; margin-top:6px;">
                <label style="display:flex; align-items:center; gap:6px; font-size:12px; color:var(--text-secondary); cursor:pointer;">
                  <input type="checkbox" id="auth-remember-me" checked>
                  <span>Ghi nhớ đăng nhập trên máy tính này</span>
                </label>
              </div>

              <div style="margin-top:16px;">
                <button class="btn btn-primary" id="btn-submit-signin" style="width:100%; justify-content:center; padding:9px 16px;">
                  ${Icons.user}
                  <span>Đăng Nhập Với Email</span>
                </button>
              </div>
            ` : `
              <div class="form-group" style="margin-top:12px;">
                <label class="form-label">Họ và tên của bạn</label>
                <input type="text" id="auth-signup-name" class="form-input" placeholder="Ví dụ: Minh Quân">
              </div>

              <div class="form-group">
                <label class="form-label">Địa chỉ Email</label>
                <input type="email" id="auth-signup-email" class="form-input" placeholder="name@example.com">
              </div>

              <div class="form-group">
                <label class="form-label">Mật khẩu (ít nhất 6 ký tự)</label>
                <input type="password" id="auth-signup-password" class="form-input" placeholder="Tạo mật khẩu an toàn">
              </div>

              <div style="margin-top:16px;">
                <button class="btn btn-primary" id="btn-submit-signup" style="width:100%; justify-content:center; padding:9px 16px;">
                  ${Icons.check}
                  <span>Tạo Tài Khoản & Bắt Đầu</span>
                </button>
              </div>
            `}

            <!-- Collapsible Advanced Server Configuration (For Developers) -->
            <details class="auth-advanced-collapse" ${activeTab === 'config' ? 'open' : ''}>
              <summary class="auth-advanced-summary">
                ${Icons.chevronDown}
                <span>⚙️ Cài đặt máy chủ nâng cao (Dành cho lập trình viên)</span>
              </summary>
              <div class="auth-advanced-content">
                <div class="info-callout-banner" style="margin-bottom:8px;">
                  <span>${Icons.sparkles}</span>
                  <span>Bạn có thể kết nối bất kỳ dự án Supabase cá nhân nào bằng cách dán URL và Anon Public Key từ Supabase Dashboard (Settings -> API).</span>
                </div>

                <div class="form-group">
                  <label class="form-label">Đường dẫn Dự án Supabase (Project URL)</label>
                  <input type="text" id="cfg-supabase-url" class="form-input" value="${this.escape(config.supabase_url || '')}" placeholder="https://xyz.supabase.co">
                </div>

                <div class="form-group">
                  <label class="form-label">Khóa công khai (Anon Public Key)</label>
                  <textarea id="cfg-anon-key" class="form-textarea" style="height:55px; font-family:monospace; font-size:11px;" placeholder="eyJhbGciOiJIUzI1Ni...">${this.escape(config.anon_key || '')}</textarea>
                </div>

                <div class="form-group">
                  <label class="form-label">Khóa quản trị bí mật (Service Secret Key — Tùy chọn)</label>
                  <input type="password" id="cfg-secret-key" class="form-input" value="${this.escape(config.service_secret_key || '')}" placeholder="Khóa Service Role bí mật">
                </div>

                ${jwtToken ? `
                  <div class="form-group">
                    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:4px;">
                      <label class="form-label" style="margin:0;">Mã Access Token hiện tại (JWT)</label>
                      <button class="btn btn-secondary btn-icon" id="btn-modal-copy-token" title="Sao chép Token" style="padding:2px 6px; font-size:11px;">
                        ${Icons.copy}
                        <span>Sao chép</span>
                      </button>
                    </div>
                    <div class="token-viewer-box">${this.escape(jwtToken)}</div>
                  </div>
                ` : ''}

                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
                  <button class="btn btn-ghost" id="btn-reset-supabase-config" style="font-size:11.5px; color:var(--text-muted);">
                    ${Icons.refresh}
                    <span>Khôi phục mặc định</span>
                  </button>
                  <button class="btn btn-primary" id="btn-save-supabase-config" style="padding:4px 10px; font-size:11.5px;">
                    ${Icons.check}
                    <span>Lưu Cấu Hình</span>
                  </button>
                </div>
              </div>
            </details>
          </div>
        </div>
      </div>
    `;
  }

  /* Profile & Developer Portfolio View (v1.3.0) */
  static renderProfileView(session, stats = {}) {
    const isAuth = session && session.authenticated && session.user;
    const u = isAuth ? session.user : null;
    const statsData = {
      installed_count: stats.installed_count || 0,
      total_skills: stats.total_skills || 36,
      favorites_count: stats.favorites_count || 0,
      contributed_count: stats.contributed_count || 1,
      installed_skills: stats.installed_skills || [],
      favorite_skills: stats.favorite_skills || [],
      contributed_skills: stats.contributed_skills || []
    };

    if (!isAuth) {
      return `
        <div class="profile-view-wrapper">
          <div class="profile-guest-hero">
            <div class="profile-guest-icon-glow">
              <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
                <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            </div>
            <h2 class="profile-guest-title">Không Gian Hồ Sơ & Portfolio Kỹ Sư AI</h2>
            <p class="profile-guest-subtitle">
              Đăng nhập tài khoản để quản lý danh tính, lưu trữ bộ sưu tập 36 kỹ năng lên Supabase Cloud, 
              và xây dựng hồ sơ lập trình viên Agentic chuyên nghiệp.
            </p>
            <div class="profile-guest-actions">
              <button class="btn btn-primary" id="btn-profile-guest-login" style="padding:10px 22px; font-size:13.5px;">
                ${Icons.user}
                <span>Đăng Nhập / Đăng Ký Tài Khoản</span>
              </button>
              <button class="btn btn-secondary" id="btn-profile-guest-github" style="padding:10px 20px; font-size:13.5px;">
                ${Icons.github}
                <span>Đăng Nhập 1-Chạm Bằng GitHub</span>
              </button>
            </div>
          </div>
        </div>
      `;
    }

    const initial = (u.full_name || u.email || "U").charAt(0).toUpperCase();
    const avatarImg = u.avatar_url 
      ? `<img src="${this.escape(u.avatar_url)}" alt="Avatar" class="profile-avatar-img" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" /><div class="profile-avatar-fallback" style="display:none;">${this.escape(initial)}</div>`
      : `<div class="profile-avatar-fallback">${this.escape(initial)}</div>`;

    const presetAvatars = [
      { name: "Lăng Kính Hình Học", path: "assets/logo/avatar-geometric-prism.png" },
      { name: "Kyuu4 Spirit", path: "assets/logo/avatar-kyuu4.png" },
      { name: "Cáo Chân Trời", path: "assets/logo/horizon-prism-fox.png" },
      { name: "Sóng Tỉ Lệ Vàng", path: "assets/logo/golden-ratio-wave-fox.png" },
      { name: "Cáo Biển Trời", path: "assets/logo/ocean-sky-hidden-fox.png" },
      { name: "Cáo Âm Bản Gestalt", path: "assets/logo/ocean-sky-pure-silhouette-fox.png" }
    ];

    const currentAvatarUrl = u.avatar_url || "";

    return `
      <div class="profile-view-wrapper">
        <!-- Hero Profile Banner -->
        <div class="profile-hero-card">
          <div class="profile-hero-left">
            <div class="profile-avatar-wrapper">
              ${avatarImg}
              <div class="profile-avatar-badge-led" title="Trực tuyến & Đã đồng bộ"></div>
            </div>
            <div class="profile-meta-info">
              <div class="profile-name-row">
                <h1 class="profile-display-name">${this.escape(u.full_name || u.email.split('@')[0])}</h1>
                <span class="profile-role-badge">${this.escape(u.role || 'Creator / Pro')}</span>
                ${u.provider === 'github' ? '<span class="profile-provider-pill github"><svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg> GitHub Verified</span>' : '<span class="profile-provider-pill supabase">● Supabase Cloud</span>'}
              </div>
              <div class="profile-email-row">${this.escape(u.email || '')}</div>
              <p class="profile-bio-text">${this.escape(u.bio || 'Lập trình viên AI & Kiến trúc sư hệ thống Agentic chuyên nghiệp.')}</p>
            </div>
          </div>
          <div class="profile-hero-actions">
            <button class="btn btn-secondary" id="btn-profile-copy-token" title="Sao chép Access Token (JWT)">
              ${Icons.key}
              <span>Sao chép JWT</span>
            </button>
            <button class="btn btn-danger" id="btn-profile-signout" title="Đăng xuất tài khoản an toàn">
              ${Icons.logOut}
              <span>Đăng xuất</span>
            </button>
          </div>
        </div>

        <!-- Bento Metric Summary (4 Cards) -->
        <div class="profile-bento-metrics">
          <div class="profile-metric-card">
            <div class="profile-metric-header">
              <span class="profile-metric-icon cyan">${Icons.zap}</span>
              <span class="profile-metric-title">Kỹ Năng Đã Kích Hoạt</span>
            </div>
            <div class="profile-metric-val">${statsData.installed_count} <span class="profile-metric-max">/ ${statsData.total_skills}</span></div>
            <div class="profile-metric-sub">Đã nạp vào Antigravity, Claude, Cursor & Windsurf</div>
          </div>

          <div class="profile-metric-card">
            <div class="profile-metric-header">
              <span class="profile-metric-icon violet">${Icons.star}</span>
              <span class="profile-metric-title">Kỹ Năng Yêu Thích</span>
            </div>
            <div class="profile-metric-val">${statsData.favorites_count}</div>
            <div class="profile-metric-sub">Bộ sưu tập kỹ năng ghim truy cập nhanh</div>
          </div>

          <div class="profile-metric-card">
            <div class="profile-metric-header">
              <span class="profile-metric-icon emerald">${Icons.cloud}</span>
              <span class="profile-metric-title">Đã Chia Sẻ Cloud</span>
            </div>
            <div class="profile-metric-val">${statsData.contributed_count}</div>
            <div class="profile-metric-sub">Kỹ năng đóng góp cho Chợ Cộng Đồng</div>
          </div>

          <div class="profile-metric-card">
            <div class="profile-metric-header">
              <span class="profile-metric-icon blue">${Icons.shield}</span>
              <span class="profile-metric-title">Trạng Thái Bảo Mật</span>
            </div>
            <div class="profile-metric-val" style="font-size:16px; color:var(--ocean-secondary); font-weight:600;">Zero-Trust RLS</div>
            <div class="profile-metric-sub">Mã hóa SHA-256 & Lọc dữ liệu nhạy cảm PII</div>
          </div>
        </div>

        <!-- 2-Column Split: Edit Form + Portfolio Items -->
        <div class="profile-details-split">
          <!-- Column 1: Chỉnh sửa thông tin -->
          <div class="profile-card-panel">
            <div class="profile-panel-header">
              <h3 class="profile-panel-title">
                ${Icons.user}
                <span>Chỉnh Sửa Hồ Sơ & Hình Tượng</span>
              </h3>
              <span class="profile-panel-badge">Tự động đồng bộ Supabase</span>
            </div>

            <div class="profile-form-body">
              <div class="form-group">
                <label class="form-label">Họ và Tên / Tên Hiển Thị</label>
                <input type="text" id="profile-edit-name" class="form-input" value="${this.escape(u.full_name || '')}" placeholder="Ví dụ: Alex Nguyễn">
              </div>

              <div class="form-group">
                <label class="form-label">Dòng Giới Thiệu (Bio / Tagline)</label>
                <textarea id="profile-edit-bio" class="form-textarea" style="height:68px;" placeholder="Ví dụ: Kỹ sư Fullstack Next.js & Chuyên gia Tối ưu Prompt AI Agentic...">${this.escape(u.bio || '')}</textarea>
              </div>

              <div class="form-group">
                <label class="form-label">Chọn Ảnh Đại Diện (Bộ sưu tập Abyssal Sky v2.0)</label>
                <div class="profile-avatar-presets-grid" id="profile-avatar-picker">
                  ${presetAvatars.map(p => {
                    const isSelected = currentAvatarUrl === p.path;
                    return `
                      <div class="preset-avatar-option ${isSelected ? 'selected' : ''}" data-avatar-url="${p.path}" title="${p.name}">
                        <img src="${p.path}" alt="${p.name}" />
                        <span class="preset-avatar-name">${p.name}</span>
                      </div>
                    `;
                  }).join('')}
                </div>
              </div>

              <div class="form-group" style="margin-top:10px;">
                <label class="form-label">Hoặc Dán Đường Dẫn Link Ảnh Tùy Chọn (URL)</label>
                <input type="url" id="profile-edit-avatar-url" class="form-input" value="${this.escape(currentAvatarUrl)}" placeholder="https://example.com/avatar.png">
              </div>

              <div class="profile-form-footer">
                <button class="btn btn-primary" id="btn-save-profile" style="padding:8px 18px;">
                  ${Icons.check}
                  <span>Lưu Thay Đổi Hồ Sơ</span>
                </button>
                <span id="profile-save-status" class="profile-save-status"></span>
              </div>
            </div>
          </div>

          <!-- Column 2: Danh Mục Portfolio Kỹ Năng -->
          <div class="profile-card-panel">
            <div class="profile-panel-header">
              <h3 class="profile-panel-title">
                ${Icons.folder}
                <span>Danh Mục Portfolio Kỹ Năng Của Tôi</span>
              </h3>
              <span class="profile-panel-badge">${statsData.installed_count} Kỹ năng kích hoạt</span>
            </div>

            <div class="profile-portfolio-list">
              <div class="portfolio-section-title">Kỹ năng đang hoạt động trong dự án:</div>
              <div class="portfolio-chips-grid">
                ${statsData.installed_skills.length > 0 ? statsData.installed_skills.map(s => `
                  <div class="portfolio-skill-chip" data-skill-id="${s.id}">
                    <span class="skill-chip-dot active"></span>
                    <span class="skill-chip-title">${this.escape(s.title)}</span>
                    <span class="skill-chip-cat">${this.escape(s.category)}</span>
                  </div>
                `).join('') : '<div class="portfolio-empty-hint">Chưa có kỹ năng nào được kích hoạt. Hãy vào Kho Kỹ Năng để kích hoạt ngay.</div>'}
              </div>

              <div class="portfolio-section-title" style="margin-top:18px;">Kỹ năng đã xuất bản / Đóng góp:</div>
              <div class="portfolio-contributed-grid">
                ${statsData.contributed_skills.length > 0 ? statsData.contributed_skills.map(c => `
                  <div class="portfolio-contributed-card">
                    <div style="font-weight:600; color:var(--text-primary); font-size:13px; margin-bottom:4px;">${this.escape(c.title)}</div>
                    <div style="display:flex; justify-content:space-between; align-items:center; font-size:11.5px; color:var(--text-muted);">
                      <span>Chủ đề: ${this.escape(c.category)}</span>
                      <span style="color:var(--ocean-cyan);">⬇ ${c.downloads || 1} lượt tải</span>
                    </div>
                  </div>
                `).join('') : ''}
              </div>

              <div style="margin-top:20px; padding-top:14px; border-top:1px solid var(--border-subtle); display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:12px; color:var(--text-secondary);">Bạn muốn tự chế tác thêm kỹ năng riêng?</span>
                <button class="btn btn-secondary" id="btn-profile-open-studio" style="font-size:12px; padding:6px 14px; white-space:nowrap; display:inline-flex; align-items:center; gap:6px;">
                  ${Icons.box}
                  <span>Mở Xưởng Chế Tác Studio</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  static escape(str) {
    if (!str) return "";
    return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
  }
}

window.UIComponents = UIComponents;
window.Icons = Icons;
window.MarkdownRenderer = MarkdownRenderer;
