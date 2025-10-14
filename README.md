<div align="center">
  <img src="https://avatars.githubusercontent.com/u/207296579?s=200&v=4" alt="Plasmatic Logo" width="120" height="120">
  <h1>SWIFT CBPR+ Transformation Package</h1>
  <p><strong>SR2025-Compliant Bidirectional MT ↔ ISO 20022 Workflows</strong></p>
  <p>Official transformation package for Reframe v3.1+ supporting SWIFT Cross-Border Payments and Reporting Plus</p>
  <br>

  [![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
  [![Reframe](https://img.shields.io/badge/Reframe-v3.1+-orange)](https://github.com/GoPlasmatic/Reframe)
  [![SR2025](https://img.shields.io/badge/SR2025-Compliant-green)](https://www.swift.com/standards/release-guide/sr2025)

  [📚 **Package Docs**](CLAUDE.md) | [🔧 **Reframe Engine**](https://github.com/GoPlasmatic/Reframe) | [🏗️ **Architecture**](https://github.com/GoPlasmatic/Reframe/blob/main/docs/architecture.md)
</div>

---

## 🌟 What is this Package?

This is a **transformation package** for [Reframe v3.1](https://github.com/GoPlasmatic/Reframe), containing JSON-based workflow definitions for bidirectional SWIFT MT ↔ ISO 20022 transformations compliant with SR2025 standards.

### Package Contents

This package provides transformation rules for the **Cross-Border Payments and Reporting Plus (CBPR+)** framework with full **SR2025 compliance**, including:

- 🔄 **Bidirectional Transformations** - Both MT→MX (outgoing) and MX→MT (incoming)
- ✅ **SR2025 Compliant** - Business Application Header v3, UETR, LEI support
- 📋 **Comprehensive Coverage** - 40+ message type mappings
- 🧪 **Test Scenarios** - Ready-to-use sample data for testing
- 🔍 **Validation Workflows** - Message compliance checking

```
┌─────────────────────────────────┐
│   Reframe Engine (v3.1)         │
│   Transformation • Generation   │
│   Validation • Hot-reload       │
└─────────────────────────────────┘
              ↓ loads
┌─────────────────────────────────┐
│  THIS PACKAGE                   │
│  reframe-package-swift-cbpr     │
│  • MT ↔ MX workflows            │
│  • SR2025 compliance rules      │
│  • CBPR+ mapping logic          │
│  • Test scenarios & samples     │
└─────────────────────────────────┘
```

---

## 🚀 Key Features

### 📊 **Comprehensive Message Support**

- **40+ Message Types**: MT101, MT103, MT200, MT202, MT205, pacs.008, pacs.009, camt.052-054, and more
- **Payment Messages**: Customer transfers, FI transfers, direct debits, margin collection
- **Status Reports**: Rejections, returns, confirmations, statements
- **Investigation Messages**: Cancellations, resolutions, billing reports
- **New SR2025 Types**: camt.105-109, admi.024, extended pacs/pain variants

### ✅ **SR2025 Compliance**

- **Business Application Header v3**: Enhanced party identification with LEI
- **Mandatory UETR**: Unique End-to-end Transaction Reference tracking
- **Service Level Codes**: G001, G002, G003, G004
- **Priority Options**: HIGH, NORM, URGT
- **Enhanced Data Quality**: Structured remittance, creditor references

### 🔄 **Bidirectional Design**

- **MT → MX (Outgoing)**: Parse MT → BAH mapping → Document mapping → Generate XML
- **MX → MT (Incoming)**: Parse XML → Variant detection → Field mapping → Assemble MT
- **Automatic Routing**: Reframe auto-detects direction and message type

### 🧪 **Testing & Validation**

- **60+ Test Scenarios**: Real-world samples for all message types
- **Validation Workflows**: Business rule and format compliance checking
- **Sample Generation**: Create test messages on-demand

---

## 🎯 Quick Start

### Prerequisites

1. **[Reframe v3.1+](https://github.com/GoPlasmatic/Reframe)** - The transformation engine
2. **Git** - To clone this package

### Option 1: With Docker (Recommended)

```bash
# 1. Clone this package
git clone https://github.com/GoPlasmatic/reframe-package-swift-cbpr.git

# 2. Clone and run Reframe
git clone https://github.com/GoPlasmatic/Reframe.git
cd Reframe

# 3. Start with docker-compose (automatically mounts the package)
docker-compose up -d

# 4. Verify package loaded
curl http://localhost:3000/packages
```

### Option 2: From Source

```bash
# 1. Clone this package and Reframe
git clone https://github.com/GoPlasmatic/reframe-package-swift-cbpr.git
git clone https://github.com/GoPlasmatic/Reframe.git
cd Reframe

# 2. Build and run Reframe with this package
cargo build --release
REFRAME_PACKAGE_PATH=../reframe-package-swift-cbpr cargo run --release

# 3. Verify package loaded
curl http://localhost:3000/packages
```

---

## 🌐 Usage Examples

Once Reframe is running with this package, you can transform messages:

### MT → MX Transformation

```bash
curl -X POST http://localhost:3000/api/transform \
  -H "Content-Type: application/json" \
  -d '{
    "message": "{1:F01BANKBEBBAXXX0000000000}{2:O1030800230714BANKDEFFAXXX00000000002307141600N}{3:{108:MT103 001}}{4:\n:20:REF123456789\n:23B:CRED\n:32A:230714USD1000,00\n:50K:/12345678\nJOHN DOE\n123 MAIN ST\nNEW YORK NY 10001 US\n:59:/98765432\nJANE SMITH\n456 HIGH ST\nLONDON EC1A 1BB GB\n:71A:OUR\n-}{5:{MAC:12345678}{CHK:123456789ABC}}"
  }'
```

**Result**: Converts MT103 to pacs.008 (ISO 20022 XML)

### MX → MT Transformation

```bash
curl -X POST http://localhost:3000/api/transform \
  -H "Content-Type: application/json" \
  -d '{
    "message": "<?xml version=\"1.0\"?><Document xmlns=\"urn:iso:std:iso:20022:tech:xsd:pacs.008.001.10\">...</Document>"
  }'
```

**Result**: Converts pacs.008 to MT103 (SWIFT MT format)

### Generate Sample Messages

```bash
# Generate a sample MT103
curl -X POST http://localhost:3000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "message_type": "MT103",
    "scenario": "standard"
  }'
```

### Validate Messages

```bash
# Validate any MT or MX message
curl -X POST http://localhost:3000/api/validate \
  -H "Content-Type: application/json" \
  -d '{
    "message": "<your-message>",
    "business_validation": true
  }'
```

---

## 📦 Package Structure

```
reframe-package-swift-cbpr/
├── reframe-package.json       # Package metadata and configuration
│
├── transform/                 # Transformation workflows
│   ├── index.json            # Workflow registry
│   ├── outgoing/             # MT → MX transformations
│   │   ├── parse-mt.json     # Common MT parser
│   │   ├── combine-xml.json  # XML assembler
│   │   ├── MT103/            # Message-specific workflows
│   │   │   ├── method-detection.json
│   │   │   ├── bah-mapping.json
│   │   │   ├── precondition.json
│   │   │   ├── document-mapping.json
│   │   │   └── postcondition.json
│   │   └── [other MT types]/
│   │
│   └── incoming/             # MX → MT transformations
│       ├── parse-mx.json     # Common MX parser
│       ├── pacs008/          # Message-specific workflows
│       │   ├── 01-variant-detection.json
│       │   ├── 02-preconditions.json
│       │   ├── 03-headers-mapping.json
│       │   ├── 04-mandatory-fields-mapping.json
│       │   └── [other mapping steps]/
│       └── [other MX types]/
│
├── generate/                  # Sample generation workflows
│   ├── index.json
│   ├── generate-mt.json
│   └── generate-mx.json
│
├── validate/                  # Validation workflows
│   ├── index.json
│   ├── validate-mt.json
│   └── validate-mx.json
│
└── scenarios/                 # Test scenarios
    ├── index.json
    ├── outgoing/             # MT → MX test cases
    │   └── [scenario files].json
    └── incoming/             # MX → MT test cases
        └── [scenario files].json
```

---

## 📋 Supported Transformations

### MT → MX (Outgoing)

| MT Type | ISO 20022 Type | Description |
|---------|---------------|-------------|
| MT101 | pain.001 | Request for Transfer |
| MT103 | pacs.008 | Customer Credit Transfer |
| MT103REJT | pacs.002 | Payment Status (Rejection) |
| MT103RETN | pacs.004 | Payment Return |
| MT192 | camt.056 | Request for Cancellation |
| MT196 | camt.029 | Cancellation Response |
| MT200 | pacs.009 | Financial Institution Transfer |
| MT202 | pacs.009 | General Financial Institution Transfer |
| MT202COV | pacs.009 | Cover Payment |
| MT202REJT | pacs.002 | Transfer Rejection |
| MT202RETN | pacs.004 | Transfer Return |
| MT205 | pacs.009 | Financial Institution Transfer Execution |
| MT205COV | pacs.009 | Cover Payment Execution |
| MT292 | camt.056 | Request for Cancellation |
| MT296 | camt.029 | Cancellation Status |
| MT900 | camt.054 | Confirmation of Debit |
| MT910 | camt.054 | Confirmation of Credit |

### MX → MT (Incoming)

| ISO 20022 Type | MT Type | Description |
|---------------|---------|-------------|
| pain.001 | MT101 | Customer Credit Transfer Initiation |
| pacs.002 | MT103REJT/MT202REJT | Payment Status Report |
| pacs.003 | MT104 | Direct Debit |
| pacs.004 | MT103RETN/MT202RETN | Payment Return |
| pacs.008 | MT103 | Customer Credit Transfer |
| pacs.009 | MT202/MT205 | Financial Institution Transfer |
| pacs.010 | MT204 | Direct Debit (Margin Collection) |
| camt.029 | MT196/MT296 | Resolution of Investigation |
| camt.052 | MT942 | Bank to Customer Account Report |
| camt.053 | MT940 | Bank to Customer Statement |
| camt.054 | MT103/MT202/MT900/MT910 | Bank to Customer Debit/Credit |
| camt.056 | MT192/MT292 | Payment Cancellation Request |
| camt.057 | MT210 | Notice to Receive |
| camt.058 | MT292 | Notification to Receive Cancellation |
| camt.105 | MTn90 | Billing Report |
| camt.106 | MTn91 | Investigation Response |
| camt.107 | MT110 | Non-deliverable Information |
| camt.108 | MT111 | Identification Verification Request |
| camt.109 | MT112 | Identification Verification Report |
| admi.024 | MT199 | System Event Notification |

---

## 🛠️ Development

### Workflow Formatting

Format workflow JSON files for optimal readability:

```bash
python3 json_semi_beautifier.py --in-place transform/incoming/pacs008/*.json
python3 json_semi_beautifier.py --in-place transform/outgoing/MT103/*.json
```

### Package Configuration

The `reframe-package.json` file defines:

```json
{
  "id": "swift-cbpr-mt-mx",
  "name": "SWIFT CBPR+ MT <-> MX Transformations - SR2025",
  "version": "2.0.0",
  "description": "Official SWIFT CBPR+ transformations",
  "engine_version": "^3.1.1",
  "required_plugins": ["swift_mt_message", "cbpr_mx_message"],
  "workflows": {
    "transform": { "path": "transform" },
    "generate": { "path": "generate" },
    "validate": { "path": "validate" }
  },
  "scenarios": { "path": "scenarios" }
}
```

### Testing with Reframe

```bash
# Hot-reload workflows after changes
curl -X POST http://localhost:3000/admin/reload-workflows

# Test specific transformation
curl -X POST http://localhost:3000/api/transform \
  -H "Content-Type: application/json" \
  -d @scenarios/outgoing/mt103_to_pacs008_cbpr_standard.json
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [**CLAUDE.md**](CLAUDE.md) | Detailed guidance for working with this package |
| [**Reframe Architecture**](https://github.com/GoPlasmatic/Reframe/blob/main/docs/architecture.md) | Understanding the engine architecture |
| [**Configuration Guide**](https://github.com/GoPlasmatic/Reframe/blob/main/docs/configuration.md) | Configuring Reframe and packages |
| [**SWIFT SR2025**](https://www.swift.com/standards/release-guide/sr2025) | Official SWIFT standards documentation |
| [**ISO 20022**](https://www.iso20022.org/catalogue-messages) | ISO 20022 message catalog |

---

## 🏗️ How It Works

### Outgoing Flow (MT → MX)

```
Input MT Message
       ↓
1. parse-mt.json          → Parse MT blocks (1-5)
       ↓
2. precondition.json      → Validate input business rules
       ↓
3. bah-mapping.json       → Create Business Application Header v3
       ↓
4. document-mapping.json  → Transform business data to MX
       ↓
5. postcondition.json     → Validate output compliance
       ↓
6. combine-xml.json       → Generate ISO 20022 XML
       ↓
Output MX Message (XML)
```

### Incoming Flow (MX → MT)

```
Input MX Message (XML)
       ↓
1. parse-mx.json                → Parse XML to JSON
       ↓
2. 01-variant-detection.json    → Identify MT variant/type
       ↓
3. 02-preconditions.json        → Validate transformation rules
       ↓
4. 03-headers-mapping.json      → Construct SWIFT headers
       ↓
5. 0X-...-mapping.json          → Sequential field mappings
       ↓
6. [final]-postconditions.json  → Assemble and publish
       ↓
Output MT Message
```

---

## ⚙️ Configuration with Reframe

### Via reframe.config.json

```json
{
  "packages": [
    {
      "path": "../reframe-package-swift-cbpr",
      "enabled": true
    }
  ]
}
```

### Via Environment Variable

```bash
export REFRAME_PACKAGE_PATH=/path/to/reframe-package-swift-cbpr
```

### Docker Volume Mount

```yaml
services:
  reframe:
    image: plasmatic/reframe:3.1
    volumes:
      - ./reframe-package-swift-cbpr:/packages/swift-cbpr:ro
    environment:
      - REFRAME_PACKAGE_PATH=/packages/swift-cbpr
```

---

## 🔍 SR2025 Compliance Details

### Business Application Header v3

- Enhanced party identification with **LEI (Legal Entity Identifier)** support
- Improved **service level codes**: G001 (high priority), G002 (normal), G003 (real-time), G004 (same day)
- Extended **priority options**: HIGH, NORM, URGT
- **Mandatory UETR** (Unique End-to-end Transaction Reference) for all payment messages

### Enhanced Data Quality

- **Structured remittance information**: Creditor references, invoice details
- **Document adjustment details**: Credit/debit notes, remittance discounts
- **Improved address structures**: Country subdivision codes, building numbers
- **Enhanced party identification**: LEI, BIC+BEI, proprietary identification schemes

### New Message Types

This package includes workflows for all new SR2025 message types:

- **camt.105**: Billing report
- **camt.106**: Investigation response
- **camt.107**: Non-deliverable information
- **camt.108**: Identification verification request
- **camt.109**: Identification verification report
- **admi.024**: System event notification

---

## 🤝 Contributing

We welcome contributions to improve this package:

- 🐛 **Report Issues**: Found a bug or mapping error? [Open an issue](https://github.com/GoPlasmatic/reframe-package-swift-cbpr/issues)
- 💡 **Suggest Enhancements**: Have ideas for new features? Share them!
- 🔧 **Submit PRs**: Contribute workflow improvements or new scenarios
- 📖 **Improve Docs**: Help make documentation clearer

---

## 📞 Community & Support

- **💬 [Discussions](https://github.com/GoPlasmatic/Reframe/discussions)** - Ask questions about package usage
- **🐛 [Issues](https://github.com/GoPlasmatic/reframe-package-swift-cbpr/issues)** - Report bugs or request features
- **📧 Email** - enquires@goplasmatic.io
- **🌐 Website** - [goplasmatic.io](https://goplasmatic.io)

---

## 📄 License

This package is licensed under the **Apache License 2.0**. You are free to use, modify, and distribute it. See [LICENSE](LICENSE) for details.

---

<div align="center">
  <p><strong>Built with ❤️ by Plasmatic</strong></p>
  <p>Making SWIFT transformations transparent, compliant, and reliable.</p>
  <br>
  <p>
    <a href="https://github.com/GoPlasmatic/reframe-package-swift-cbpr">⭐ Star this Package</a> •
    <a href="https://github.com/GoPlasmatic/Reframe">🚀 Reframe Engine</a> •
    <a href="CLAUDE.md">📚 Package Documentation</a>
  </p>
</div>
