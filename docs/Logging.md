# Logging

## Strategy
- Every entry point funnels through the shared `readme_automation` logger, configured via `configure_logging()` in `prototype.py`.
- Log levels: `DEBUG` (diagnostics, e.g., file scans), `INFO` (milestones like README writes), `WARNING` (fallback behaviour), `ERROR` (OpenAI/Git failures), `CRITICAL` (missing credentials).
- Runtime level is controlled with the `LOG_LEVEL` env var. It defaults to `DEBUG` on CI for maximum visibility and `INFO` elsewhere.
- External streaming is suppressed whenever `CI` is truthy so automated runs stay local.

## Framework
- Base framework: Python's stdlib `logging` module with a custom configuration helper.
- Real-time streaming handler: Custom `BetterStackHandler` class (lines 22-57) that sends logs directly to Better Stack's ingestion API using HTTP POST requests. The handler formats logs as JSON with timestamps, log levels, and messages, matching Better Stack's expected format.
- The handler uses the `requests` library to POST logs to the Better Stack endpoint when `LOGTAIL_SOURCE_TOKEN` is provided.
- Dependencies are tracked in `requirements.txt`; the handler automatically enables when the token is present and `CI` is not set.

## Monitoring Console
- Console: [Better Stack Logtail](https://betterstack.com/logs/). The source is configured to receive logs at the ingestion endpoint `https://s1597068.eu-nbg-2.betterstackdata.com`.
- Dashboard URL: Access your Better Stack dashboard to view logs in real-time. Share the dashboard URL and credentials via Brightspace as required.
- Token wiring: set `LOGTAIL_SOURCE_TOKEN=<source_token>` in local environment or hosting provider secrets; leave it unset in CI to honour the "no CI ingestion" rule.
- Log ingestion happens in real time via HTTP POST requests; expect events to surface within one second of emission.

## CI Configuration
- `.github/workflows/main.yml` exports `LOG_LEVEL=DEBUG`, ensuring the test job shows the most verbose stream.
- Because `CI` is automatically set by GitHub Actions, no external streaming occurs during CI runs, keeping the monitoring console focused on runtime environments.
- Latest CI Run Permalink (showing DEBUG logs from "Run prototype.py to demonstrate logging" step):
  - https://github.com/CSCI-40500-Fall-2025/project-project-15/actions/runs/19511577678/job/55852405236

## Reference Links
- Framework config (BetterStackHandler class and configure_logging function): https://github.com/CSCI-40500-Fall-2025/project-project-15/blob/37a0359f7e63db390b581650fffd00a8ef9599c2/prototype.py#L22-L99

- Critical credential validation (CRITICAL level): https://github.com/CSCI-40500-Fall-2025/project-project-15/blob/37a0359f7e63db390b581650fffd00a8ef9599c2/prototype.py#L112

- README generation lifecycle (INFO/ERROR levels): https://github.com/CSCI-40500-Fall-2025/project-project-15/blob/37a0359f7e63db390b581650fffd00a8ef9599c2/prototype.py#L120-L176

- File scanning + commit ingestion (DEBUG/INFO/WARNING levels): https://github.com/CSCI-40500-Fall-2025/project-project-15/blob/37a0359f7e63db390b581650fffd00a8ef9599c2/prototype.py#L181-L258

- Output lifecycle (DEBUG/INFO levels): https://github.com/CSCI-40500-Fall-2025/project-project-15/blob/37a0359f7e63db390b581650fffd00a8ef9599c2/prototype.py#L278-L282

## Submission Checklist
1. Capture a recent GitHub Actions run URL after pushing these changes; confirm the logs show `DEBUG` statements. (Link provided above)
2. Copy the four reference links above into GitHub wiki → "Logging" page as permalinks (use "View file" → "Copy permalink" once the commit is on GitHub to replace the paths if needed).
3. Add the monitoring console URL plus credential instructions on the wiki; double-check that CI logs are absent from the console's stream.
4. Submit the wiki URL and console credentials on Brightspace per the assignment brief.
