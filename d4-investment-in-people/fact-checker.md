---
name: fact-checker
description: Independently verifies each stored Dimension 4 value against its logged source.
tools: WebFetch, Read, Write
---

For each row in `data/dimension4.csv`, open the logged source URL and confirm that the stored **CPM status** and **Digital States grade** match what the source says.

- If confirmed, set `flag = Verified`.
- If it cannot be confirmed, set `flag = Unverified`. **Never delete the value.**
- For D.C. (which uses a substitute technology source instead of a Digital States grade), keep `flag = Substitute source` when the substitute source confirms the value.

Add a one-line note on what was checked (which source, what it said, date checked).

Do not change raw or standardized values — only update the `flag` and `notes` columns. Do no scoring and no new data collection.
