# Appendix 07 | Verification report

**Scope:** Tables P7-2-1, P7-3-1, P7-3-2 transcribed from two photographs supplied by the user.

**Status:** `checked_against_photos_and_arithmetic`; final owner approval and full-text code compliance review are still pending.

## Checks performed

| Table | Rows | Source-photo transcription review | Arithmetic checks |
|---|---:|---|---|
| P7-2-1 | 5 | Reviewed all six columns against photograph | Area ft²→m² and gpm→L/s, allowing printed rounding |
| P7-3-1 | 8 | Reviewed three pairs of slope columns against photograph | Capacity generally increases with diameter and slope |
| P7-3-2 | 8 | Reviewed three pairs of slope columns against photograph | Flow approximately equals roof area × 0.0254 m/h ÷ 3.6 (L/s), allowing printed rounding |

**Automated arithmetic result:** no discrepancies exceeding configured tolerance in P7-2-1 (area tolerance max(2 m², 0.2%), flow tolerance 0.25 L/s) or P7-3-2 (flow tolerance max(0.15 L/s, 1.5%)). These are *quality-control tolerances*, not design tolerances.

## Engineering safeguards

1. All three tables use **25.4 mm/h** rainfall intensity.
2. Horizontal pipe sizing requires a slope; vertical downpipe sizing does not use the horizontal-pipe slope table.
3. Nominal inch and mm sizes must be selected from the source table, not computed by exact unit conversion.
4. Roof areas must be assigned to the specific drainage segment, not indiscriminately to every pipe.
5. No extrapolation or automatic interpolation outside tabulated conditions without confirming the applicable text provisions.
6. Table values are preserved as printed, including rounding; arithmetic verification is not a license to silently rewrite the source.

**Important:** Arithmetic agreement and visual review do not independently establish that the table is legally applicable to a given project or edition. Final approval requires checking the surrounding appendix text and user acceptance.
