# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Reframe v3.0 SWIFT CBPR+ Transformation Package** for bidirectional SWIFT MT ↔ ISO 20022 MX message transformations. It's SR2025-compliant and processes messages through the dataflow-rs engine using JSON-based workflow definitions.

**Key Concepts:**
- **Workflows**: JSON files containing JSONLogic-based transformation rules
- **Bidirectional**: Supports both "outgoing" (MT→MX) and "incoming" (MX→MT) transformations
- **SR2025 Compliance**: Implements Business Application Header v3, UETR tracking, LEI support, and enhanced data quality features

## Architecture

### Directory Structure

```
transform/
├── outgoing/          # MT → MX transformations
│   ├── parse-mt.json        # Common MT parser (priority 1)
│   ├── combine-xml.json     # XML assembler (final step)
│   └── [MT-Type]/           # Message-specific workflows
│       ├── method-detection.json  # Variant detection (if needed)
│       ├── bah-mapping.json       # Business App Header v3 mapping
│       ├── precondition.json      # Pre-transformation validation
│       ├── document-mapping.json  # Core field transformations
│       └── postcondition.json     # Post-transformation validation
│
├── incoming/          # MX → MT transformations
│   ├── parse-mx.json        # Common MX parser (priority 1)
│   └── [MX-Type]/           # Message-specific workflows
│       ├── 01-variant-detection.json  # Detect MT variant
│       ├── 02-preconditions.json      # Validation rules
│       ├── 03-headers-mapping.json    # SWIFT header construction
│       ├── 0X-...-mapping.json        # Sequential field mappings
│       └── [final]-postconditions.json # Final assembly & publishing
│
└── index.json         # Workflow registry (defines loading order)

generate/              # Sample message generation workflows
validate/              # Message validation workflows
scenarios/             # Test scenarios with sample data
```

### Workflow Execution Model

**Outgoing Flow (MT → MX):**
1. `parse-mt.json` → Parse MT blocks (1-5)
2. `precondition.json` → Business rule validation
3. `bah-mapping.json` → Create BAH v3 header
4. `document-mapping.json` → Transform business data
5. `postcondition.json` → Final validations
6. `combine-xml.json` → Generate ISO 20022 XML

**Incoming Flow (MX → MT):**
1. `parse-mx.json` → Parse XML to JSON
2. `01-variant-detection.json` → Identify MT variant/type
3. `02-preconditions.json` → Validate transformation rules
4. `0X-...-mapping.json` → Sequential field mappings (headers, mandatory, parties, agents, etc.)
5. `[final]-postconditions.json` → Assemble and publish MT message

### Workflow Structure

Each workflow JSON has this structure:
```json
{
  "id": "unique-workflow-id",
  "name": "Human Readable Name",
  "description": "What this workflow does",
  "priority": 1,
  "condition": { /* JSONLogic condition for when to execute */ },
  "tasks": [
    {
      "id": "task-id",
      "name": "Task Name",
      "description": "What this task does",
      "function": { /* Function name and input/output mappings */ }
    }
  ]
}
```

### Data Flow Variables

Workflows operate on a shared data context with these key paths:

**Outgoing (MT→MX):**
- `payload` → Raw input MT message
- `SwiftMT.*` → Parsed MT data (blocks, fields)
- `metadata.transformation_direction` → "mt-to-mx"
- `metadata.progress.*` → Workflow execution state
- `Document.*` → Output ISO 20022 structure

**Incoming (MX→MT):**
- `payload` → Raw input MX XML
- `ISO20022_MX.*` → Parsed MX data
- `metadata.transformation_direction` → "mx-to-mt"
- `data.SwiftMT.*` → Output MT message structure
- `data.temp_data.*` → Temporary working variables

## Common Development Tasks

### Formatting Workflow Files

Use the JSON semi-beautifier to format workflow files for readability:

```bash
python3 json_semi_beautifier.py --in-place transform/incoming/pacs008/*.json
python3 json_semi_beautifier.py --in-place transform/outgoing/MT103/*.json
```

### Testing Transformations

Test scenarios are organized in `scenarios/index.json`:

```bash
# Structure of test scenarios
scenarios/
├── outgoing/  # MT → MX test cases
└── incoming/  # MX → MT test cases
```

Each scenario file contains sample input messages and expected outputs for specific transformation variants.

### Validation

The package includes validation workflows in `validate/`:
- `validate-mt.json` → Validate SWIFT MT messages
- `validate-mx.json` → Validate ISO 20022 MX messages

## JSONLogic Operations

Workflows use JSONLogic extensively. Common patterns:

**Variable Access:**
```json
{"var": "data.ISO20022_MX.Document.FIToFICstmrCdtTrf.CdtTrfTxInf.0.Amt.InstdAmt.#text"}
```

**Conditionals:**
```json
{"if": [
  {"==": [{"var": "variant"}, "STP"]},
  "103STP",
  "103"
]}
```

**Array Mapping:**
```json
{"map": [
  {"var": "transactions"},
  {"cat": [{"var": "id"}, "-", {"var": "amount"}]}
]}
```

## SR2025-Specific Features

When working with SR2025-compliant transformations:

- **UETR**: Unique End-to-End Transaction Reference is mandatory in payment messages
- **BAH v3**: Business Application Header version 3 with enhanced party identification
- **LEI**: Legal Entity Identifier support in party fields
- **Service Level Codes**: G001, G002, G003, G004 for different service levels
- **Priority Options**: HIGH, NORM, URGT

## Message Type Coverage

### Supported MT → MX Transformations

MT101→pain.001, MT103→pacs.008, MT103REJT→pacs.002, MT103RETN→pacs.004, MT192→camt.056, MT196→camt.029, MT200→pacs.009, MT202→pacs.009, MT202COVER→pacs.009 (COVE), MT202REJT→pacs.002, MT202RETN→pacs.004, MT205→pacs.009, MT205COVER→pacs.009 (ADV), MT205REJT→pacs.002, MT205RETN→pacs.004, MT292→camt.056, MT296→camt.029, MT900→camt.054, MT910→camt.054, MT940→camt.053, MT942→camt.052

### Supported MX → MT Transformations

pain.001→MT101, pacs.002→MT103REJT/MT202REJT, pacs.003→MT104, pacs.004→MT103RETN/MT202RETN/MT205RETN, pacs.008→MT103, pacs.009→MT202/MT202COV/MT202ADV/MT205/MT205COV, pacs.010→MT204, camt.029→MT196/MT296, camt.052→MT942, camt.053→MT940, camt.054→MT103/MT202/MT900/MT910, camt.056→MT192/MT292, camt.057→MT210, camt.058→MT292, camt.105→MTn90, camt.106→MTn91, camt.107→MT110, camt.108→MT111, camt.109→MT112, admi.024→MT199

## Workflow Development Guidelines

### Creating New Workflows

1. **Determine Direction**: Is this MT→MX (outgoing) or MX→MT (incoming)?
2. **Name Consistently**:
   - Outgoing: `[MT-Type]/[step-name].json`
   - Incoming: `[MX-Type]/[NN-step-name].json` (numbered sequence)
3. **Set Priority**: Lower numbers execute first (parsers use priority 1)
4. **Define Conditions**: Use JSONLogic to specify when the workflow should execute
5. **Register in index.json**: Add entry with path and description
6. **Test with Scenarios**: Create or update test scenarios to validate behavior

### Variant Detection

Many message types have variants (e.g., MT103 standard vs. STP, MT202 CORE vs. COVER vs. ADV). Variant detection workflows:
- Execute early (priority 2 or step 01)
- Set `data.SwiftMT.variant` or `data.SwiftMT.message_type` to control downstream logic
- Use message content to determine the appropriate variant

### Mapping Patterns

Field mappings typically follow this pattern:
```json
{
  "function": {
    "name": "map",
    "input": {
      "mappings": [
        {
          "path": "output.field.path",
          "logic": {"var": "input.field.path"}
        }
      ]
    }
  }
}
```

### Preconditions vs. Postconditions

- **Preconditions**: Validate input before transformation (e.g., required fields exist, formats are valid)
- **Postconditions**: Validate output after transformation, perform final assembly, publish message

## Package Configuration

The `reframe-package.json` file defines:
- Package metadata (id, name, version)
- Engine version requirement (`^3.1.1`)
- Required plugins: `swift_mt_message`, `cbpr_mx_message`
- Workflow paths and descriptions
- Scenarios path

This file is used by the dataflow-rs engine to load and configure the transformation package.

## Important Notes

- **Sequential Numbering**: Incoming workflows use 01, 02, 03... prefixes to control execution order
- **Context Preservation**: Data from previous workflows is preserved in the shared context
- **Error Handling**: Workflows should include validation and error reporting in preconditions
- **Field Paths**: Use exact JSON paths; array indexing starts at 0
- **Publishing**: Only postcondition workflows should publish final messages
