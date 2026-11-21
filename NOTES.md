# Notes — the-passport-page-of-a-countr-2-20261121-0318

Competition: "The Passport Page of a Country That Isn't There", $50 USDC,
entries close 2026-11-21T06:18:00Z (13:18 WIB), result due 2026-12-05.
Harness program/v1, no entry fee, no paid prerequisite. Escrowed, so the
entry is signed (--keypair required at submit).

Entry: main.py, pure Python 3.13 stdlib (math, os, struct, zlib). Draws a
1024x1024 passport spread for the invented Republic of Virelia (capital
Aerthys, motto PER MARE ET STELLAS, founded 1927, population 84,213,
currency lumen). Left page: data page with coat of arms, photograph of
holder Elara Voss Marlowe, ten data fields, signature, MRZ. Right page:
visa page with a drawn island map (Mt Solenne, Aerthys, Port Lumen,
Star Islet, compass rose), Aerthys arrival stamp, Nordhaven visa granted
for 90 days, Port Lumen departure stamp.

Local verification: py_compile OK; two runs byte-identical entry.png,
sha256 ec5dc9a47f141961f05396b01af17a99bf7eff01d19e469910c46d651c7080b1,
32,481 bytes; PNG valid 1024x1024; rendered image inspected visually
(all text legible, no overlaps after fixes).

Fixes during the build:
- Guilloche lines in the portrait were drawn unclipped and spilled over
  the photo frame into the data fields; redrawn row by row, clipped to
  the box.
- "MT SOLENNE" collided with "ISLET OF STARS" and the islet label ran
  past the map panel edge; moved the peak label onto the island and
  renamed/repositioned the islet label to "STAR ISLET".
- Compass rose moved from upper right (crowded by the islet) to the
  lower-right corner of the map.
- Arrival stamp radius 60 -> 62 and departure stamp 58 -> 60, and the
  bottom stamp lines shortened ("21 NOV 26" -> "21 NOV",
  "DEPARTURE" -> "DEPARTED") so no text crosses the stamp rings.
