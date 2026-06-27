# Coding Task A: Read/Write Classification (100 tools)

You are an independent second coder. For each tool below, read the name,
description, and source excerpt, then decide whether the tool is **read** or
**write** using the single decision rule:

**Persistent-effect rule**: if calling the tool twice produces a different world
state than not calling it at all, AND that effect survives process termination,
classify it as **write**. Otherwise classify it as **read**. If there is
genuinely not enough context to decide, use **unknown** (use sparingly).

- **read**  -- retrieves, queries, searches, lists, previews, validates; no persistent state change.
- **write** -- creates, modifies, deletes, executes, sends, saves; any persistent state change.
- **unknown** -- insufficient context.

For each tool, type your answer on the `ANSWER:` line directly beneath it, and any
notes on the `NOTES:` line. Edit this same file and send it back -- one file, no
spreadsheet. Code only from what you see here; do not look for the project's own labels.

---

## 1. `whats_new`

**Server**: model-advisor-mcp (`Semicolon-D/model-advisor-mcp`)
**Description**: Discover recently added AI models. Answers

Source: `src/server.ts:138`

```typescript
     136:   },
     137:   {
>>>  138:     name: "whats_new",
     139:     description:
     140:       'Discover recently added AI models. Answers "what new models dropped this week?" Filter by time window and category.',
     141:     inputSchema: {
     142:       type: "object" as const,
     143:       properties: {
     144:         since: {
     145:           type: "string",
     146:           description:
     147:             'Time window: "24h", "7d" (default), "14d", "30d", "4w"',
     148:         },
     149:         category: {
     150:           type: "string",
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 2. `cc_diff_files`

**Server**: ellmos-codecommander-mcp (`ellmos-ai/ellmos-codecommander-mcp`)

Source: `src/index.ts:2102`

```typescript
    2100: // ============================================================================
    2101: 
>>> 2102: server.registerTool(
    2103:   "cc_diff_files",
    2104:   {
    2105:     title: "Diff Files",
    2106:     description: t().cc_diff_files.description,
    2107:     inputSchema: {
    2108:       file_a: z.string().min(1).describe("Path to first file"),
    2109:       file_b: z.string().min(1).describe("Path to second file"),
    2110:       context_lines: z.number().int().min(0).max(20).default(3).describe("Number of context lines (default: 3)")
    2111:     },
    2112:     annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false }
    2113:   },
    2114:   async (params) => {
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 3. `subscribe_feed`

**Server**: feedkit (`QuartzUnit/feedkit`)
**Description**: Subscribe to an RSS feed for ongoing collection.

Source: `feedkit/mcp_server.py:132`

```python
     130: 
     131: 
>>>  132: @mcp.tool()
     133: def subscribe_feed(url: str, title: str = "", category: str = "") -> str:
     134:     """Subscribe to an RSS feed for ongoing collection.
     135: 
     136:     Args:
     137:         url: RSS/Atom feed URL.
     138:         title: Display title (optional).
     139:         category: Category label (optional).
     140:     """
     141:     store = _get_store()
     142:     store.subscribe(url, title=title, category=category)
     143:     return json.dumps({"status": "subscribed", "url": url})
     144: 
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 4. `get_reservation`

**Server**: mcp-southwest (`markswendsen-code/mcp-southwest`)
**Description**: Look up an existing Southwest reservation by confirmation number and passenger name. Returns flight details, fare type,

Source: `src/index.ts:128`

```typescript
     126:   },
     127:   {
>>>  128:     name: "get_reservation",
     129:     description:
     130:       "Look up an existing Southwest reservation by confirmation number and passenger name. Returns flight details, fare type, and booking status.",
     131:     inputSchema: zodToJsonSchema(getReservationSchema),
     132:   },
     133:   {
     134:     name: "change_flight",
     135:     description:
     136:       "Modify an existing Southwest booking. Southwest never charges change fees — you only pay/receive credit for fare differences.",
     137:     inputSchema: zodToJsonSchema(changeFlightSchema),
     138:   },
     139:   {
     140:     name: "cancel_flight",
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 5. `get_device_status`

**Server**: wemo-mcp-server (`apiarya/wemo-mcp-server`)
**Description**: Get the current status of a WeMo device.

Source: `src/wemo_mcp_server/server.py:680`

```python
     678: 
     679: 
>>>  680: @mcp.tool()
     681: async def get_device_status(device_identifier: str) -> dict[str, Any]:
     682:     """Get the current status of a WeMo device.
     683: 
     684:     Retrieves the current state and information for a device by name or IP address.
     685:     The device must have been discovered via scan_network first.
     686: 
     687:     Args:
     688:     ----
     689:         device_identifier: Device name (e.g., "Office Light") or IP address (e.g., "192.168.1.100")
     690: 
     691:     Returns:
     692:     -------
     693:         Dictionary containing:
     694:         - device_name: Name of the device
     695:         - state: Current state ("on" or "off")
     696:         - Additional device information
     697: 
     698:     """
     699:     # Validate input
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 6. `show_toast`

**Server**: uiautomator2-mcp-server (`tanbro/uiautomator2-mcp-server`)
**Description**: Display a Toast message on the Android device.

Source: `src/u2mcp/tools/toast.py:37`

```python
      35: 
      36: 
>>>   37: @mcp.tool("show_toast", tags={"toast:action"})
      38: async def show_toast(serial: str, text: str, duration: float = 1.0):
      39:     """Display a Toast message on the Android device.
      40: 
      41:     Args:
      42:         serial (str): Android device serial number.
      43:         text (str): The message text to display in the Toast.
      44:         duration (float): Display duration in seconds (default: 1.0).
      45:     """
      46:     async with get_device(serial) as device:
      47:         await to_thread.run_sync(lambda: device.toast.show(text, duration))
      48: 
      49: 
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 7. `preview_raw`

**Server**: rawtherapee-mcp-server (`lucamarien/rawtherapee-mcp-server`)

Source: `src/rawtherapee_mcp/server.py:625`

```python
     623: 
     624: 
>>>  625: @mcp.tool()
     626: async def preview_raw(
     627:     ctx: Context,
     628:     file_path: str,
     629:     profile_path: str | None = None,
     630:     max_width: int | None = None,
     631:     return_image: bool = True,
     632: ) -> dict[str, Any] | ToolResult:
     633:     """Generate a small preview JPEG for visual analysis.
     634: 
     635:     Use this to create a quick preview of how a RAW file will look with
     636:     specific processing settings. The preview is a small JPEG suitable for
     637:     visual inspection of composition, exposure, and color. When return_image
     638:     is True, the preview image is returned inline for the LLM to see.
     639:     Params: file_path, profile_path, max_width, return_image
     640:     """
     641:     config = get_config(ctx)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 8. `analyze_jira_issues`

**Server**: jira-cloud (`aaronsb/jira-cloud`)
**Description**: Compute project metrics over issues selected by JQL or a saved filter. For counting and breakdown questions (

Source: `src/schemas/tool-schemas.ts:367`

```typescript
     365: 
     366:   analyze_jira_issues: {
>>>  367:     name: 'analyze_jira_issues',
     368:     description: 'Compute project metrics over issues selected by JQL or a saved filter. For counting and breakdown questions ("how many by status/assignee/priority"), use metrics: ["summary"] with groupBy — this gives exact counts with no issue cap. Use detail metrics (points, time, schedule, cycle, distribution) for per-issue analysis (capped at maxResults). Use flow for status transition patterns — how issues move through statuses, where they bounce, and how long they stay. Tip: save complex JQL as a filter with manage_jira_filter, then reuse the filterId here for repeated analysis. Read jira://analysis/recipes for composition patterns.',
     369:     inputSchema: {
     370:       type: 'object',
     371:       properties: {
     372:         jql: {
     373:           type: 'string',
     374:           description: 'JQL query selecting the issues to analyze. Either jql, filterId, or dataRef is required (dataRef > filterId > jql precedence). Examples: "project in (AA, GC, LGS)", "sprint in openSprints()", "assignee = currentUser() AND resolution = Unresolved".',
     375:         },
     376:         filterId: {
     377:           type: 'string',
     378:           description: 'ID of a saved Jira filter to use as the query source. The filter\'s JQL is resolved automatically. Use this to run different analyses against a saved query without repeating the JQL. Create filters with manage_jira_filter.',
     379:         },
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 9. `zen_scroll`

**Server**: zen-mcp (`sh6drack/zen-mcp`)
**Description**: Scroll the page or scroll an element into view

Source: `server.mjs:511`

```javascript
     509:   },
     510:   {
>>>  511:     name: 'zen_scroll',
     512:     description: 'Scroll the page or scroll an element into view',
     513:     inputSchema: {
     514:       type: 'object',
     515:       properties: {
     516:         direction: { type: 'string', enum: ['up', 'down', 'top', 'bottom'] },
     517:         amount: { type: 'number', description: 'Pixels (default: 500)' },
     518:         selector: { type: 'string', description: 'Element to scroll into view' },
     519:       },
     520:     },
     521:   },
     522:   {
     523:     name: 'zen_wait',
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 10. `remove_background`

**Server**: mcp-server-bedrock-image (`Yaksh36/mcp-server-bedrock-image`)

Source: `src/mcp_server_bedrock_image/server.py:144`

```python
     142: 
     143: 
>>>  144: @mcp.tool(name="remove_background")
     145: async def tool_remove_background(
     146:     image_path: str = Field(description="Path to the image file"),
     147:     filename: Optional[str] = Field(default=None, description="Output filename"),
     148:     output_dir: Optional[str] = Field(
     149:         default=None, description="Override output directory"
     150:     ),
     151: ) -> dict:
     152:     """Remove the background from an image."""
     153:     image_b64 = _read_image_as_b64(image_path)
     154:     body = build_remove_background_body(image=image_b64)
     155:     response = _get_bedrock().invoke_model(
     156:         model_id=MODELS["remove_background"], body=body
     157:     )
     158:     images, _ = parse_generate_response(response)
     159:     out = output_dir or _output_dir()
     160:     paths = [save_image(img, output_dir=out, filename=filename) for img in images]
     161:     return {"status": "success", "paths": paths}
     162: 
     163: 
     164: @mcp.tool(name="style_transfer")
     165: async def tool_style_transfer(
     166:     prompt: str = Field(description="Description of desired output"),
     167:     image_path: str = Field(description="Path to the source image"),
     168:     style_image_path: str = Field(description="Path to the style reference image"),
     169:     negative_prompt: Optional[str] = Field(default=None, description="What to exclude"),
     170:     filename: Optional[str] = Field(default=None, description="Output filename"),
     171:     output_dir: Optional[str] = Field(
     172:         default=None, description="Override output directory"
     173:     ),
     174: ) -> dict:
     175:     """Apply the style of a reference image to a source image."""
     176:     image_b64 = _read_image_as_b64(image_path)
     177:     style_b64 = _read_image_as_b64(style_image_path)
     178:     body = build_style_transfer_body(
     179:         prompt=prompt,
     180:         image=image_b64,
     181:         style_image=style_b64,
     182:         negative_prompt=negative_prompt,
     183:     )
     184:     response = _get_bedrock().invoke_model(model_id=MODELS["style_transfer"], body=body)
     185:     images, _ = parse_generate_response(response)
     186:     out = output_dir or _output_dir()
     187:     paths = [save_image(img, output_dir=out, filename=filename) for img in images]
     188:     return {"status": "success", "paths": paths}
     189: 
     190: 
     191: @mcp.tool(name="search_and_recolor")
     192: async def tool_search_and_recolor(
     193:     image_path: str = Field(description="Path to the image file"),
     194:     prompt: str = Field(description="Description of the scene"),
     195:     select_prompt: str = Field(description="What to select for recoloring"),
     196:     recolor_prompt: str = Field(
     197:         description="New color/appearance for the selected element"
     198:     ),
     199:     filename: Optional[str] = Field(default=None, description="Output filename"),
     200:     output_dir: Optional[str] = Field(
     201:         default=None, description="Override output directory"
     202:     ),
     203: ) -> dict:
     204:     """Recolor specific elements in an image."""
     205:     image_b64 = _read_image_as_b64(image_path)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 11. `manage_workspace`

**Server**: jira-cloud (`aaronsb/jira-cloud`)
**Description**: Manage files in the local workspace staging area (local only — no Jira impact). Files downloaded via manage_jira_media l

Source: `src/schemas/tool-schemas.ts:542`

```typescript
     540: 
     541:   manage_workspace: {
>>>  542:     name: 'manage_workspace',
     543:     description: 'Manage files in the local workspace staging area (local only — no Jira impact). Files downloaded via manage_jira_media land here. Delete only removes the local copy. Use manage_jira_media to affect attachments on Jira issues.',
     544:     inputSchema: {
     545:       type: 'object',
     546:       properties: {
     547:         operation: {
     548:           type: 'string',
     549:           enum: ['list', 'read', 'write', 'delete', 'mkdir', 'move'],
     550:           description: 'Operation to perform. list: show staged files. read: display file content. write: stage base64 content. delete: remove local file only (does not affect Jira). mkdir: create directory. move: rename/relocate file.',
     551:         },
     552:         filename: {
     553:           type: 'string',
     554:           description: 'Filename or path within workspace. Supports nesting with / separators.',
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 12. `create_task`

**Server**: Dida365MCP (`evalor/Dida365MCP`)
**Description**: Create one or more tasks in a project. Supports batch creation.

Source: `src/tools/task/create-task.ts:43`

```typescript
>>>   43:     server.registerTool(
      44:         "create_task",
      45:         {
      46:             title: "Create Task(s)",
      47:             description: `Create one or more tasks in a project. Supports batch creation.
      48:
      49: WHEN TO USE:
      50: - Add new tasks to a project or inbox
      51: - Create tasks with due dates, priorities, reminders
      52: - Create tasks with sub-tasks
      53:
      54: REQUIRED (per task):
      55: - title: Task name
      56: - projectId: Target project ID, or "inbox" for inbox`,
      57:             inputSchema: TaskInputSchema,
      58:         },
      59:         async (args) => {
      60:             const input = TaskInputSchema.parse(args);
      61:             // ... creates task via API
      62:         }
      63:     );
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 13. `validate_config`

**Server**: oh-my-posh (`JanDeDobbeleer/oh-my-posh`)
**Description**: Validate an oh-my-posh configuration against the schema

Source: `website/api/mcp/index.js:25`

```javascript
      23:         tools: [
      24:           {
>>>   25:             name: 'validate_config',
      26:             description: 'Validate an oh-my-posh configuration against the schema',
      27:             inputSchema: {
      28:               type: 'object',
      29:               properties: {
      30:                 content: {
      31:                   type: 'string',
      32:                   description: 'The configuration content as a string (JSON, YAML, or TOML)'
      33:                 },
      34:                 format: {
      35:                   type: 'string',
      36:                   enum: ['json', 'yaml', 'toml', 'auto'],
      37:                   description: 'The format of the configuration (auto-detect if not specified)',
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 14. `process_raw`

**Server**: rawtherapee-mcp-server (`lucamarien/rawtherapee-mcp-server`)

Source: `src/rawtherapee_mcp/server.py:556`

```python
     554: 
     555: 
>>>  556: @mcp.tool()
     557: async def process_raw(
     558:     ctx: Context,
     559:     file_path: str,
     560:     profile_path: str,
     561:     output_format: str = "jpeg",
     562:     output_path: str | None = None,
     563:     jpeg_quality: int | None = None,
     564:     bit_depth: int = 16,
     565:     include_preview: bool = True,
     566:     preview_max_width: int = 600,
     567: ) -> dict[str, Any] | ToolResult:
     568:     """Process a RAW file with a PP3 processing profile.
     569: 
     570:     Use this to convert a RAW file to JPEG, TIFF, or PNG using a PP3 profile.
     571:     The profile controls all processing parameters (exposure, white balance,
     572:     sharpening, etc.). Returns an inline thumbnail when include_preview is True.
     573:     Params: file_path, profile_path, output_format, output_path, jpeg_quality, bit_depth,
     574:     include_preview, preview_max_width
     575:     """
     576:     config = get_config(ctx)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 15. `pg_extension_list`

**Server**: mcp-postgres (`itunified-io/mcp-postgres`)
**Description**: List installed PostgreSQL extensions with versions.

Source: `src/tools.ts:188`

```typescript
     186:   },
     187:   {
>>>  188:     name: "pg_extension_list",
     189:     description: "List installed PostgreSQL extensions with versions.",
     190:     inputSchema: { target },
     191:     domain: "pg",
     192:     action: "schema extensions",
     193:   },
     194: 
     195:   // ── CRUD (4 tools) ──────────────────────────────────────────────────
     196:   {
     197:     name: "pg_insert",
     198:     description: "Insert one or more rows into a table. Returns inserted rows.",
     199:     inputSchema: {
     200:       target,
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 16. `pivot_table`

**Server**: csv-analytics-mcp (`CSOAI-ORG/csv-analytics-mcp`)
**Description**: Create a pivot table from a dataset. Reshapes data by grouping rows

Source: `server.py:562`

```python
     560: 
     561: 
>>>  562: @mcp.tool()
     563: def pivot_table(name: str, index: str, columns: str, values: str,
     564:                 aggfunc: str = "mean", api_key: str = "") -> dict:
     565:     """Create a pivot table from a dataset. Reshapes data by grouping rows
     566:     and spreading column values, similar to Excel pivot tables.
     567: 
     568:     Args:
     569:         name: Dataset name (from load_csv)
     570:         index: Column to use as row labels
     571:         columns: Column whose unique values become new columns
     572:         values: Column to aggregate
     573:         aggfunc: Aggregation function (mean, sum, count, min, max, median, std)
     574: 
     575:     Behavior:
     576:         This tool generates structured output without modifying external systems.
     577:         Output is deterministic for identical inputs. No side effects.
     578:         Free tier: 10/day rate limit. Pro tier: unlimited.
     579:         No authentication required for basic usage.
     580: 
     581:     When to use:
     582:         Use this tool when you need structured analysis or classification
     583:         of inputs against established frameworks or standards.
     584: 
     585:     When NOT to use:
     586:         Not suitable for real-time production decision-making without
     587:         human review of results.
     588:     Behavioral Transparency:
     589:         - Side Effects: This tool is read-only and produces no side effects. It does not modify
     590:           any external state, databases, or files. All output is computed in-memory and returned
     591:           directly to the caller.
     592:         - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
     593:           require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
     594:         - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
     595:           included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
     596:         - Error Handling: Returns structured error objects with 'error' key on failure.
     597:           Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
     598:         - Idempotency: Fully idempotent — calling with the same inputs always produces the
     599:           same output. Safe to retry on timeout or transient failure.
     600:         - Data Privacy: No input data is stored, logged, or transmitted to external services.
     601:           All processing happens locally within the MCP server process.
     602:     """
     603:     allowed, msg, tier = check_access(api_key)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 17. `start_scrcpy`

**Server**: uiautomator2-mcp-server (`tanbro/uiautomator2-mcp-server`)
**Description**: Startup scrcpy in background and returns process id.

Source: `src/u2mcp/tools/scrcpy.py:20`

```python
      18: 
      19: 
>>>   20: @mcp.tool("start_scrcpy", tags={"screen:mirror"})
      21: async def start_scrcpy(serial: str = "", timeout: float = 5.0) -> int:
      22:     """Startup scrcpy in background and returns process id.
      23: 
      24:     scrcpy is an application mirrors Android devices (video and audio) connected via USB or TCP/IP and allows control using the computer's keyboard and mouse.
      25: 
      26:     The scrcpy process will run in the background after successful startup.
      27:     Use stop_scrcpy to terminate the process.
      28: 
      29:     Args:
      30:         serial (str): Android device serialno. If empty string, connects to the unique device if only one device is connected.
      31:         timeout (float): Seconds to wait for process to confirm startup.
      32:             If process is still running after this time, startup is considered successful.
      33: 
      34:     Returns:
      35:         int: process id (pid)
      36:     """
      37: 
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 18. `get_prices`

**Server**: merx-mcp (`Hovsteder/merx-mcp`)
**Description**: Get current energy and bandwidth prices from all Merx providers, sorted by best (minimum) price across all duration tier

Source: `src/tools/prices.ts:15`

```typescript
      13: 
      14: const getPrices: McpTool = {
>>>   15:   name: 'get_prices',
      16:   description: 'Get current energy and bandwidth prices from all Merx providers, sorted by best (minimum) price across all duration tiers. Each provider lists ALL its duration tiers (5min/1h/1d/7d/30d etc) — short rentals are usually more expensive per unit than long ones, so always check tier-by-tier. Optionally filter by exact duration in seconds. No auth required.',
      17:   inputSchema: {
      18:     type: 'object',
      19:     properties: {
      20:       resource: {
      21:         type: 'string',
      22:         enum: ['ENERGY', 'BANDWIDTH'],
      23:         description: 'Filter by resource type. Omit for all.',
      24:       },
      25:       duration: {
      26:         type: 'number',
      27:         description: 'Filter to providers offering this exact duration in seconds (e.g. 3600 for 1h, 86400 for 1d, 604800 for 7d, 2592000 for 30d). Omit to see all tiers.',
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 19. `zen_list_pages`

**Server**: zen-mcp (`sh6drack/zen-mcp`)
**Description**: List all open pages/tabs in Zen browser with URLs and titles

Source: `server.mjs:383`

```javascript
     381: const TOOLS = [
     382:   {
>>>  383:     name: 'zen_list_pages',
     384:     description: 'List all open pages/tabs in Zen browser with URLs and titles',
     385:     inputSchema: { type: 'object', properties: {} },
     386:   },
     387:   {
     388:     name: 'zen_select_page',
     389:     description: 'Select a page/tab by index (from zen_list_pages) as the active target',
     390:     inputSchema: {
     391:       type: 'object',
     392:       properties: { index: { type: 'number', description: 'Page index' } },
     393:       required: ['index'],
     394:     },
     395:   },
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 20. `cc_regex_test`

**Server**: ellmos-codecommander-mcp (`ellmos-ai/ellmos-codecommander-mcp`)

Source: `src/index.ts:2169`

```typescript
    2167: // ============================================================================
    2168: 
>>> 2169: server.registerTool(
    2170:   "cc_regex_test",
    2171:   {
    2172:     title: "Regex Tester",
    2173:     description: t().cc_regex_test.description,
    2174:     inputSchema: {
    2175:       pattern: z.string().min(1).describe("Regular expression pattern"),
    2176:       flags: z.string().default('g').describe("Regex flags (g, i, m, s, u)"),
    2177:       text: z.string().optional().describe("Text to test against (or use file_path)"),
    2178:       file_path: z.string().optional().describe("File to test against (alternative to text)"),
    2179:       replace_with: z.string().optional().describe("Optional replacement string")
    2180:     },
    2181:     annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false }
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 21. `preview_with_adjustments`

**Server**: rawtherapee-mcp-server (`lucamarien/rawtherapee-mcp-server`)

Source: `src/rawtherapee_mcp/server.py:2428`

```python
    2426: 
    2427: 
>>> 2428: @mcp.tool()
    2429: async def preview_with_adjustments(
    2430:     ctx: Context,
    2431:     file_path: str,
    2432:     profile_path: str,
    2433:     max_width: int = 600,
    2434:     include_histogram: bool = False,
    2435: ) -> dict[str, Any] | ToolResult:
    2436:     """Preview a RAW file with all active local adjustments applied.
    2437: 
    2438:     Renders a preview JPEG using RT CLI with the full profile including
    2439:     Locallab spots. Optionally includes histogram statistics for the
    2440:     processed result. Use this after add_luminance_adjustment or
    2441:     apply_local_preset to verify the effect visually.
    2442: 
    2443:     Params: file_path, profile_path, max_width, include_histogram
    2444:     """
    2445:     config = get_config(ctx)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 22. `add_route`

**Server**: next2d-development-mcp (`Next2D/next2d-development-mcp`)

Source: `src/tools/addRoute.ts:5`

```typescript
       3: 
       4: export function registerAddRoute(server: McpServer): void {
>>>    5:     server.registerTool(
       6:         "add_route",
       7:         {
       8:             "description":
       9:                 "Generate a route entry for routing.json. " +
      10:                 "Supports request types: json, content, custom, cluster. " +
      11:                 "The route key becomes the URL path and determines the View class name (CamelCase).",
      12:             "inputSchema": {
      13:                 "path": z.string().describe(
      14:                     "Route path (e.g. 'home', 'quest/list'). " +
      15:                     "Becomes URL path and View class name in CamelCase."
      16:                 ),
      17:                 "requests": z
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 23. `screen_record_start`

**Server**: uiautomator2-mcp-server (`tanbro/uiautomator2-mcp-server`)
**Description**: Start screen recording to file. Runs in background, use screen_record_stop to stop.

Source: `src/u2mcp/tools/screenrecord.py:17`

```python
      15: 
      16: 
>>>   17: @mcp.tool("screen_record_start", tags={"screen:record"})
      18: async def screen_record_start(serial: str, file: str, duration: float) -> str:
      19:     """Start screen recording to file. Runs in background, use screen_record_stop to stop.
      20: 
      21:     Args:
      22:         serial (str): Android device serial number.
      23:         file (str): Output file path for the recording.
      24:         duration (float): Maximum recording duration in seconds.
      25: 
      26:     Returns:
      27:         str: Output file path.
      28:     """
      29:     task_group = get_background_task_group()
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 24. `preview_lut`

**Server**: rawtherapee-mcp-server (`lucamarien/rawtherapee-mcp-server`)

Source: `src/rawtherapee_mcp/server.py:2806`

```python
    2804: 
    2805: 
>>> 2806: @mcp.tool()
    2807: async def preview_lut(
    2808:     ctx: Context,
    2809:     file_path: str,
    2810:     lut_name: str,
    2811:     base_profile: str | None = None,
    2812:     strength: int = 100,
    2813:     max_width: int = 600,
    2814: ) -> dict[str, Any] | ToolResult:
    2815:     """Render an inline preview of a RAW file with a HaldCLUT film simulation applied.
    2816: 
    2817:     Optionally merges onto an existing PP3 base_profile so WB, exposure, etc.
    2818:     are preserved. Returns an inline thumbnail image.
    2819:     Params: file_path, lut_name, base_profile (optional PP3 path), strength (0-100), max_width
    2820:     """
    2821:     config = get_config(ctx)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 25. `aggregate`

**Server**: csv-analytics-mcp (`CSOAI-ORG/csv-analytics-mcp`)
**Description**: Aggregate data with GROUP BY and compute metrics.

Source: `server.py:468`

```python
     466: 
     467: 
>>>  468: @mcp.tool()
     469: def aggregate(name: str, group_by: list[str], metrics: dict[str, str], api_key: str = "") -> dict:
     470:     """Aggregate data with GROUP BY and compute metrics.
     471: 
     472:     Supported aggregation functions: sum, mean, min, max, count, median, std, first, last, nunique
     473: 
     474:     Args:
     475:         name: Dataset name (from load_csv)
     476:         group_by: List of columns to group by (e.g. ["department", "year"])
     477:         metrics: Dict of column -> aggregation function (e.g. {"salary": "mean", "id": "count"})
     478: 
     479:     Behavior:
     480:         This tool is read-only and stateless — it produces analysis output
     481:         without modifying any external systems, databases, or files.
     482:         Safe to call repeatedly with identical inputs (idempotent).
     483:         Free tier: 10/day rate limit. Pro tier: unlimited.
     484:         No authentication required for basic usage.
     485: 
     486:     When to use:
     487:         Use this tool when you need structured analysis or classification
     488:         of inputs against established frameworks or standards.
     489: 
     490:     When NOT to use:
     491:         Not suitable for real-time production decision-making without
     492:         human review of results.
     493:     """
     494:     allowed, msg, tier = check_access(api_key)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 26. `get_cache_info`

**Server**: wemo-mcp-server (`apiarya/wemo-mcp-server`)
**Description**: Get information about the persistent device cache.

Source: `src/wemo_mcp_server/server.py:579`

```python
     577: 
     578: 
>>>  579: @mcp.tool()
     580: async def get_cache_info() -> dict[str, Any]:
     581:     """Get information about the persistent device cache.
     582: 
     583:     Returns information about the cache file including age, expiration status,
     584:     and device count. Useful for determining if a rescan is needed.
     585: 
     586:     Returns
     587:     -------
     588:         Dictionary containing:
     589:         - exists: Whether cache file exists
     590:         - path: Path to cache file
     591:         - age_seconds: Age of cache in seconds
     592:         - expired: Whether cache has expired
     593:         - device_count: Number of devices in cache
     594:         - ttl_seconds: Time-to-live for cache entries
     595: 
     596:     """
     597:     try:
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 27. `outlook_move_message`

**Server**: outlook-mcp (`mpalermiti/outlook-mcp`)
**Description**: Move a message to a folder.

Source: `src/outlook_mcp/server.py:241`

```python
     239: 
     240: 
>>>  241: @mcp.tool()
     242: async def outlook_move_message(
     243:     ctx: Context,
     244:     message_id: str,
     245:     folder: str,
     246: ) -> dict:
     247:     """Move a message to a folder.
     248: 
     249:     `folder` accepts display names ("Junk Email", "Archive", "TLDR"), well-known
     250:     names ("inbox", "deleteditems"), or Graph IDs. Prefer names.
     251:     """
     252:     client = _get_graph_client(ctx)
     253:     config = _get_config(ctx)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 28. `select_flight`

**Server**: mcp-southwest (`markswendsen-code/mcp-southwest`)
**Description**: Select a flight from search results with a specific fare type. Use after search_flights to proceed with booking.

Source: `src/index.ts:104`

```typescript
     102:   },
     103:   {
>>>  104:     name: "select_flight",
     105:     description:
     106:       "Select a flight from search results with a specific fare type. Use after search_flights to proceed with booking.",
     107:     inputSchema: zodToJsonSchema(selectFlightSchema),
     108:   },
     109:   {
     110:     name: "get_fares",
     111:     description:
     112:       "Compare all Southwest fare classes (Wanna Get Away, Wanna Get Away+, Anytime, Business Select) with prices and benefits for a route.",
     113:     inputSchema: zodToJsonSchema(getFaresSchema),
     114:   },
     115:   {
     116:     name: "add_early_bird",
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 29. `create_channel`

**Server**: srgplus-mcp (`srgplus/srgplus-mcp`)
**MCP Annotations**: readOnlyHint=false, destructiveHint=false

Source: `srg_mcp/channels.py:79`

```python
      77: 
      78: 
>>>   79: @mcp.tool(
      80:     annotations=ToolAnnotations(
      81:         title="Create channel",
      82:         readOnlyHint=False,
      83:         destructiveHint=False,
      84:         openWorldHint=True,
      85:     )
      86: )
      87: def create_channel(
      88:     name: str,
      89:     hub_profile_id: str,
      90:     workspace_id: str,
      91:     privacy: str = "Private",
      92: ) -> str:
      93:     """Create a new channel in a hub profile. Returns the new channel ID.
      94: 
      95:     workspace_id: target workspace ID — get available IDs from list_workspaces()
      96:     privacy: "Private" (default) or "Public"
      97:     """
      98:     return get_client().channels.create(
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 30. `batch_execute`

**Server**: starkfi (`ahmetenesdur/starkfi`)
**Description**: Execute multiple DeFi operations in a single Starknet transaction (multicall). Supports: swap, stake, supply, send, borr

Source: `src/mcp/tools/trade.ts:109`

```typescript
     107:   );
     108: 
>>>  109:   server.registerTool(
     110:     "batch_execute",
     111:     {
     112:       description:
     113:         "Execute multiple DeFi operations in a single Starknet transaction (multicall). Supports: swap, stake, supply, send, borrow, repay, withdraw, dca-create, dca-cancel. Requires at least 2 operations.",
     114:       inputSchema: z.object({
     115:         operations: z
     116:           .array(
     117:             z.object({
     118:               type: z
     119:                 .enum([
     120:                   "swap",
     121:                   "stake",
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 31. `load_csv`

**Server**: csv-analytics-mcp (`CSOAI-ORG/csv-analytics-mcp`)
**Description**: Load a CSV file into memory for analysis. The dataset is stored under

Source: `server.py:318`

```python
     316: 
     317: 
>>>  318: @mcp.tool()
     319: def load_csv(file_path: str, name: str = "", delimiter: str = ",", encoding: str = "utf-8", api_key: str = "") -> dict:
     320:     """Load a CSV file into memory for analysis. The dataset is stored under
     321:     a name (defaults to filename) and can be referenced in subsequent calls.
     322: 
     323:     Args:
     324:         file_path: Absolute path to the CSV file
     325:         name: Optional name for the dataset (default: filename without extension)
     326:         delimiter: Column delimiter (default: comma)
     327:         encoding: File encoding (default: utf-8)
     328: 
     329:     Behavior:
     330:         This tool is read-only and stateless — it produces analysis output
     331:         without modifying any external systems, databases, or files.
     332:         Safe to call repeatedly with identical inputs (idempotent).
     333:         Free tier: 10/day rate limit. Pro tier: unlimited.
     334:         No authentication required for basic usage.
     335: 
     336:     When to use:
     337:         Use this tool when you need structured analysis or classification
     338:         of inputs against established frameworks or standards.
     339: 
     340:     When NOT to use:
     341:         Not suitable for real-time production decision-making without
     342:         human review of results.
     343:     Behavioral Transparency:
     344:         - Side Effects: This tool is read-only and produces no side effects. It does not modify
     345:           any external state, databases, or files. All output is computed in-memory and returned
     346:           directly to the caller.
     347:         - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
     348:           require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
     349:         - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
     350:           included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
     351:         - Error Handling: Returns structured error objects with 'error' key on failure.
     352:           Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
     353:         - Idempotency: Fully idempotent — calling with the same inputs always produces the
     354:           same output. Safe to retry on timeout or transient failure.
     355:         - Data Privacy: No input data is stored, logged, or transmitted to external services.
     356:           All processing happens locally within the MCP server process.
     357:     """
     358:     allowed, msg, tier = check_access(api_key)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 32. `pg_switch_database`

**Server**: mcp-postgres (`itunified-io/mcp-postgres`)
**Description**: Switch the active connection profile. All subsequent queries will use this profile unless overridden.

Source: `src/tools.ts:54`

```typescript
      52:   },
      53:   {
>>>   54:     name: "pg_switch_database",
      55:     description:
      56:       "Switch the active connection profile. All subsequent queries will use this profile unless overridden.",
      57:     inputSchema: {
      58:       target,
      59:       profile: z.string().describe("Named profile to switch to"),
      60:     },
      61:     domain: "pg",
      62:     action: "connect switch",
      63:   },
      64: 
      65:   // ── Query (3 tools) ─────────────────────────────────────────────────
      66:   {
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 33. `search_cortex_docs`

**Server**: cortex-cloud-docs-mcp-server (`clarkemn/cortex-cloud-docs-mcp-server`)
**Description**: Search Cortex Cloud documentation

Source: `server.py:191`

```python
     189: 
     190: 
>>>  191: @mcp.tool()
     192: async def search_cortex_docs(query: str) -> str:
     193:     """Search Cortex Cloud documentation"""
     194:     results = await indexer.search_docs(query, site='cortex_cloud')
     195:     return json.dumps(results, indent=2)
     196: 
     197: @mcp.tool()
     198: async def search_cortex_api_docs(query: str) -> str:
     199:     """Search Cortex Cloud API documentation"""
     200:     results = await indexer.search_docs(query, site='cortex_api')
     201:     return json.dumps(results, indent=2)
     202: 
     203: @mcp.tool()
     204: async def search_all_docs(query: str) -> str:
     205:     """Search across all Cortex Cloud documentation sites."""
     206:     results = await indexer.search_docs(query)
     207:     return json.dumps(results, indent=2)
     208: 
     209: @mcp.tool()
     210: async def index_cortex_docs(max_pages: int = 50) -> str:
     211:     """Index Cortex Cloud documentation. Call this first before searching."""
     212:     pages_indexed = await indexer.index_site('cortex_cloud', max_pages)
     213:     return f"Indexed {pages_indexed} pages from Cortex Cloud documentation"
     214: 
     215: @mcp.tool()
     216: async def index_cortex_api_docs(max_pages: int = 50) -> str:
     217:     """Index Cortex Cloud API documentation. Call this first before searching."""
     218:     pages_indexed = await indexer.index_site('cortex_api', max_pages)
     219:     return f"Indexed {pages_indexed} pages from Cortex Cloud API documentation"
     220: 
     221: @mcp.tool()
     222: async def get_index_status() -> str:
     223:     """Check how many documents are currently cached."""
     224:     total_docs = len(indexer.cached_pages)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 34. `disconnect_all`

**Server**: uiautomator2-mcp-server (`tanbro/uiautomator2-mcp-server`)
**Description**: Disconnect from all Android devices

Source: `src/u2mcp/tools/device.py:182`

```python
     180: 
     181: 
>>>  182: @mcp.tool("disconnect_all", tags={"device:manage"})
     183: async def disconnect_all():
     184:     """Disconnect from all Android devices"""
     185:     async with _global_device_connection_lock:
     186:         _devices.clear()
     187: 
     188: 
     189: @mcp.tool("window_size", tags={"device:info"})
     190: async def window_size(serial: str) -> dict[str, int]:
     191:     """Get window size of an Android device
     192: 
     193:     Args:
     194:         serial (str): Android device serialno
     195: 
     196:     Returns:
     197:         dict[str,int]: Window size object:
     198:             - "width" (int): Window width
     199:             - "height" (int): Window height
     200:     """
     201:     async with get_device(serial) as device:
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 35. `send_bulk_template_messages`

**Server**: whatsapp-mcp (`nakulben/whatsapp-mcp`)

Source: `whatsapp_mcp/server.py:546`

```python
     544: 
     545: 
>>>  546: @mcp.tool()
     547: async def send_bulk_template_messages(
     548:     to_list: list[str],
     549:     template_name: str,
     550:     language: str = "en",
     551:     components: list[dict] | None = None,
     552: ) -> str:
     553:     """
     554:     Send an approved template message to multiple phone numbers.
     555: 
     556:     Messages are sent sequentially (one API call per recipient).
     557:     Each result is tracked individually.
     558: 
     559:     Args:
     560:         to_list: List of phone numbers with country code
     561:         template_name: Name of the approved template
     562:         language: Language code (default "en")
     563:         components: Optional parameter components (same for all recipients)
     564: 
     565:     Returns:
     566:         JSON with per-recipient results (successes and failures).
     567:     """
     568:     api = _get_api()
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 36. `trending_coins`

**Server**: toolfi (`Tsubaki414/toolfi`)
**Description**: 获取CoinGecko热门币种

Source: `mcp-server/src/server.py:340`

```python
     338: 
     339: 
>>>  340: @mcp.tool()
     341: async def trending_coins() -> str:
     342:     """
     343:     获取CoinGecko热门币种
     344: 
     345:     Returns:
     346:         热门币种列表
     347:     """
     348:     try:
     349:         trending = await coingecko.get_trending()
     350: 
     351:         result = []
     352:         for item in trending[:10]:
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 37. `pg_upsert`

**Server**: mcp-postgres (`itunified-io/mcp-postgres`)
**Description**: Insert or update on conflict. Requires confirm=true.

Source: `src/tools.ts:239`

```typescript
     237:   },
     238:   {
>>>  239:     name: "pg_upsert",
     240:     description: "Insert or update on conflict. Requires confirm=true.",
     241:     inputSchema: {
     242:       target,
     243:       table: z.string().describe("Table name"),
     244:       schema: z.string().optional().describe("Schema name (default: 'public')"),
     245:       columns: z.string().describe("JSON array of column names"),
     246:       values: z.string().describe("JSON array of values to insert"),
     247:       conflict_columns: z.string().describe("JSON array of columns for ON CONFLICT clause"),
     248:       confirm: z.string().describe("Must be 'true' to execute this destructive operation"),
     249:     },
     250:     domain: "pg",
     251:     action: "crud upsert",
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: displays details but also needs user confirmation

---
## 38. `update_permission_group`

**Server**: srgplus-mcp (`srgplus/srgplus-mcp`)
**Description**: Rename a permission group.
**MCP Annotations**: readOnlyHint=false, destructiveHint=false

Source: `srg_mcp/permission_groups.py:74`

```python
      72: 
      73: 
>>>   74: @mcp.tool(
      75:     annotations=ToolAnnotations(
      76:         title="Update permission group",
      77:         readOnlyHint=False,
      78:         destructiveHint=False,
      79:         openWorldHint=True,
      80:     )
      81: )
      82: def update_permission_group(group_id: str, name: str, workspace_id: str) -> dict | None:
      83:     """Rename a permission group.
      84: 
      85:     workspace_id: target workspace ID — get available IDs from list_workspaces()
      86:     """
      87:     return get_client().permission_groups.update(
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 39. `call_contract`

**Server**: merx-mcp (`Hovsteder/merx-mcp`)
**Description**: Execute a state-changing smart contract function. Estimates resources,

Source: `src/tools/contracts.ts:128`

```typescript
     126: 
     127: const callContract: McpTool = {
>>>  128:   name: 'call_contract',
     129:   description:
     130:     'Execute a state-changing smart contract function. Estimates resources, ' +
     131:     'buys via Merx if needed. Requires TRON_PRIVATE_KEY and TRON_ADDRESS.',
     132:   inputSchema: {
     133:     type: 'object',
     134:     properties: {
     135:       contract_address: {
     136:         type: 'string',
     137:         description: 'Contract TRON address.',
     138:       },
     139:       function_selector: {
     140:         type: 'string',
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 40. `analyze_prices`

**Server**: merx-mcp (`Hovsteder/merx-mcp`)
**Description**: Market price analysis with trends and recommendations. No auth required.

Source: `src/tools/prices.ts:89`

```typescript
      87: 
      88: const analyzePrices: McpTool = {
>>>   89:   name: 'analyze_prices',
      90:   description: 'Market price analysis with trends and recommendations. No auth required.',
      91:   inputSchema: {
      92:     type: 'object',
      93:     properties: {
      94:       resource: {
      95:         type: 'string',
      96:         enum: ['ENERGY', 'BANDWIDTH'],
      97:         description: 'Filter by resource type. Omit for all.',
      98:       },
      99:     },
     100:   },
     101:   async handler(input) {
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 41. `get_invitation_link`

**Server**: srgplus-mcp (`srgplus/srgplus-mcp`)
**MCP Annotations**: readOnlyHint=true, destructiveHint=false

Source: `srg_mcp/users.py:163`

```python
     161: 
     162: 
>>>  163: @mcp.tool(
     164:     annotations=ToolAnnotations(
     165:         title="Get invitation link",
     166:         readOnlyHint=True,
     167:         destructiveHint=False,
     168:         openWorldHint=True,
     169:     )
     170: )
     171: def get_invitation_link(
     172:     hub_profile_id: str,
     173:     email: str,
     174:     role_id: int,
     175:     workspace_id: str,
     176: ) -> dict:
     177:     """Generate a shareable invitation link for a single email address.
     178: 
     179:     workspace_id: target workspace ID — get available IDs from list_workspaces()
     180:     role_id: 1 = Admin, 2 = Editor, 3 = Viewer
     181:     Returns the invitation ID and access link URL.
     182:     """
     183:     result = get_client().invitations.invite_with_link(
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 42. `xpath_set_text`

**Server**: uiautomator2-mcp-server (`tanbro/uiautomator2-mcp-server`)
**Description**: Find element by XPath and set its text content.

Source: `src/u2mcp/tools/xpath.py:178`

```python
     176: 
     177: 
>>>  178: @mcp.tool("xpath_set_text", tags={"xpath:modify"})
     179: async def xpath_set_text(serial: str, xpath: str, text: str):
     180:     """Find element by XPath and set its text content.
     181: 
     182:     Args:
     183:         serial (str): Android device serial number.
     184:         xpath (str): Element XPath expression.
     185:         text (str): Text content to set.
     186:     """
     187:     async with get_device(serial) as device:
     188:         await to_thread.run_sync(lambda: device.xpath(xpath).set_text(text))
     189: 
     190: 
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 43. `customer_engagement`

**Server**: dingdawg-agent-1 (`dingdawg/dingdawg-agent-1`)

Source: `gateway/isg_agent/mcp/tools/business_skill_tools.py:360`

```python
     358:     # -----------------------------------------------------------------------
     359: 
>>>  360:     @mcp.tool(
     361:         name="customer_engagement",
     362:         description=(
     363:             "Track customer loyalty, run campaigns, and measure engagement for a "
     364:             "business agent. Actions: add_points, get_loyalty, create_campaign, "
     365:             "list_campaigns, track_interaction."
     366:         ),
     367:     )
     368:     async def customer_engagement_tool(
     369:         agent_handle: str,
     370:         action: str,
     371:         contact_id: Optional[str] = None,
     372:         points: Optional[int] = None,
     373:         campaign_name: Optional[str] = None,
     374:         campaign_type: Optional[str] = None,
     375:         interaction_type: Optional[str] = None,
     376:         metadata: Optional[str] = None,
     377:     ) -> Dict[str, Any]:
     378:         """Manage customer engagement for a business agent."""
     379:         params: Dict[str, Any] = {}
     380:         if contact_id:
     381:             params["contact_id"] = contact_id
     382:         if points is not None:
     383:             params["points"] = points
     384:         if campaign_name:
     385:             params["campaign_name"] = campaign_name
     386:         if campaign_type:
     387:             params["campaign_type"] = campaign_type
     388:         if interaction_type:
     389:             params["interaction_type"] = interaction_type
     390:         if metadata:
     391:             try:
     392:                 params["metadata"] = json.loads(metadata)
     393:             except json.JSONDecodeError:
     394:                 params["metadata"] = {"note": metadata}
     395:         return await _run_skill("customer-engagement", agent_handle, action, params)
     396: 
     397:     # -----------------------------------------------------------------------
     398:     # Tool 8: manage_reviews
     399:     # -----------------------------------------------------------------------
     400: 
     401:     @mcp.tool(
     402:         name="manage_reviews",
     403:         description=(
     404:             "Request, track, and respond to customer reviews for a business "
     405:             "agent. Actions: request, list, get, respond, report."
     406:         ),
     407:     )
     408:     async def manage_reviews(
     409:         agent_handle: str,
     410:         action: str,
     411:         contact_name: Optional[str] = None,
     412:         contact_email: Optional[str] = None,
     413:         rating: Optional[int] = None,
     414:         review_text: Optional[str] = None,
     415:         response_text: Optional[str] = None,
     416:         review_id: Optional[str] = None,
     417:     ) -> Dict[str, Any]:
     418:         """Manage customer reviews for a business agent."""
     419:         params: Dict[str, Any] = {}
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: passes points as parameter

---
## 44. `batch_process`

**Server**: rawtherapee-mcp-server (`lucamarien/rawtherapee-mcp-server`)

Source: `src/rawtherapee_mcp/server.py:1119`

```python
    1117: 
    1118: 
>>> 1119: @mcp.tool()
    1120: async def batch_process(
    1121:     ctx: Context,
    1122:     file_paths: list[str],
    1123:     profile_path: str,
    1124:     output_format: str = "jpeg",
    1125:     output_dir: str | None = None,
    1126:     device_preset: str | None = None,
    1127: ) -> dict[str, Any]:
    1128:     """Process multiple RAW files with the same PP3 profile.
    1129: 
    1130:     Use this for bulk processing of a set of RAW files with identical settings.
    1131:     Params: file_paths, profile_path, output_format, output_dir, device_preset
    1132:     """
    1133:     config = get_config(ctx)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 45. `describe_columns`

**Server**: csv-analytics-mcp (`CSOAI-ORG/csv-analytics-mcp`)
**Description**: Get detailed statistics for every column in a dataset:

Source: `server.py:417`

```python
     415: 
     416: 
>>>  417: @mcp.tool()
     418: def describe_columns(name: str, api_key: str = "") -> dict:
     419:     """Get detailed statistics for every column in a dataset:
     420:     - Numeric columns: mean, std, min, max, median, quartiles
     421:     - Categorical columns: unique count, top 5 values with frequencies
     422: 
     423:     Args:
     424:         name: Dataset name (from load_csv)
     425: 
     426:     Behavior:
     427:         This tool is read-only and stateless — it produces analysis output
     428:         without modifying any external systems, databases, or files.
     429:         Safe to call repeatedly with identical inputs (idempotent).
     430:         Free tier: 10/day rate limit. Pro tier: unlimited.
     431:         No authentication required for basic usage.
     432: 
     433:     When to use:
     434:         Use this tool when you need structured analysis or classification
     435:         of inputs against established frameworks or standards.
     436: 
     437:     When NOT to use:
     438:         Not suitable for real-time production decision-making without
     439:         human review of results.
     440:     Behavioral Transparency:
     441:         - Side Effects: This tool is read-only and produces no side effects. It does not modify
     442:           any external state, databases, or files. All output is computed in-memory and returned
     443:           directly to the caller.
     444:         - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
     445:           require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
     446:         - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
     447:           included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
     448:         - Error Handling: Returns structured error objects with 'error' key on failure.
     449:           Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
     450:         - Idempotency: Fully idempotent — calling with the same inputs always produces the
     451:           same output. Safe to retry on timeout or transient failure.
     452:         - Data Privacy: No input data is stored, logged, or transmitted to external services.
     453:           All processing happens locally within the MCP server process.
     454:     """
     455:     allowed, msg, tier = check_access(api_key)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 46. `workboard_get_teams_tool`

**Server**: mcp-workboard (`crunchtools/mcp-workboard`)
**Description**: Get all teams the authenticated user belongs to.

Source: `src/mcp_workboard_crunchtools/server.py:148`

```python
     146: 
     147: 
>>>  148: @mcp.tool()
     149: async def workboard_get_teams_tool() -> dict[str, Any]:
     150:     """Get all teams the authenticated user belongs to.
     151: 
     152:     Returns team IDs, names, and owner user IDs. Use workboard_get_team_members_tool
     153:     to get the full member list (with user_ids) for a specific team.
     154: 
     155:     Returns:
     156:         List of teams with team_id, team_name, team_owner_id, is_team_owner
     157:     """
     158:     return await get_teams()
     159: 
     160: 
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 47. `query_data`

**Server**: csv-analytics-mcp (`CSOAI-ORG/csv-analytics-mcp`)
**Description**: Query a loaded dataset with filtering, column selection, and sorting.

Source: `server.py:371`

```python
     369: 
     370: 
>>>  371: @mcp.tool()
     372: def query_data(name: str, filter_expr: str = "", columns: Optional[list[str]] = None,
     373:                sort_by: str = "", ascending: bool = True, limit: int = 100, api_key: str = "") -> dict:
     374:     """Query a loaded dataset with filtering, column selection, and sorting.
     375: 
     376:     Uses pandas query syntax for filters:
     377:     - 'age > 30'
     378:     - 'city == "London" and salary > 50000'
     379:     - 'status.isin(["active", "pending"])'
     380: 
     381:     Args:
     382:         name: Dataset name (from load_csv)
     383:         filter_expr: Pandas query expression for filtering rows
     384:         columns: List of column names to return (default: all)
     385:         sort_by: Column name to sort by
     386:         ascending: Sort order (default: True)
     387:         limit: Max rows to return (default: 100)
     388: 
     389:     Behavior:
     390:         This tool is read-only and stateless — it produces analysis output
     391:         without modifying any external systems, databases, or files.
     392:         Safe to call repeatedly with identical inputs (idempotent).
     393:         Free tier: 10/day rate limit. Pro tier: unlimited.
     394:         No authentication required for basic usage.
     395: 
     396:     When to use:
     397:         Use this tool when you need structured analysis or classification
     398:         of inputs against established frameworks or standards.
     399: 
     400:     When NOT to use:
     401:         Not suitable for real-time production decision-making without
     402:         human review of results.
     403:     """
     404:     allowed, msg, tier = check_access(api_key)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 48. `compare_models`

**Server**: model-advisor-mcp (`Semicolon-D/model-advisor-mcp`)
**Description**: Compare AI models side-by-side in a table. Works across providers and categories — compare LLMs against each other, imag

Source: `src/server.ts:52`

```typescript
      50:   },
      51:   {
>>>   52:     name: "compare_models",
      53:     description:
      54:       "Compare AI models side-by-side in a table. Works across providers and categories — compare LLMs against each other, image generators, or even mix categories. Auto-adapts columns based on model types. Includes speed metrics (TTFT, tokens/sec) and benchmark scores (MMLU) when available.",
      55:     inputSchema: {
      56:       type: "object" as const,
      57:       properties: {
      58:         model_ids: {
      59:           type: "array",
      60:           items: { type: "string" },
      61:           description:
      62:             'Model IDs to compare. Examples: ["openai/gpt-4o", "anthropic/claude-sonnet-4"] or ["fal-ai/flux-pro/v1.1", "fal-ai/stable-diffusion-v35-large"]',
      63:         },
      64:       },
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 49. `manage_jira_project`

**Server**: jira-cloud (`aaronsb/jira-cloud`)
**Description**: List projects or get project configuration and metadata. For issue counts, workload, or cross-project comparison, use an

Source: `src/schemas/tool-schemas.ts:280`

```typescript
     278: 
     279:   manage_jira_project: {
>>>  280:     name: 'manage_jira_project',
     281:     description: 'List projects or get project configuration and metadata. For issue counts, workload, or cross-project comparison, use analyze_jira_issues with metrics: ["summary"] instead.',
     282:     inputSchema: {
     283:       type: 'object',
     284:       properties: {
     285:         operation: {
     286:           type: 'string',
     287:           enum: ['get', 'list'],
     288:           description: 'Operation to perform',
     289:         },
     290:         projectKey: {
     291:           type: 'string',
     292:           description: 'Project key (e.g., PROJ). Required for get.',
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 50. `contextkeeper_update_task`

**Server**: workbench (`TheRealDataBoss/workbench`)
**Description**: Update the status of an existing task. Creates a new handoff version.

Source: `packages/python/contextkeeper/mcp_server.py:155`

```python
     153: 
     154: 
>>>  155: @mcp.tool()
     156: def contextkeeper_update_task(task_id: str, status: str) -> str:
     157:     """Update the status of an existing task. Creates a new handoff version.
     158: 
     159:     Args:
     160:         task_id: Task ID to update (e.g. TASK-0001)
     161:         status: New status (pending, in_progress, done, blocked)
     162:     """
     163:     try:
     164:         handoff = _client().update_task_status(task_id, status)
     165:         return f"Task {task_id} updated to '{status}'. Handoff v{handoff.version}"
     166:     except Exception as exc:
     167:         return f"Error: {exc}"
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 51. `create_ticket`

**Server**: odoo-mcp-gateway (`parth-unjiya/odoo-mcp-gateway`)

Source: `src/odoo_mcp_gateway/plugins/core/helpdesk.py:127`

```python
     125:                 return {"error": context.sanitize_error(e)}
     126: 
>>>  127:         @server.tool()
     128:         async def create_ticket(
     129:             name: str,
     130:             description: str = "",
     131:             team_id: int | None = None,
     132:             priority: str = "1",
     133:         ) -> dict[str, Any]:
     134:             """Create a new helpdesk ticket.
     135: 
     136:             Args:
     137:                 name: Ticket subject/title
     138:                 description: Detailed description
     139:                 team_id: Helpdesk team ID (optional)
     140:                 priority: Priority level (0=Low, 1=Medium, 2=High, 3=Urgent)
     141:             """
     142:             client = get_client(context)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 52. `estimate_transaction_cost`

**Server**: merx-mcp (`Hovsteder/merx-mcp`)
**Description**: Estimate cost of a TRON transaction BEFORE sending. Aliases: estimate_cost, calculate_cost, transaction_cost, energy_cos

Source: `src/tools/estimation.ts:75`

```typescript
      73: 
      74: const estimateTransactionCost: McpTool = {
>>>   75:   name: 'estimate_transaction_cost',
      76:   description:
      77:     'Estimate cost of a TRON transaction BEFORE sending. Aliases: estimate_cost, calculate_cost, transaction_cost, energy_cost, transfer_cost. Calculate exactly how much energy, bandwidth, and TRX a TRON transaction will cost before sending it. Use this to answer questions like "how much does a USDT transfer cost?" or "what will it cost me to send 100 USDT to address X?". Returns: energy units needed, bandwidth needed, TRX cost if you burn directly, and TRX cost if you rent energy from Merx (typically 70-80% cheaper). Supports trc20_transfer (e.g. USDT/USDC), trc20_approve, trx_transfer, and custom contract calls. No auth required.',
      78:   inputSchema: {
      79:     type: 'object',
      80:     properties: {
      81:       operation: {
      82:         type: 'string',
      83:         enum: ['trc20_transfer', 'trc20_approve', 'trx_transfer', 'custom'],
      84:         description: 'Transaction type.',
      85:       },
      86:       from_address: { type: 'string', description: 'Sender TRON address.' },
      87:       to_address: { type: 'string', description: 'Recipient TRON address.' },
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 53. `interpolate_profiles`

**Server**: rawtherapee-mcp-server (`lucamarien/rawtherapee-mcp-server`)

Source: `src/rawtherapee_mcp/server.py:1971`

```python
    1969: 
    1970: 
>>> 1971: @mcp.tool()
    1972: async def interpolate_profiles(
    1973:     ctx: Context,
    1974:     profile_a: str,
    1975:     profile_b: str,
    1976:     factor: float = 0.5,
    1977:     output_name: str = "interpolated",
    1978:     file_path: str | None = None,
    1979:     include_preview: bool = False,
    1980:     preview_max_width: int = 600,
    1981: ) -> dict[str, Any] | ToolResult:
    1982:     """Blend two PP3 profiles by linear interpolation.
    1983: 
    1984:     Numeric values are interpolated (factor=0.0 gives profile A, factor=1.0
    1985:     gives profile B). Non-numeric values are taken from the nearer profile.
    1986:     Useful for creating intermediate looks between two processing styles.
    1987:     Params: profile_a, profile_b, factor, output_name, file_path,
    1988:     include_preview, preview_max_width
    1989:     """
    1990:     config = get_config(ctx)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 54. `outlook_update_task`

**Server**: outlook-mcp (`mpalermiti/outlook-mcp`)

Source: `src/outlook_mcp/server.py:571`

```python
     569: 
     570: 
>>>  571: @mcp.tool()
     572: async def outlook_update_task(
     573:     ctx: Context,
     574:     task_id: str,
     575:     list_id: str | None = None,
     576:     title: str | None = None,
     577:     due: str | None = None,
     578:     body: str | None = None,
     579:     importance: str | None = None,
     580: ) -> dict:
     581:     """Update a task in a To Do list (partial patch)."""
     582:     client = _get_graph_client(ctx)
     583:     config = _get_config(ctx)
     584:     return await todo.update_task(
     585:         client.sdk_client,
     586:         task_id,
     587:         list_id,
     588:         title,
     589:         due,
     590:         body,
     591:         importance,
     592:         config=config,
     593:     )
     594: 
     595: 
     596: @mcp.tool()
     597: async def outlook_complete_task(
     598:     ctx: Context,
     599:     task_id: str,
     600:     list_id: str | None = None,
     601: ) -> dict:
     602:     """Mark a task as completed."""
     603:     client = _get_graph_client(ctx)
     604:     config = _get_config(ctx)
     605:     return await todo.complete_task(
     606:         client.sdk_client,
     607:         task_id,
     608:         list_id,
     609:         config=config,
     610:     )
     611: 
     612: 
     613: @mcp.tool()
     614: async def outlook_delete_task(
     615:     ctx: Context,
     616:     task_id: str,
     617:     list_id: str | None = None,
     618: ) -> dict:
     619:     """Delete a task from a To Do list."""
     620:     client = _get_graph_client(ctx)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 55. `delete_template`

**Server**: whatsapp-mcp (`nakulben/whatsapp-mcp`)
**Description**: Delete a WhatsApp template by name.

Source: `whatsapp_mcp/server.py:437`

```python
     435: 
     436: 
>>>  437: @mcp.tool()
     438: async def delete_template(template_name: str) -> str:
     439:     """
     440:     Delete a WhatsApp template by name.
     441: 
     442:     WARNING: This permanently deletes ALL language variants of the template.
     443: 
     444:     Args:
     445:         template_name: Name of the template to delete
     446: 
     447:     Returns:
     448:         JSON confirming deletion.
     449:     """
     450:     try:
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 56. `search_procurement`

**Server**: ph-civic-data-mcp (`xmpuspus/ph-civic-data-mcp`)

Source: `src/ph_civic_data_mcp/sources/philgeps.py:87`

```python
      85: 
      86: 
>>>   87: @mcp.tool()
      88: async def search_procurement(
      89:     keyword: str,
      90:     agency: str | None = None,
      91:     region: str | None = None,
      92:     date_from: str | None = None,
      93:     date_to: str | None = None,
      94:     limit: int = 20,
      95: ) -> list[dict]:
      96:     """Search PH government procurement from PhilGEPS open data.
      97: 
      98:     Note: the PhilGEPS public portal does not expose server-side search for
      99:     external clients, so this tool fetches the latest ~100 bid notices and
     100:     filters them in-memory. Data is cached 6 hours. Keyword/agency/region
     101:     filters are applied client-side (case-insensitive substring match).
     102: 
     103:     Args:
     104:         keyword: Search term matched against title + agency + classification.
     105:         agency: Partial match on procuring entity name.
     106:         region: PH region filter (partial match).
     107:         date_from / date_to: YYYY-MM-DD bounds on publish date.
     108:         limit: Max results (default 20, max 100).
     109:     """
     110:     limit = max(1, min(int(limit), 100))
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 57. `get_air_quality`

**Server**: ph-civic-data-mcp (`xmpuspus/ph-civic-data-mcp`)
**Description**: Real-time air quality for a Philippine city via Open-Meteo (no API key).

Source: `src/ph_civic_data_mcp/sources/open_meteo_aq.py:57`

```python
      55: 
      56: 
>>>   57: @mcp.tool()
      58: async def get_air_quality(location: str) -> dict:
      59:     """Real-time air quality for a Philippine city via Open-Meteo (no API key).
      60: 
      61:     Returns PM2.5, PM10, CO, NO2, SO2, O3 plus European AQI and US AQI with
      62:     category interpretation. Covers ~80 major PH cities via local coordinate
      63:     table. For unlisted locations, caller can pass coordinates directly via
      64:     the latitude/longitude form in a future version.
      65: 
      66:     Args:
      67:         location: City or municipality name (e.g. "Manila", "Cebu City", "Davao").
      68:     """
      69:     ckey = cache_key({"tool": "aq", "loc": location.strip().lower()})
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 58. `add_text_annotation`

**Server**: cml-mcp (`xorrkaz/cml-mcp`)

Source: `src/cml_mcp/tools/annotations.py:84`

```python
      82:     #          text_bold, text_content, text_font, text_italic, text_size, text_unit
      83:     # Omitted: type (injected as "text")
>>>   84:     @mcp.tool(
      85:         annotations={
      86:             "title": "Add Text Annotation",
      87:             "readOnlyHint": False,
      88:             "destructiveHint": False,
      89:         },
      90:     )
      91:     async def add_text_annotation(
      92:         lab_id: UUID4Type,
      93:         x1: CoordinateFloat,
      94:         y1: CoordinateFloat,
      95:         text_content: Annotated[str, field_from(TextAnnotation, "text_content")],
      96:         text_font: Annotated[str, field_from(TextAnnotation, "text_font")],
      97:         text_size: Annotated[int, field_from(TextAnnotation, "text_size")],
      98:         text_unit: Annotated[Literal["pt", "px", "em"], field_from(TextAnnotation, "text_unit")],
      99:         text_bold: Annotated[bool, field_from(TextAnnotation, "text_bold")],
     100:         text_italic: Annotated[bool, field_from(TextAnnotation, "text_italic")],
     101:         border_color: AnnotationColor,
     102:         border_style: Annotated[Literal["", "2,2", "4,2"], field_from(TextAnnotation, "border_style")],
     103:         color: AnnotationColor,
     104:         thickness: Annotated[int, field_from(TextAnnotation, "thickness")],
     105:         z_index: Annotated[int, field_from(TextAnnotation, "z_index")],
     106:         rotation: Annotated[int, field_from(TextAnnotation, "rotation")],
     107:     ) -> UUID4Type:
     108:         """
     109:         Add a text label annotation to a lab canvas. Returns the annotation UUID.
     110: 
     111:         Coordinates: x1/y1 are the text anchor (top-left). All coords -15000..15000.
     112: 
     113:         Required: x1, y1 (coords -15000 to 15000), text_content (0-8192 chars), text_font (0-128 chars),
     114:         text_size (1-128), text_unit ("pt"/"px"/"em"), text_bold, text_italic (bool),
     115:         border_color, color (e.g., "#FF0000"), border_style (""/"2,2"/"4,2"), thickness (1-32),
     116:         z_index (-10240 to 10240), rotation (0-360 degrees).
     117: 
     118:         Examples:
     119:         - "Add a 'Core Network' text label at position 0,0 in my lab"
     120:         - "Label the router cluster at coordinates 100,200"
     121:         - "Put a bold red 'IMPORTANT' note at -50,-50"
     122:         """
     123:         client = get_cml_client_dep()
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 59. `stake_tokens`

**Server**: starkfi (`ahmetenesdur/starkfi`)
**Description**: Stake tokens in a delegation pool on Starknet. Smart stake: auto-detects whether the user needs to enter the pool or jus

Source: `src/mcp/tools/staking.ts:75`

```typescript
      73:   );
      74: 
>>>   75:   server.registerTool(
      76:     "stake_tokens",
      77:     {
      78:       description:
      79:         "Stake tokens in a delegation pool on Starknet. Smart stake: auto-detects whether the user needs to enter the pool or just add to an existing delegation. Supports STRK, WBTC, tBTC, SolvBTC, LBTC.",
      80:       inputSchema: z.object({
      81:         amount: z.string().describe("Amount to stake (e.g. '100', '0.01')"),
      82:         pool: z.string().describe("Staking pool contract address (0x...)"),
      83:         token: z
      84:           .string()
      85:           .optional()
      86:           .describe(
      87:             "Token symbol to stake (default: STRK). Supported: STRK, WBTC, tBTC, SolvBTC, LBTC"
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 60. `compose_branded`

**Server**: mcp-server-bedrock-image (`Yaksh36/mcp-server-bedrock-image`)

Source: `src/mcp_server_bedrock_image/server.py:308`

```python
     306: 
     307: 
>>>  308: @mcp.tool(name="compose_branded")
     309: async def tool_compose_branded(
     310:     image_path: str = Field(description="Path to the source image"),
     311:     logo_path: str = Field(description="Path to the logo file (RGBA PNG)"),
     312:     output_path: str = Field(description="Where to save the branded image"),
     313:     logo_variant: str = Field(default="auto", description="'light', 'dark', or 'auto'"),
     314:     logo_scale: float = Field(
     315:         default=0.08, description="Logo size as fraction of image width"
     316:     ),
     317: ) -> dict:
     318:     """Overlay logo with composition-aware placement."""
     319:     path = compose_branded_image(
     320:         image_path=image_path,
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 61. `download_lab_topology`

**Server**: cml-mcp (`xorrkaz/cml-mcp`)
**Description**: Download the full topology for a lab by UUID as a YAML string. Present this to the user

Source: `src/cml_mcp/tools/labs.py:509`

```python
     507:             raise ToolError(e)
     508: 
>>>  509:     @mcp.tool(
     510:         annotations={"title": "Download lab topology", "readOnlyHint": True},
     511:     )
     512:     async def download_lab_topology(lab_id: UUID4Type) -> str:
     513:         """
     514:         Download the full topology for a lab by UUID as a YAML string. Present this to the user
     515:         for saving to a .yaml file (e.g. for backup or sharing).
     516: 
     517:         Examples:
     518:         - "Export lab abc123 as YAML"
     519:         - "Download my OSPF lab topology"
     520:         - "Give me a backup of lab xyz"
     521:         """
     522:         client = get_cml_client_dep()
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: user will decide to save or not

---
## 62. `cancel_flight`

**Server**: mcp-southwest (`markswendsen-code/mcp-southwest`)
**Description**: Cancel a Southwest reservation. Wanna Get Away fares receive travel funds (valid 12 months). Anytime/Business Select far

Source: `src/index.ts:140`

```typescript
     138:   },
     139:   {
>>>  140:     name: "cancel_flight",
     141:     description:
     142:       "Cancel a Southwest reservation. Wanna Get Away fares receive travel funds (valid 12 months). Anytime/Business Select fares are fully refundable.",
     143:     inputSchema: zodToJsonSchema(cancelFlightSchema),
     144:   },
     145:   {
     146:     name: "check_in",
     147:     description:
     148:       "Check in online for a Southwest flight. Check-in opens exactly 24 hours before departure. Returns boarding group (A/B/C) and position number.",
     149:     inputSchema: zodToJsonSchema(checkInSchema),
     150:   },
     151:   {
     152:     name: "get_boarding_pass",
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 63. `calc_delivery`

**Server**: boxberry-mcp (`theYahia/boxberry-mcp`)
**Description**: Расчёт стоимости и сроков доставки Boxberry.

Source: `src/index.ts:23`

```typescript
      21:     async (params) => ({ content: [{ type: "text", text: await handleListPoints(params) }] }));
      22: 
>>>   23:   server.tool("calc_delivery", "Расчёт стоимости и сроков доставки Boxberry.", calcDeliverySchema.shape,
      24:     async (params) => ({ content: [{ type: "text", text: await handleCalcDelivery(params) }] }));
      25: 
      26:   server.tool("track", "Отслеживание отправления Boxberry по трек-номеру.", trackSchema.shape,
      27:     async (params) => ({ content: [{ type: "text", text: await handleTrack(params) }] }));
      28: 
      29:   server.tool("zip_check", "Проверка почтового индекса на доступность доставки Boxberry.", zipCodesSchema.shape,
      30:     async (params) => ({ content: [{ type: "text", text: await handleZipCodes(params) }] }));
      31: 
      32:   server.tool("list_services", "Список оказанных услуг по отправлению Boxberry.", listServicesSchema.shape,
      33:     async (params) => ({ content: [{ type: "text", text: await handleListServices(params) }] }));
      34: 
      35:   return server;
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: description is in Russian - translation: "Calculation of the cost and delivery time for Boxberry."

---
## 64. `estimate_contract_call`

**Server**: merx-mcp (`Hovsteder/merx-mcp`)
**Description**: Estimate energy and bandwidth cost for a smart contract call.

Source: `src/tools/contracts.ts:66`

```typescript
      64: 
      65: const estimateContractCall: McpTool = {
>>>   66:   name: 'estimate_contract_call',
      67:   description:
      68:     'Estimate energy and bandwidth cost for a smart contract call. ' +
      69:     'Compares rental vs burn cost. No auth required.',
      70:   inputSchema: {
      71:     type: 'object',
      72:     properties: {
      73:       contract_address: {
      74:         type: 'string',
      75:         description: 'Contract TRON address.',
      76:       },
      77:       function_selector: {
      78:         type: 'string',
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 65. `outlook_delete_message`

**Server**: outlook-mcp (`mpalermiti/outlook-mcp`)
**Description**: Delete a message. Moves to Deleted Items by default. Set permanent=true to hard delete.

Source: `src/outlook_mcp/server.py:257`

```python
     255: 
     256: 
>>>  257: @mcp.tool()
     258: async def outlook_delete_message(
     259:     ctx: Context,
     260:     message_id: str,
     261:     permanent: bool = False,
     262: ) -> dict:
     263:     """Delete a message. Moves to Deleted Items by default. Set permanent=true to hard delete."""
     264:     client = _get_graph_client(ctx)
     265:     config = _get_config(ctx)
     266:     return await mail_triage.delete_message(client.sdk_client, message_id, permanent, config=config)
     267: 
     268: 
     269: @mcp.tool()
     270: async def outlook_flag_message(
     271:     ctx: Context,
     272:     message_id: str,
     273:     status: str,
     274: ) -> dict:
     275:     """Set follow-up flag. Status: flagged, complete, or notFlagged."""
     276:     client = _get_graph_client(ctx)
     277:     config = _get_config(ctx)
     278:     return await mail_triage.flag_message(client.sdk_client, message_id, status, config=config)
     279: 
     280: 
     281: @mcp.tool()
     282: async def outlook_categorize_message(
     283:     ctx: Context,
     284:     message_id: str,
     285:     categories: list[str],
     286: ) -> dict:
     287:     """Set categories on a message."""
     288:     client = _get_graph_client(ctx)
     289:     config = _get_config(ctx)
     290:     return await mail_triage.categorize_message(
     291:         client.sdk_client, message_id, categories, config=config
     292:     )
     293: 
     294: 
     295: @mcp.tool()
     296: async def outlook_mark_read(
     297:     ctx: Context,
     298:     message_id: str,
     299:     is_read: bool,
     300: ) -> dict:
     301:     """Mark a message as read or unread."""
     302:     client = _get_graph_client(ctx)
     303:     config = _get_config(ctx)
     304:     return await mail_triage.mark_read(client.sdk_client, message_id, is_read, config=config)
     305: 
     306: 
     307: @mcp.tool()
     308: async def outlook_reclassify_message(
     309:     ctx: Context,
     310:     message_id: str,
     311:     classification: str,
     312: ) -> dict:
     313:     """Reclassify a message's Focused Inbox placement. classification: "focused" or "other"."""
     314:     client = _get_graph_client(ctx)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 66. `structured`

**Server**: claude-mcp-bridge (`hampsterx/claude-mcp-bridge`)

Source: `src/index.ts:145`

```typescript
     143: // --- structured tool ---
     144: 
>>>  145: server.registerTool(
     146:   "structured",
     147:   {
     148:     title: "Structured Output",
     149:     description: structuredDescription,
     150:     inputSchema: {
     151:       prompt: z.string().describe("What to generate or extract"),
     152:       schema: z.string().describe("JSON Schema as a JSON string"),
     153:       files: z
     154:         .array(z.string())
     155:         .optional()
     156:         .describe("Text file paths to include as context"),
     157:       model: z.string().optional().describe("Model alias or full Claude model name"),
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 67. `get_skill`

**Server**: helpbase (`Codehagen/helpbase`)
**Description**: Fetch the full content of a single skill (writing-style / tone / formatting rule) by name. Use list_skills to discover available names.

Source: `registry/helpbase-mcp/server.ts:126`

```typescript
     124:   )
     125: 
>>>  126:   server.registerTool(
     127:     "get_skill",
     128:     {
     129:       title: "Get skill",
     130:       description:
     131:         "Fetch the full content of a single skill (writing-style / tone / " +
     132:         "formatting rule) by name. Use list_skills to discover available " +
     133:         "names.",
     134:       inputSchema: getSkillInput.shape,
     135:     },
     136:     async (input) => handleGetSkill(skills, input),
     137:   )
     138: 
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 68. `can_create_child`

**Server**: srgplus-mcp (`srgplus/srgplus-mcp`)
**MCP Annotations**: readOnlyHint=true, destructiveHint=false

Source: `srg_mcp/users.py:383`

```python
     381: 
     382: 
>>>  383: @mcp.tool(
     384:     annotations=ToolAnnotations(
     385:         title="Check create-child permission",
     386:         readOnlyHint=True,
     387:         destructiveHint=False,
     388:         openWorldHint=True,
     389:     )
     390: )
     391: def can_create_child(
     392:     parent_target_type: str,
     393:     parent_target_id: str,
     394:     child_target_type: str,
     395:     workspace_id: str,
     396: ) -> bool:
     397:     """Check whether the current user can create a child resource inside a parent.
     398: 
     399:     workspace_id: target workspace ID — get available IDs from list_workspaces()
     400:     Example: can the user create a "Channel" inside a "HubProfile"?
     401:     """
     402:     return get_client().permissions.can_create_child(
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 69. `get_hub_profile_by_username`

**Server**: srgplus-mcp (`srgplus/srgplus-mcp`)
**Description**: Get hub profile details by its URL username/slug.
**MCP Annotations**: readOnlyHint=true, destructiveHint=false

Source: `srg_mcp/hub_profiles.py:64`

```python
      62: 
      63: 
>>>   64: @mcp.tool(
      65:     annotations=ToolAnnotations(
      66:         title="Get hub profile by username",
      67:         readOnlyHint=True,
      68:         destructiveHint=False,
      69:         openWorldHint=True,
      70:     )
      71: )
      72: def get_hub_profile_by_username(username: str, workspace_id: str) -> dict:
      73:     """Get hub profile details by its URL username/slug.
      74: 
      75:     workspace_id: target workspace ID — get available IDs from list_workspaces()
      76:     """
      77:     return (
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 70. `delay`

**Server**: uiautomator2-mcp-server (`tanbro/uiautomator2-mcp-server`)
**Description**: Delay for a specific amount of time.

Source: `src/u2mcp/tools/delay.py:10`

```python
       8: 
       9: 
>>>   10: @mcp.tool("delay", tags={"util:delay"})
      11: async def delay(seconds: float):
      12:     """Delay for a specific amount of time.
      13: 
      14:     Args:
      15:         seconds (float): Delay duration in seconds.
      16:     """
      17:     await anyio.sleep(seconds)
      18: 
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 71. `get_my_workflows`

**Server**: data-intelligence-mcp-server (`ibm/data-intelligence-mcp-server`)
**Description**: Watsonx Orchestrator compatible wrapper for get_my_workflows.

Source: `app/services/workflow/tools/get_my_workflows.py:809`

```python
     807: 
     808: 
>>>  809: @service_registry.tool(
     810:     name="get_my_workflows",
     811:     description="Watsonx Orchestrator compatible wrapper for get_my_workflows." + get_my_workflows_description,
     812:     tags={"wxo", "workflow", "flowable", "governance", "glossary", "my_workflows"},
     813:     meta={"version": "2.0", "service": "workflows"},
     814: )
     815: @auto_context
     816: async def wxo_get_my_workflows(
     817:     max_results: int = 50,
     818:     state: str = None,
     819:     deep_dive: bool = False,
     820:     include_tasks: bool = True,
     821:     stalled_days: int = None,
     822:     workflow_id: str = None,
     823:     format: str = "table",
     824:     ctx: Context = None
     825: ) -> GetMyWorkflowsResponse:
     826:     """Watsonx Orchestrator compatible version of get_my_workflows."""
     827: 
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 72. `agent_debate_start`

**Server**: Agestra (`mua-vtuber/Agestra`)
**Description**: Start a multi-provider debate on a topic. Optionally enable enhanced mode with goal-based quality validation.

Source: `packages/mcp-server/src/tools/agent-session/tool-registry.ts:30`

```typescript
      28:   return [
      29:     {
>>>   30:       name: "agent_debate_start",
      31:       title: "Start AI Debate",
      32:       description: "Start a multi-provider debate on a topic. Optionally enable enhanced mode with goal-based quality validation.",
      33:       inputSchema: zodToMcpSchema(AgentDebateStartSchema),
      34:     },
      35:     {
      36:       name: "agent_debate_status",
      37:       title: "Check Debate Status",
      38:       description: "Check the status and result of a debate session.",
      39:       inputSchema: zodToMcpSchema(AgentDebateStatusSchema),
      40:     },
      41:     {
      42:       name: "agent_cross_validate",
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 73. `create_template`

**Server**: whatsapp-mcp (`nakulben/whatsapp-mcp`)

Source: `whatsapp_mcp/server.py:202`

```python
     200: 
     201: 
>>>  202: @mcp.tool()
     203: async def create_template(
     204:     name: str,
     205:     category: str,
     206:     language: str,
     207:     components: list[dict],
     208: ) -> str:
     209:     """
     210:     Create and submit a WhatsApp template to Meta for approval.
     211: 
     212:     The template will go through Meta's review process. Check status
     213:     with check_template_status after submission.
     214: 
     215:     Args:
     216:         name: Template name (lowercase, underscores, starts with letter, max 512)
     217:         category: MARKETING or UTILITY
     218:         language: Language code (e.g. "en", "en_US", "hi")
     219:         components: List of component dicts. Each has a "type" (HEADER, BODY,
     220:             FOOTER, BUTTONS) and type-specific fields. Example:
     221:             [
     222:                 {"type": "HEADER", "format": "TEXT", "text": "Hello {{1}}",
     223:                  "example": {"header_text": ["John"]}},
     224:                 {"type": "BODY", "text": "Your order {{1}} is {{2}}.",
     225:                  "example": {"body_text": [["ORD-123", "confirmed"]]}},
     226:                 {"type": "FOOTER", "text": "Reply STOP to opt out"},
     227:                 {"type": "BUTTONS", "buttons": [
     228:                     {"type": "QUICK_REPLY", "text": "Track Order"},
     229:                     {"type": "URL", "text": "View Details",
     230:                      "url": "https://example.com/order/{{1}}",
     231:                      "example": ["https://example.com/order/123"]}
     232:                 ]}
     233:             ]
     234: 
     235:     Returns:
     236:         JSON with template ID and status on success, or error details.
     237:     """
     238:     try:
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 74. `deposit_trx`

**Server**: merx-mcp (`Hovsteder/merx-mcp`)
**Description**: Deposit TRX to your Merx account. Requires MERX_API_KEY + TRON_PRIVATE_KEY.

Source: `src/tools/payments.ts:108`

```typescript
     106: 
     107: const depositTrxTool: McpTool = {
>>>  108:   name: 'deposit_trx',
     109:   description: 'Deposit TRX to your Merx account. Requires MERX_API_KEY + TRON_PRIVATE_KEY.',
     110:   inputSchema: {
     111:     type: 'object',
     112:     properties: { amount_trx: { type: 'string', description: 'Amount of TRX to deposit' } },
     113:     required: ['amount_trx'],
     114:   },
     115:   async handler(input) {
     116:     if (!hasApiKey()) return errorResult('MERX_API_KEY is required')
     117:     if (!hasPrivateKey()) return errorResult('TRON_PRIVATE_KEY is required')
     118:     try {
     119:       const amountTrx = parseFloat(input.amount_trx as string)
     120:       const tx = await signDepositTrx(Math.round(amountTrx * 1_000_000))
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 75. `contextkeeper_add_decision`

**Server**: workbench (`TheRealDataBoss/workbench`)

Source: `packages/python/contextkeeper/mcp_server.py:170`

```python
     168: 
     169: 
>>>  170: @mcp.tool()
     171: def contextkeeper_add_decision(
     172:     decision_id: str,
     173:     summary: str,
     174:     rationale: str = "",
     175:     made_by: str = "human",
     176: ) -> str:
     177:     """Add a decision to the latest handoff. Creates a new handoff version.
     178: 
     179:     Args:
     180:         decision_id: Decision ID in format DEC-XXXX
     181:         summary: Decision summary
     182:         rationale: Rationale for the decision
     183:         made_by: Who made the decision
     184:     """
     185:     try:
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 76. `book_appointment`

**Server**: dingdawg-agent-1 (`dingdawg/dingdawg-agent-1`)

Source: `gateway/isg_agent/mcp/tools/business_skill_tools.py:100`

```python
      98:     # -----------------------------------------------------------------------
      99: 
>>>  100:     @mcp.tool(
     101:         name="book_appointment",
     102:         description=(
     103:             "Schedule, cancel, reschedule, complete, or list appointments for a "
     104:             "DingDawg business agent. Actions: schedule, cancel, reschedule, "
     105:             "complete, list, get."
     106:         ),
     107:     )
     108:     async def book_appointment(
     109:         agent_handle: str,
     110:         action: str,
     111:         contact_name: Optional[str] = None,
     112:         contact_email: Optional[str] = None,
     113:         contact_phone: Optional[str] = None,
     114:         title: Optional[str] = None,
     115:         description: Optional[str] = None,
     116:         start_time: Optional[str] = None,
     117:         end_time: Optional[str] = None,
     118:         location: Optional[str] = None,
     119:         notes: Optional[str] = None,
     120:         appointment_id: Optional[str] = None,
     121:         status_filter: Optional[str] = None,
     122:     ) -> Dict[str, Any]:
     123:         """Manage appointments for a business agent."""
     124:         params: Dict[str, Any] = {}
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 77. `agent_changes_accept`

**Server**: Agestra (`mua-vtuber/Agestra`)
**Description**: Accept and merge file changes from an isolated worktree back to the main branch.

Source: `packages/mcp-server/src/tools/agent-session/tool-registry.ts:78`

```typescript
      76:     },
      77:     {
>>>   78:       name: "agent_changes_accept",
      79:       title: "Accept File Changes",
      80:       description: "Accept and merge file changes from an isolated worktree back to the main branch.",
      81:       inputSchema: zodToMcpSchema(AgentChangesAcceptSchema),
      82:     },
      83:     {
      84:       name: "agent_changes_reject",
      85:       title: "Reject File Changes",
      86:       description: "Reject file changes and clean up the isolated worktree.",
      87:       inputSchema: zodToMcpSchema(AgentChangesRejectSchema),
      88:     },
      89:     {
      90:       name: AGENT_DEBATE_STRUCTURED_TOOL,
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 78. `outlook_download_attachment`

**Server**: outlook-mcp (`mpalermiti/outlook-mcp`)

Source: `src/outlook_mcp/server.py:731`

```python
     729: 
     730: 
>>>  731: @mcp.tool()
     732: async def outlook_download_attachment(
     733:     ctx: Context,
     734:     message_id: str,
     735:     attachment_id: str,
     736:     save_path: str | None = None,
     737: ) -> dict:
     738:     """Download an attachment. Returns base64 content or saves to file."""
     739:     client = _get_graph_client(ctx)
     740:     return await mail_attachments.download_attachment(
     741:         client.sdk_client,
     742:         message_id,
     743:         attachment_id,
     744:         save_path,
     745:     )
     746: 
     747: 
     748: @mcp.tool()
     749: async def outlook_send_with_attachments(
     750:     ctx: Context,
     751:     to: list[str],
     752:     subject: str,
     753:     body: str,
     754:     attachment_paths: list[str],
     755:     cc: list[str] | None = None,
     756:     bcc: list[str] | None = None,
     757:     is_html: bool = False,
     758:     importance: str = "normal",
     759:     reply_to: list[str] | None = None,
     760: ) -> dict:
     761:     """Send a message with file attachments. Handles large files automatically.
     762: 
     763:     Pass ``reply_to`` to route recipient replies to a different address than
     764:     the authenticated sender.
     765:     """
     766:     client = _get_graph_client(ctx)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 79. `outlook_reply`

**Server**: outlook-mcp (`mpalermiti/outlook-mcp`)

Source: `src/outlook_mcp/server.py:209`

```python
     207: 
     208: 
>>>  209: @mcp.tool()
     210: async def outlook_reply(
     211:     ctx: Context,
     212:     message_id: str,
     213:     body: str,
     214:     reply_all: bool = False,
     215:     is_html: bool = False,
     216: ) -> dict:
     217:     """Reply or reply-all to a message."""
     218:     client = _get_graph_client(ctx)
     219:     config = _get_config(ctx)
     220:     return await mail_write.reply(
     221:         client.sdk_client, message_id, body, reply_all, is_html, config=config
     222:     )
     223: 
     224: 
     225: @mcp.tool()
     226: async def outlook_forward(
     227:     ctx: Context,
     228:     message_id: str,
     229:     to: list[str],
     230:     comment: str | None = None,
     231: ) -> dict:
     232:     """Forward a message to recipients."""
     233:     client = _get_graph_client(ctx)
     234:     config = _get_config(ctx)
     235:     return await mail_write.forward(client.sdk_client, message_id, to, comment, config=config)
     236: 
     237: 
     238: # ── Mail Triage Tools ───────────────────────────────────
     239: 
     240: 
     241: @mcp.tool()
     242: async def outlook_move_message(
     243:     ctx: Context,
     244:     message_id: str,
     245:     folder: str,
     246: ) -> dict:
     247:     """Move a message to a folder.
     248: 
     249:     `folder` accepts display names ("Junk Email", "Archive", "TLDR"), well-known
     250:     names ("inbox", "deleteditems"), or Graph IDs. Prefer names.
     251:     """
     252:     client = _get_graph_client(ctx)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 80. `filter_hub_profiles`

**Server**: srgplus-mcp (`srgplus/srgplus-mcp`)
**Description**: Batch-fetch lightweight hub profile data for a list of IDs.
**MCP Annotations**: readOnlyHint=true, destructiveHint=false

Source: `srg_mcp/hub_profiles.py:84`

```python
      82: 
      83: 
>>>   84: @mcp.tool(
      85:     annotations=ToolAnnotations(
      86:         title="Filter hub profiles",
      87:         readOnlyHint=True,
      88:         destructiveHint=False,
      89:         openWorldHint=True,
      90:     )
      91: )
      92: def filter_hub_profiles(
      93:     ids: list[str],
      94:     workspace_id: str,
      95:     availability_level: str | None = None,
      96: ) -> list[dict]:
      97:     """Batch-fetch lightweight hub profile data for a list of IDs.
      98: 
      99:     workspace_id: target workspace ID — get available IDs from list_workspaces()
     100:     availability_level: "Public" or "Private" to filter by visibility
     101:     """
     102:     return [
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 81. `measure_behavior`

**Server**: aga-mcp-server (`attestedintelligence/aga-mcp-server`)

Source: `src/server.ts:388`

```typescript
     386:   // TOOL: measure_behavior (NIST-2025-0035)
     387:   // ══════════════════════════════════════════════════════════════
>>>  388:   server.tool('measure_behavior',
     389:     'Measure behavioral patterns of agent tool usage. Detects unauthorized tools, rate violations, and forbidden sequences. (NIST-2025-0035)',
     390:     {},
     391:     async () => {
     392:       const measurement = behavioralMonitor.measure();
     393:       if (measurement.drift_detected) {
     394:         await autoChain('INTERACTION_RECEIPT', {
     395:           type: 'BEHAVIORAL_DRIFT',
     396:           violations: measurement.violations,
     397:           behavioral_hash: measurement.behavioral_hash,
     398:         });
     399:       }
     400:       return j({
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 82. `outlook_rename_folder`

**Server**: outlook-mcp (`mpalermiti/outlook-mcp`)
**Description**: Rename a mail folder.

Source: `src/outlook_mcp/server.py:841`

```python
     839: 
     840: 
>>>  841: @mcp.tool()
     842: async def outlook_rename_folder(
     843:     ctx: Context,
     844:     folder_id: str,
     845:     name: str,
     846: ) -> dict:
     847:     """Rename a mail folder."""
     848:     client = _get_graph_client(ctx)
     849:     config = _get_config(ctx)
     850:     return await mail_folders.rename_folder(
     851:         client.sdk_client,
     852:         folder_id,
     853:         name,
     854:         config=config,
     855:     )
     856: 
     857: 
     858: @mcp.tool()
     859: async def outlook_delete_folder(ctx: Context, folder_id: str) -> dict:
     860:     """Delete a user-created mail folder."""
     861:     client = _get_graph_client(ctx)
     862:     config = _get_config(ctx)
     863:     return await mail_folders.delete_folder(
     864:         client.sdk_client,
     865:         folder_id,
     866:         config=config,
     867:     )
     868: 
     869: 
     870: # ── Mail Thread Tools ─────────────────────────────────
     871: 
     872: 
     873: @mcp.tool()
     874: async def outlook_list_thread(
     875:     ctx: Context,
     876:     conversation_id: str,
     877:     count: int = 50,
     878: ) -> dict:
     879:     """List messages in a conversation thread, chronological order."""
     880:     client = _get_graph_client(ctx)
     881:     return await mail_thread.list_thread(client.sdk_client, conversation_id, count)
     882: 
     883: 
     884: @mcp.tool()
     885: async def outlook_copy_message(
     886:     ctx: Context,
     887:     message_id: str,
     888:     folder: str,
     889: ) -> dict:
     890:     """Copy a message to a folder.
     891: 
     892:     `folder` accepts display names, well-known names, or Graph IDs. Prefer names.
     893:     """
     894:     client = _get_graph_client(ctx)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 83. `query_hashrate`

**Server**: hive-mcp-mos (`srotzin/hive-mcp-mos`)
**Description**: Query the current hashrate telemetry for a registered MOS site. Returns TH/s per unit, pool-accepted shares, and varianc

Source: `src/index.js:45`

```javascript
      43: const TOOLS = [
      44:   {
>>>   45:     name: 'query_hashrate',
      46:     description: 'Query the current hashrate telemetry for a registered MOS site. Returns TH/s per unit, pool-accepted shares, and variance window. Read-only. Backend pending (Q3 2026).',
      47:     inputSchema: {
      48:       type: 'object',
      49:       required: ['site_did'],
      50:       properties: {
      51:         site_did: {
      52:           type: 'string',
      53:           description: 'Decentralized Identifier (DID) of the registered MOS site (e.g. did:hive:mos:0x...)',
      54:         },
      55:       },
      56:     },
      57:   },
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 84. `analyze_cnv`

**Server**: ChatSpatial (`cafferychen777/ChatSpatial`)
**Description**: Analyze copy number variations (CNVs) in spatial transcriptomics data.
**MCP Annotations**: readOnlyHint=false, idempotentHint=true, openWorldHint=false

Source: `chatspatial/server.py:390`

```python
     388: 
     389: 
>>>  390: @mcp.tool(
     391:     annotations=ToolAnnotations(
     392:         readOnlyHint=False,
     393:         idempotentHint=True,
     394:         openWorldHint=False,
     395:     )
     396: )
     397: @mcp_tool_error_handler()
     398: async def analyze_cnv(
     399:     data_id: str,
     400:     params: CNVParameters,
     401:     context: Optional[Context] = None,
     402: ) -> CNVResult:
     403:     """Analyze copy number variations (CNVs) in spatial transcriptomics data.
     404: 
     405:     Args:
     406:         data_id: Dataset identifier
     407:         params: Required - reference_key, reference_categories, and optional method/thresholds.
     408:     """
     409:     ctx = ToolContext(_data_manager=data_manager, _mcp_context=context)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 85. `supply_assets`

**Server**: starkfi (`ahmetenesdur/starkfi`)
**Description**: Supply (lend) tokens into a Vesu V2 pool to earn interest as an earn position.

Source: `src/mcp/tools/lending.ts:56`

```typescript
      54:   );
      55: 
>>>   56:   server.registerTool(
      57:     "supply_assets",
      58:     {
      59:       description:
      60:         "Supply (lend) tokens into a Vesu V2 pool to earn interest as an earn position.",
      61:       inputSchema: z.object({
      62:         pool: z
      63:           .string()
      64:           .describe("Pool name (e.g. 'Prime', 'Re7') or contract address (0x...)"),
      65:         amount: z.string().describe("Amount to supply (e.g. '100', '0.5')"),
      66:         token: z.string().describe("Token symbol to supply (e.g. 'STRK', 'ETH', 'USDC')"),
      67:         simulate: z
      68:           .boolean()
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 86. `ping`

**Server**: claude-mcp-bridge (`hampsterx/claude-mcp-bridge`)

Source: `src/index.ts:316`

```typescript
     314: // --- ping tool ---
     315: 
>>>  316: server.registerTool(
     317:   "ping",
     318:   {
     319:     title: "Health Check",
     320:     description: pingDescription,
     321:     inputSchema: {},
     322:     annotations: pingAnnotations,
     323:   },
     324:   async () => {
     325:     const start = Date.now();
     326:     try {
     327:       const result = await executePing();
     328:       const lines = [
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 87. `cc_cleanup_file`

**Server**: ellmos-codecommander-mcp (`ellmos-ai/ellmos-codecommander-mcp`)

Source: `src/index.ts:1136`

```typescript
    1134: // ============================================================================
    1135: 
>>> 1136: server.registerTool(
    1137:   "cc_cleanup_file",
    1138:   {
    1139:     title: "Cleanup File",
    1140:     description: `Cleans up source code files: BOM, NUL bytes, trailing whitespace, line endings.
    1141: 
    1142: Args:
    1143:   - path (string): Path to the file
    1144:   - remove_bom (boolean): Remove BOM
    1145:   - remove_trailing_whitespace (boolean): Trailing whitespace
    1146:   - normalize_line_endings (string): "lf" | "crlf"
    1147:   - remove_nul_bytes (boolean): Remove NUL bytes
    1148:   - dry_run (boolean): Preview only`,
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: might show preview first as stated in the parameters before user saves

---
## 88. `delete_invitation`

**Server**: srgplus-mcp (`srgplus/srgplus-mcp`)
**Description**: Cancel and permanently delete a pending invitation.
**MCP Annotations**: readOnlyHint=false, destructiveHint=true

Source: `srg_mcp/users.py:222`

```python
     220: 
     221: 
>>>  222: @mcp.tool(
     223:     annotations=ToolAnnotations(
     224:         title="Delete invitation",
     225:         readOnlyHint=False,
     226:         destructiveHint=True,
     227:         openWorldHint=True,
     228:     )
     229: )
     230: def delete_invitation(
     231:     hub_profile_id: str,
     232:     invitation_id: str,
     233:     workspace_id: str,
     234: ) -> str:
     235:     """Cancel and permanently delete a pending invitation.
     236: 
     237:     workspace_id: target workspace ID — get available IDs from list_workspaces()
     238:     """
     239:     get_client().invitations.delete(
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 89. `swap_tokens`

**Server**: starkfi (`ahmetenesdur/starkfi`)
**Description**: Execute a token swap via Fibrous (default) or a specified provider. Set simulate=true to estimate fees without executing

Source: `src/mcp/tools/trade.ts:43`

```typescript
      41:   );
      42: 
>>>   43:   server.registerTool(
      44:     "swap_tokens",
      45:     {
      46:       description:
      47:         "Execute a token swap via Fibrous (default) or a specified provider. Set simulate=true to estimate fees without executing. ONLY call this after showing the user a quote via get_swap_quote.",
      48:       inputSchema: z.object({
      49:         amount: z.string().describe("Amount to swap in (e.g. '0.1', '100')"),
      50:         from_token: z.string().describe("Source token symbol to sell (e.g. 'ETH', 'STRK')"),
      51:         to_token: z
      52:           .string()
      53:           .describe("Destination token symbol to buy (e.g. 'USDC', 'DAI')"),
      54:         slippage: z.number().optional().describe("Slippage tolerance % (default: 1)"),
      55:         simulate: z
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 90. `convert_address`

**Server**: merx-mcp (`Hovsteder/merx-mcp`)
**Description**: Convert TRON address between base58 (T...) and hex (41...) formats. No auth required.

Source: `src/tools/network.ts:35`

```typescript
      33: 
      34: const convertAddress: McpTool = {
>>>   35:   name: 'convert_address',
      36:   description: 'Convert TRON address between base58 (T...) and hex (41...) formats. No auth required.',
      37:   inputSchema: {
      38:     type: 'object',
      39:     properties: {
      40:       address: {
      41:         type: 'string',
      42:         description: 'TRON address in base58 (T...) or hex (41...).',
      43:       },
      44:     },
      45:     required: ['address'],
      46:   },
      47:   async handler(input) {
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 91. `pg_connect`

**Server**: mcp-postgres (`itunified-io/mcp-postgres`)
**Description**: Connect to a PostgreSQL server target. If multiple targets are configured, specify which one. Otherwise connects to the default target.

Source: `src/tools.ts:12`

```typescript
      10:   // ── Connection (5 tools) ────────────────────────────────────────────
      11:   {
>>>   12:     name: "pg_connect",
      13:     description:
      14:       "Connect to a PostgreSQL server target. If multiple targets are configured, specify which one. Otherwise connects to the default target.",
      15:     inputSchema: {
      16:       target,
      17:       profile: z.string().optional().describe("Named connection profile (optional, uses default if omitted)"),
      18:     },
      19:     domain: "pg",
      20:     action: "connect add",
      21:   },
      22:   {
      23:     name: "pg_disconnect",
      24:     description: "Disconnect from a PostgreSQL server target. Omit profile to disconnect all.",
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 92. `get_receipts`

**Server**: aga-mcp-server (`attestedintelligence/aga-mcp-server`)
**Description**: Get all signed receipts, optionally filtered by artifact.

Source: `src/server.ts:411`

```typescript
     409:   // TOOL: get_receipts - V3 NEW
     410:   // ══════════════════════════════════════════════════════════════
>>>  411:   server.tool('get_receipts', 'Get all signed receipts, optionally filtered by artifact.',
     412:     { artifact_hash: z.string().optional() },
     413:     async ({ artifact_hash }) => {
     414:       const receipts = artifact_hash
     415:         ? await storage.getReceiptsByArtifact(artifact_hash)
     416:         : await storage.getAllReceipts();
     417:       return j({ count: receipts.length, receipts: receipts.map(r => ({ receipt_id: r.receipt_id, drift_detected: r.drift_detected, enforcement_action: r.enforcement_action, measurement_type: r.measurement_type, timestamp: r.timestamp })) });
     418:     }
     419:   );
     420: 
     421:   // ══════════════════════════════════════════════════════════════
     422:   // TOOL: get_chain_events - V3 NEW
     423:   // ══════════════════════════════════════════════════════════════
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 93. `agent_debate_create`

**Server**: Agestra (`mua-vtuber/Agestra`)
**Description**: Create a turn-based debate session. Returns a debate ID for use with agent_debate_turn and agent_debate_conclude.

Source: `packages/mcp-server/src/tools/agent-session/tool-registry.ts:48`

```typescript
      46:     },
      47:     {
>>>   48:       name: "agent_debate_create",
      49:       title: "Create Turn-Based Debate",
      50:       description: "Create a turn-based debate session. Returns a debate ID for use with agent_debate_turn and agent_debate_conclude.",
      51:       inputSchema: zodToMcpSchema(AgentDebateCreateSchema),
      52:     },
      53:     {
      54:       name: "agent_debate_turn",
      55:       title: "Execute Debate Turn",
      56:       description: "Execute one provider's turn in a debate. Optionally inject Claude's comment before the provider responds. Returns the provider's response. Use provider: \"claude\" with claude_comment to record Claude's own independent opinion as a debate turn.",
      57:       inputSchema: zodToMcpSchema(AgentDebateTurnSchema),
      58:     },
      59:     {
      60:       name: "agent_debate_conclude",
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 94. `list_workspaces`

**Server**: srgplus-mcp (`srgplus/srgplus-mcp`)
**Description**: List all workspaces accessible with the current API key(s).
**MCP Annotations**: readOnlyHint=true, destructiveHint=false

Source: `srg_mcp/workspaces.py:6`

```python
       4: 
       5: 
>>>    6: @mcp.tool(
       7:     annotations=ToolAnnotations(
       8:         title="List workspaces",
       9:         readOnlyHint=True,
      10:         destructiveHint=False,
      11:         openWorldHint=True,
      12:     )
      13: )
      14: def list_workspaces() -> list[dict]:
      15:     """List all workspaces accessible with the current API key(s).
      16: 
      17:     When multiple API keys were provided during OAuth, this returns all workspaces
      18:     across all keys. Use the workspace_id from this list to target a specific
      19:     workspace in any other tool that requires a workspace_id parameter.
      20:     """
      21:     client = get_client()
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 95. `claim_rewards`

**Server**: starkfi (`ahmetenesdur/starkfi`)
**Description**: Extract earned rewards from a delegation staking pool to the user

Source: `src/mcp/tools/staking.ts:121`

```typescript
     119:   );
     120: 
>>>  121:   server.registerTool(
     122:     "claim_rewards",
     123:     {
     124:       description:
     125:         "Extract earned rewards from a delegation staking pool to the user's wallet. WARNING: This ONLY works with delegation pools, NOT with Endur LST positions (use get_lst_position instead — LST yield is embedded in share price).",
     126:       inputSchema: z.object({
     127:         pool: z.string().describe("Staking pool contract address (0x...)"),
     128:       }),
     129:       annotations: { readOnlyHint: false, destructiveHint: true, idempotentHint: false },
     130:     },
     131:     withErrorHandling(handleClaimRewards)
     132:   );
     133: 
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 96. `export_multi_device`

**Server**: rawtherapee-mcp-server (`lucamarien/rawtherapee-mcp-server`)

Source: `src/rawtherapee_mcp/server.py:1709`

```python
    1707: 
    1708: 
>>> 1709: @mcp.tool()
    1710: async def export_multi_device(
    1711:     ctx: Context,
    1712:     file_path: str,
    1713:     profile_path: str,
    1714:     device_presets: list[str],
    1715:     output_format: str = "jpeg",
    1716:     output_dir: str | None = None,
    1717:     include_previews: bool = False,
    1718:     preview_max_width: int = 600,
    1719: ) -> dict[str, Any] | ToolResult:
    1720:     """Export a RAW file optimized for multiple devices in one call.
    1721: 
    1722:     Processes the same RAW file with device-specific crop/resize for each
    1723:     target device. Output filenames include the device name. Set
    1724:     include_previews=True to return inline thumbnails per export.
    1725:     Params: file_path, profile_path, device_presets, output_format, output_dir,
    1726:     include_previews, preview_max_width
    1727:     """
    1728:     config = get_config(ctx)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 97. `index_cortex_docs`

**Server**: cortex-cloud-docs-mcp-server (`clarkemn/cortex-cloud-docs-mcp-server`)
**Description**: Index Cortex Cloud documentation. Call this first before searching.

Source: `src/main.py:209`

```python
     207:     return json.dumps(results, indent=2)
     208: 
>>>  209: @mcp.tool()
     210: async def index_cortex_docs(max_pages: int = 50) -> str:
     211:     """Index Cortex Cloud documentation. Call this first before searching."""
     212:     pages_indexed = await indexer.index_site('cortex_cloud', max_pages)
     213:     return f"Indexed {pages_indexed} pages from Cortex Cloud documentation"
     214: 
     215: @mcp.tool()
     216: async def index_cortex_api_docs(max_pages: int = 50) -> str:
     217:     """Index Cortex Cloud API documentation. Call this first before searching."""
     218:     pages_indexed = await indexer.index_site('cortex_api', max_pages)
     219:     return f"Indexed {pages_indexed} pages from Cortex Cloud API documentation"
     220: 
     221: @mcp.tool()
     222: async def get_index_status() -> str:
     223:     """Check how many documents are currently cached."""
     224:     total_docs = len(indexer.cached_pages)
     225:     sites = {}
     226:     for page in indexer.cached_pages.values():
     227:         site = page.site
     228:         sites[site] = sites.get(site, 0) + 1
     229: 
     230:     # Also show cache statistics
     231:     expired_count = sum(1 for page in indexer.cached_pages.values() if page.is_expired)
     232: 
     233:     return json.dumps({
     234:         'total_cached_pages': total_docs,
     235:         'expired_pages': expired_count,
     236:         'search_cache_entries': len(indexer.search_cache),
     237:         'by_site': sites
     238:     }, indent=2)
     239: 
     240: def main():
     241:     """Main entry point for HTTP mode deployment"""
     242:     print("MCP Server starting in HTTP mode...")
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 98. `xpath_save_screenshot`

**Server**: uiautomator2-mcp-server (`tanbro/uiautomator2-mcp-server`)
**Description**: Find element by XPath and save screenshot to file.

Source: `src/u2mcp/tools/xpath.py:136`

```python
     134: 
     135: 
>>>  136: @mcp.tool("xpath_save_screenshot", tags={"xpath:capture"})
     137: async def xpath_save_screenshot(serial: str, xpath: str, file: str) -> str:
     138:     """Find element by XPath and save screenshot to file.
     139: 
     140:     Args:
     141:         serial (str): Android device serial number.
     142:         xpath (str): Element XPath expression.
     143:         file (str): File path to save the screenshot. Format determined by extension.
     144: 
     145:     Returns:
     146:         str: Absolute path to the saved screenshot file.
     147:     """
     148:     async with get_device(serial) as device:
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 99. `get_record`

**Server**: odoo-mcp-gateway (`parth-unjiya/odoo-mcp-gateway`)
**Description**: Read a single record by ID from any Odoo model.

Source: `src/odoo_mcp_gateway/tools/crud.py:295`

```python
     293:             return {"error": gateway.sanitize_error(e)}
     294: 
>>>  295:     @server.tool()
     296:     async def get_record(
     297:         model: str,
     298:         record_id: int,
     299:         fields: list[str] | None = None,
     300:     ) -> dict[str, Any]:
     301:         """Read a single record by ID from any Odoo model."""
     302:         try:
     303:             model = _validate_model(model)
     304:             if record_id <= 0:
     305:                 return {"error": "record_id must be a positive integer"}
     306:             client = _get_client(gateway)
     307:             auth_mgr = _get_auth_manager(gateway)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: read

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 100. `outlook_create_folder`

**Server**: outlook-mcp (`mpalermiti/outlook-mcp`)
**Description**: Create a mail folder, optionally under a parent folder.

Source: `src/outlook_mcp/server.py:824`

```python
     822: 
     823: 
>>>  824: @mcp.tool()
     825: async def outlook_create_folder(
     826:     ctx: Context,
     827:     name: str,
     828:     parent_folder: str | None = None,
     829: ) -> dict:
     830:     """Create a mail folder, optionally under a parent folder."""
     831:     client = _get_graph_client(ctx)
     832:     config = _get_config(ctx)
     833:     return await mail_folders.create_folder(
     834:         client.sdk_client,
     835:         name,
     836:         parent_folder,
     837:         config=config,
     838:     )
     839: 
     840: 
     841: @mcp.tool()
     842: async def outlook_rename_folder(
     843:     ctx: Context,
     844:     folder_id: str,
     845:     name: str,
     846: ) -> dict:
     847:     """Rename a mail folder."""
     848:     client = _get_graph_client(ctx)
     849:     config = _get_config(ctx)
     850:     return await mail_folders.rename_folder(
     851:         client.sdk_client,
     852:         folder_id,
     853:         name,
     854:         config=config,
     855:     )
     856: 
     857: 
     858: @mcp.tool()
     859: async def outlook_delete_folder(ctx: Context, folder_id: str) -> dict:
     860:     """Delete a user-created mail folder."""
     861:     client = _get_graph_client(ctx)
     862:     config = _get_config(ctx)
     863:     return await mail_folders.delete_folder(
     864:         client.sdk_client,
     865:         folder_id,
     866:         config=config,
     867:     )
     868: 
     869: 
     870: # ── Mail Thread Tools ─────────────────────────────────
     871: 
     872: 
     873: @mcp.tool()
     874: async def outlook_list_thread(
     875:     ctx: Context,
     876:     conversation_id: str,
     877:     count: int = 50,
     878: ) -> dict:
     879:     """List messages in a conversation thread, chronological order."""
     880:     client = _get_graph_client(ctx)
```

**Your classification** -- write exactly one of: `read`, `write`, `unknown`
ANSWER: write

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
