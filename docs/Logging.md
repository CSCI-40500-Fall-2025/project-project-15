# Logging

## Strategy
- Every entry point funnels through the shared `readme_automation` logger, configured via `configure_logging()` in `prototype.py`.
- Log levels: `DEBUG` (diagnostics, e.g., file scans), `INFO` (milestones like README writes), `WARNING` (fallback behaviour), `ERROR` (OpenAI/Git failures), `CRITICAL` (missing credentials).
- Runtime level is controlled with the `LOG_LEVEL` env var. It defaults to `DEBUG` on CI for maximum visibility and `INFO` elsewhere.
- External streaming is suppressed whenever `CI` is truthy so automated runs stay local.

## Framework
- Base framework: Python’s stdlib `logging` module with a custom configuration helper.
- Real-time streaming handler: [`logtail-python`](https://pypi.org/project/logtail-python/) which pushes every structured record to the Logtail API when `LOGTAIL_SOURCE_TOKEN` is provided.
- Dependencies are tracked in `requirements.txt`; installing the project automatically enables the handler when the token is present.

## Monitoring Console
- Console: [Better Stack Logtail](https://betterstack.com/logs/). Create a source named “README Automation” and store the generated token in a secrets manager.
- URL pattern: `https://betterstack.com/logs/team/<team-id>/source/<source-id>`. Replace `<team-id>`/`<source-id>` with the values from your workspace and share credentials via Brightspace as required.
- Token wiring: set `LOGTAIL_SOURCE_TOKEN=<source_token>` in local `.env` or hosting provider secrets; leave it unset in CI to honour the “no CI ingestion” rule.
- Log tailing happens in real time; expect events to surface within one second of emission.

## CI Configuration
- `.github/workflows/main.yml` exports `LOG_LEVEL=DEBUG`, ensuring the test job shows the most verbose stream.
- Because `CI` is automatically set by GitHub Actions, no external streaming occurs during CI runs, keeping the monitoring console focused on runtime environments.
- Provide a permalink to the latest successful run (Actions → workflow run → copy URL) when submitting the deliverable.

## Reference Links
- Framework config: `prototype.py#L14-L55`
- Critical credential validation: `prototype.py#L61-L71`
- README generation lifecycle (INFO/ERROR): `prototype.py#L73-L135`
- File scanning + commit ingestion (DEBUG/INFO/WARNING): `prototype.py#L137-L212`
- Output lifecycle (DEBUG/INFO): `prototype.py#L218-L236`

## Submission Checklist
1. Capture a recent GitHub Actions run URL after pushing these changes; confirm the logs show `DEBUG` statements.
2. Copy the four reference links above into GitHub wiki → “Logging” page as permalinks (use “View file” → “Copy permalink” once the commit is on GitHub to replace the paths).
3. Add the monitoring console URL plus credential instructions on the wiki; double-check that CI logs are absent from the console’s stream.
4. Submit the wiki URL and console credentials on Brightspace per the assignment brief.

