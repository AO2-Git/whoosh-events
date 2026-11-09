# Whoosh Events

Whoosh Events is a responsive website that consolidates UTD events from the
UTD Calendar and Nebula Labs Club Calendar into one searchable event list.
The project is being developed by Team 05 for UTD CS3354, Fall 2026.

## Product scope

The site will:

- Display at least 20 upcoming events on the main page.
- Filter events by category, organizer, and source.
- Show event details, including title, date, location, organizer, and source.
- Load additional events through pagination or an equivalent progressive list.
- Export an event to a personal calendar.
- Provide a copyable link to an individual event.
- Explain how an organization can host or submit a UTD event.
- Work on mobile, desktop, and keyboard-accessible interfaces.

The site will not provide user accounts, direct event creation, comments,
recommendations, or a full calendar-view interface. Event data comes only from
the approved source sites.

## Planned architecture

The frontend will be a Vite React application written in TypeScript. It will
read a generated JSON dataset from `public/data/events.json`, allowing the
deployed site to remain stateless and compatible with Vercel's free hosting
plan.

```text
UTD Calendar ─┐
              ├─ GitHub Actions scraper ── public/data/events.json ── Vercel
Nebula Labs ──┘                                      │
                                                     └─ React event list
```

### Technology stack

- React and TypeScript
- Vite for local development and production builds
- CSS for responsive, accessible styling
- Node.js and Cheerio for the scraping scripts
- GitHub Actions for scheduled scraping
- Vercel for hosting and deployment
- Vitest and Playwright for automated testing
- Zod for validating normalized scraped data
- ICS and/or Google Calendar links for calendar export

## Data refresh and deployment

GitHub Actions will run the scraper hourly. The scraper will:

1. Fetch both approved event sources while respecting their `robots.txt` rules.
2. Normalize events into a shared schema and validate the result.
3. Keep the last successful JSON dataset if a source is temporarily unavailable.
4. Commit changed data to `main`.
5. Let Vercel deploy the updated site after the data commit.

The application should display the dataset's last refresh time and source
information. Stable event IDs will support deduplication and shareable links.

## Local development

Requirements: Node.js 20 or newer and npm.

```bash
npm install
npm run dev
```

Open the local URL printed by Vite. To create a production build:

```bash
npm run build
npm run preview
```

## Repository layout

```text
src/
  App.tsx          React starter page
  main.tsx         Application entry point
  styles.css       Global responsive styles
public/
  data/events.json Generated event data (future scraper output)
tests/
  spikes/
    spike1.js      P2 architecture spike experiment
  OtherTests/      Future unit, integration, and acceptance tests
docs/p1/           P1 requirements document
temp/              Working project documents
```

## Requirements and references

- [P1 requirements](docs/p1/CS3354_F2026_TEAM05_P1.pdf)
- [P2 analysis and high-level design](temp/Team%2005%20%E2%80%93%20P2%20Analysis%20and%20High-Level%20Design%20%28WORKING%20DOC%29.pdf)
- [P2 plan and task split](temp/Team%2005%20%E2%80%93%20P2%20Plan%20and%20Task%20Split.pdf)
- [UTD Calendar](https://calendar.utdallas.edu/calendar)
- [Nebula Labs Club Calendar](https://clubs.utdnebula.com/events?page=1)
