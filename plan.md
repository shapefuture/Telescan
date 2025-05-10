# Project: Telegram Extractor & Summarizer (td with the cleaned history and user prompt.
    *   It will save cleaned history text, participant text, and LLl + Node.js/TypeScript) (v6.0)

**Goal:** Develop a user-friendly command-line applicationM summary text to organized `.txt` files.
    *   It will generate a beautiful `report.html` using Node.js/TypeScript that orchestrates the `tdl` (Go-based Telegram CLI tool) to extract chat history/participants from a user's Telegram account. The application will then process this data, optionally call an LLM that links to these `.txt` files.

**`implementation_plan.md` (v6.0 - ` API for summarization based on a user prompt, and generate a polished HTML report for viewing results and accessing cleaned data files.

**tdl` Engine + Node.js/TypeScript Orchestrator)**

```markdown
# Project: Telegram Data Orchestrator & Insight Reporter (v6.0 - tdl + Node.js/TS)

**Goal:** Develop a robustArchitecture:**
1.  **Telegram Engine:** `tdl` executable (user installs manually, authenticates via `tdl login command-line application using Node.js/TypeScript that orchestrates the `tdl` tool to extract Telegram chat data` once).
2.  **Orchestrator & Report Generator:** Node.js/TypeScript CLI application.

**User, processes this data, interacts with an LLM for insights based on a user prompt, saves all outputs, and generates a Interaction Flow:**
1.  User installs `tdl` and `tdl login` once.
2.  User polished HTML report for easy viewing.

**Architecture:** `tdl` (Go CLI for Telegram Interaction) + Node. installs Node.js and the orchestrator app (e.g., via `npm install -g` or cloning repo + `npm install`).
3.  User runs the orchestrator: `telegram-processor` (or `node dist/main.js`).
4.  Orchestrator lists chats (by calling `tdl chat ls`).js/TypeScript Application (Orchestration, JSON Processing, Text Cleaning, LLM API Calls, File Saving, HTML Report Generation).

**User Flow:**
1.  User installs `tdl` and authenticates via `tdl login
5.  Orchestrator prompts for chat selection and LLM prompt.
6.  Orchestrator calls` (one-time).
2.  User installs Node.js and the orchestrator application (e.g., `tdl chat export` and `tdl chat users` for selected chats.
7.  Orchestr via `npm install -g` or by cloning repo + `npm install`).
3.  User runs the orchestrator fromator processes JSON, cleans text, calls LLM API.
8.  Orchestrator generates `report.html` their terminal: `telegram-reporter --chats "@channel1,group_id_123" --prompt "Summar and cleaned `.txt` files.
9.  User opens `report.html` in browser.

**Technology Stack:**
*   **Telegram Engine:** `tdl` (Go binary)
*   **Orchestrator:**ize key decisions." --output-dir ./my_reports`
4.  The application calls `tdl` to Node.js (LTS version) with TypeScript
*   **CLI Interaction (Orchestrator):** `inquirer` fetch data, processes it, calls LLM, saves text files, and generates `report.html` in the specified output directory.
5.  User opens `report.html` in their browser.

**Guiding Principles:** (for prompts), `chalk` (for colored console output), `commander` or `yargs` (for command-line arguments - optional if fully interactive).
*   **Subprocess Execution:** Node.js `child_process`
*   **User Experience:** Simple CLI invocation, clear console feedback, beautiful HTML report.
*   **AI module (`exec`, `spawn`).
*   **File System:** Node.js `fs` module (preferably `fs/ Development Ease:** Focus AI on TypeScript/Node.js for well-defined tasks (subprocess, JSON, HTTP, filepromises`).
*   **HTTP Client (LLM):** `axios` or built-in `fetch` (Node.js I/O, HTML string gen). `tdl` handles Telegram complexity.
*   **Robustness:** Solid 18+).
*   **Configuration:** `.env` files using `dotenv` package.
*   **Logging:** error handling for `tdl` calls, file operations, and API interactions.
*   **Maintainability & Testability:** Clean `winston` or `pino` (for structured logging).
*   **Testing:** Jest or Vitest, TypeScript code, type safety, unit tests.
*   **Performance:** Node.js for efficient I/O and `ts-mock-imports`.
*   **Linting/Formatting:** ESLint, Prettier.
*   **Build:** TypeScript Compiler (`tsc`).
*   **Packaging (Optional):** `pkg` or `nexe` to create a processing. `tdl` is performant.

**Technology Stack:**
*   **Telegram Engine:** `td single executable for the orchestrator.

**Project Structure (Node.js/TypeScript Orchestrator):**

/telegraml` (pre-built Go executable).
*   **Orchestrator:** Node.js (v18+ recommended) with TypeScript.
*   **CLI Argument Parsing:** `yargs` or `commander`.
*   **Sub-ts-processor
|-- package.json
|-- tsconfig.json
|-- .env                   # LLprocess Execution:** Node.js `child_process` module (`execFile` or `spawn`).
*   **HTTP Client (M API Key, output paths
|-- .gitignore
|-- implementation_plan.md
|-- /src
|   |-- main.ts            # Main CLI entry point
|   |-- config.ts          # Loadfor LLM):** `axios` or built-in `fetch` (Node.js 18+)./validate environment variables
|   |-- tdl_orchestrator.ts # Functions to call `tdl`
*   **File System:** Node.js `fs` module (preferably `fs/promises`).
*   **HTML subprocesses
|   |-- data_processor.ts  # Functions to parse JSON, clean text
|   |-- Generation:** String templates or a lightweight template literal function. (Avoid heavy template engines to keep it simple for AI).
*    llm_service.ts     # Functions to call LLM API
|   |-- report_generator.ts# Functions to generate HTML report and TXT files
|   |-- ui_prompts.ts      # In**Configuration:** `.env` file for API keys (`dotenv` package).
*   **Logging:** A simple console logger (`quirer prompts for user interaction
|   |-- utils.ts           # General utility functions (e.g., file helpersconsole.log`, `console.error`) or a lightweight library like `pino` or `winston` if, logging setup)
|   |-- /types             # TypeScript type definitions
|       |-- tdl_types more structure is needed.
*   **Testing:** Jest or Vitest.
*   **Linting/Formatting:** ESLint, Prettier.
*   **Build (Optional):** `tsc` for TypeScript compilation, potentially.ts   # Types for `tdl` JSON output (messages, users)
|       |-- app_types.ts   # Internal app types
|-- /output                # Default directory for `tdl` JSON and generated TXT/HTML `pkg` or `nexe` to bundle into a single executable (adds complexity, might be a later step).

**Project Structure:**

/telegram-reporter-node
|-- src/
|   |-- index.ts             
|   |-- /tdl_json_exports  # Raw JSON from `tdl`
|   |--# Main application entry point
|   |-- tdl_orchestrator.ts  # Functions to call t /cleaned_data      # Cleaned TXT files
|   |-- report.html
|-- /testsdl and parse output
|   |-- text_cleaner.ts      # Text cleaning logic (regex)
|
|   |-- /__mocks__         # Mocks for external modules
|   |-- tdl_orche   |-- llm_service.ts       # Functions to call LLM API
|   |-- file_saverstrator.test.ts
|   |-- data_processor.test.ts
|   |-- ll.ts        # Functions to save processed data to .txt files
|   |-- html_reporter.ts     # Functions to generate report.html
|   |-- types.ts             # TypeScript interfaces/types
|   m_service.test.ts
|   |-- report_generator.test.ts

---
**AI Implementation Best Practices Checklist (MANDATORY for each step):**
*   **[ ] Code Style & Linting:** Enforce Prettier formatting, check with ESLint (with TypeScript plugins). Resolve ALL issues.
*   **[ ]|-- config.ts            # Load and export config (API keys etc.)
|-- tests/
|    Typing:** Strict TypeScript. Use interfaces/types for all data structures, especially `tdl` output and LLM API responses.|-- tdl_orchestrator.test.ts
|   |-- text_cleaner.test.ts
|   |-- llm_service.test.ts
|   |-- html_reporter.test.ts
|
*   **[ ] Modularity:** Adhere to structure. Small, focused functions/classes. Clear async/await usage-- .env                     # API Keys (LLM_API_KEY)
|-- .gitignore
|-- package.
*   **[ ] Configuration (`src/config.ts`):** Load from `.env` using `dotenv.json
|-- tsconfig.json
|-- jest.config.js or vitest.config.ts #`. Validate critical configs. Export a typed config object.
*   **[ ] Security:** Sanitize any user input If using these test runners
|-- README.md
|-- implementation_plan.md   # This file

 used in file paths or commands. Ensure API keys are loaded from env vars and not committed. Be careful with `child---
**AI Implementation Best Practices Checklist (MANDATORY for each step):**
*   **(All relevant general best practices apply: Style, Typing, Modularity, Config, Security, Error Handling, Logging, Testing, Docs, Dependencies_process.exec` (prefer `spawn` for better control over arguments and avoiding shell injection if command parts are dynamic)**
*   **[ ] TypeScript First:** Use TypeScript for all custom code. Leverage strong typing.
*   ** - though `tdl` commands are mostly static here).
*   **[ ] Error Handling:** Use `try...catch` for subprocess execution, file I/O, API calls, JSON parsing. Log detailed errors. Provide user-friendly console[ ] Async/Await:** Use `async/await` for all I/O operations (`fs/promises`, `child messages. Define custom error classes if beneficial.
*   **[ ] Logging (`src/utils.ts` - `_process` execution if wrapped, HTTP calls).
*   **[ ] Subprocess Management:** Handle `tdl` execution carefully:
    *   Use `execFile` or `spawn` from `child_process`.
    *   setupLogging`):** Use `winston` or `pino`. Log key operations, errors, subprocess commands, and output. Include correlation IDs if processing multiple chats.
*   **[ ] Testing:** Unit test all service/Capture `stdout` and `stderr` properly.
    *   Check exit codes for errors.
    *   Implement timeouts for `tdl` commands.
    *   Ensure `tdl` is expected to be in the system PATHprocessor/generator functions. Mock `child_process` module for `tdl` calls. Mock `axios`/`fetch` for or provide a configurable path to it.
*   **[ ] JSON Safety:** Validate structure of JSON received from `tdl` before accessing nested properties. Use try-catch for `JSON.parse()`.
*   **[ ] File LLM calls. Mock `fs` for file operations. Test JSON parsing and text cleaning with sample data. Use Jest/Vitest with `ts-jest` or `ts-node`.
*   **[ ] Documentation:** J Paths:** Use `path.join()` for constructing paths. Handle relative vs. absolute paths correctly. Ensure output directories areSDoc/TSDoc comments for all functions/classes. `README.md` for setup and usage.
* created (`fs.mkdir(..., { recursive: true })`).
*   **[ ] LLM API:** Secure   **[ ] Dependency Management:** Use `npm` or `yarn`. Keep `package.json` and `package-lock.json` committed.
*   **[ ] Explicit Instructions:** For AI: "In `src/tdl_orchestrator.ts`, write an async function `exportChatHistory(chatIdOrName: string,ly handle API key. Implement robust error handling and timeouts for LLM calls. Handle LLM context window limits (trunc outputDir: string): Promise<string>` that executes `tdl chat export -c ${chatIdOrName} --all -o ${outputPath}` using `child_process.spawn`. It should return the path to the JSON file on success oration).
*   **[ ] HTML Generation:** Use template literals or simple string concatenation. Embed CSS in `<style>` tags within the HTML for simplicity.
*   **[ ] Explicit Instructions:** "Using Node.js `child_process. throw an error. Capture and log stdout/stderr."

---

## Phase 1: Core Setup, Config, LoggingexecFile`, execute the `tdl` command `['chat', 'export', '-c', CHAT_ID,, Basic `tdl` Orchestration

**Goal:** Set up the Node.js/TypeScript project, configure environment, '--all', '-o', outputJsonPath]`. Capture stdout/stderr. If exit code is not 0, throw logging, and implement basic functions to call `tdl chat ls` and `tdl chat export` as subprocesses. an error..." "Define a TypeScript interface `TdlMessage` based on the expected JSON structure of a single message from `td

**Steps:**

1.  **[v] Project Setup:** `npm init -y`, install TS, ESLl chat export`."

---

## Phase 1: Core Setup, Config, CLI Arguments, and Basic `int, Prettier, Jest/Vitest, core dependencies (`dotenv`, `inquirer`, `chalk`, `commander`/tdl` Orchestration

**Goal:** Set up the Node.js/TypeScript project, configure environment variables, implement CLI argument parsing, and create basic functions to call `tdl chat ls` and parse its output.

**Steps:**

1.  **[v] Project Setup:** Create directories/files per structure. `npm init -y`. Install`yargs`, `axios`). Setup `tsconfig.json`, ESLint/Prettier configs. Create directory structure. Add core dependencies: `typescript`, `ts-node`, `@types/node`, `dotenv`, `yargs` (or ` `.gitignore`.
2.  **[ ] Configuration (`src/config.ts`, `.env`):**
    commander`), `eslint`, `prettier`, testing framework (`jest` or `vitest`).
2.  **[*   `config.ts`: Load `LLM_API_KEY`, `LLM_ENDPOINT_URL` (optional), `TDL_OUTPUT_DIR`, `CLEANED_DATA_DIR`, `REPORT_HTML_PATH` from `.env` using `dotenv`. Validate critical values. Export typed config object.
    *   `. ] `tsconfig.json`:** Configure TypeScript compiler options (target, module, outDir, sourceMap, strict,env`: Define local values.
3.  **[ ] Logging Setup (`src/utils.ts`):** Implement esModuleInterop, etc.).
3.  **[ ] `package.json` Scripts:** Add scripts for `build` `setupLogger()` using `winston` or `pino`.
4.  **[ ] Basic CLI Entry Point (`src (`tsc`), `start` (`ts-node src/index.ts`), `dev` (`nodemon --watch src/main.ts`):**
    *   Import logger setup, config.
    *   Basic `async function --exec ts-node src/index.ts`), `lint`, `test`.
4.  **[ ] run() { ... }` called at end. Placeholder for now.
5.  **[ ] `tdl Configuration (`src/config.ts`, `.env`):**
    *   `src/config.ts`: Use` Orchestrator (`src/tdl_orchestrator.ts`):**
    *   Import `spawn `dotenv.config()`. Export constants like `LLM_API_KEY`, `LLM_ENDPOINT_URL`, `LLM_MODEL_NAME`, `TDL_EXECUTABLE_PATH` (optional, default to `tdl`).` from `child_process`, `config`.
    *   Implement `async function executeTdlCommand(args: string[]): Promise<{ stdout: string, stderr: string, success: boolean }>`:
        *   Uses Validate that critical API keys are present.
    *   `.env`: Store `LLM_API_KEY` `spawn('tdl', args, { stdio: 'pipe' })`.
        *   Captures `stdout and any other secrets. Update `.gitignore`.
5.  **[ ] Logging:** Implement a simple logger (e.g`, `stderr`. Handles `error` and `close` events.
        *   Returns object with captured output and success., functions wrapping `console.log/error` with timestamps/levels, or use `pino`).
6.  **[ ] CLI Argument Parsing (`src/index.ts`):**
    *   Use `yargs`. Define status. Log command and output.
    *   Implement `async function listChats(): Promise<Array<{ id: string, arguments:
        *   `--chats` (string, required, comma-separated list of chat IDs/usernames/ title: string, type: string }>>` (Conceptual, `tdl chat ls` output is not JSON bylinks).
        *   `--prompt` (string, required, the LLM prompt).
        *   ` default, might need to parse text or check if `tdl chat ls -o json` exists and is usable). *--output-dir` (string, optional, default `./telegram_reports`).
        *   `--tdl-Simpler: Instruct user to use `tdl chat ls` manually first to get IDs.*
    *   Implement `asyncpath` (string, optional, path to `tdl` if not in PATH).
7.  **[ function exportChatHistory(chatIdOrName: string, outputJsonPath: string): Promise<void>`: Calls ] `tdl` Orchestrator Basics (`src/tdl_orchestrator.ts`):**
    *    `executeTdlCommand` with `['chat', 'export', '-c', chatIdOrName, '--all', '-o', outputJsonPath]`. Throws error on failure.
    *   Implement `async function exportChatParticipants(chatIdImplement `async function executeTdlCommand(tdlPath: string, args: string[]): Promise<{ stdout: string;OrName: string, outputJsonPath: string): Promise<void>`: Calls `executeTdlCommand` with `['chat', 'users', '-c', chatIdOrName, '-o', outputJsonPath]`. Throws error on failure stderr: string; success: boolean }>`:
        *   Uses `child_process.execFile(tdlPath, args, { timeout: ... })`.
        *   Wraps in `new Promise` to handle callback or uses. (Note: Check if `tdl` can determine if it's a group before trying to export users, `util.promisify`.
        *   Logs command, stdout, stderr, exit code. Returns success status or handle error if it's a channel).
6.  **[ ] TypeScript Types (`src/types/td.
    *   Implement `async function listChats(tdlPath: string): Promise<Array<{id: string |l_types.ts`):** Define basic interfaces for the expected structure of `tdl`'s JSON output for messages and number; title: string; type: string}>>`:
        *   Calls `executeTdlCommand` with `[' users (based on `tdl` documentation or sample output).
7.  **[ ] Initial Tests (`tests/tdchat', 'ls', '-o', 'json']`.
        *   Parses the JSON output from `stdoutl_orchestrator.test.ts`):**
    *   Mock `child_process.spawn`.`. Validates structure.
        *   Transforms into a clean array of chat objects. Handles `tdl` command Test that `executeTdlCommand` constructs commands correctly and handles different exit codes/errors.
    *   Test errors.
8.  **[ ] Main Entry (`src/index.ts`):**
    *   Parse `exportChatHistory` and `exportChatParticipants` call `executeTdlCommand` with correct args.
8. CLI args.
    *   (For testing Phase 1) Call `listChats`, print results.
    *   Basic  **[ ] Manual Testing:**
    *   Ensure `tdl` is installed and authenticated (`tdl login` error handling.
9.  **[ ] Testing (`tests/tdl_orchestrator.test.ts` done manually).
    *   Run parts of `tdl_orchestrator.ts` (e.g):** Unit test `executeTdlCommand` (mock `child_process.execFile`). Test `listChats., via a test script or temporary calls in `main.ts`).
    *   Verify `tdl` commands are executed` by mocking `executeTdlCommand` to return sample JSON output.
10. **[ ] Manual Testing and JSON files are created in `config.TDL_OUTPUT_DIR`. Check console logs.

**End of Phase :** Ensure `tdl` is installed and `tdl login` has been done. Run `npm run dev --1:** Core project setup complete. The orchestrator can call `tdl` commands to export raw data as JSON files.

---

## Phase 2: User Interaction, Data Processing & Cleaning

**Goal:** Implement console prompts for chat selection and LL --help`. Run `npm run dev -- --chats "@somechannel" --prompt "test"` (it will just listM prompt. Parse `tdl` JSON output, clean history text.

**Steps:**

1.  **[ chats for now). Check console output and logs.

**End of Phase 1:** TypeScript project setup is complete. The ] UI Prompts (`src/ui_prompts.ts`):**
    *   Import `inquirer`.
 app can parse CLI arguments and successfully call `tdl chat ls` and parse its output.

---

## Phase     *   Implement `async function getChatSelectionsFromUser(availableChats: Array<{ name: string, value: string }>): Promise<string[]>`: Uses `inquirer.prompt` with `type: 'checkbox'` to let user select chats from2: Data Extraction from `tdl` and File Saving

**Goal:** Implement logic to use `tdl` to export history and participants for selected chats, parse the JSON, and save raw (uncleaned) data to temporary JSON files.

**Steps:**

1.  **[ ] `tdl` Orchestrator (`src/tdl_orchestrator a list (list provided by `tdl chat ls` output, which needs to be fetched and parsed first, or user.ts`):**
    *   Implement `async function exportChatHistory(tdlPath: string, chatId enters IDs manually).
    *   Implement `async function getChatIdentifiersFromUser(): Promise<string[]>`: Prompts: string, outputJsonPath: string): Promise<boolean>`:
        *   Calls `executeTdlCommand` with `['chat', 'export', '-c', chatId, '--all', '-o', outputJsonPath]`. user to manually enter comma-separated chat IDs or usernames.
    *   Implement `async function getLlmPromptFromUser(): Promise<string>`: Uses `inquirer.prompt` with `type: 'input'` or `'editor'`.

        *   Returns success status. Handles `tdl` errors.
    *   Implement `async function exportChat2.  **[ ] `tdl` Orchestrator Update (`src/tdl_orchestrator.Participants(tdlPath: string, chatId: string, outputJsonPath: string): Promise<boolean>`:
ts`):**
    *   Refine `listChats()`: If `tdl chat ls -o json`        *   Calls `executeTdlCommand` with `['chat', 'users', '-c', chatId, '-o', outputJsonPath]`.
        *   Returns success status. Handles `tdl` errors.
2 *is not* an option, this function might call `tdl chat ls`, capture its text output, and parse.  **[ ] File Saver (`src/file_saver.ts` - Initial for JSON):**
     it (regex/string splitting) to create the `availableChats` structure for `inquirer`. This parsing can be brittle*   Implement `async function ensureOutputDir(dirPath: string): Promise<void>` using `fs.mkdir(..., { recursive: true })`.
3.  **[ ] Main Logic (`src/index.ts`):**
    *   Get. **Simpler initial approach: `getChatIdentifiersFromUser` from `ui_prompts.ts` where `tdlPath` from config or args. Get `outputDir` from args.
    *   Call `ensure user types IDs/names they already know.**
3.  **[ ] Data Processor (`src/data_processor.ts`):**
    *   Import `fs/promises`, `config`, types from `tdl_types.OutputDir`.
    *   **Iterate `parsedArgs.chats`:** (Split comma-separated string, resolvets`.
    *   Implement `function cleanMessageText(messageText: string, options?: { removeUrls?: boolean, remove to IDs if necessary - for now, assume user provides correct IDs/usernames usable by `tdl`).
    *Usernames?: boolean }): string | null`: (Port the Python regex cleaning logic to TypeScript/JavaScript regex).
    *   For each `chatIdentifier`:
        *   Define `historyJsonPath` and `participantsJsonPath` in a temporary subfolder of `outputDir` (e.g., `outputDir/temp_json/`).
        *   Implement `async function processHistoryJson(jsonFilePath: string, cleanedHistoryTxtPath: string): Promise<{ success   Call `await tdlOrchestrator.exportChatHistory(tdlPath, chatIdentifier, historyJsonPath)`.: boolean, error?: string }>`:
        *   Reads JSON file. Validates structure against `tdl_ Log success/failure.
        *   Call `await tdlOrchestrator.exportChatParticipants(tdltypes.ts`.
        *   Iterates messages, extracts text, calls `cleanMessageText`.
        *   WritesPath, chatIdentifier, participantsJsonPath)`. Log success/failure. *Note: `tdl chat users` might fail cleaned text to `cleanedHistoryTxtPath`.
        *   Returns status. Handles file/JSON errors.
     for channels; handle gracefully.*
4.  **[ ] Testing:** Unit test new `tdl_orchestrator` functions (mock `executeTdlCommand`).
5.  **[ ] Manual Testing:** Run with actual*   Implement `async function processParticipantsJson(jsonFilePath: string, cleanedParticipantsTxtPath: string): Promise<{ success: boolean, error?: string }>`:
        *   Reads JSON file. Validates.
        *    chat IDs. Verify `tdl` is called correctly. Check `temp_json/` folder for raw JSON export files. Examine logs for errors.

**End of Phase 2:** The application can extract raw history and participant dataIterates users, formats "ID: ..., Username: ..., Name: ..." lines.
        *   Writes to `cleanedParticipantsTxtPath`.
        *   Returns status. Handles errors.
4.  **[ ] Main CLI for specified chats using `tdl` and save these as intermediate JSON files.

---

## Phase 3: Text Flow (`src/main.ts`):**
    *   Call `config.load()` (or ensure config is loaded). Call `setupLogger()`.
    *   `chatIdentifiers = await ui_prompts.getChatIdentifiersFromUser()`. Cleaning, LLM Interaction, Saving Processed Text

**Goal:** Parse the raw JSON, clean text, call LLM API, and save cleaned history, participants, and LLM summary to final `.txt` files.

**Steps:**

1. (Or call `tdl_orchestrator.listChats` then `ui_prompts.getChatSelectionsFromUser`).
    *   `llmPrompt = await ui_prompts.getLlmPromptFromUser()  **[ ] Text Cleaner (`src/text_cleaner.ts`):**
    *   Implement `function`.
    *   Create output directories (`config.TDL_OUTPUT_DIR`, `config.CLEANED_DATA_DIR`) if they don't exist.
    *   Loop `chatIdentifiers`:
        *   Define cleanMessageText(messageText: string, options?: { removeUrls?: boolean; removeUserMentions?: boolean /* ...other options */ }): string | null`:
        *   Define and apply regex for system messages, media placeholders, URLs, paths for raw JSON output and cleaned TXT output.
        *   `await tdl_orchestrator. user mentions/prefixes.
        *   Return cleaned string or `null` if empty/irrelevant.
2.  **[ ] LLM Service (`src/llm_service.ts`):**
    *   Implement `async function getexportChatHistory(identifier, historyJsonPath)`.
        *   `await data_processor.processHistoryJson(historyLlmSummary(apiKey: string, endpointUrl: string | undefined, modelName: string | undefined, combinedPromptAndHistory: string, maxHistoryTokens: number): Promise<string | null>`:
        *   Implement truncation logic forJsonPath, historyTxtPath)`.
        *   If group (how to determine this? `tdl` `combinedPromptAndHistory` based on `maxHistoryTokens`.
        *   Use `axios` or `fetch` might error, or `tdl chat ls` output might indicate):
            *   `await tdl_orchestrator.exportChatParticipants(identifier, participantsJsonPath)`.
            *   `await data_processor.processParticipants to call LLM API.
        *   Handle API errors, timeouts. Parse response. Return summary or `null`.
Json(participantsJsonPath, participantsTxtPath)`.
        *   Store paths of generated cleaned files for report generation.
    3.  **[ ] File Saver (`src/file_saver.ts` - for TXT):**
    *   Implement `async function saveTextFile(filePath: string, content: string): Promise<void>` using*   Log completion/errors for each step.
5.  **[ ] Testing:** Unit test `ui_prompts.ts` (mock `inquirer`). Unit test `data_processor.ts` functions with sample `tdl` JSON `fs.writeFile`.
4.  **[ ] Main Logic (`src/index.ts` - extend loop from Phase 2):**
    *   Inside the loop for each `chatIdentifier`:
        *   **After data and regex cleaning logic.
6.  **[ ] Manual Testing:** Run `npm start` (or compiled successful JSON export:**
            *   Define final output paths for cleaned history TXT, participants TXT, and summary TXT in executable). Test chat selection, prompt input. Verify `tdl` calls, JSON creation, and TXT file creation with a structured way within `outputDir` (e.g., `outputDir/chat_XYZ/history.txt`). cleaned content.

**End of Phase 2:** User can interactively select chats, provide a prompt. The application
            *   **Process History JSON:**
                *   Read `historyJsonPath` (`fs.readFile`). orchestrates `tdl` to get raw data, then processes and cleans it into `.txt` files.

---

## Parse JSON.
                *   Iterate messages, extract text, call `text_cleaner.cleanMessageText`. Phase 3: LLM Integration & HTML Report Generation

**Goal:** Call the chosen LLM API with cleaned history
                *   Concatenate cleaned texts into `fullCleanedHistory`.
                *   Call `file_saver.saveTextFile(cleanedHistoryTxtPath, fullCleanedHistory)`.
            *   **Process Participants JSON:**
                *   Read `participantsJsonPath`. Parse JSON.
                *   Iterate users, format (ID, Username, Name). and user prompt. Generate a final HTML report displaying summaries and links to data files.

**Steps:**

1.  **[ ] LLM Service (`src/llm_service.ts`):**
    *   Import `axios` or use `fetch`, `config`.
    *   Implement `async function getLlmSummary(user
                *   Concatenate into `formattedParticipantsText`.
                *   Call `file_saver.saveTextFile(participantsTxtPath, formattedParticipantsText)`.
            *   **Call LLM:**
                *   Load `LLPrompt: string, historyText: string): Promise<string | null>`:
        *   Load `LLM_API_KEY`, `LLM_ENDPOINT_URL` from `config`.
        *   Implement truncation for `historyText`M_API_KEY` etc. from `config`.
                *   Construct prompt for LLM: `User Prompt: ${parsedArgs.prompt}\n\nChat History:\n${fullCleanedHistory}`.
                 based on `config.MAX_LLM_HISTORY_TOKENS`.
        *   Construct final prompt for LLM.
        *   Make `axios.post` or `fetch` call. Handle headers, body, timeout.
        *   Implement robust error handling for API calls (status codes, network errors). Log errors.
        *   Parse response*   `summary = await llm_service.getLlmSummary(apiKey, ..., combinedPrompt)`.
                *   If `summary`, call `file_saver.saveTextFile(summaryTxtPath, summary)`. Else, extract summary. Return summary or `null`.
2.  **[ ] Report Generator (`src/report_generator.ts`):**
    *   Import `fs/promises`, `path`, `config`.
    *    log LLM failure.
            *   (Optional) Delete temporary JSON files from `outputDir/temp_json/`.
Implement `interface ReportChatItem { chatId: string; chatTitle?: string; summary?: string | null; historyTxtPath?: string;5.  **[ ] Types (`src/types.ts`):** Define interfaces for `tdl` message structure participantsTxtPath?: string; error?: string; }`.
    *   Implement `function generateHtmlReport(report, participant structure, etc., to help with JSON parsing.
6.  **[ ] Testing:** Unit test `textItems: ReportChatItem[]): string`:
        *   Generates HTML string. Embed CSS in `<style>` tag_cleaner`. Unit test `llm_service` (mock HTTP client). Unit test main processing logic (mock for simplicity.
        *   Loops `reportItems`. For each item, creates a section displaying title/ID, the file reads/writes, mock `tdl_orchestrator` outputs, mock `llm_service`).
7.  **[ ] Manual Testing:** Run with chat IDs and a prompt. Check the final `outputDir` for ` LLM summary (or error message), and relative links to cleaned `.txt` files (e.g., `<a href="./history.txt`, `participants.txt`, and `summary.txt`. Verify content and cleaning. Check LLM APIcleaned_data/chat_123_history.txt">View History</a>`).
        *   Design for a "beautiful call logs/errors.

**End of Phase 3:** Full data pipeline from `tdl` extraction to cleaned, award-winning" look.
3.  **[ ] Main CLI Flow Update (`src/main.ts text files and LLM summary files is working.

---

## Phase 4: HTML Report Generation

**Goal:** Generate a`):**
    *   Inside the loop processing each chat identifier:
        *   After `data_processor.process polished `report.html` file that lists processed chats and links to their respective output text files.

**Steps:**

1HistoryJson`:
            *   Read the cleaned history text from the generated TXT file.
            *   `.  **[ ] HTML Reporter (`src/html_reporter.ts`):**
    *   Implement `interfacesummary = await llm_service.getLlmSummary(llmPrompt, cleanedHistoryText)`.
            *   Store ProcessedChatData { chatId: string; title?: string; historyFile?: string; participantsFile?: string; summary `summary` along with file paths.
    *   After the loop:
        *   Collect all `ReportChatItem` data.
        *   `htmlContent = report_generator.generateHtmlReport(allReportItems)`.
        *   `await fs.writeFile(config.REPORT_HTML_PATH, htmlContent)`.
        *File?: string; error?: string; }`
    *   Implement `async function generateReport(processedChats: ProcessedChatData[], reportHtmlPath: string): Promise<void>`:
        *   **CSS Styles:** Define CSS as   Log `Report generated: ${config.REPORT_HTML_PATH}`. Optionally open it automatically (`open` package on npm).
4.  **[ ] Testing:** Unit test `llm_service.ts` (mock a string constant within the function (or load from a simple CSS file string). Aim for clean, modern, responsive.
        *   **HTML Structure:** Use template literals to build the HTML string.
            *   Include header, `axios`/`fetch`, test truncation). Unit test `report_generator.ts` (check HTML output structure and title, embedded CSS.
            *   Loop through `processedChats`.
            *   For each chat, create a section links).
5.  **[ ] Manual Testing:** Run full flow. Verify LLM calls are made. Check/card:
                *   Display `chatId` (and `title` if you manage to get it from ` `report.html` content, summaries, and links. Test with LLM API errors.

**End of Phase tdl` output or user input).
                *   If `historyFile`, add `<a href="./${path3:** Full application complete. User interacts via console, data is extracted via `tdl`, processed, summarized by LLM,.relative(path.dirname(reportHtmlPath), historyFile)}">View History</a>`. Make links relative to the and presented in a local HTML report.

---

## Phase 4: Polishing, Packaging & Documentation

**Goal:** Ref report's location.
                *   Same for `participantsFile` and `summaryFile`.
                *   If `ine error handling, improve user feedback, consider packaging for easier distribution, and write comprehensive documentation.

**Steps:**

error`, display the error message.
        *   Call `file_saver.saveTextFile(reportHtmlPath, generatedHtmlString)`.
2.  **[ ] Main Logic (`src/index.ts` - extend):**
1.  **[ ] Error Handling & User Feedback:**
    *   Review all `try...catch` blocks    *   After the loop processing all chats:
        *   Collect `ProcessedChatData` objects for each chat. Ensure user-friendly error messages are printed to console using `chalk` for better visibility.
    *   Provide clear progress indicators during `tdl` execution and LLM calls (e.g., "Exporting history for Chat X... (this (with paths to the TXT files created in Phase 3, or error messages).
        *   Define `reportHtmlPath = path.join(outputDir, 'report.html')`.
        *   Call `await html_reporter.generateReport(allProcessedChatData, reportHtmlPath)`.
        *   Print `Report generated: ${reportHtmlPath}` may take a while)"). `ora` package can be used for spinners.
2.  **[ ] Configuration Flexibility:**
    *   Consider adding command-line arguments (via `commander` or `yargs`) to override `. to console.
3.  **[ ] Testing:** Unit test `generateReport` (provide mock `ProcessedChatData`, check if output HTML string contains correct links and structure).
4.  **[ ] Manual Testing:** Run the full applicationenv` config for output directories, LLM model, etc.
3.  **[ ] Packaging (Optional):. Open the generated `report.html` in a browser. Verify links work, content is displayed, and styling is acceptable**
    *   Investigate `pkg` or `nexe` to bundle the Node.js/TS app into a single executable. This simplifies distribution *but user still needs `tdl` installed separately*.
    *   Document this process if. Test with scenarios where some files might be missing (e.g., participants for a channel, or LLM summary implemented.
4.  **[ ] README.md:**
    *   Detailed setup instructions: Installing Node.js, failed).

**End of Phase 4:** A beautiful HTML report is generated, providing a user-friendly interface to `tdl`, running `tdl login`, cloning repo, `npm install`.
    *   How to configure `. the extracted and summarized data.

---

## Phase 5: Polishing, Error Handling, Build & Distribution (env` (API keys).
    *   How to run the application.
    *   Explanation of output filesOptional)

**Goal:** Refine error handling, improve user feedback, add minor features, and prepare for potential distribution and `report.html`.
    *   Troubleshooting common issues.
5.  **[ ] Final Code.

**Steps:**

1.  **[ ] Enhanced Error Handling & Feedback:**
    *   Throughout all Review & Refactor:** Clean up code, ensure consistency, remove dead code, verify all AI best practices are met.
6 `tdl` calls and API calls, provide more specific error messages to the console.
    *   In the HTML report,.  **[ ] Extensive Manual Testing:** Test on different OS if possible (if packaging). Test with various chat types clearly indicate if a step failed for a particular chat (e.g., "History: Extracted", "Participants: and sizes. Test different LLM prompts.

**End of Phase 4:** A polished, well-documented CLI N/A (Channel)", "Summary: Failed - API Error").
2.  **[ ] Configuration for Cleaning:** Allow users to pass CLI flags to toggle `removeUrls`, `removeUserMentions` in `text_cleaner application that is relatively easy for users (who are comfortable with installing `tdl` and Node.js) to use.
.ts` (pass options down).
3.  **[ ] Resolve Chat Titles:** Modify `tdl_orchestr```

This plan provides a very detailed, step-by-step guide suitable for an AI developer agent, focusing on Nodeator.listChats` to also return titles. Store these and use them in the processing loop and HTML report for better.js/TypeScript for orchestration and leveraging the external `tdl` tool for the core Telegram functionality. It aims for UX.
4.  **[ ] User Input Validation:** More robust validation for `--chats` argument (e. a good user experience via console interaction and a final HTML report, while keeping the custom code complexity manageable.
