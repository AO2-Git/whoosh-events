import { mkdir, readFile, writeFile } from 'node:fs/promises'
import { performance } from 'node:perf_hooks'
import * as cheerio from 'cheerio'

const sources = [
  {
    name: 'UTD Calendar',
    url: 'https://calendar.utdallas.edu/calendar',
    parse: parseJsonLdEvents,
  },
  {
    name: 'UTD Calendar API',
    url: 'https://calendar.utdallas.edu/api/2/events',
    parse: parseUtdApiEvents,
    format: 'json',
    measurementOnly: true,
  },
  {
    name: 'Nebula Labs Club Calendar',
    url: 'https://clubs.utdnebula.com/events?page=1',
    parse: parseNebulaEvents,
  },
]

const outputPath = new URL('./events.json', import.meta.url)

async function fetchAndParse(source) {
  const startedAt = performance.now()

  try {
    const response = await fetch(source.url, {
      headers: {
        'user-agent': 'Whoosh-Events-S01-Spike/0.1 (CS3354 student project)',
      },
    })
    const body = await response.text()
    const payload = source.format === 'json' ? JSON.parse(body) : body
    const events = response.ok ? source.parse(payload, source) : []

    return {
      source: source.name,
      url: source.url,
      status: response.status,
      ok: response.ok,
      durationMs: round(performance.now() - startedAt),
      bytes: Buffer.byteLength(body),
      eventsFound: events.length,
      fieldCompleteness: getFieldCompleteness(events),
      events,
      error: response.ok ? null : `HTTP ${response.status}`,
    }
  } catch (error) {
    return {
      source: source.name,
      url: source.url,
      status: null,
      ok: false,
      durationMs: round(performance.now() - startedAt),
      bytes: 0,
      eventsFound: 0,
      fieldCompleteness: getFieldCompleteness([]),
      events: [],
      error: error instanceof Error ? error.message : String(error),
    }
  }
}

function parseJsonLdEvents(html, source) {
  const $ = cheerio.load(html)
  const events = []

  $('script[type="application/ld+json"]').each((_, element) => {
    try {
      const value = JSON.parse($(element).contents().text())
      const candidates = flatten(value)
      for (const candidate of candidates) {
        if (!isEventType(candidate?.['@type'])) continue
        events.push(normalizeEvent(candidate, source, candidate.url))
      }
    } catch {
      // Ignore unrelated or malformed JSON-LD blocks in the source page.
    }
  })

  return events.filter(Boolean)
}

function parseUtdApiEvents(payload, source) {
  if (!Array.isArray(payload?.events)) return []

  return payload.events
    .map((item) => item?.event)
    .filter(Boolean)
    .map((event) => {
      const instance = event.event_instances?.[0]?.event_instance
      const startDate = instance?.all_day
        ? instance.start?.slice(0, 10)
        : instance?.start
      return normalizeEvent({
        id: event.id,
        name: event.title,
        startDate,
        location: event.location_name || event.location || event.address,
        organizer: event.departments?.[0]?.name,
        url: event.localist_url || event.url,
      }, source, event.id)
    })
    .filter(Boolean)
}

function parseNebulaEvents(html, source) {
  const $ = cheerio.load(html)
  const events = []

  $('a.EventCardLink').each((_, link) => {
    const href = $(link).attr('href')
    const card = $(link).parent()
    const details = card.find('div.flex.flex-col.space-y-2\\.5').first()
    const title = details.find('h3').first().text().trim()
    const organizer = details.find('div').eq(0).text().trim()
    const schedule = details.find('div').eq(1).text().trim()
    const parsedSchedule = parseNebulaSchedule(schedule)

    if (!href || !title) return

    events.push(normalizeEvent({
      name: title,
      organizer,
      startDate: parsedSchedule.startDate,
      location: null,
      url: new URL(href, source.url).href,
    }, source, href))
  })

  return events
}

function normalizeEvent(event, source, fallbackId) {
  const title = clean(event.name || event.title)
  if (!title) return null

  const sourceUrl = event.url
    ? new URL(event.url, source.url).href
    : source.url

  return {
    id: stableId(source.name, event.id || fallbackId || title),
    title,
    date: event.startDate ? String(event.startDate).slice(0, 10) : null,
    time: event.startDate ? String(event.startDate).slice(11, 16) : null,
    location: formatLocation(event.location),
    organizer: clean(event.organizer?.name || event.organizer),
    source: source.name,
    sourceUrl,
  }
}

function flatten(value) {
  if (!Array.isArray(value)) return [value]
  return value.flatMap(flatten)
}

function isEventType(type) {
  return Array.isArray(type) ? type.includes('Event') : type === 'Event'
}

function parseNebulaSchedule(schedule) {
  const match = schedule.match(
    /^(?:\w{3}, )?([A-Z][a-z]{2} \d{1,2}), (\d{1,2}:\d{2} [AP]M)/
  )
  if (!match) return { startDate: null }

  const now = new Date()
  const currentYear = now.getUTCFullYear()
  const parsed = new Date(`${match[1]}, ${currentYear}`)
  if (Number.isNaN(parsed.getTime())) return { startDate: null }
  if (parsed < new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()))) {
    parsed.setUTCFullYear(currentYear + 1)
  }

  const [hour, minute] = match[2].match(/\d+/g).map(Number)
  const isPm = match[2].endsWith('PM')
  const hour24 = (hour % 12) + (isPm ? 12 : 0)
  const date = parsed.toISOString().slice(0, 10)
  return {
    startDate: `${date}T${String(hour24).padStart(2, '0')}:${String(minute).padStart(2, '0')}:00`,
  }
}

function formatLocation(location) {
  if (!location) return null
  if (typeof location === 'string') return clean(location)
  return clean([
    location.name,
    location.address?.streetAddress || location.address,
    location.address?.addressLocality,
  ].filter(Boolean).join(', '))
}

function stableId(source, value) {
  return `${source.toLowerCase().replaceAll(/[^a-z0-9]+/g, '-')}-${String(value)
    .toLowerCase()
    .replaceAll(/[^a-z0-9]+/g, '-')
    .replaceAll(/^-|-$/g, '')}`
}

function clean(value) {
  if (value === null || value === undefined) return null
  const result = String(value).replace(/\s+/g, ' ').trim()
  return result || null
}

function round(value) {
  return Math.round(value)
}

function getFieldCompleteness(events) {
  const fields = ['title', 'date', 'time', 'location']
  return Object.fromEntries(fields.map((field) => [
    field,
    {
      present: events.filter((event) => event[field]).length,
      missing: events.filter((event) => !event[field]).length,
    },
  ]))
}

const startedAt = performance.now()
const results = await Promise.all(sources.map(fetchAndParse))
const previousEvents = await readPreviousEvents()
const refreshedResults = results.filter((result) => {
  const source = sources.find((candidate) => candidate.name === result.source)
  return !source?.measurementOnly
})
const refreshedEvents = refreshedResults
  .filter((result) => result.ok && result.eventsFound > 0)
  .flatMap((result) => result.events)
const retainedEvents = results
  .filter((result) => {
    const source = sources.find((candidate) => candidate.name === result.source)
    return !source?.measurementOnly && (!result.ok || result.eventsFound === 0)
  })
  .flatMap((result) => previousEvents.filter((event) => event.source === result.source))
const allEvents = [...refreshedEvents, ...retainedEvents]
const uniqueEvents = [...new Map(allEvents.map((event) => [event.id, event])).values()]
const requiredFields = ['id', 'title', 'date', 'source', 'sourceUrl']
const incompleteFieldCounts = Object.fromEntries(
  requiredFields
    .map((field) => [
      field,
      uniqueEvents.filter((event) => !event[field]).length,
    ])
    .filter(([, count]) => count > 0),
)
const output = {
  generatedAt: new Date().toISOString(),
  events: uniqueEvents,
}

await mkdir(new URL('./', outputPath), { recursive: true })
await writeFile(outputPath, `${JSON.stringify(output, null, 2)}\n`)

const report = {
  generatedAt: output.generatedAt,
  totalDurationMs: round(performance.now() - startedAt),
  sourceResults: results.map(({ events, ...result }) => result),
  totalEventsFound: allEvents.length,
  refreshedEvents: refreshedEvents.length,
  retainedEvents: retainedEvents.length,
  duplicateEventsRemoved: allEvents.length - uniqueEvents.length,
  validEvents: uniqueEvents.length,
  incompleteFieldCounts,
  outputPath: outputPath.pathname,
}

console.log(JSON.stringify(report, null, 2))
if (results.every((result) => !result.ok)) process.exitCode = 1

async function readPreviousEvents() {
  try {
    const previous = JSON.parse(await readFile(outputPath, 'utf8'))
    return Array.isArray(previous.events) ? previous.events : []
  } catch {
    return []
  }
}
