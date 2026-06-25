# BountyBoard New Design

This document describes the current pixel-art design system used by BountyBoard.

## Design Direction

BountyBoard now uses a retro RPG quest-board style. The app should feel like a campus bounty board where each task is a quest card.

Core style goals:

- Pixel-art inspired interface
- Hard rectangular edges
- Thick black borders
- Chunky buttons with offset shadows
- Parchment-style background
- Quest-board wording where appropriate
- Mobile-friendly card layout
- Highly scannable bounty amounts, deadlines, and actions

## Visual Theme

The theme is defined in `static/src/input.css` using Tailwind CSS v4 theme variables.

### Fonts

Primary UI font:

```css
"Pixelify Sans", system-ui, sans-serif
```

Display font for logo and major headings:

```css
"Press Start 2P", "Pixelify Sans", system-ui, sans-serif
```

Usage guidance:

- Use `font-sans` for normal UI text.
- Use `font-display` only for headings, labels, and short title text.
- Avoid long paragraphs in `font-display` because it is harder to read.

## Color Palette

| Token | Value | Usage |
| --- | --- | --- |
| `primary` | `#ffcc00` | Main buttons, selected category, reward highlights |
| `primary-active` | `#ff9f1c` | Button hover state |
| `ink` | `#1a1a1a` | Borders, main text, dark navbar |
| `body` | `#3d2f24` | Paragraph text |
| `muted` | `#715943` | Secondary text |
| `canvas` | `#f8e7b0` | Page background |
| `canvas-soft` | `#ffeec2` | Input and note backgrounds |
| `surface-card` | `#fff7d6` | Card and panel backgrounds |
| `surface-strong` | `#ffd166` | Category tags and emphasis blocks |
| `on-primary` | `#1a1a1a` | Text on yellow buttons |
| `on-dark` | `#fff7d6` | Text on dark navbar |
| `semantic-error` | `#ff4d6d` | Error messages |
| `semantic-success` | `#2ec27e` | Success messages or future completed states |

## Layout Style

The page background uses a subtle pixel grid:

```css
background-image:
  linear-gradient(rgba(26, 26, 26, 0.05) 1px, transparent 1px),
  linear-gradient(90deg, rgba(26, 26, 26, 0.05) 1px, transparent 1px);
background-size: 18px 18px;
```

The main content uses:

```html
max-w-5xl mx-auto px-5 py-12
```

Cards and page sections should use strong spacing and avoid visual clutter.

## Shape System

The design intentionally avoids soft rounded corners.

Theme radii:

```css
--radius-sm: 0px;
--radius-md: 0px;
--radius-lg: 0px;
```

Use square blocks, thick outlines, and offset shadows instead of rounded cards.

## Reusable Components

These component classes are defined in `static/src/input.css`.

### Pixel Panel

Used for major sections and important cards.

```html
<section class="pixel-panel p-6">
    ...
</section>
```

CSS behavior:

```css
border-4 border-ink bg-surface-card shadow-[8px_8px_0_#1a1a1a]
```

### Small Pixel Panel

Used for task cards, sidebar cards, and compact sections.

```html
<article class="pixel-panel-sm p-5">
    ...
</article>
```

CSS behavior:

```css
border-4 border-ink bg-surface-card shadow-[5px_5px_0_#1a1a1a]
```

### Pixel Button

Primary action button.

```html
<a class="pixel-button" href="#">Accept Quest</a>
```

Used for:

- Post Quest
- View
- Accept Quest
- Submit Proof
- Submit Review
- Login/Register buttons

Behavior:

- Yellow background
- Black border
- Offset black shadow
- Moves down/right on hover
- Shadow disappears on hover

### Dark Pixel Button

Alternative button for dark areas.

```html
<a class="pixel-button-dark" href="#">Action</a>
```

Use sparingly when a button sits on a darker background.

### Pixel Input

Used for all form fields.

```html
<input class="pixel-input">
```

Behavior:

- Thick black border
- Soft parchment background
- White background on focus
- Square corners

### Pixel Label

Used for form labels.

```html
<label class="pixel-label">Username</label>
```

Behavior:

- Small uppercase label
- Bold with wide tracking

## Navigation

The navbar uses a dark pixel header:

```html
bg-ink text-on-dark border-b-4 border-primary
```

The logo uses `font-display` and should remain short:

```text
BountyBoard
```

Authenticated users see:

- `P1: username`
- Profile
- Post Quest
- Log Out

Guest users see:

- Log In
- Register

## Task Feed

The homepage is the main bounty feed and uses quest-board language.

Primary heading block:

```text
Quest Board
Campus Bounties
Claim tasks. Earn cash. Build your rep.
```

Category filters are square pixel pills:

- Selected state: `bg-primary text-ink`
- Default state: `bg-surface-card text-ink hover:bg-surface-strong`

Task grid:

```html
grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3
```

## Task Cards

Task cards use `pixel-panel-sm`.

Important visual priorities:

1. Category tag
2. RM/MYR bounty amount
3. Task title
4. Short description
5. Deadline and poster username
6. View button

Bounty amount should remain prominent:

```html
border-4 border-ink bg-primary px-3 py-1 text-lg font-bold text-ink
```

## Task Detail Page

The task detail page uses a two-column layout on desktop:

```html
grid gap-6 lg:grid-cols-[1fr_360px]
```

Main task detail uses `pixel-panel`.

Sidebar sections use `pixel-panel-sm`.

Terminology:

- `Bounty actions` becomes `Quest Actions`
- `Claim status` becomes `Quest Status`
- `Claim Bounty` becomes `Accept Quest`
- `Approve Completion` becomes `Approve Clear`

Payment note must stay visible:

```text
Payment is arranged outside BountyBoard. The app only tracks the bounty, claim, proof, completion, and review.
```

## Forms

All forms should use:

- `pixel-panel` for the form container
- `pixel-label` for labels
- `pixel-input` for inputs, selects, textareas, and file fields
- `pixel-button` for submit actions

Form pages should keep short headings because `font-display` is intentionally chunky.

Examples:

- `Post Quest`
- `Player Login`
- `New Player`

## Profile Page

The profile page uses player-card language.

Main heading:

```text
Player Card
My Profile
```

Sections:

- Posted quests
- Claimed quests
- Received reviews

Each task link uses a bordered pixel row rather than a soft card.

## Content Language

Use marketplace terms where clarity matters, but prefer quest language for UI personality.

Recommended wording:

| Old | New |
| --- | --- |
| Post a Bounty | Post Quest |
| Claim Bounty | Accept Quest |
| Browse Bounties | Browse Quests |
| Posted bounties | Posted quests |
| Claimed tasks | Claimed quests |
| Bounty actions | Quest Actions |
| Claim status | Quest Status |

Keep `bounty` for money-related text because the platform concept is still BountyBoard.

## Responsiveness

The UI remains mobile-first.

Rules:

- Task cards stack in one column on mobile.
- Navbar wraps vertically on small screens.
- Detail page stacks before becoming two columns on large screens.
- Buttons should remain large enough to tap.

## Build Step

After editing styles or templates, rebuild Tailwind CSS:

```bash
npm run build
```

Generated CSS is written to:

```text
static/css/output.css
```

The app loads this file from `templates/base.html`:

```django
{% static 'css/output.css' %}
```

## Verification

After design changes, run:

```bash
npm run build
./venv/bin/python manage.py check
```

Recommended smoke-test pages:

```text
/
/tasks/
/accounts/login/
/accounts/register/
/accounts/profile/
```
