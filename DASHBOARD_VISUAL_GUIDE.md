# Dashboard Visual Architecture Guide

## 🎨 Complete Dashboard Layout

### Desktop View (1024px+)
```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🏠 LegacyMind AI                                    [Refresh] [Export] [⚙️] │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📦 repository-name / owner                    ⭐ 1.2k  📝 TypeScript  🕐 2h │
├─────────────────────────────────────────────────────────────────────────────┤
│ [Summary] [Architecture] [Dependencies] [Risks] [Modernization]             │
├──────────────────────────────────────────────────────┬──────────────────────┤
│                                                       │  💬 AI Assistant     │
│  📊 MAIN CONTENT AREA                                │  ─────────────────── │
│                                                       │                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │  User: How does...   │
│  │  Card 1  │ │  Card 2  │ │  Card 3  │            │                      │
│  │  Stats   │ │  Stats   │ │  Stats   │            │  AI: The auth...     │
│  └──────────┘ └──────────┘ └──────────┘            │                      │
│                                                       │  [Type message...]   │
│  ┌─────────────────────────────────────┐            │  [Send]              │
│  │  Detailed Section                    │            │                      │
│  │  • Item 1                            │            │  [Collapse] ◀        │
│  │  • Item 2                            │            │                      │
│  └─────────────────────────────────────┘            │                      │
│                                                       │                      │
└──────────────────────────────────────────────────────┴──────────────────────┘
```

### Mobile View (320px - 767px)
```
┌─────────────────────────────┐
│ ☰  LegacyMind AI        ⚙️  │
├─────────────────────────────┤
│ 📦 repo-name                │
│ ⭐ 1.2k  📝 TS  🕐 2h       │
├─────────────────────────────┤
│ ← Summary →                 │
├─────────────────────────────┤
│                             │
│  ┌───────────────────────┐ │
│  │  Card 1               │ │
│  │  Stats                │ │
│  └───────────────────────┘ │
│                             │
│  ┌───────────────────────┐ │
│  │  Card 2               │ │
│  │  Stats                │ │
│  └───────────────────────┘ │
│                             │
│  ┌───────────────────────┐ │
│  │  Detailed Section     │ │
│  │  • Item 1             │ │
│  │  • Item 2             │ │
│  └───────────────────────┘ │
│                             │
└─────────────────────────────┘
│ 💬 Chat (tap to open)      │
└─────────────────────────────┘
```

## 📑 Tab Content Layouts

### 1. Summary Tab
```
┌─────────────────────────────────────────────────────────┐
│  Repository Statistics                                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ 📁 Files │ │ 📝 Lines │ │ 👥 Contri│ │ 🕐 Update│  │
│  │   1,234  │ │  45.6K   │ │    12    │ │  2 hrs   │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│                                                          │
│  Overview                                                │
│  ┌────────────────────────────────────────────────────┐ │
│  │ 📦 Modern React application with TypeScript        │ │
│  │ 🏗️ Architecture: Component-based SPA               │ │
│  │ 🎯 Primary Language: TypeScript (78%)              │ │
│  │ 📊 Health Score: 85/100 ⭐⭐⭐⭐                    │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  Quick Insights                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ ✅ Well-structured component hierarchy             │ │
│  │ ⚠️  Some dependencies are outdated                 │ │
│  │ 💡 Consider migrating to Next.js 15                │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 2. Architecture Tab
```
┌─────────────────────────────────────────────────────────┐
│  Interactive Architecture Graph                          │
│  [Fit View] [Zoom In] [Zoom Out] [Layout: Horizontal]  │
│  ┌────────────────────────────────────────────────────┐ │
│  │                                                     │ │
│  │     ┌─────────┐                                    │ │
│  │     │  App    │                                    │ │
│  │     └────┬────┘                                    │ │
│  │          │                                         │ │
│  │     ┌────┴────┬────────┬────────┐                │ │
│  │     │         │        │        │                │ │
│  │  ┌──▼──┐  ┌──▼──┐  ┌──▼──┐  ┌──▼──┐            │ │
│  │  │Auth │  │Home │  │User │  │API  │            │ │
│  │  └─────┘  └─────┘  └─────┘  └─────┘            │ │
│  │                                                     │ │
│  │  [Mini-map]                                        │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  Selected Node: Auth Module                             │
│  ┌────────────────────────────────────────────────────┐ │
│  │ 📦 auth/                                           │ │
│  │ • 5 files                                          │ │
│  │ • 1,234 lines                                      │ │
│  │ • Dependencies: jwt, bcrypt                        │ │
│  │ • Exports: login, logout, verify                   │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 3. Dependencies Tab
```
┌─────────────────────────────────────────────────────────┐
│  Dependency Overview                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ 📦 Total │ │ ⚠️ Outdat│ │ 🔴 Vulner│ │ 📅 Avg   │  │
│  │    45    │ │    12    │ │     3    │ │ 18 mo    │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│                                                          │
│  Outdated Packages (12)                                  │
│  ┌────────────────────────────────────────────────────┐ │
│  │ react 17.0.2 → 18.3.1 [Update] 🟡 Breaking        │ │
│  │ next 12.0.0 → 15.0.3 [Update] 🟡 Breaking         │ │
│  │ axios 0.21.1 → 1.7.7 [Update] 🟢 Safe             │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  Security Vulnerabilities (3)                            │
│  ┌────────────────────────────────────────────────────┐ │
│  │ 🔴 CRITICAL: lodash < 4.17.21                      │ │
│  │    CVE-2021-23337 - Prototype Pollution            │ │
│  │    Fix: npm install lodash@latest                  │ │
│  │                                                     │ │
│  │ 🟠 HIGH: axios < 0.21.2                            │ │
│  │    CVE-2021-3749 - SSRF Vulnerability              │ │
│  │    Fix: npm install axios@latest                   │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 4. Risks Tab
```
┌─────────────────────────────────────────────────────────┐
│  Technical Debt Score                                    │
│  ┌────────────────────────────────────────────────────┐ │
│  │              ╭─────────╮                           │ │
│  │            ╱             ╲                         │ │
│  │          ╱       72       ╲                        │ │
│  │         │                  │                       │ │
│  │          ╲               ╱                         │ │
│  │            ╲           ╱                           │ │
│  │              ╰─────────╯                           │ │
│  │         🟢 Good (60-80)                            │ │
│  │         Trending: ↗️ Improving                     │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  Risk Matrix                                             │
│  ┌────────────────────────────────────────────────────┐ │
│  │ High │ 🟡 Config  │ 🔴 Security │                  │ │
│  │ Impact│  Issues   │   Vulns     │                  │ │
│  │      │            │             │                  │ │
│  │ Low  │ 🟢 Docs    │ 🟡 Tech     │                  │ │
│  │ Impact│  Missing  │   Debt      │                  │ │
│  │      └────────────┴─────────────┘                  │ │
│  │        Low Prob     High Prob                       │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  Risk Breakdown                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Code Quality      ████████░░ 80%                   │ │
│  │ Security          ██████░░░░ 60%                   │ │
│  │ Performance       █████████░ 90%                   │ │
│  │ Maintainability   ███████░░░ 70%                   │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 5. Modernization Tab
```
┌─────────────────────────────────────────────────────────┐
│  Modernization Suggestions (8)                           │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ 🚀 Migrate to Next.js 15                           │ │
│  │ Impact: 🔴 High  |  Effort: 🟡 Medium (2-3 days)  │ │
│  │                                                     │ │
│  │ Benefits:                                           │ │
│  │ • Server Components for better performance          │ │
│  │ • Improved routing with App Router                  │ │
│  │ • Built-in optimizations                            │ │
│  │                                                     │ │
│  │ [View Guide] [Start Migration]                     │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ 🔧 Update Dependencies                             │ │
│  │ Impact: 🟡 Medium  |  Effort: 🟢 Low (2-4 hours)  │ │
│  │                                                     │ │
│  │ Benefits:                                           │ │
│  │ • Security patches                                  │ │
│  │ • Bug fixes                                         │ │
│  │ • Performance improvements                          │ │
│  │                                                     │ │
│  │ [View Details] [Auto-Update]                       │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  Priority Matrix                                         │
│  ┌────────────────────────────────────────────────────┐ │
│  │ High │ 🎯 Quick   │ 🚀 Major    │                  │ │
│  │ Impact│   Wins    │   Projects  │                  │ │
│  │      │ • Deps    │ • Next.js   │                  │ │
│  │      │ • Tests   │ • TypeScript│                  │ │
│  │      │            │             │                  │ │
│  │ Low  │ 📝 Fill-ins│ ⏰ Time     │                  │ │
│  │ Impact│ • Docs    │   Sinks     │                  │ │
│  │      │ • Comments│ • Refactor  │                  │ │
│  │      └────────────┴─────────────┘                  │ │
│  │        Low Effort   High Effort                     │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 💬 Chatbot Panel States

### Collapsed State
```
┌──────────────────┐
│ 💬 AI Assistant  │
│ ─────────────────│
│                  │
│ [Expand] ▶       │
│                  │
└──────────────────┘
```

### Expanded State
```
┌────────────────────────────┐
│ 💬 AI Assistant    [✕]     │
├────────────────────────────┤
│                            │
│ User: How does auth work?  │
│                            │
│ AI: The authentication     │
│ system uses JWT tokens...  │
│                            │
│ ```typescript              │
│ const token = jwt.sign()   │
│ ```                        │
│                            │
│ User: Show me the login    │
│                            │
│ AI: Here's the login...    │
│                            │
├────────────────────────────┤
│ [Type your message...]     │
│ [📎] [Send]                │
└────────────────────────────┘
```

### Mobile Overlay
```
┌─────────────────────────────┐
│ 💬 AI Assistant        [✕]  │
├─────────────────────────────┤
│                             │
│ User: How does auth work?   │
│                             │
│ AI: The authentication      │
│ system uses JWT tokens...   │
│                             │
│                             │
│                             │
│                             │
│                             │
│                             │
│                             │
├─────────────────────────────┤
│ [Type your message...]      │
│ [Send]                      │
└─────────────────────────────┘
```

## 🎨 Component States

### Loading State
```
┌─────────────────────────────┐
│ ┌─────────────────────────┐ │
│ │ ░░░░░░░░░░░░░░░░░░░░░░ │ │ (Skeleton)
│ │ ░░░░░░░░░░░░░░░░░░░░░░ │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ ░░░░░░░░░░░░░░░░░░░░░░ │ │
│ │ ░░░░░░░░░░░░░░░░░░░░░░ │ │
│ └─────────────────────────┘ │
└─────────────────────────────┘
```

### Error State
```
┌─────────────────────────────┐
│      ⚠️                      │
│   Failed to load data        │
│                             │
│ [Retry] [Go Back]           │
└─────────────────────────────┘
```

### Empty State
```
┌─────────────────────────────┐
│      📭                      │
│   No data available          │
│                             │
│ Try analyzing a repository  │
│ [Get Started]               │
└─────────────────────────────┘
```

## 🎭 Animation Sequences

### Page Load Animation
```
1. Header fades in (0ms)
2. Tabs slide in from top (100ms)
3. Cards stagger in (200ms, 100ms delay each)
4. Chat panel slides in from right (500ms)
```

### Tab Switch Animation
```
1. Current content fades out (150ms)
2. New content fades in (150ms, starts at 100ms)
3. Active tab indicator slides (300ms)
```

### Card Hover Animation
```
1. Card lifts up 2px (200ms)
2. Glow effect intensifies (200ms)
3. Border color brightens (200ms)
```

### Chat Message Animation
```
1. Message slides in from bottom (200ms)
2. Fade in (200ms)
3. Auto-scroll to bottom (300ms)
```

## 🎨 Color Usage Guide

### Status Colors
```
✅ Success: #43e97b (Green)
⚠️ Warning: #f5a623 (Amber)
❌ Error: #f5576c (Red)
ℹ️ Info: #4facfe (Blue)
```

### Severity Colors
```
🔴 Critical: #f5576c
🟠 High: #f5a623
🟡 Medium: #f5d547
🟢 Low: #43e97b
```

### Gradient Usage
```
Primary: Headers, CTAs, Important elements
Accent: Highlights, Active states, Links
Success: Positive metrics, Completed items
```

## 📐 Spacing System

### Card Spacing
```
Padding: 1.5rem (24px)
Gap between cards: 1rem (16px)
Section margin: 2rem (32px)
```

### Typography Spacing
```
Heading margin-bottom: 1rem (16px)
Paragraph margin-bottom: 0.75rem (12px)
List item spacing: 0.5rem (8px)
```

### Layout Spacing
```
Header height: 4rem (64px)
Tab bar height: 3rem (48px)
Chat panel width: 24rem (384px)
Content padding: 2rem (32px)
```

## 🎯 Interactive Elements

### Buttons
```
Primary:   [Gradient background, white text, glow on hover]
Secondary: [Glass background, white text, lift on hover]
Ghost:     [Transparent, white text, background on hover]
```

### Cards
```
Default:   [Glass background, subtle border]
Hover:     [Lift 2px, glow effect, brighter border]
Active:    [Pressed state, no lift]
```

### Inputs
```
Default:   [Glass background, subtle border]
Focus:     [Brighter border, glow effect, no outline]
Error:     [Red border, error message below]
```

## 📱 Responsive Breakpoints

### Mobile (320px - 767px)
- Single column layout
- Stacked cards
- Bottom sheet chat
- Hamburger menu
- Touch-optimized controls

### Tablet (768px - 1023px)
- 2-column grid
- Drawer chat panel
- Visible tabs
- Medium-sized cards

### Desktop (1024px+)
- 3-column grid
- Side panel chat
- Full navigation
- Large cards
- Hover effects

---

*This visual guide complements the DASHBOARD_BUILD_PLAN.md*
*Use these layouts as reference during implementation*