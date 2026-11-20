# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/dankurniaone/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/dankurniaone/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

The World in One Day — a one-image summary of the world's news of Friday 20 November 2026, entered in make.fun's `news-image-20261120` bounty. The entry is a light-paper broadsheet, a single 680×1024 PNG rendered at 2× and downscaled: a cyclone lead with a real storm photograph owns the top of the page, two story columns with real photographs carry the middle, a markets strip and a one-line red ticker carry the day's other fragments.

Bounty: https://make.fun/bounty/news-image-20261120 — referral: https://make.fun/r/adyjn11j

## What's on the page

- **Lead — Cyclone Akvan makes landfall.** Severe Cyclone Akvan crosses India's east coast near Gopalpur around noon, with winds of 90–100 km/h gusting to 110. Over 300,000 people evacuated; 423 rescue teams deployed, 69 trains cancelled. Shown with a real photograph of palm trees bending in a storm wind over a grey sea.
- **Ukraine — Missiles strike Kyiv at dawn.** Debris from a Russian missile strike set a three-storey building ablaze in the Obolonskyi district in the early hours of Friday; explosions were heard across the capital. Shown with a real aerial photograph of Kyiv and the Dnipro at first light.
- **Italy — General strike.** The CGIL union's 24-hour general strike brings some 100 marches across Italy, schools and buses halted, in protest at the 2027 budget and the cost of living. The Rome march sets off at 9:30 from Piazza Vittorio. Shown with a real photograph of a crowded street in Rome.
- **Markets — Taiwan.** A day after the Taiex fell 4.4% — its worst month since 2008 — Taiwan's new short-selling curbs take effect: intraday borrowed shares capped at 1%, no shorting below the close after a 3.5% drop.
- **Ticker.** COP31: final deal due today · Taiwan short-sell curbs take effect · Fed: Dec hike likely.

## How it was made

`news.json` holds the day's copy; `tools/render20.py` draws the whole broadsheet in Pillow — masthead, headlines, columns, markets strip, ticker — pastes in the three photographs, and renders at 2× (1360×2048) before a LANCZOS downscale to 680×1024, so the small type stays crisp. `main.ts` validates `entry.png` (PNG signature, 680×1024, at most 1 MiB) and copies it to `MAKEFUN_OUTPUT_DIR`.

## Photos

The three photographs are freely-licensed Pexels file photos, credited here; none is a picture from 20 November itself, and the page says so in its footer:

- Storm coast, palm trees bending in the wind — Atlantic Ambience, Pexels photo 12661315 (https://www.pexels.com/photo/coconut-trees-near-the-sea-12661315/)
- Kyiv and the Dnipro — Maryia Plashchynskaya, Pexels photo 3442567 (https://www.pexels.com/photo/aerial-photo-of-a-city-3442567/)
- Crowded street in Rome — Paweł L., Pexels photo 1423619 (https://www.pexels.com/photo/people-walking-on-sidewalk-beside-road-1423619/)

News copy is sourced from Reuters, IMD, AP and BBC reporting of 20 November 2026 (see the footer on the page). Every story on the page is an event of Friday 20 November 2026 itself — Akvan's landfall is today, the Kyiv strike was in the early hours of today, the Italian strike is today, Taiwan's curbs take effect today, and the COP31 final deal is due today.

## Run it

```sh
python3 tools/render20.py        # rebuild entry.png (680x1024)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
