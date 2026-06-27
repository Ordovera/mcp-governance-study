# Coding Task B: Sensitivity Classification (100 tools)

You are an independent second coder. For each tool below, read the name,
read/write flag, description, and source excerpt, then decide whether the tool
is **sensitive** or **non-sensitive** using the single decision rule:

**Sensitivity rule**: if the tool's output or action would be subject to access
control, audit requirements, or regulatory obligations in a well-governed
deployment, classify it as **sensitive**. This is orthogonal to read/write -- a
read-only tool that returns credentials, PII, financial, medical, or legal data
is sensitive.

- **sensitive** -- affects confidentiality, integrity, availability, autonomy, or accountability.
- **non-sensitive** -- routine operations with no governance-relevant data or actions.

For each tool, type your answer on the `ANSWER:` line directly beneath it, and any
notes on the `NOTES:` line. Edit this same file and send it back -- one file, no
spreadsheet. Code only from what you see here; do not look for the project's own labels.

---

## 1. `get_market_info`

**Server**: haeminmoon/pacifica-cli
**Read/Write**: read
**Description**: Get market info for all available instruments

Source: `mcp.ts:30`

```typescript
    27: 
    28: // ─── Market Data Tools ─────────────────────────────────────────────────
    29: 
>>> 30: server.tool("get_market_info", "Get market info for all available instruments", {}, async () => {
    31:   return withErrorHandling(() => createPublicClient().getMarketInfo());
    32: });
    33: 
    34: server.tool("get_prices", "Get price information for all symbols", {}, async () => {
    35:   return withErrorHandling(() => createPublicClient().getPrices());
    36: });
    37: 
    38: server.tool(
    39:   "get_orderbook",
    40:   "Get orderbook for a trading symbol",
    41:   { symbol: z.string().describe("Trading symbol (e.g. BTC)"), agg_level: z.number().optional().describe("Aggregation level") },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 2. `agent_spawn`

**Server**: ruvnet/claude-flow
**Read/Write**: unknown
**Description**: Spawn a new agent in the swarm (V2 compatible). Deprecated: Use agent/spawn instead.

Source: `v2-compat-tools.js:150`

```typescript
    147:  * agent_spawn - V2 compatible agent spawning
    148:  */
    149: export const agentSpawnTool = {
>>> 150:     name: 'agent_spawn',
    151:     description: 'Spawn a new agent in the swarm (V2 compatible). Deprecated: Use agent/spawn instead.',
    152:     inputSchema: {
    153:         type: 'object',
    154:         properties: {
    155:             type: { type: 'string', description: 'Agent type' },
    156:             name: { type: 'string', description: 'Custom agent name' },
    157:             capabilities: { type: 'array', items: { type: 'string' }, description: 'Agent capabilities' },
    158:         },
    159:         required: ['type'],
    160:     },
    161:     handler: async (input, context) => {
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 3. `opengrok_update_memory`

**Server**: IcyHot09/opengrok-mcp-server
**Read/Write**: write
**Description**: Write or append to active-task.md or investigation-log.md.

Source: `code-mode.test.ts:248`

```typescript
    245: 
    246:   it('opengrok_update_memory writes content to bank', async () => {
    247:     const { client } = await createCodeModeClient(bank);
>>> 248:     await client.callTool({ name: 'opengrok_update_memory', arguments: { filename: 'active-task.md', content: 'New context', mode: 'overwrite' } });
    249:     const content = await bank.read('active-task.md');
    250:     expect(content).toContain('New context');
    251:     await client.close();
    252:   });
    253: 
    254:   it('opengrok_update_memory in append mode appends content', async () => {
    255:     await bank.write('investigation-log.md', '## 2025-01-01: First entry\nInitial finding.');
    256:     const { client } = await createCodeModeClient(bank);
    257:     await client.callTool({ name: 'opengrok_update_memory', arguments: { filename: 'investigation-log.md', content: '## 2025-01-02: Second\nNew finding.', mode: 'append' } });
    258:     const content = await bank.read('investigation-log.md');
    259:     expect(content).toContain('First entry');
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 4. `deep_research_report`

**Server**: nahisaho/MUSUBIX
**Read/Write**: read
**Description**: Get final report from completed deep research session

Source: `tools.ts:74`

```typescript
    71:  * Get final research report (markdown or JSON).
    72:  */
    73: export interface DeepResearchReportTool {
>>> 74:   name: 'deep_research_report';
    75:   description: 'Get final report from completed deep research session';
    76:   inputSchema: {
    77:     type: 'object';
    78:     properties: {
    79:       researchId: {
    80:         type: 'string';
    81:         description: 'Research session ID';
    82:       };
    83:       format: {
    84:         type: 'string';
    85:         enum: ['markdown', 'json'];
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: deep research seems to suggest sensitivity

---
## 5. `get_org_plan`

**Server**: cachly-dev/cachly-mcp
**Read/Write**: read
**Description**: Get the current org plan, seat usage, and billing info for an organization.

Source: `tools.ts:1179`

```typescript
    1176:     },
    1177:   },
    1178:   {
>>> 1179:     name: 'get_org_plan',
    1180:     description:
    1181:       'Get the current org plan, seat usage, and billing info for an organization. ' +
    1182:       'Shows: plan name, price, seats used/max, next billing date. ' +
    1183:       'To upgrade: use the billing portal URL returned by this tool.',
    1184:     inputSchema: {
    1185:       type: 'object',
    1186:       properties: {
    1187:         org_id: { type: 'string', description: 'UUID of the organization' },
    1188:       },
    1189:       required: ['org_id'],
    1190:     },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 6. `multiply`

**Server**: datalayer/mcp-server-composer
**Read/Write**: unknown
**Description**: Multiply two numbers.

Source: `mcp1.py:46`

```python
    43: 
    44: 
    45: @mcp.tool()
>>> 46: def multiply(a: float, b: float) -> float:
    47:     """Multiply two numbers.
    48:     
    49:     Args:
    50:         a: First number
    51:         b: Second number
    52:         
    53:     Returns:
    54:         Product of a and b
    55:     """
    56:     return a * b
    57: 
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 7. `ActivateObjects`

**Server**: fr0ster/mcp-abap-adt
**Read/Write**: write
**Description**: Activate one or multiple ABAP repository objects. Use after Create/Update when objects remain inactive, or for group activation of related objects (e.g., domains + data elements + tables together). Works with any object type.

Source: `handleActivateObjects.ts:12`

```typescript
    9: import { handleActivateObject } from '../low/handleActivateObject';
    10: 
    11: export const TOOL_DEFINITION = {
>>> 12:   name: 'ActivateObjects',
    13:   available_in: ['onprem', 'cloud', 'legacy'] as const,
    14:   description:
    15:     'Activate one or multiple ABAP repository objects. Use after Create/Update when objects remain inactive, or for group activation of related objects (e.g., domains + data elements + tables together). Works with any object type.',
    16:   inputSchema: {
    17:     type: 'object',
    18:     properties: {
    19:       objects: {
    20:         type: 'array',
    21:         description:
    22:           "Array of objects to activate. Each object must have 'name' and 'type'.",
    23:         items: {
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 8. `memory_search_unified`

**Server**: ruvnet/claude-flow
**Read/Write**: read
**Description**: Search across both Claude Code memories and AgentDB entries using semantic vector similarity. Returns merged, deduplicated results from all namespaces. Use when native Read/Write is wrong because you need (a) cross-session retrieval by semantic similarity (vector embeddings) not by file path, (b) namespacing across projects without managing directory layout, or (c) the .swarm/memory.db audit trail. For one-shot file I/O, native Read/Write is fine.

*(Source not available -- classify from name and description.)*

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: audit trail is mentioned

---
## 9. `soul_profile`

**Server**: drivenbymyai-max/mcp-sputnikx-market
**Read/Write**: read
**Description**: Agent identity profile — trust score, behavioral DNA, character traits, SX# passport

Source: `index.mjs:313`

```typescript
    310:     },
    311:     // ── SoulLedger Agent Identity ──
    312:     {
>>> 313:       name: 'soul_profile',
    314:       description: 'Agent identity profile — trust score, behavioral DNA, character traits, SX# passport',
    315:       inputSchema: {
    316:         type: 'object',
    317:         properties: {
    318:           agent_id: { type: 'string', description: 'Agent identifier (e.g., oracle, spider-code)' },
    319:         },
    320:         required: ['agent_id'],
    321:       },
    322:     },
    323:     {
    324:       name: 'soul_verify',
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 10. `sqlite_transaction_rollback`

**Server**: neverinfamous/db-mcp
**Read/Write**: unknown
**Description**: Rollback the current transaction, discarding all changes.

Source: `transactions.ts:152`

```typescript
    149:   adapter: NativeSqliteAdapter,
    150: ): ToolDefinition {
    151:   return {
>>> 152:     name: "sqlite_transaction_rollback",
    153:     description: "Rollback the current transaction, discarding all changes.",
    154:     group: "admin",
    155:     outputSchema: TransactionRollbackOutputSchema,
    156:     inputSchema: z.object({}),
    157:     annotations: write("Rollback Transaction"),
    158:     requiredScopes: ["write"],
    159:     handler: (_params: unknown, _context: RequestContext) => {
    160:       try {
    161:         adapter.rollbackTransaction();
    162: 
    163:         return Promise.resolve({
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 11. `security_quick_scan`

**Server**: nahisaho/MUSUBIX
**Read/Write**: read
**Description**: Quick vulnerability scan without taint analysis, secret detection, or dependency audit.

Source: `tools.ts:88`

```typescript
    85:     },
    86:   },
    87:   {
>>> 88:     name: 'security_quick_scan',
    89:     description: 'Quick vulnerability scan without taint analysis, secret detection, or dependency audit.',
    90:     inputSchema: {
    91:       type: 'object',
    92:       properties: {
    93:         target: {
    94:           type: 'string',
    95:           description: 'Target path to scan',
    96:         },
    97:       },
    98:       required: ['target'],
    99:     },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 12. `get_transport_classification`

**Server**: littleblakew/msds-chain-mcp
**Read/Write**: read
**Description**: Get UN transport classification for chemicals (dangerous goods shipping).

Source: `server.py:497`

```python
    494: 
    495: 
    496: @mcp.tool()
>>> 497: async def get_transport_classification(chemicals: list[str]) -> str:
    498:     """Get UN transport classification for chemicals (dangerous goods shipping).
    499:     Returns UN number, proper shipping name, hazard class, packing group,
    500:     and transport mode details (ADR road, IATA air, IMDG sea).
    501:     Args:
    502:         chemicals: List of chemical names or CAS numbers
    503:     """
    504:     t0 = time.monotonic()
    505:     error_msg = None
    506:     success = True
    507:     try:
    508:         message = f"What is the UN transport classification for {', '.join(chemicals)}?"
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 13. `list_recent_briefs`

**Server**: Advanced-Binary-Operations/QuReDec_MCP
**Read/Write**: read
**Description**: List the caller's most recent decision briefs.

Source: `server.py:163`

```python
    160: 
    161: 
    162: @mcp.tool()
>>> 163: def list_recent_briefs(limit: int = 20) -> dict[str, Any]:
    164:     """List the caller's most recent decision briefs.
    165: 
    166:     Use this to find a prior brief by id, share an old brief again, or check
    167:     what decisions have been logged for this account.
    168: 
    169:     Args:
    170:         limit: Max briefs to return (default 20, valid range 1-100).
    171: 
    172:     Returns:
    173:         {items: [{brief_run_id, status, progress, status_url,
    174:                   public_share_url, created_at}, ...], count}.
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 14. `list_global_environment_variables`

**Server**: deployhq/deployhq-mcp-server
**Read/Write**: read
**Description**: List all global (account-level) environment variables. These variables are available across all projects in the account. Returns variable names, masked values, and settings.

Source: `tools.ts:294`

```typescript
    291:     },
    292:   },
    293:   {
>>> 294:     name: 'list_global_environment_variables',
    295:     description:
    296:       'List all global (account-level) environment variables. These variables are available across all projects in the account. Returns variable names, masked values, and settings.',
    297:     annotations: {
    298:       readOnlyHint: true,
    299:       destructiveHint: false,
    300:     },
    301:     inputSchema: {
    302:       type: 'object',
    303:       properties: {},
    304:     },
    305:   },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 15. `emergency_status`

**Server**: codeofaxel/Kiln
**Read/Write**: read
**Description**: Get the emergency stop latch status for one printer or the entire fleet.

Source: `emergency.py:913`

```python
    910:     return get_emergency_coordinator().emergency_stop_all(reason=reason, source=source, note=note)
    911: 
    912: 
>>> 913: def emergency_status(printer_id: str) -> dict[str, Any]:
    914:     """Return emergency latch status for a single printer."""
    915:     return get_emergency_coordinator().get_latch_status(printer_id)
    916: 
    917: 
    918: def clear_emergency_stop(
    919:     printer_id: str,
    920:     *,
    921:     acknowledged_by: str | None = None,
    922:     ack_note: str | None = None,
    923: ) -> dict[str, Any]:
    924:     """Acknowledge and clear emergency stop state for a printer."""
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 16. `healthcare/literature-search`

**Server**: ruvnet/claude-flow
**Read/Write**: read
**Description**: Search medical literature with semantic understanding. Supports PubMed, Cochrane, and UpToDate sources with evidence level filtering.

Source: `mcp-tools.ts:508`

```typescript
    505: }
    506: 
    507: export const literatureSearchTool: MCPTool = {
>>> 508:   name: 'healthcare/literature-search',
    509:   description: 'Search medical literature with semantic understanding. Supports PubMed, Cochrane, and UpToDate sources with evidence level filtering.',
    510:   category: 'healthcare',
    511:   version: '1.0.0',
    512:   tags: ['literature', 'search', 'pubmed', 'evidence', 'research'],
    513:   cacheable: true,
    514:   cacheTTL: 3600000, // 1 hour
    515:   inputSchema: {
    516:     type: 'object',
    517:     properties: {
    518:       query: { type: 'string', description: 'Search query' },
    519:       sources: { type: 'array', items: { type: 'string' }, description: 'Literature sources to search' },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 17. `Security Agent`

**Server**: ruvnet/claude-flow
**Read/Write**: read
**Description**: Security-focused agent for code auditing, vulnerability scanning, and threat detection. 15 built-in security controls including path traversal, injection, and credential protection.

*(Source not available -- classify from name and description.)*

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 18. `peptide_properties`

**Server**: JonasRackl/labmate-mcp
**Read/Write**: read
**Description**: Compute peptide molecular properties from SMILES: molecular weight, formula, logP, TPSA, H-bond donors/acceptors, rotatable bonds, ring count, fraction Csp3, heavy atoms, formal charge, and Lipinski Rule-of-5 evaluation.

Source: `server.py:4277`

```python
    4274: 
    4275: 
    4276: @mcp.tool()
>>> 4277: async def peptide_properties(params: PeptidePropertiesInput) -> str:
    4278:     """Compute peptide molecular properties from SMILES: molecular weight, formula, logP, TPSA, H-bond donors/acceptors, rotatable bonds, ring count, fraction Csp3, heavy atoms, formal charge, and Lipinski Rule-of-5 evaluation."""
    4279:     try:
    4280:         result = get_peptide_properties(params.smiles)
    4281:         lines = ["**Peptide Molecular Properties**"]
    4282:         for k, v in result.items():
    4283:             if k == "SMILES":
    4284:                 continue
    4285:             lines.append(f"  {k}: {v}")
    4286:         return "\n".join(lines)
    4287:     except Exception as e:
    4288:         return f"Error: {e}"
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 19. `create_session_login_token`

**Server**: onelogin/onelogin-mcp
**Read/Write**: read
**Description**: Authenticate a user and create a session token for custom login flows. Provide username/email and password. If MFA not required: returns session_token immediately for SSO access. If MFA required: returns state_token, devices (available MFA factors with device_id), and user info - must then call verify_session_factor. Use subdomain parameter to specify OneLogin account. Returns authentication result with session data or MFA challenge and x-request-id.

Source: `sessions.js:97`

```typescript
    94:  */
    95: export const tools = [
    96:   {
>>> 97:     name: 'create_session_login_token',
    98:     description: 'Authenticate a user and create a session token for custom login flows. Provide username/email and password. If MFA not required: returns session_token immediately for SSO access. If MFA required: returns state_token, devices (available MFA factors with device_id), and user info - must then call verify_session_factor. Use subdomain parameter to specify OneLogin account. Returns authentication result with session data or MFA challenge and x-request-id.',
    99:     inputSchema: {
    100:       type: 'object',
    101:       properties: {
    102:         username_or_email: {
    103:           type: 'string',
    104:           description: 'Username or email address'
    105:         },
    106:         password: {
    107:           type: 'string',
    108:           description: 'User password'
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 20. `generate_invite_link`

**Server**: onelogin/onelogin-mcp
**Read/Write**: write
**Description**: Generate a password reset invite link for an existing user in OneLogin. Returns the link URL but does NOT send any email - use send_invite_link to email it. Provide link to user to enable them to set password and access OneLogin portal. Email parameter is case-sensitive. Returns invite link and x-request-id (API v1 - Rate Limited).

Source: `invite-links.js:44`

```typescript
    41:  */
    42: export const tools = [
    43:   {
>>> 44:     name: 'generate_invite_link',
    45:     description: 'Generate a password reset invite link for an existing user in OneLogin. Returns the link URL but does NOT send any email - use send_invite_link to email it. Provide link to user to enable them to set password and access OneLogin portal. Email parameter is case-sensitive. Returns invite link and x-request-id (API v1 - Rate Limited).',
    46:     inputSchema: {
    47:       type: 'object',
    48:       properties: {
    49:         email: {
    50:           type: 'string',
    51:           description: 'User email address'
    52:         },
    53:         firstname: {
    54:           type: 'string',
    55:           description: 'User first name (optional)'
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 21. `key`

**Server**: kaiser-data/kitsune-mcp
**Read/Write**: unknown
**Description**: Save an API key to .env for persistent use. e.g. key('EXA_API_KEY', 'sk-...')

Source: `onboarding.py:120`

```python
    117: 
    118: 
    119: @mcp.tool()
>>> 120: async def key(env_var: str, value: str) -> str:
    121:     """Save an API key to .env for persistent use. e.g. key('EXA_API_KEY', 'sk-...')"""
    122:     var = env_var.upper().replace(" ", "_")
    123:     _save_to_env(var, value)
    124:     _state._registry.bust_cache()  # credentials changed — invalidate cached server records
    125:     preview = value[:4] + "***" + value[-2:] if len(value) > 6 else "***"
    126:     return f"Saved: {var} = {preview} written to .env (mode 0o600) and active for this session."
    127: 
    128: 
    129: @mcp.tool()
    130: async def auto(
    131:     task: str,
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 22. `pattern_store`

**Server**: ruvnet/claude-flow
**Read/Write**: unknown
**Description**: Store learned pattern

*(Source not available -- classify from name and description.)*

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: seems to suggest behaviour

---
## 23. `create_purchase_intent`

**Server**: AiAgentKarl/agent-commerce-mcp-server
**Read/Write**: write

Source: `commerce.py:17`

```python
    14:     """Commerce-bezogene MCP-Tools registrieren."""
    15: 
    16:     @mcp.tool()
>>> 17:     async def create_purchase_intent(
    18:         item: str,
    19:         quantity: int = 1,
    20:         budget_max: float = 0,
    21:         budget_currency: str = "USD",
    22:         delivery_address: str = "",
    23:         delivery_notes: str = "",
    24:     ) -> dict:
    25:         """Strukturierte Kaufabsicht erstellen.
    26: 
    27:         Erstellt einen neuen Kaufvorgang, der dann mit Angeboten
    28:         verglichen und weiterverfolgt werden kann.
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: the language is German and the dict translation is: Create structured intent to purchase. Creates a new purchasing process, which can then be compared with offers and followed up.

---
## 24. `credentials_set`

**Server**: aibtcdev/aibtc-mcp-server
**Read/Write**: write
**Description**: Store or update a credential. Encrypts the value with AES-256-GCM and saves to ~/.aibtc/credentials.enc. If the service/key pair already exists, it is updated.

Source: `credentials.tools.ts:92`

```typescript
    89:    * Set or update a credential
    90:    */
    91:   server.registerTool(
>>> 92:     "credentials_set",
    93:     {
    94:       description:
    95:         "Store or update a credential. Encrypts the value with AES-256-GCM and saves to ~/.aibtc/credentials.enc. If the service/key pair already exists, it is updated.",
    96:       inputSchema: {
    97:         service: z.string().min(1).describe("Service name (e.g. 'github', 'openrouter')"),
    98:         key: z.string().min(1).describe("Key name within the service (e.g. 'api_key', 'token')"),
    99:         value: z
    100:           .string()
    101:           .min(1)
    102:           .describe("The credential value to store — WARNING: sensitive"),
    103:       },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 25. `create_account`

**Server**: onelogin/onelogin-mcp
**Read/Write**: read
**Description**: Create a new child account under your reseller account. Requires reseller privileges. The account object should contain name and optionally address1, address2, city, state, zip, country, phone, homepage, notes. Optionally specify plan (subscription plan name), subscription_state, enforce_user_limit, email_activation (true to send activation email to account owner), and api_credential (with name and permission: authentication_only, read_users, manage_users, read_all, or manage_all) to auto-create API credentials. Returns created account data with new ID and x-request-id for log tracing.

Source: `accounts.js:118`

```typescript
    115:     }
    116:   },
    117:   {
>>> 118:     name: 'create_account',
    119:     description: 'Create a new child account under your reseller account. Requires reseller privileges. The account object should contain name and optionally address1, address2, city, state, zip, country, phone, homepage, notes. Optionally specify plan (subscription plan name), subscription_state, enforce_user_limit, email_activation (true to send activation email to account owner), and api_credential (with name and permission: authentication_only, read_users, manage_users, read_all, or manage_all) to auto-create API credentials. Returns created account data with new ID and x-request-id for log tracing.',
    120:     inputSchema: {
    121:       type: 'object',
    122:       properties: {
    123:         account: {
    124:           type: 'object',
    125:           description: 'Account details (name, address1, address2, city, state, zip, country, phone, homepage, notes)',
    126:           properties: {
    127:             name: { type: 'string', description: 'Account name (required)' },
    128:             address1: { type: 'string', description: 'Address line 1' },
    129:             address2: { type: 'string', description: 'Address line 2' },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 26. `gw_reset_password`

**Server**: aringad/google-workspace-mcp
**Read/Write**: write
**Description**: Resetta la password di un utente. Se non specificata, ne genera una temporanea sicura.

Source: `server.py:466`

```python
    463:         "openWorldHint": False,
    464:     }
    465: )
>>> 466: async def gw_reset_password(params: ResetPasswordInput) -> str:
    467:     """Resetta la password di un utente. Se non specificata, ne genera una temporanea sicura.
    468: 
    469:     Returns:
    470:         str: Conferma con nuova password temporanea.
    471:     """
    472:     try:
    473:         service = get_directory_service()
    474:         password = params.new_password or generate_temp_password()
    475: 
    476:         updated = service.users().update(
    477:             userKey=params.user_key,
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 27. `search_geolocations`

**Server**: Happygallo/apple-ads-mcp
**Read/Write**: read
**Description**: Search or look up geo locations for campaign geo targeting. Search by name (query) to find locations, or provide geoIds to look up specific locations by ID. Returns location display name, entity type (Country/AdminArea/Locality), and ID for use in ad group targeting.

Source: `apps.ts:171`

```typescript
    168:   // get_supported_countries_regions is now a Resource (apple-ads://countries)
    169: 
    170:   server.registerTool(
>>> 171:     "search_geolocations",
    172:     {
    173:       title: "Search / Lookup Geo Locations",
    174:       description: "Search or look up geo locations for campaign geo targeting. Search by name (query) to find locations, or provide geoIds to look up specific locations by ID. Returns location display name, entity type (Country/AdminArea/Locality), and ID for use in ad group targeting.",
    175:       inputSchema: {
    176:         query: z.string().optional().describe("Search query (e.g., 'New York', 'United Kingdom')"),
    177:         entity: z.string().optional().describe("Entity type filter: Country, AdminArea, Locality"),
    178:         countryCode: z.string().optional().describe("Filter by country code (e.g., 'US')"),
    179:         geoIds: z.array(z.string()).optional().describe("Array of geo location IDs to look up (alternative to query)"),
    180:       },
    181:       annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: true },
    182:     },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 28. `checkout`

**Server**: markswendsen-code/mcp-delta
**Read/Write**: read
**Description**: Complete the flight booking. IMPORTANT: Set confirm=true only when you have explicit user confirmation to purchase. Without confirm=true, returns a preview of the booking details.

Source: `index.ts:249`

```typescript
    246:         },
    247:       },
    248:       {
>>> 249:         name: "checkout",
    250:         description:
    251:           "Complete the flight booking. IMPORTANT: Set confirm=true only when you have explicit user confirmation to purchase. Without confirm=true, returns a preview of the booking details.",
    252:         inputSchema: {
    253:           type: "object",
    254:           properties: {
    255:             confirm: {
    256:               type: "boolean",
    257:               description:
    258:                 "Set to true to actually complete the purchase. If false or omitted, returns a preview only. NEVER set to true without explicit user confirmation.",
    259:             },
    260:           },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 29. `baserow_auth_login`

**Server**: ayyazzafar/mcp-baserow
**Read/Write**: read
**Description**: Login with username and password to get JWT token

Source: `auth.ts:15`

```typescript
    12:       }
    13:     },
    14:     {
>>> 15:       name: 'baserow_auth_login',
    16:       description: 'Login with username and password to get JWT token',
    17:       inputSchema: {
    18:         type: 'object',
    19:         properties: {
    20:           username: {
    21:             type: 'string',
    22:             description: 'Baserow account email/username'
    23:           },
    24:           password: {
    25:             type: 'string',
    26:             description: 'Baserow account password'
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 30. `backup_database`

**Server**: codeofaxel/Kiln
**Read/Write**: unknown
**Description**: Back up the Kiln database with optional credential redaction.

Source: `backup.py:47`

```python
    44:     """Raised when a backup or restore operation fails."""
    45: 
    46: 
>>> 47: def backup_database(
    48:     db_path: str,
    49:     output_path: str | None = None,
    50:     *,
    51:     redact_credentials: bool = True,
    52: ) -> str:
    53:     """Create a backup copy of the Kiln database.
    54: 
    55:     :param db_path: Path to the source SQLite database.
    56:     :param output_path: Destination path.  Defaults to
    57:         ~/.kiln/backups/kiln-YYYYMMDD-HHMMSS.db.
    58:     :param redact_credentials: If True, replace credential columns
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 31. `ordinals_p2p_counter`

**Server**: aibtcdev/aibtc-mcp-server
**Read/Write**: read

Source: `ordinals-p2p.tools.ts:465`

```typescript
    462:   // ==========================================================================
    463: 
    464:   server.registerTool(
>>> 465:     "ordinals_p2p_counter",
    466:     {
    467:       description: `Counter an existing offer with a new proposed price.
    468: 
    469: Submits a counter-offer linked to a parent trade. The active wallet signs the
    470: counter with BIP-137 to prove identity. Either party in a trade may counter.
    471: 
    472: Requires an unlocked wallet with Bitcoin keys.`,
    473:       inputSchema: {
    474:         parent_trade_id: z
    475:           .number()
    476:           .int()
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 32. `klaviyo_events_get_profile`

**Server**: doinglean/klaviyo-mcp
**Read/Write**: read
**Description**: Get the profile associated with an event.

Source: `events.ts:242`

```typescript
    239:       },
    240:     },
    241:     {
>>> 242:       name: 'klaviyo_events_get_profile',
    243:       description: 'Get the profile associated with an event.',
    244:       inputSchema: {
    245:         type: 'object',
    246:         properties: {
    247:           event_id: {
    248:             type: 'string',
    249:             description: 'The event ID',
    250:           },
    251:           additional_fields: {
    252:             type: 'array',
    253:             items: { type: 'string', enum: ['subscriptions', 'predictive_analytics'] },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 33. `GetVirtualFoldersLow`

**Server**: fr0ster/mcp-abap-adt
**Read/Write**: read
**Description**: [low-level] Retrieve hierarchical virtual folder contents from ADT information system. Used for browsing ABAP objects by package, group, type, etc.

Source: `handleGetVirtualFolders.ts:13`

```typescript
    10: import { return_error, return_response } from '../../../lib/utils';
    11: 
    12: export const TOOL_DEFINITION = {
>>> 13:   name: 'GetVirtualFoldersLow',
    14:   available_in: ['onprem', 'cloud'] as const,
    15:   description:
    16:     '[low-level] Retrieve hierarchical virtual folder contents from ADT information system. Used for browsing ABAP objects by package, group, type, etc.',
    17:   inputSchema: {
    18:     type: 'object',
    19:     properties: {
    20:       object_search_pattern: {
    21:         type: 'string',
    22:         description:
    23:           'Object search pattern (e.g., "*", "Z*", "ZCL_*"). Default: "*"',
    24:         default: '*',
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 34. `sieve_usage`

**Server**: lmwharton/sieve-mcp
**Read/Write**: read
**Description**: Check your Sieve API usage for the current billing period.

Source: `server.py:146`

```python
    143:         "openWorldHint": True,
    144:     }
    145: )
>>> 146: async def sieve_usage() -> dict:
    147:     """Check your Sieve API usage for the current billing period.
    148: 
    149:     Shows screens used, monthly limit, tier, and organization name.
    150:     """
    151:     return await client.usage()
    152: 
    153: 
    154: @mcp.tool(
    155:     annotations={
    156:         "readOnlyHint": True,
    157:         "destructiveHint": False,
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 35. `ruvllm_sona_create`

**Server**: ruvnet/claude-flow
**Read/Write**: write
**Description**: Create a SONA instant adaptation loop (<1ms adaptation cycles). Use when sending every prompt to the Anthropic API is wrong because you need local inference — air-gapped environments, MicroLoRA-fine-tuned per-task adapters, or sub-cent per-call cost. For general Claude work native Task is the right call.

Source: `ruvllm-tools.test.ts:126`

```typescript
    123:     });
    124:   });
    125: 
>>> 126:   describe('ruvllm_sona_create', () => {
    127:     it('should create SONA instance', async () => {
    128:       const tool = findTool('ruvllm_sona_create');
    129:       const result = await tool.handler({ hiddenDim: 32 }) as any;
    130:       const data = JSON.parse(result.content[0].text);
    131:       expect(data.success).toBe(true);
    132:       expect(data.sonaId).toMatch(/^sona-/);
    133:     });
    134:   });
    135: 
    136:   describe('ruvllm_sona_adapt', () => {
    137:     it('should adapt with quality signal', async () => {
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 36. `ActivateDataElementLow`

**Server**: fr0ster/mcp-abap-adt
**Read/Write**: read
**Description**: Operation: Activate, Create, Update. Subject: DataElement. Will be useful for activating, creating, or updating data element. [low-level] Activate an ABAP data element. Returns activation status and any warnings/errors. Can use session_id and session_state from GetSession to maintain the same session.

Source: `handleActivateDataElement.ts:19`

```typescript
    16: } from '../../../lib/utils';
    17: 
    18: export const TOOL_DEFINITION = {
>>> 19:   name: 'ActivateDataElementLow',
    20:   available_in: ['onprem', 'cloud'] as const,
    21:   description:
    22:     'Operation: Activate, Create, Update. Subject: DataElement. Will be useful for activating, creating, or updating data element. [low-level] Activate an ABAP data element. Returns activation status and any warnings/errors. Can use session_id and session_state from GetSession to maintain the same session.',
    23:   inputSchema: {
    24:     type: 'object',
    25:     properties: {
    26:       data_element_name: {
    27:         type: 'string',
    28:         description: 'Data element name (e.g., ZDT_MY_ELEMENT).',
    29:       },
    30:       session_id: {
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 37. `create_api_authorization`

**Server**: onelogin/onelogin-mcp
**Read/Write**: read
**Description**: Create a new API authorization (OAuth 2.0 resource server) to protect your APIs with OneLogin. Required: name. Optional: description, connector_id (omit to use the account default API authorization connector), and a nested configuration object ({audiences, resource_identifier, access_token_expiration_minutes, refresh_token_expiration_minutes}). For convenience this tool also accepts top-level audience/audiences/resource_identifier/*_expiration_minutes and hoists them into configuration. Scopes can be provided as an array of {value, description} objects (value required); claims as an array of {name, user_attribute_mappings, user_attribute_macros?, attributes_transformations?} objects (name and user_attribute_mappings required) — both created alongside the authorization. Returns created authorization with ID and x-request-id.

Source: `api-authorization.js:489`

```typescript
    486:     }
    487:   },
    488:   {
>>> 489:     name: 'create_api_authorization',
    490:     description: 'Create a new API authorization (OAuth 2.0 resource server) to protect your APIs with OneLogin. Required: name. Optional: description, connector_id (omit to use the account default API authorization connector), and a nested configuration object ({audiences, resource_identifier, access_token_expiration_minutes, refresh_token_expiration_minutes}). For convenience this tool also accepts top-level audience/audiences/resource_identifier/*_expiration_minutes and hoists them into configuration. Scopes can be provided as an array of {value, description} objects (value required); claims as an array of {name, user_attribute_mappings, user_attribute_macros?, attributes_transformations?} objects (name and user_attribute_mappings required) — both created alongside the authorization. Returns created authorization with ID and x-request-id.',
    491:     inputSchema: {
    492:       type: 'object',
    493:       properties: {
    494:         name: { type: 'string', description: 'Authorization name' },
    495:         description: { type: 'string', description: 'Authorization description' },
    496:         connector_id: { type: 'number', description: 'Connector ID; omit to use the account default API authorization connector' },
    497:         audience: { type: 'string', description: 'Convenience alias for configuration.audiences' },
    498:         audiences: { type: 'string', description: 'Convenience alias for configuration.audiences' },
    499:         resource_identifier: { type: 'string', description: 'Convenience alias for configuration.resource_identifier' },
    500:         access_token_expiration_minutes: { type: 'number', description: 'Convenience alias for configuration.access_token_expiration_minutes' },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 38. `list_supported_stocks`

**Server**: evidai/lemon-cake
**Read/Write**: read
**Description**: List tokenized US stocks tradable via Dinari. Without DINARI_API_KEY, returns a representative subset (10 high-confidence tickers) so the tool is useful for inspection. With credentials, fetches live from Dinari.

Source: `index.ts:89`

```typescript
    86:       },
    87:     },
    88:     {
>>> 89:       name:        "list_supported_stocks",
    90:       description: "List tokenized US stocks tradable via Dinari. Without DINARI_API_KEY, returns a representative subset (10 high-confidence tickers) so the tool is useful for inspection. With credentials, fetches live from Dinari.",
    91:       annotations: { title: "List supported stocks", readOnlyHint: true, idempotentHint: true, openWorldHint: true },
    92:       inputSchema: { type: "object", properties: {}, additionalProperties: false },
    93:     },
    94:     {
    95:       name:        "get_quote",
    96:       description: "Latest bid/ask/mid for a Dinari dShare symbol (e.g. AAPL.d). Requires DINARI_API_KEY for real quotes; returns null with hint otherwise.",
    97:       annotations: { title: "Get quote", readOnlyHint: true, idempotentHint: true, openWorldHint: true },
    98:       inputSchema: {
    99:         type: "object",
    100:         required: ["symbol"],
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: credentials are optional

---
## 39. `credentials_list`

**Server**: aibtcdev/aibtc-mcp-server
**Read/Write**: read
**Description**: List all stored credentials. Shows service names, key names, and last-updated timestamps. Does NOT reveal credential values.

Source: `credentials.tools.ts:27`

```typescript
    24:    * List stored credentials (service/key names only, no values)
    25:    */
    26:   server.registerTool(
>>> 27:     "credentials_list",
    28:     {
    29:       description:
    30:         "List all stored credentials. Shows service names, key names, and last-updated timestamps. Does NOT reveal credential values.",
    31:       inputSchema: {},
    32:     },
    33:     async () => {
    34:       try {
    35:         await ensureUnlocked();
    36:         const entries = credentials.list();
    37: 
    38:         return createJsonResponse({
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 40. `get_summary_profile`

**Server**: kanishka-namdeo/yfnhanced-mcp
**Read/Write**: read
**Description**: Get company profile information including sector, industry, and business summary. Handles missing sector data with fallback classification.

Source: `summary.ts:518`

```typescript
    515:   getTools(): Tool[] {
    516:     return [
    517:       {
>>> 518:         name: 'get_summary_profile',
    519:         description: 'Get company profile information including sector, industry, and business summary. Handles missing sector data with fallback classification.',
    520:         inputSchema: {
    521:           type: 'object',
    522:           properties: {
    523:             symbol: {
    524:               type: 'string',
    525:               description: 'Stock ticker symbol (e.g., AAPL, MSFT)'
    526:             },
    527:             includeBusinessSummary: {
    528:               type: 'boolean',
    529:               description: 'Include business summary in response',
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 41. `memory_store`

**Server**: ruvnet/claude-flow
**Read/Write**: read
**Description**: Persistent key-value store with vector embedding — survives across sessions and is searchable by meaning, not just by file path. Use when native Write is wrong because the data is not a file (e.g. a learned pattern, a decision, a budget config) AND you need to recall it later by semantic query, not by path. Defaults to namespace=

Source: `mcp-tools-deep.test.ts:1136`

```typescript
    1133:   // --------------------------------------------------------------------------
    1134:   describe('Memory Tools - Handler Invocation', () => {
    1135:     it('memory_store stores an entry', async () => {
>>> 1136:       const tool = memoryTools.find(t => t.name === 'memory_store')!;
    1137:       expect(tool).toBeDefined();
    1138:       const result: any = await tool.handler({ key: 'test-key', value: 'test-value' });
    1139:       expect(result).toBeDefined();
    1140:     });
    1141: 
    1142:     it('memory_list returns entries', async () => {
    1143:       const tool = memoryTools.find(t => t.name === 'memory_list')!;
    1144:       expect(tool).toBeDefined();
    1145:       const result: any = await tool.handler({});
    1146:       expect(result).toBeDefined();
    1147:     });
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 42. `1ly_list_keys`

**Server**: 1lystore/1ly-mcp-server
**Read/Write**: read
**Description**: List API keys for the authenticated agent store (requires ONELY_API_KEY).

Source: `list-keys.ts:6`

```typescript
    3: import { mcpOk } from "../mcp.js";
    4: 
    5: export const listKeysTool = {
>>> 6:   name: "1ly_list_keys",
    7:   description: "List API keys for the authenticated agent store (requires ONELY_API_KEY).",
    8:   inputSchema: {
    9:     type: "object" as const,
    10:     properties: {},
    11:   },
    12: };
    13: 
    14: export async function handleListKeys(_args: unknown, config: Config) {
    15:   if (!config.apiKey) {
    16:     throw new Error("Missing ONELY_API_KEY for listing keys");
    17:   }
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 43. `get_top_expenses`

**Server**: NyxToolsDev/quickbooks-mcp-server
**Read/Write**: read
**Description**: Get top expenses grouped by category or vendor.

Source: `expenses.py:111`

```python
    108:         return "\n".join(lines)
    109: 
    110:     @server.tool()
>>> 111:     async def get_top_expenses(
    112:         period: str = "this_month",
    113:         group_by: str = "category",
    114:         limit: int = 10,
    115:     ) -> str:
    116:         """Get top expenses grouped by category or vendor.
    117: 
    118:         Args:
    119:             period: Time period - this_month, last_month, this_quarter, this_year
    120:                 (default: this_month).
    121:             group_by: Group results by 'category' or 'vendor' (default: category).
    122:             limit: Number of top entries to show (default: 10).
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 44. `verify_audit_chain`

**Server**: levelsofself/mcp-nervous-system
**Read/Write**: read
**Description**: Walks the hash-chained audit log and verifies every entry. Returns chain integrity status - valid/invalid, entry count, and where the chain breaks if tampered.

Source: `index.js:648`

```typescript
    645:   },
    646:   // NEW: Verify Audit Chain
    647:   {
>>> 648:     name: 'verify_audit_chain',
    649:     annotations: { title: 'Verify Audit Chain', readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
    650:     description: 'Walks the hash-chained audit log and verifies every entry. Returns chain integrity status - valid/invalid, entry count, and where the chain breaks if tampered.',
    651:     inputSchema: { type: 'object', properties: {} }
    652:   },
    653:   // NEW: Dispatch to LLM
    654:   {
    655:     name: 'dispatch_to_llm',
    656:     annotations: { title: 'Dispatch Task to LLM Agent', readOnlyHint: false, destructiveHint: false, idempotentHint: false, openWorldHint: true },
    657:     description: 'Spawns a background LLM agent to handle a task. Checks RAM (needs 500MB+), enforces max 2 concurrent dispatches. Returns PID and log file path.',
    658:     inputSchema: {
    659:       type: 'object',
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 45. `send_invite_link`

**Server**: onelogin/onelogin-mcp
**Read/Write**: write
**Description**: Send a password reset invite link email to an existing user in OneLogin. User clicks link to set password and access OneLogin portal. Email parameter is case-sensitive. Use personal_email to send to different address than user\

Source: `invite-links.js:74`

```typescript
    71:     }
    72:   },
    73:   {
>>> 74:     name: 'send_invite_link',
    75:     description: 'Send a password reset invite link email to an existing user in OneLogin. User clicks link to set password and access OneLogin portal. Email parameter is case-sensitive. Use personal_email to send to different address than user\'s OneLogin email. Returns success message with recipient email and x-request-id (API v1 - Rate Limited).',
    76:     inputSchema: {
    77:       type: 'object',
    78:       properties: {
    79:         email: {
    80:           type: 'string',
    81:           description: 'User email address'
    82:         },
    83:         firstname: {
    84:           type: 'string',
    85:           description: 'User first name (optional)'
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 46. `decode_invoice`

**Server**: lightningfaucet/lightning-wallet-mcp
**Read/Write**: unknown
**Description**: Decode a BOLT11 invoice without paying it. Returns amount, description, expiry, and destination.

Source: `index.ts:619`

```typescript
    616:       },
    617:     },
    618:     {
>>> 619:       name: 'decode_invoice',
    620:       description: 'Decode a BOLT11 invoice without paying it. Returns amount, description, expiry, and destination.',
    621:       inputSchema: {
    622:         type: 'object',
    623:         properties: {
    624:           bolt11: { type: 'string', description: 'BOLT11 invoice string to decode' },
    625:         },
    626:         required: ['bolt11'],
    627:       },
    628:     },
    629:     {
    630:       name: 'get_rate_limits',
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 47. `get_transcript`

**Server**: zlatkoc/youtube-summarize
**Read/Write**: read

Source: `main.py:261`

```python
    258: 
    259: 
    260: @mcp.tool()
>>> 261: def get_transcript(
    262:     url: str,
    263:     languages: list[str] | None = None,
    264:     format: str = "text",
    265:     preserve_formatting: bool = False,
    266:     include_timestamps: bool = False,
    267:     include_metadata: bool = True,
    268: ) -> str:
    269:     """Fetch a YouTube video's transcript.
    270: 
    271:     Args:
    272:         url: YouTube video URL or video ID
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 48. `get_text_extents`

**Server**: daedalus/mcp-kicad
**Read/Write**: read
**Description**: Calculate the bounding box of a text string.

Source: `mcp_server.py:258`

```python
    255: 
    256: 
    257: @mcp.tool()
>>> 258: def get_text_extents(text: str, size: int = 10) -> dict:
    259:     """Calculate the bounding box of a text string.
    260: 
    261:     Args:
    262:         text: The text string to measure.
    263:         size: Font size in mm. Default 10.
    264: 
    265:     Returns:
    266:         Dictionary with x, y, width, height of the bounding box.
    267: 
    268:     Example:
    269:         >>> get_text_extents("Hello")
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 49. `ReadMetadataExtension`

**Server**: babamba2/abap-mcp-adt-powerup
**Read/Write**: read
**Description**: [read-only] Read ABAP metadata extension (DDLX) source code and metadata (package, responsible, description, etc.).

Source: `handleReadMetadataExtension.ts:10`

```typescript
    7: } from '../../../lib/utils';
    8: 
    9: export const TOOL_DEFINITION = {
>>> 10:   name: 'ReadMetadataExtension',
    11:   available_in: ['onprem', 'cloud'] as const,
    12:   description:
    13:     '[read-only] Read ABAP metadata extension (DDLX) source code and metadata (package, responsible, description, etc.).',
    14:   inputSchema: {
    15:     type: 'object',
    16:     properties: {
    17:       metadata_extension_name: {
    18:         type: 'string',
    19:         description: 'Metadata extension name (e.g., Z_MY_DDLX).',
    20:       },
    21:       version: {
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 50. `tapd_get_test_plan_count`

**Server**: xihe-lab/tapd-mcp-server
**Read/Write**: read
**Description**: Get the count of test plans

Source: `test.ts:121`

```typescript
    118:     },
    119:   },
    120:   {
>>> 121:     name: "tapd_get_test_plan_count",
    122:     description: "Get the count of test plans",
    123:     inputSchema: z.object({
    124:       workspace_id: z.number().describe("Project ID (required)"),
    125:       id: z.string().optional().describe("Test plan ID"),
    126:       name: z.string().optional().describe("Test plan name"),
    127:       status: z.string().optional().describe("Status"),
    128:       creator: z.string().optional().describe("Creator"),
    129:       owner: z.string().optional().describe("Owner"),
    130:     }),
    131:     handler: async (client, params) => {
    132:       return client.get("/test_plans/count", params);
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 51. `create_api_key`

**Server**: alainsvrd/borealhost-mcp
**Read/Write**: write
**Description**: Create a new API key with specified scopes.

Source: `server.py:863`

```python
    860: 
    861: 
    862: @mcp.tool()
>>> 863: def create_api_key(name: str, scopes: str = "read", site_slug: str = "") -> dict:
    864:     """Create a new API key with specified scopes.
    865: 
    866:     Cannot create keys with higher scopes than the current key.
    867:     Site-scoped keys restrict access to a single site.
    868: 
    869:     Requires: API key with write scope.
    870: 
    871:     Args:
    872:         name: Human-readable name for the key (1-100 chars)
    873:         scopes: Comma-separated scopes. Options: "read", "read,write",
    874:                 "read,write,admin". Default: "read"
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 52. `1ly_update_link`

**Server**: 1lystore/1ly-mcp-server
**Read/Write**: write
**Description**: Update an API link by id (requires ONELY_API_KEY).

Source: `update-link.ts:7`

```typescript
    4: import { mcpOk } from "../mcp.js";
    5: 
    6: export const updateLinkTool = {
>>> 7:   name: "1ly_update_link",
    8:   description: "Update an API link by id (requires ONELY_API_KEY).",
    9:   inputSchema: {
    10:     type: "object" as const,
    11:     properties: {
    12:       id: { type: "string" },
    13:       title: { type: "string" },
    14:       url: { type: "string" },
    15:       description: { type: "string" },
    16:       slug: { type: "string" },
    17:       price: { type: "string" },
    18:       isPublic: { type: "boolean" },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 53. `ryvo_protocol_config`

**Server**: Agonx402/agon-gateway-agentic
**Read/Write**: read
**Description**: Fetch Ryvo Protocol global config and token registry.

Source: `server.js:17`

```typescript
    14: 
    15: const tools = [
    16:   {
>>> 17:     name: "ryvo_protocol_config",
    18:     description: "Fetch Ryvo Protocol global config and token registry.",
    19:     inputSchema: {
    20:       type: "object",
    21:       additionalProperties: false,
    22:       properties: {
    23:         rpcUrl: { type: "string" },
    24:         programId: { type: "string" },
    25:       },
    26:     },
    27:   },
    28:   {
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 54. `verify_session_factor`

**Server**: onelogin/onelogin-mcp
**Read/Write**: read
**Description**: Complete MFA verification during session login to obtain session token. Use in conjunction with create_session_login_token after MFA challenge. Provide device_id (from MFA challenge) and state_token. For OTP factors (SMS, Email, Authenticator): include otp_token. For OneLogin Protect: first call triggers push, subsequent calls poll with do_not_notify=true. Returns session_token on success or pending status for push factors. Returns session data and x-request-id.

Source: `sessions.js:124`

```typescript
    121:     }
    122:   },
    123:   {
>>> 124:     name: 'verify_session_factor',
    125:     description: 'Complete MFA verification during session login to obtain session token. Use in conjunction with create_session_login_token after MFA challenge. Provide device_id (from MFA challenge) and state_token. For OTP factors (SMS, Email, Authenticator): include otp_token. For OneLogin Protect: first call triggers push, subsequent calls poll with do_not_notify=true. Returns session_token on success or pending status for push factors. Returns session data and x-request-id.',
    126:     inputSchema: {
    127:       type: 'object',
    128:       properties: {
    129:         device_id: {
    130:           type: 'string',
    131:           description: 'MFA device ID from login challenge'
    132:         },
    133:         state_token: {
    134:           type: 'string',
    135:           description: 'State token from initial login'
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 55. `get_smart_hook_env_vars`

**Server**: onelogin/onelogin-mcp
**Read/Write**: read
**Description**: Get environment variable names configured for a Smart Hook. Returns only variable names, not values (values are redacted for security). Environment variables store sensitive configuration like API keys, tokens, or service URLs that hook code can access via process.env. Use to audit what config variables a hook uses. Returns env var names array and x-request-id.

Source: `smart-hooks.js:372`

```typescript
    369:     }
    370:   },
    371:   {
>>> 372:     name: 'get_smart_hook_env_vars',
    373:     description: 'Get environment variable names configured for a Smart Hook. Returns only variable names, not values (values are redacted for security). Environment variables store sensitive configuration like API keys, tokens, or service URLs that hook code can access via process.env. Use to audit what config variables a hook uses. Returns env var names array and x-request-id.',
    374:     inputSchema: {
    375:       type: 'object',
    376:       properties: {
    377:         hook_id: {
    378:           type: 'string',
    379:           description: 'The OneLogin Smart Hook ID'
    380:         }
    381:       },
    382:       required: ['hook_id'],
    383:       additionalProperties: false
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 56. `find_opendart_compensation`

**Server**: sayouzone/mcp-opendart-server
**Read/Write**: read
**Description**: OpenDART에서 기업의 이사 및 감사 보수 정보를 수집합니다.

Source: `opendarts.py:170`

```python
    167:     """,
    168:     tags={"opendart", "dividend", "korea", "standardized", "cached"}
    169: )
>>> 170: async def find_opendart_compensation(stock: str, year: Optional[int] = None, quarter: Optional[int] = None):
    171:     """
    172:     OpenDART에서 기업의 이사 및 감사 보수 정보를 수집합니다.
    173: 
    174:     Args:
    175:         year: 연도
    176:         quarter: 분기
    177:         stock: 종목 코드 (예: "005930", "삼성전자")
    178: 
    179:     Returns:
    180:         dict: 이사 및 감사 보수 정보
    181: 
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: language is Korean and translation of description is "Collects information on director and auditor compensation of corporations from OpenDART."

---
## 57. `file_upload_delete`

**Server**: PrefectHQ/fastmcp-ts
**Read/Write**: write
**Description**: Delete a previously uploaded file by its handle

Source: `FileUpload.ts:106`

```typescript
    103: 
    104:     this.server.tool(
    105:       {
>>> 106:         name: 'file_upload_delete',
    107:         description: 'Delete a previously uploaded file by its handle',
    108:         inputSchema: {
    109:           type: 'object',
    110:           properties: {
    111:             handle: { type: 'string', description: 'The file handle returned by file_upload_submit' },
    112:           },
    113:           required: ['handle'],
    114:         },
    115:         ui: { visibility: ['app'] },
    116:       },
    117:       (args: Record<string, unknown>) => {
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 58. `get_connection_string`

**Server**: cachly-dev/cachly-mcp
**Read/Write**: read
**Description**: Get the Redis/Valkey connection string (redis:// URL) for a running instance.

Source: `tools.ts:55`

```typescript
    52:     },
    53:   },
    54:   {
>>> 55:     name: 'get_connection_string',
    56:     description:
    57:       'Get the Redis/Valkey connection string (redis:// URL) for a running instance. ' +
    58:       'Use this to configure your application or set environment variables.',
    59:     inputSchema: {
    60:       type: 'object',
    61:       properties: {
    62:         instance_id: { type: 'string', description: 'UUID of the instance' },
    63:       },
    64:       required: ['instance_id'],
    65:     },
    66:   },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 59. `sona/lora/apply-base`

**Server**: ruvnet/claude-flow
**Read/Write**: write
**Description**: Apply base-layer LoRA adaptation

Source: `sona-tools.js:597`

```typescript
    594:         version: '1.0.0',
    595:     },
    596:     {
>>> 597:         name: 'sona/lora/apply-base',
    598:         description: 'Apply base-layer LoRA adaptation',
    599:         inputSchema: {
    600:             type: 'object',
    601:             properties: {
    602:                 adapterId: { type: 'string', description: 'LoRA adapter ID' },
    603:                 input: { type: 'string', description: 'Input to adapt' },
    604:                 strength: { type: 'number', default: 0.5 },
    605:             },
    606:             required: ['input'],
    607:         },
    608:         handler: async (input, ctx) => handleBaseLoraApply(loraApplySchema.parse(input), ctx),
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 60. `board_read`

**Server**: lightningfaucet/lightning-wallet-mcp
**Read/Write**: read
**Description**: Browse the Lightning Faucet message board. Returns recent posts from AI agents with scores, topics, and reply counts. Free — no payment required. Use this to discover what other agents are discussing.

Source: `index.ts:795`

```typescript
    792:     // MESSAGE BOARD TOOLS
    793:     // ==========================================
    794:     {
>>> 795:       name: 'board_read',
    796:       description: 'Browse the Lightning Faucet message board. Returns recent posts from AI agents with scores, topics, and reply counts. Free — no payment required. Use this to discover what other agents are discussing.',
    797:       inputSchema: {
    798:         type: 'object',
    799:         properties: {
    800:           sort: { type: 'string', enum: ['trending', 'newest', 'top'], default: 'trending', description: 'Sort order' },
    801:           topic: { type: 'string', description: 'Filter by topic (e.g. "bitcoin", "ai", "mcp")' },
    802:           limit: { type: 'integer', minimum: 1, maximum: 50, default: 20, description: 'Max posts to return' },
    803:           offset: { type: 'integer', minimum: 0, default: 0, description: 'Skip posts for pagination' },
    804:         },
    805:         required: [],
    806:       },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 61. `GetNodeStructureLow`

**Server**: babamba2/abap-mcp-adt-powerup
**Read/Write**: read
**Description**: [low-level] Fetch node structure from ADT repository. Used for object tree navigation and structure discovery. Can use session_id and session_state from GetSession to maintain the same session.

Source: `handleGetNodeStructure.ts:13`

```typescript
    10: import { return_error, return_response } from '../../../lib/utils';
    11: 
    12: export const TOOL_DEFINITION = {
>>> 13:   name: 'GetNodeStructureLow',
    14:   available_in: ['onprem', 'cloud'] as const,
    15:   description:
    16:     '[low-level] Fetch node structure from ADT repository. Used for object tree navigation and structure discovery. Can use session_id and session_state from GetSession to maintain the same session.',
    17:   inputSchema: {
    18:     type: 'object',
    19:     properties: {
    20:       parent_type: {
    21:         type: 'string',
    22:         description: 'Parent object type (e.g., "CLAS/OC", "PROG/P", "DEVC/K")',
    23:       },
    24:       parent_name: {
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 62. `ssh_resolve_host`

**Server**: oaslananka-lab/mcp-ssh-tool
**Read/Write**: unknown
**Description**: Resolves a host alias from ~/.ssh/config to connection parameters

Source: `session.provider.ts:167`

```typescript
    164:         },
    165:       },
    166:       {
>>> 167:         name: "ssh_resolve_host",
    168:         description: "Resolves a host alias from ~/.ssh/config to connection parameters",
    169:         annotations: annotate({
    170:           title: "Resolve SSH Host",
    171:           readOnly: true,
    172:           idempotent: true,
    173:           openWorld: false,
    174:         }),
    175:         outputSchema: objectOutputSchema("Resolved SSH connection parameters"),
    176:         inputSchema: {
    177:           type: "object" as const,
    178:           properties: {
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 63. `cache_status`

**Server**: alainsvrd/borealhost-mcp
**Read/Write**: read
**Description**: Get cache status (Redis, WP object cache, hit rates).

Source: `server.py:1348`

```python
    1345: # ── Cache Management ──
    1346: 
    1347: @mcp.tool()
>>> 1348: def cache_status(slug: str) -> dict:
    1349:     """Get cache status (Redis, WP object cache, hit rates).
    1350: 
    1351:     Requires: API key with read scope.
    1352: 
    1353:     Args:
    1354:         slug: Site identifier
    1355: 
    1356:     Returns:
    1357:         {"redis_running": true, "object_cache_enabled": true,
    1358:          "hit_rate": 0.95, "memory_used_mb": 12}
    1359:     """
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 64. `keysend`

**Server**: lightningfaucet/lightning-wallet-mcp
**Read/Write**: write
**Description**: Send a payment directly to a node without an invoice (keysend/spontaneous payment). REQUIRES AGENT KEY.

Source: `index.ts:779`

```typescript
    776:       },
    777:     },
    778:     {
>>> 779:       name: 'keysend',
    780:       description: 'Send a payment directly to a node without an invoice (keysend/spontaneous payment). REQUIRES AGENT KEY.',
    781:       inputSchema: {
    782:         type: 'object',
    783:         properties: {
    784:           destination: { type: 'string', description: 'Destination node public key' },
    785:           amount_sats: { type: 'integer', minimum: 1, description: 'Amount in satoshis' },
    786:           message: { type: 'string', maxLength: 1000, description: 'Optional TLV message' },
    787:         },
    788:         required: ['destination', 'amount_sats'],
    789:       },
    790:     },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 65. `update_event`

**Server**: PhilflowIO/dav-mcp
**Read/Write**: write
**Description**: PREFERRED: Update event fields without iCal formatting. Supports: SUMMARY (title), DESCRIPTION (details), LOCATION (place), DTSTART (start time), DTEND (end time), STATUS (TENTATIVE/CONFIRMED/CANCELLED), and any RFC 5545 property including custom X-* properties (e.g., X-ZOOM-LINK, X-MEETING-ROOM).

Source: `update-event-fields.js:29`

```typescript
    26:  * - Field-agnostic: no pre-defined field list required
    27:  */
    28: export const updateEventFields = {
>>> 29:   name: 'update_event',
    30:   description: 'PREFERRED: Update event fields without iCal formatting. Supports: SUMMARY (title), DESCRIPTION (details), LOCATION (place), DTSTART (start time), DTEND (end time), STATUS (TENTATIVE/CONFIRMED/CANCELLED), and any RFC 5545 property including custom X-* properties (e.g., X-ZOOM-LINK, X-MEETING-ROOM).',
    31:   inputSchema: {
    32:     type: 'object',
    33:     properties: {
    34:       event_url: {
    35:         type: 'string',
    36:         description: 'The URL of the event to update'
    37:       },
    38:       event_etag: {
    39:         type: 'string',
    40:         description: 'The etag of the event (required for conflict detection)'
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 66. `renew_access_token`

**Server**: Vedhasagaran/dhan-mcp-py
**Read/Write**: unknown
**Description**: Renew the DhanHQ access token for another 24 hours.

Source: `server.py:65`

```python
    62:         }
    63: 
    64: @mcp.tool()
>>> 65: def renew_access_token() -> dict:
    66:     """
    67:     Renew the DhanHQ access token for another 24 hours.
    68:     This expires the current token and provides a new token with 24 hours validity.
    69:     Note: Only works with tokens generated from Dhan Web (web.dhan.co).
    70:     Returns the new access token that should be updated in your environment variables.
    71:     """
    72:     url = "https://api.dhan.co/v2/RenewToken"
    73:     headers = {
    74:         "access-token": access_token,
    75:         "dhanClientId": client_id
    76:     }
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 67. `ryvo_gateway_call`

**Server**: Agonx402/agon-gateway-agentic
**Read/Write**: write
**Description**: Call an Ryvo Gateway route. Use without payment/SIWX headers to issue a challenge, then retry with PAYMENT-SIGNATURE, X-PAYMENT, or SIGN-IN-WITH-X. Devnet RPC/DAS/Wallet routes settle in devnet USDC; mainnet routes settle in mainnet USDC; Tokens API SIWX routes are free.

Source: `server.js:100`

```typescript
    97:     },
    98:   },
    99:   {
>>> 100:     name: "ryvo_gateway_call",
    101:     description: "Call an Ryvo Gateway route. Use without payment/SIWX headers to issue a challenge, then retry with PAYMENT-SIGNATURE, X-PAYMENT, or SIGN-IN-WITH-X. Devnet RPC/DAS/Wallet routes settle in devnet USDC; mainnet routes settle in mainnet USDC; Tokens API SIWX routes are free.",
    102:     inputSchema: {
    103:       type: "object",
    104:       additionalProperties: false,
    105:       required: ["method", "path"],
    106:       properties: {
    107:         baseUrl: { type: "string" },
    108:         method: { type: "string", description: "HTTP method, for example GET or POST." },
    109:         path: { type: "string", description: "Gateway path, for example /v1/catalog." },
    110:         query: {
    111:           oneOf: [
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 68. `hive_settle`

**Server**: srotzin/hive-mcp-connector
**Read/Write**: write
**Description**: Settle a payment between two agents on one of 4 rails: Base USDC (Coinbase L2),

Source: `server.js:103`

```typescript
    100:   },
    101: 
    102:   hive_settle: {
>>> 103:     name: 'hive_settle',
    104:     description:
    105:       'Settle a payment between two agents on one of 4 rails: Base USDC (Coinbase L2), ' +
    106:       'Aleo USDCx (privacy-preserving), Aleo USAd (stablecoin), or Aleo native (ALEO token). ' +
    107:       'AP2/x402 compatible. Returns tx_hash, settlement confirmation, and a W3C VC receipt.',
    108:     inputSchema: {
    109:       type: 'object',
    110:       properties: {
    111:         from_did: {
    112:           type: 'string',
    113:           description: 'Sender\'s W3C DID (did:hive:* or did:aleo:*)'
    114:         },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 69. `validate_iban`

**Server**: cammac-creator/ibanforge
**Read/Write**: read
**Description**: Verify a European IBAN AND enrich it with bank, compliance and routing data. Use whenever the user mentions an IBAN, asks who the bank is, or asks if a SEPA payment will go through. Returns: valid, country, BIC, bank name, EMI/vIBAN flag, SEPA + VoP, risk_score, Swiss bc_nummer for CH/LI. Cost: $0.005.

Source: `async_client.py:120`

```python
    117:         _raise_for_status(res)
    118:         return res.json()
    119: 
>>> 120:     async def validate_iban(self, iban: str) -> IBANValidationResult:
    121:         res = await self._client.post("/v1/iban/validate", json={"iban": iban})
    122:         _raise_for_status(res)
    123:         return res.json()
    124: 
    125:     async def validate_batch(self, ibans: Iterable[str]) -> IBANBatchResult:
    126:         ibans_list = list(ibans)
    127:         if not ibans_list:
    128:             raise InvalidInputError("ibans must contain at least one IBAN")
    129:         if len(ibans_list) > 100:
    130:             raise InvalidInputError(
    131:                 "ibans must be at most 100 entries (got {})".format(len(ibans_list))
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 70. `create_app`

**Server**: onelogin/onelogin-mcp
**Read/Write**: read
**Description**: Create a new app based on a OneLogin connector. Minimum required: connector_id and name. For OIDC apps, use configuration to set login_url, redirect_uri, etc. For complete configuration options, use get_app on an existing app with the same connector. For OpenId Connect apps: response includes client_id and client_secret. Returns created app data and x-request-id.

Source: `apps.js:383`

```typescript
    380:     }
    381:   },
    382:   {
>>> 383:     name: 'create_app',
    384:     description: 'Create a new app based on a OneLogin connector. Minimum required: connector_id and name. For OIDC apps, use configuration to set login_url, redirect_uri, etc. For complete configuration options, use get_app on an existing app with the same connector. For OpenId Connect apps: response includes client_id and client_secret. Returns created app data and x-request-id.',
    385:     inputSchema: {
    386:       type: 'object',
    387:       properties: {
    388:         connector_id: { type: 'number', description: 'Connector ID for the app type (required)' },
    389:         name: { type: 'string', description: 'App name (required)' },
    390:         description: { type: 'string', description: 'App description' },
    391:         notes: { type: 'string', description: 'App notes' },
    392:         visible: { type: 'boolean', description: 'Whether app is visible in user portal' },
    393:         policy_id: { type: 'number', description: 'Security policy ID to assign' },
    394:         allow_assumed_signin: { type: 'boolean', description: 'Allow assumed sign-in' },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 71. `get_restock_suggestions`

**Server**: codeofaxel/Kiln
**Read/Write**: read
**Description**: Find materials running low and generate purchase links.

Source: `material_inventory.py:511`

```python
    508:     )
    509: 
    510: 
>>> 511: def get_restock_suggestions(db: Any) -> list[RestockSuggestion]:
    512:     """Find materials running low and generate purchase links.
    513: 
    514:     Examines all material types in the inventory and returns suggestions
    515:     for any that are projected to run out within 30 days, sorted by urgency
    516:     (critical first).
    517:     """
    518:     summaries = get_fleet_material_summary(db)
    519:     history = get_consumption_history(db, days=30)
    520: 
    521:     rate_map: dict[str, float] = {}
    522:     for h in history:
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 72. `purchase`

**Server**: 123Ergo/unphurl-mcp
**Read/Write**: unknown

Source: `billing.ts:27`

```typescript
    24: 
    25: Credits are consumed only when unknown domains run through the full analysis pipeline. Known domains (Tranco Top 100K) and cached domains (previously analysed by any Unphurl customer) are always free.
    26: 
>>> 27: If credits_remaining is 0, you can still check known and cached domains for free. To check unknown domains, purchase more credits using the "purchase" tool.`,
    28:       inputSchema: {},
    29:     },
    30:     async () => {
    31:       if (!api.hasApiKey) return authError();
    32: 
    33:       try {
    34:         const result = await api.balance();
    35:         return successResult(result);
    36:       } catch (err) {
    37:         if (err instanceof ApiRequestError) return apiErrorToResult(err);
    38:         return errorResult(err instanceof Error ? err.message : "Unknown error");
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 73. `claim_api_key`

**Server**: alainsvrd/borealhost-mcp
**Read/Write**: unknown
**Description**: Claim an API key using a claim token from the container.

Source: `server.py:146`

```python
    143: 
    144: 
    145: @mcp.tool()
>>> 146: def claim_api_key(claim_token: str) -> dict:
    147:     """Claim an API key using a claim token from the container.
    148: 
    149:     After calling request_api_key(), read the claim token from
    150:     ~/.borealhost/.claim_token on your container and pass it here.
    151: 
    152:     The token is single-use — once claimed, it cannot be used again.
    153:     The API key is automatically activated for this MCP session.
    154: 
    155:     Args:
    156:         claim_token: The claim token string read from the container file
    157: 
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 74. `set_api_key`

**Server**: Pattyboi101/indiestack
**Read/Write**: write
**Description**: Activate an IndieStack API key for this session.

Source: `mcp_server.py:131`

```python
    128: # ── Set API Key (session) ────────────────────────────────────────────────
    129: 
    130: @mcp.tool()
>>> 131: async def set_api_key(key: str) -> str:
    132:     """Activate an IndieStack API key for this session.
    133: 
    134:     Call this when the user provides their API key (starts with isk_).
    135:     This unlocks Pro rate limits (1,000/day vs 15/day keyless) and enables
    136:     Maker Pro citation analytics. Migration data and all search tools work
    137:     without a key — the key removes limits and powers the analytics dashboard.
    138:     No restart needed — takes effect on the next query.
    139: 
    140:     Args:
    141:         key: The API key starting with isk_ (get one at indiestack.ai/developer)
    142:     """
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 75. `lightning_pay_invoice`

**Server**: aibtcdev/aibtc-mcp-server
**Read/Write**: unknown
**Description**: Pay a BOLT-11 Lightning invoice from the embedded Lightning wallet.

Source: `lightning.tools.ts:344`

```typescript
    341:   // --- Manual Lightning ops -------------------------------------------------
    342: 
    343:   server.registerTool(
>>> 344:     "lightning_pay_invoice",
    345:     {
    346:       description:
    347:         "Pay a BOLT-11 Lightning invoice from the embedded Lightning wallet. " +
    348:         "Returns the payment preimage (proof of payment) and fees paid.",
    349:       inputSchema: {
    350:         bolt11: z
    351:           .string()
    352:           .describe("BOLT-11 encoded Lightning invoice (starts with lnbc... or lntb...)"),
    353:         maxFeeSats: z
    354:           .number()
    355:           .int()
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 76. `self_check`

**Server**: levelsofself/mcp-nervous-system
**Read/Write**: read
**Description**: Runs automated self-diagnosis on the Nervous System. Checks for: rate-limiting own operations, secrets in source code, info leakage in tool output, hardcoded paths, missing smoke tests, and version desync. Run before every publish and as part of security audits.

Source: `index.js:759`

```typescript
    756:   },
    757:   // NEW: Self-Check
    758:   {
>>> 759:     name: 'self_check',
    760:     annotations: { title: 'Self-Check', readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
    761:     description: 'Runs automated self-diagnosis on the Nervous System. Checks for: rate-limiting own operations, secrets in source code, info leakage in tool output, hardcoded paths, missing smoke tests, and version desync. Run before every publish and as part of security audits.',
    762:     inputSchema: {
    763:       type: 'object',
    764:       properties: {}
    765:     }
    766:   },
    767:   // NEW: Bot Compliance Check
    768:   {
    769:     name: 'bot_compliance_check',
    770:     annotations: { title: 'Bot Compliance Check', readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 77. `fedbrain_search`

**Server**: cachly-dev/cachly-mcp
**Read/Write**: read
**Description**: FedBrain context-weighted search: Search the global commons, weighting results by tech-stack similarity.

Source: `tools.ts:1590`

```typescript
    1587:     },
    1588:   },
    1589:   {
>>> 1590:     name: 'fedbrain_search',
    1591:     description:
    1592:       'FedBrain context-weighted search: Search the global commons, weighting results by tech-stack similarity. ' +
    1593:       'Brains with matching domain context (Go/Kubernetes/Postgres) rank higher than unrelated stacks. ' +
    1594:       'Shows certificate provenance, confirm_count, and Gold Standard badges.',
    1595:     inputSchema: {
    1596:       type: 'object',
    1597:       properties: {
    1598:         instance_id: { type: 'string', description: 'Brain instance ID' },
    1599:         query: { type: 'string', description: 'What to search for' },
    1600:         context_hints: {
    1601:           type: 'array',
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 78. `retrieve_credential`

**Server**: codeofaxel/Kiln
**Read/Write**: unknown
**Description**: Decrypt and return a stored credential.

Source: `credential_store.py:651`

```python
    648:     return get_credential_store().store(credential_type, value, label=label)
    649: 
    650: 
>>> 651: def retrieve_credential(credential_id: str) -> str:
    652:     """Convenience: decrypt and return a credential via the singleton.
    653: 
    654:     :param credential_id: The credential to retrieve.
    655:     :returns: The decrypted plaintext string.
    656:     """
    657:     return get_credential_store().retrieve(credential_id)
    658: 
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 79. `drift_java`

**Server**: dadbodgeoff/drift
**Read/Write**: read
**Description**: Analyze Java projects: routes, error handling, data access, annotations. Actions: status (project overview), routes (HTTP routes - Spring MVC, JAX-RS, Micronaut, Quarkus), errors (error handling patterns), data-access (database patterns - Spring Data JPA, Hibernate, JDBC, MyBatis), annotations (annotation usage).

Source: `enterprise-server.ts:759`

```typescript
    756:     case 'drift_python':
    757:       return executePythonTool(args as unknown as PythonArgs, { projectRoot });
    758: 
>>> 759:     case 'drift_java':
    760:       return executeJavaTool(args as unknown as JavaArgs, { projectRoot });
    761: 
    762:     case 'drift_php':
    763:       return executePhpTool(args as unknown as PhpArgs, { projectRoot });
    764: 
    765:     case 'drift_iec61131':
    766:       return executeIEC61131Tool(args as unknown as IEC61131Args, { projectRoot });
    767: 
    768:     case 'drift_constants':
    769:       return handleConstants(projectRoot, args as Parameters<typeof handleConstants>[1]);
    770: 
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 80. `memory_store`

**Server**: ruvnet/claude-flow
**Read/Write**: read
**Description**: Persistent key-value store with vector embedding — survives across sessions and is searchable by meaning, not just by file path. Use when native Write is wrong because the data is not a file (e.g. a learned pattern, a decision, a budget config) AND you need to recall it later by semantic query, not by path. Defaults to namespace=

Source: `mcp-tools-deep.test.ts:1136`

```typescript
    1133:   // --------------------------------------------------------------------------
    1134:   describe('Memory Tools - Handler Invocation', () => {
    1135:     it('memory_store stores an entry', async () => {
>>> 1136:       const tool = memoryTools.find(t => t.name === 'memory_store')!;
    1137:       expect(tool).toBeDefined();
    1138:       const result: any = await tool.handler({ key: 'test-key', value: 'test-value' });
    1139:       expect(result).toBeDefined();
    1140:     });
    1141: 
    1142:     it('memory_list returns entries', async () => {
    1143:       const tool = memoryTools.find(t => t.name === 'memory_list')!;
    1144:       expect(tool).toBeDefined();
    1145:       const result: any = await tool.handler({});
    1146:       expect(result).toBeDefined();
    1147:     });
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 81. `get_board_labels`

**Server**: delorenj/mcp-server-trello
**Read/Write**: read
**Description**: Get all labels of a specific board

Source: `index.ts:1177`

```typescript
    1174: 
    1175:     // Label management tools
    1176:     this.server.registerTool(
>>> 1177:       'get_board_labels',
    1178:       {
    1179:         title: 'Get Board Labels',
    1180:         description: 'Get all labels of a specific board',
    1181:         inputSchema: {
    1182:           boardId: z
    1183:             .string()
    1184:             .optional()
    1185:             .describe('ID of the Trello board (uses default if not provided)'),
    1186:         },
    1187:       },
    1188:       async ({ boardId }) => {
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 82. `protect_pdf`

**Server**: EigenCharlie/pdf-toolkit-mcp
**Read/Write**: write
**Description**: Add password protection to a PDF. Anyone opening the output will need the supplied password.

Source: `security.ts:48`

```typescript
    45: });
    46: 
    47: export const protectPdfTool: ToolDefinition<typeof protectSchema> = {
>>> 48:   name: 'protect_pdf',
    49:   description:
    50:     'Add password protection to a PDF. Anyone opening the output will need the supplied password.',
    51:   inputSchema: protectSchema,
    52:   async handler(args, ctx) {
    53:     const [input] = await resolveInputs([args.input_file], ['.pdf']);
    54:     const outputPath = resolveOutput(args.output_path, input, 'protected', 'pdf');
    55:     const { outputBuffers, taskId } = await runTask({
    56:       tool: 'protect',
    57:       files: [input],
    58:       params: { password: args.password },
    59:       onProgress: createProgressAdapter(ctx.sendProgress),
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 83. `get_deposit_invoice`

**Server**: lightningfaucet/lightning-wallet-mcp
**Read/Write**: read
**Description**: Create a Lightning invoice to fund your operator account. Pay this invoice to add sats to your balance.

Source: `index.ts:404`

```typescript
    401:       },
    402:     },
    403:     {
>>> 404:       name: 'get_deposit_invoice',
    405:       description: 'Create a Lightning invoice to fund your operator account. Pay this invoice to add sats to your balance.',
    406:       inputSchema: {
    407:         type: 'object',
    408:         properties: {
    409:           amount_sats: { type: 'integer', minimum: 100, description: 'Amount in satoshis to deposit' },
    410:         },
    411:         required: ['amount_sats'],
    412:       },
    413:     },
    414:     {
    415:       name: 'create_agent',
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 84. `audit_mcp_server`

**Server**: joepangallo/mcp-audit-server
**Read/Write**: read
**Description**: Launch a target MCP server over stdio, enumerate tools, and run active security probes against its exposed tools. Requires AGENT_SECURITY_ADMIN_MODE=1.

Source: `index.js:30`

```typescript
    27:     }
    28:   },
    29:   {
>>> 30:     name: "audit_mcp_server",
    31:     description: "Launch a target MCP server over stdio, enumerate tools, and run active security probes against its exposed tools. Requires AGENT_SECURITY_ADMIN_MODE=1.",
    32:     inputSchema: {
    33:       type: "object",
    34:       properties: {
    35:         command: { type: "string" },
    36:         args: { type: "array", items: { type: "string" } },
    37:         env: { type: "object", additionalProperties: { type: "string" } }
    38:       },
    39:       required: ["command"]
    40:     }
    41:   },
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 85. `get_hiro_api_key`

**Server**: aibtcdev/aibtc-mcp-server
**Read/Write**: read
**Description**: Check whether a Hiro API key is configured. Shows the key source (stored file or environment variable) and a masked preview.

Source: `settings.tools.ts:65`

```typescript
    62:    * Get Hiro API key status
    63:    */
    64:   server.registerTool(
>>> 65:     "get_hiro_api_key",
    66:     {
    67:       description:
    68:         "Check whether a Hiro API key is configured. Shows the key source (stored file or environment variable) and a masked preview.",
    69:       inputSchema: {},
    70:     },
    71:     async () => {
    72:       try {
    73:         await initializeStorage();
    74:         const storedKey = await getHiroApiKey();
    75:         const envKey = process.env.HIRO_API_KEY || "";
    76: 
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 86. `drift_session_create`

**Server**: dadbodgeoff/drift
**Read/Write**: write
**Description**: Create a new Cortex session for tracking token usage and loaded memories.

*(Source not available -- classify from name and description.)*

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 87. `moltguard_credential_issue`

**Server**: MoltyCel/moltrust-mcp-server
**Read/Write**: unknown
**Description**: Issue a W3C Verifiable Credential (AgentTrustCredential) for a wallet.

Source: `server.py:904`

```python
    901: 
    902: 
    903: @mcp.tool()
>>> 904: async def moltguard_credential_issue(
    905:     address: str,
    906:     ctx: Context[ServerSession, MolTrustClient] | None = None,
    907: ) -> str:
    908:     """Issue a W3C Verifiable Credential (AgentTrustCredential) for a wallet.
    909: 
    910:     The credential contains the agent's trust score, Sybil score,
    911:     ERC-8004 registration status, and MolTrust verification status.
    912:     It is cryptographically signed with Ed25519 (JWS).
    913: 
    914:     Args:
    915:         address: Base (EVM) wallet address (0x...)
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 88. `salary_ai_risk`

**Server**: drivenbymyai-max/mcp-sputnikx-market
**Read/Write**: read
**Description**: AI automation risk scores by ISCO occupation or NACE sector — exposure, complementarity, risk level

Source: `index.mjs:290`

```typescript
    287:       inputSchema: { type: 'object', properties: {} },
    288:     },
    289:     {
>>> 290:       name: 'salary_ai_risk',
    291:       description: 'AI automation risk scores by ISCO occupation or NACE sector — exposure, complementarity, risk level',
    292:       inputSchema: {
    293:         type: 'object',
    294:         properties: {
    295:           occupation: { type: 'string', description: 'ISCO occupation code or keyword' },
    296:           sector: { type: 'string', description: 'NACE sector code or keyword' },
    297:         },
    298:       },
    299:     },
    300:     {
    301:       name: 'salary_lv_wages',
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 89. `get_dividends`

**Server**: mhajder/ghostfolio-mcp
**Read/Write**: read

Source: `ghostfolio_tools.py:621`

```python
    618:             "idempotentHint": True,
    619:         },
    620:     )
>>> 621:     async def get_dividends(
    622:         group_by: Annotated[
    623:             str,
    624:             Field(
    625:                 default="month",
    626:                 description="Grouping period for dividend data. Options: day, week, month, quarter, year",
    627:             ),
    628:         ] = "month",
    629:         date_range: Annotated[
    630:             str,
    631:             Field(
    632:                 default="max",
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 90. `ryvo_gateway_call_with_headers`

**Server**: Agonx402/agon-gateway-agentic
**Read/Write**: write
**Description**: Call a Gateway route with caller-supplied auth/payment headers. MCP does not sign, pay, or execute wallet commands. Devnet routes expect devnet-USDC payment headers; mainnet routes expect mainnet-USDC headers; Tokens API SIWX routes are free.

Source: `server.js:169`

```typescript
    166:     },
    167:   },
    168:   {
>>> 169:     name: "ryvo_gateway_call_with_headers",
    170:     description: "Call a Gateway route with caller-supplied auth/payment headers. MCP does not sign, pay, or execute wallet commands. Devnet routes expect devnet-USDC payment headers; mainnet routes expect mainnet-USDC headers; Tokens API SIWX routes are free.",
    171:     inputSchema: {
    172:       type: "object",
    173:       additionalProperties: false,
    174:       required: ["method", "path", "headers"],
    175:       properties: {
    176:         baseUrl: { type: "string" },
    177:         method: { type: "string" },
    178:         path: { type: "string" },
    179:         query: {
    180:           oneOf: [
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 91. `paean_list_tasks`

**Server**: paean-ai/openpaean
**Read/Write**: read
**Description**: List tasks with optional filtering

Source: `tools.ts:320`

```typescript
    317:       },
    318:     },
    319:     {
>>> 320:       name: 'paean_list_tasks',
    321:       description: 'List tasks with optional filtering',
    322:       inputSchema: {
    323:         type: 'object',
    324:         properties: {
    325:           status: {
    326:             type: 'string',
    327:             enum: ['all', 'pending', 'in_progress', 'completed'],
    328:             description: 'Filter by task status',
    329:           },
    330:           priority: {
    331:             type: 'string',
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 92. `ssh_connect`

**Server**: zibdie/SSH-MCP-Server
**Read/Write**: unknown
**Description**: Connect to an SSH server using password or SSH key authentication. Supports IPv4 and IPv6.

Source: `index.js:41`

```typescript
    38:     this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
    39:       tools: [
    40:         {
>>> 41:           name: 'ssh_connect',
    42:           description: 'Connect to an SSH server using password or SSH key authentication. Supports IPv4 and IPv6.',
    43:           inputSchema: {
    44:             type: 'object',
    45:             properties: {
    46:               host: {
    47:                 type: 'string',
    48:                 description: 'SSH server hostname or IP address (IPv4 or IPv6)',
    49:               },
    50:               port: {
    51:                 type: 'number',
    52:                 description: 'SSH server port',
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 93. `wallet_rotate_password`

**Server**: aibtcdev/aibtc-mcp-server
**Read/Write**: unknown

Source: `wallet-management.tools.ts:471`

```typescript
    468:    * Rotate wallet password
    469:    */
    470:   server.registerTool(
>>> 471:     "wallet_rotate_password",
    472:     {
    473:       description: `Change the password for a wallet's encrypted keystore.
    474: Performs an atomic operation: backs up the keystore, re-encrypts with the new password, verifies the round-trip, then cleans up. If anything fails, the original keystore is restored.
    475: If the wallet is currently unlocked, it will be locked after rotation (requires re-unlock with new password).`,
    476:       inputSchema: {
    477:         walletId: z
    478:           .string()
    479:           .optional()
    480:           .describe("Wallet ID to rotate password for (uses active wallet if not specified)"),
    481:         oldPassword: z.string().describe("Current wallet password - WARNING: sensitive value"),
    482:         newPassword: z
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 94. `morph_list_supermodels`

**Server**: srotzin/hive-mcp-morph
**Read/Write**: read
**Description**: List all supermodels (W1 through W19): id, name, role, lane, lead shape, tagline. The supermodel directory is the canonical lineage for every spawned brood variant. Free up to 100 calls/day per agent-DID; $0.001/call thereafter via x402 USDC settlement on Base.

Source: `server.js:42`

```typescript
    39: },
    40:       },
    41:     },{
>>> 42:   name: 'morph_list_supermodels',
    43:   description: 'List all supermodels (W1 through W19): id, name, role, lane, lead shape, tagline. The supermodel directory is the canonical lineage for every spawned brood variant. Free up to 100 calls/day per agent-DID; $0.001/call thereafter via x402 USDC settlement on Base.',
    44:   inputSchema: {
    45:     type: 'object',
    46:     properties: {
    47: 
    48:     },
    49:   },
    50: },    {
    51:       name: 'morph_get_supermodel',
    52:       description: 'Fetch a single supermodel by name or id (e.g. \'MONROE\', \'W1\'). Returns full role, lane, lead-shape, tagline, address, and brood conversion summary.',
    53:       inputSchema: {
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 95. `get_settings_metadata`

**Server**: Pollamin/opendock-mcp
**Read/Write**: read
**Description**: Get all settings metadata for an entity type

Source: `settings-metadata.test.ts:21`

```typescript
    18: 
    19:   it("get_settings_metadata sends GET /settings-metadata/:entityType", async () => {
    20:     api.request.mockResolvedValueOnce([{ key: "timezone", type: "string" }]);
>>> 21:     const result = await server.call("get_settings_metadata", { entityType: "warehouse" });
    22:     expect(api.request).toHaveBeenCalledWith({ path: "/settings-metadata/warehouse" });
    23:     expect(JSON.parse(result.content[0].text)).toEqual([{ key: "timezone", type: "string" }]);
    24:   });
    25: 
    26:   it("get_setting_metadata sends GET /settings-metadata/:entityType/:settingKey", async () => {
    27:     api.request.mockResolvedValueOnce({ key: "timezone", type: "string", required: true });
    28:     const result = await server.call("get_setting_metadata", { entityType: "warehouse", settingKey: "timezone" });
    29:     expect(api.request).toHaveBeenCalledWith({ path: "/settings-metadata/warehouse/timezone" });
    30:     expect(JSON.parse(result.content[0].text)).toEqual({ key: "timezone", type: "string", required: true });
    31:   });
    32: 
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 96. `jingswap_cancel_sbtc`

**Server**: aibtcdev/aibtc-mcp-server
**Read/Write**: read
**Description**: Cancel your sBTC deposit from the current Jingswap auction cycle and get a full refund.

Source: `jingswap.tools.ts:407`

```typescript
    404:   // ── Cancel sBTC Deposit ─────────────────────────────────────
    405: 
    406:   server.registerTool(
>>> 407:     "jingswap_cancel_sbtc",
    408:     {
    409:       description:
    410:         "Cancel your sBTC deposit from the current Jingswap auction cycle and get a full refund. " +
    411:         "Only works during the deposit phase. Works the same for both markets.",
    412:       inputSchema: {
    413:         market: z.string().optional().describe('Market: "sbtc-stx" (default) or "sbtc-usdcx"'),
    414:       },
    415:     },
    416:     async ({ market }) => {
    417:       try {
    418:         const m = getMarket(market);
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 97. `generate_social_kit`

**Server**: Rakesh1002/namemyapp-mcp
**Read/Write**: write
**Description**: Generate a social media strategy + content kit (posts, captions, calendar, analytics framework). Requires Founder sub or SOCIAL_MEDIA_KIT purchase.

Source: `index.ts:239`

```typescript
    236:     },
    237:   },
    238:   {
>>> 239:     name: "generate_social_kit",
    240:     description: "Generate a social media strategy + content kit (posts, captions, calendar, analytics framework). Requires Founder sub or SOCIAL_MEDIA_KIT purchase.",
    241:     inputSchema: {
    242:       type: "object",
    243:       properties: {
    244:         businessName: { type: "string" },
    245:         industry: { type: "string" },
    246:         description: { type: "string" },
    247:         targetAudience: { type: "string" },
    248:         goals: { type: "array", items: { type: "string" } },
    249:         platforms: {
    250:           type: "array",
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 98. `archive35_run_command`

**Server**: wolfschram/archive-35.com
**Read/Write**: unknown

Source: `archive35_mcp.py:150`

```python
    147:         return out
    148:     except Exception as e: return f'Error: {e}'
    149: 
>>> 150: @mcp.tool(name='archive35_run_command')
    151: async def run_command(p:ShellIn)->str:
    152:     '''Run a shell command in the repo directory.'''
    153:     try:
    154:         r=subprocess.run(p.command,shell=True,cwd=ROOT,capture_output=True,text=True,timeout=p.timeout)
    155:         o=r.stdout.strip()
    156:         if r.stderr.strip(): o+=f'\nSTDERR: {r.stderr.strip()}'
    157:         return o or '(no output)'
    158:     except Exception as e: return f'Error: {e}'
    159: 
    160: @mcp.tool(name='archive35_overview')
    161: async def overview()->str:
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 99. `BuyWhere Singapore catalog`

**Server**: richmondteo-code/buywhere-mcp
**Read/Write**: read
**Description**: Available product categories in Singapore

Source: `index.ts:519`

```typescript
    516:   resources: [
    517:     {
    518:       uri: "buywhere://catalog/sg",
>>> 519:       name: "BuyWhere Singapore catalog",
    520:       description: "Available product categories in Singapore",
    521:       mimeType: "application/json",
    522:     },
    523:     {
    524:       uri: "buywhere://catalog/my",
    525:       name: "BuyWhere Malaysia catalog",
    526:       description: "Available product categories in Malaysia",
    527:       mimeType: "application/json",
    528:     },
    529:     {
    530:       uri: "buywhere://catalog/id",
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
## 100. `get_project_schemes`

**Server**: drewster99/xcode-mcp-server
**Read/Write**: read
**Description**: Get the available build schemes for the specified Xcode project or workspace.

Source: `get_project_schemes.py:15`

```python
    12: 
    13: @mcp.tool()
    14: @apply_config
>>> 15: def get_project_schemes(project_path: str) -> str:
    16:     """
    17:     Get the available build schemes for the specified Xcode project or workspace.
    18: 
    19:     Args:
    20:         project_path: Path to an Xcode project/workspace directory, which must
    21:         end in '.xcodeproj' or '.xcworkspace' and must exist.
    22: 
    23:     Returns:
    24:         A newline-separated list of scheme names, with the active scheme listed first.
    25:         If no schemes are found, returns an empty string.
    26:     """
```

**Your classification** -- write exactly one of: `sensitive`, `non-sensitive`
ANSWER: non-sensitive

**Notes (optional)** -- anything you found genuinely ambiguous
NOTES: 

---
