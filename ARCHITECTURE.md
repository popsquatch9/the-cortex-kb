# Cortex KB Architecture & Deployment

```
┌─────────────────────────────────────────────────────────────┐
│                    Cortex Knowledge Base                     │
│                     (Python CLI App)                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              │
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        ▼                                           ▼
┌──────────────┐                            ┌──────────────┐
│   Local      │                            │   Remote     │
│ Deployment   │                            │ Deployment   │
└──────────────┘                            └──────────────┘
        │                                           │
        │                                           │
   ┌────┴────┐                               ┌─────┴─────┐
   │         │                               │           │
   ▼         ▼                               ▼           ▼
┌──────┐ ┌────────┐                    ┌────────┐ ┌──────────┐
│ Bare │ │ Docker │                    │  VPS   │ │  Cloud   │
│Metal │ │        │                    │        │ │Codespaces│
└──────┘ └────────┘                    └────────┘ └──────────┘
   │         │                              │           │
   │         │                              │           │
   └────┬────┘                              └─────┬─────┘
        │                                         │
        ▼                                         ▼
   ┌─────────────────┐                  ┌──────────────────┐
   │  Your Computer  │                  │   Server/Cloud   │
   │                 │                  │                  │
   │  cortex_data/   │                  │   cortex_data/   │
   │  ├─ nodes.json  │                  │   ├─ nodes.json  │
   │  └─ edges.json  │                  │   └─ edges.json  │
   └─────────────────┘                  └──────────────────┘
```

## Deployment Methods

### 1. Local Bare Metal
```bash
pip install -r requirements.txt
python cortex_cli.py add document.md
```
- ✅ Direct access, fastest
- ✅ Full control
- ❌ Requires Python setup

### 2. Docker Container
```bash
docker-compose up -d
docker-compose exec cortex-kb python cortex_cli.py stats
```
- ✅ Isolated environment
- ✅ Consistent across systems
- ❌ Requires Docker

### 3. VPS/Server
```bash
ssh user@server
git clone repo && pip install -r requirements.txt
```
- ✅ Remote access
- ✅ Always available
- ❌ Requires server management

### 4. GitHub Codespaces
```
Create → Wait → pip install -r requirements.txt
```
- ✅ No local setup
- ✅ Browser-based
- ❌ Temporary environment

## Data Flow

```
┌──────────┐      ┌───────────────┐      ┌──────────────┐
│   You    │─────▶│  cortex_cli   │─────▶│   Cortex     │
│          │      │  (interface)  │      │   (core)     │
└──────────┘      └───────────────┘      └──────────────┘
                                                  │
                                                  ▼
                                         ┌─────────────────┐
                                         │  Knowledge      │
                                         │  Graph          │
                                         │                 │
                                         │  Semantic       │
                                         │  Engine         │
                                         │                 │
                                         │  Source         │
                                         │  Discovery      │
                                         └─────────────────┘
                                                  │
                                                  ▼
                                         ┌─────────────────┐
                                         │  cortex_data/   │
                                         │  ├─ nodes.json  │
                                         │  └─ edges.json  │
                                         └─────────────────┘
```

## What WON'T Work

```
┌──────────────────┐
│  GitHub Pages    │ ❌ Static HTML only
└──────────────────┘    Can't run Python

┌──────────────────┐
│  Direct Browser  │ ❌ No web UI
└──────────────────┘    (yet)

┌──────────────────┐
│  Mobile App      │ ❌ Not implemented
└──────────────────┘    (future)
```

## What WILL Work

```
┌──────────────────┐
│  Command Line    │ ✅ Primary interface
└──────────────────┘

┌──────────────────┐
│  Python Scripts  │ ✅ Programmatic API
└──────────────────┘

┌──────────────────┐
│  Docker          │ ✅ Containerized
└──────────────────┘

┌──────────────────┐
│  pip install     │ ✅ System-wide
└──────────────────┘
```

## Installation Flow

```
START
  │
  ▼
Clone Repository ────┐
  │                  │
  ▼                  │
Choose Method        │
  │                  │
  ├─ Automated ──────┤
  │    └─ ./install.sh
  │                  │
  ├─ Manual ─────────┤
  │    └─ pip install -r requirements.txt
  │                  │
  ├─ Docker ─────────┤
  │    └─ docker-compose up
  │                  │
  └─ Package ────────┤
       └─ pip install -e .
                      │
  ┌───────────────────┘
  ▼
Verify Installation
  │
  └─ python cortex_cli.py --help
  │
  ▼
Configure (.env)
  │
  ▼
Start Using!
```

## Future Architecture (Roadmap)

```
┌─────────────────────────────────────────────────────────────┐
│                        Web UI (Future)                       │
│                    ┌──────────────────┐                     │
│                    │   Flask/FastAPI   │                     │
│                    │   REST API        │                     │
│                    └──────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Current Cortex Core                       │
│                     (Python CLI)                             │
└─────────────────────────────────────────────────────────────┘
```

Then GitHub Pages COULD host the web UI frontend!

## Summary

**Current State:**
- ✅ Python CLI application
- ✅ Multiple deployment options
- ✅ Local or cloud ready
- ❌ Not suitable for GitHub Pages (it's not a website)

**Future Possibilities:**
- 🔄 Web UI (can be hosted on GitHub Pages)
- 🔄 REST API
- 🔄 Mobile app
- 🔄 Browser extension

---

See [HOW_TO_LAUNCH.md](HOW_TO_LAUNCH.md) for detailed launch instructions.
