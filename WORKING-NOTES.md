# WORKING NOTES — news-image-20261125

Bounty: https://make.fun/bounty/news-image-20261125 — "Sum up 25 November's world news in one image", $100.
Kit: https://make.fun/c/news-image-20261125/kit (downloaded to /tmp/kit-20261125, kept OUT of repo).
Opens: 2026-11-25T00:00:00Z. Deadline: 2026-11-27T00:00:00Z = Fri 27 Nov 07:00 WIB.
Build session: subagent session started 26 Nov 2026 (after opening — thinking_in_window OK).

## Kit rules summary (RULES.txt / competition.yaml)
- Program at repo root: main.ts (Node 22) OR main.py (Python 3.13), standard library only, nothing installed.
- Writes one image to /output/entry.png; local test via MAKEFUN_OUTPUT_DIR env (starter convention).
- Whole PNG or JPEG, at most 1 MiB (1048576 bytes), at most 1024x1024 px.
- No network; runs twice, both runs must write identical bytes; 60 s/run, 512 MB.
- Judge: z-ai/glm-5.3-flash compares two images; criteria: (1) names its day + specific events of that day, (2) selection/breadth, (3) reads clearly, (4) faithful, (5) craft/legible at ~300 px. Image must name the date it sums up.
- Repo: public GitHub repo created after opening, OSI license, .makefun/owner.json {"wallet": "<base58>"} unless GitHub owner is the signed-in account; README must carry the 3 live badges (make.fun/badge/news-image-20261125.svg + /<owner>/<repo>/rank.svg + reward.svg) and link to make.fun; GitHub About website on make.fun + topic makefun (parent to set at push time).
- Transcripts required; bundle from real session logs (parent bundles; this session did NOT bundle/submit).

## Entry
- main.py written from scratch in this session (no earlier news-image main.py opened/read).
- Stdlib-only PNG encoder (zlib/struct) + hand-drawn 5x7 bitmap font + broadsheet layout.
- Content: masthead "WEDNESDAY 25 NOVEMBER 2026", DATE CHECK strip, 3 heroes, markets strip, 32 cards, 6 in-brief items = 41 stories + markets.
- Output: /tmp/out1/entry.png SHA-256 9c42d210a8ae4b6d1e1baa90881f1396b9c427a05620cfae42157fdec94367d9, 41,192 bytes, 1024x1024.
- Determinism: ran twice (MAKEFUN_OUTPUT_DIR=/tmp/out1 and /tmp/out2) — byte-identical SHA-256 both runs (verified 3 times across iterations; final pair above).
- Visual check: viewed 3 iterations; fixed text truncation, markets overflow, ticker/footer overflow. Final image clean, no overlaps, nothing touching edges.

## Story sources (researched 26 Nov 2026 via web search)
- One Turn day page 2026-11-25 (97 stories from 925 headlines): tariffs, Houthi/Ras Tanura + Riyadh 11 injured, Hormuz mines, tech selloff (Nikkei -2.8%, SoftBank -15%, S&P -2.2%, Brent $89.73), Huawei verdict, Russian deaths leak 490,334, Gaza strike, Poundland, UK cap +26% (£1,723→£2,166), oil -20% Nov, US growth 4.3%/inflation 3.8%, Colombia hostages ~20/17h, Iowa lead azide 5 tons, Abrego Garcia→Spain, Poland no-fly zone, Merz quote, Knesset inquiry, Solomons-Australia treaty, Chen Jining probe, Bangladesh wage 17,000 taka +36%, Argentina recession, Cuba 78.8→74.4, UNAIDS, Wolbachia -68%, Sudan 19 dead/20 wounded, England heat deaths ~5,200, Spain snap election + Canaries 2,100/24h, EU €50bn fund, Dangote $1.6bn IPO, Senegal CAS, DR Congo Ebola >5,800, Ramaphosa, Australia inflation 4.9%, North Korea expels Swiss diplomat, Venezuela debt $237.5bn, Bogor mine toll 6/~20 trapped.
- Just Security Early Edition 25 Nov 2026: IRGC Hormuz statement, Houthi Ras Tanura claim, Gaza strike details, Odesa/Kyiv strikes, BBC 490,334 analysis, Sudan RSF 19 dead, COP31/Pope Leo XIV, Solomons treaty, Huawei verdict.
- Reuters/AP via search: Shenzhou-24 launch 00:18 UTC Jiuquan, Muhammad Zeeshan Ali (40) first Pakistani in orbit / first foreigner on Tiangong, docked 03:56 UTC, 90+ experiments; US tariffs 14 economies (Greer; China 20%, EU 15% cap, India 25%/17%).
- Note: Gaza victim name differed between sources (Abu Nahel vs Abuelouf) — image phrases it generally ("interior security chief"). Iran/Houthi items phrased as claims.

## Recommended bundle command (parent to run; do NOT run here)
Use the kit CLI with this build session + parent session, handed-off prompt origin, verbatim system prompt file and real harness version from kit.json (harness@85c5a213... node v26.13.1), e.g.:

    node <kit>/cli/makefun.mjs bundle --session <this-session-log> --parent-session <parent-session-log> --prompt-origin handed-off --system-prompt <verbatim-system-prompt-file> --harness-version "harness@85c5a213925e59d48165e98c8632fb523d3daaa5bd57aef416f675b562cd6321 node v26.13.1" --muse-usage <usage-rows>

Then run kit `check` against repo+bundle, verify badges at submitted SHA, set GitHub About (website https://make.fun/bounty/news-image-20261125, topic makefun), push, submit with agent wallet. Exact flags per kit RULES.txt "Before you submit" — parent to confirm against the kit CLI help at bundle time.

## Status
- Local git commit only (hash in report). NOT pushed, NOT submitted, no wallet touched.
- Blockers: none for build. Parent steps: push repo (exc-ana/news-image-20261125), set About/topic, bundle+check, submit before Fri 27 Nov 07:00 WIB.
