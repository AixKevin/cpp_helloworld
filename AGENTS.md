# PROJECT KNOWLEDGE BASE

**Purpose**: C++ Learning Repository using LearnCpp.com.cn tutorials

## OVERVIEW

This is a C++ learning project containing practice code and downloaded LearnCpp tutorial documentation. **All chapters (0-28, O, F) have been fully downloaded** to the `docs/` folder for offline access.

## STRUCTURE

```
cpp_helloworld/
├── docs/                          # LearnCpp documentation (COMPLETE - all chapters downloaded)
│   ├── LEARNING_PLAN.md          # Complete learning roadmap
│   ├── README.md                 # Docs folder documentation
│   ├── fetch_learncpp.py         # Script to download/update tutorials
│   ├── chapter_0/                # Introduction (14 files)
│   ├── chapter_1/                # C++ Basics (11 files)
│   ├── chapter_2/                # Functions and Files (13 files)
│   ├── chapter_3/                # Debugging (10 files)
│   ├── chapter_4/                # Fundamental Data Types (12 files)
│   ├── chapter_5/                # Constants and Strings (9 files)
│   ├── chapter_6/                # Operators (8 files)
│   ├── chapter_7/                # Scope and Linkage (14 files)
│   ├── chapter_8/                # Control Flow (15 files)
│   ├── chapter_9/                # Error Handling (6 files)
│   ├── chapter_10/               # Type System
│   ├── chapter_11/               # Function Templates
│   ├── chapter_12/               # References and Pointers
│   ├── chapter_13/               # Enums and Structs
│   ├── chapter_14/               # Classes Introduction
│   ├── chapter_15/               # More on Classes
│   ├── chapter_16/               # std::vector
│   ├── chapter_17/               # std::array
│   ├── chapter_18/               # Iterators and Algorithms
│   ├── chapter_19/               # Dynamic Memory
│   ├── chapter_20/               # Functions (Advanced)
│   ├── chapter_21/               # Operator Overloading
│   ├── chapter_22/               # Move Semantics
│   ├── chapter_23/               # Object Relationships
│   ├── chapter_24/               # Inheritance
│   ├── chapter_25/               # Virtual Functions
│   ├── chapter_26/               # Templates
│   ├── chapter_27/               # Exceptions
│   ├── chapter_28/               # I/O Streams
│   ├── chapter_O/                # Bit Operations
│   ├── chapter_F/                # Constexpr Functions
│   └── appendix_A-D/             # Appendices
├── 00-test_program/               # Basic C++ programs
├── 04-basic_data_type/            # Data types practice
└── AGENTS.md                      # This file
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Learn C++ | docs/LEARNING_PLAN.md | Complete learning roadmap |
| Chapter X.Y | docs/chapter_X/X_Y.md | **ALWAYS read from local files** |
| Practice code | 00-test_program/, 04-basic_data_type/ | Examples and exercises |
| Build system | 04-basic_data_type/CMakeLists.txt | CMake-based build |

## CHAPTER LOOKUP TABLE

All chapters are stored locally in `docs/chapter_X/` directories. **DO NOT use webfetch** - read directly from disk.

### Naming Convention
- Chapter files: `X_Y.md` (e.g., `5_4.md` for 5.4)
- Some files may have longer descriptive names from URL

### Quick Reference
| Chapter | Topics | File Pattern |
|---------|--------|--------------|
| 0 | Introduction, Setup | `chapter_0/*.md` |
| 1 | C++ Basics | `chapter_1/*.md` |
| 2 | Functions, Forward Declarations | `chapter_2/*.md` |
| 3 | Debugging | `chapter_3/*.md` |
| 4 | Data Types, sizeof | `chapter_4/*.md` |
| 5 | const, constexpr, string, string_view | `chapter_5/*.md` |
| 6 | Operators, Precedence | `chapter_6/*.md` |
| 7 | Scope, Linkage, static, extern | `chapter_7/*.md` |
| 8 | Control Flow, Loops, Random | `chapter_8/*.md` |
| 9 | Testing, Error Handling | `chapter_9/*.md` |
| 28 | I/O Streams | `chapter_28/*.md` |
| 27 | Exceptions | `chapter_27/*.md` |
| 26 | Templates | `chapter_26/*.md` |
| 25 | Virtual Functions | `chapter_25/*.md` |
| 24 | Inheritance | `chapter_24/*.md` |
| 23 | Object Relationships | `chapter_23/*.md` |
| 21 | Copying | `chapter_21/*.md` |
| 20 | Functions (Advanced) | `chapter_20/*.md` |
| 19 | Dynamic Memory | `chapter_19/*.md` |
| 18 | Iterators and Algorithms | `chapter_18/*.md` |
| 17 | std::array | `chapter_17/*.md` |
| 16 | std::vector | `chapter_16/*.md` |
| 15 | More on Classes | `chapter_15/*.md` |
| 14 | Classes Introduction | `chapter_14/*.md` |
| 13 | Enums and Structs | `chapter_13/*.md` |
| 12 | Pointers and References | `chapter_12/*.md` |
| 11 | Function Overloading | `chapter_11/*.md` |
| 10 | Type System, Conversions | `chapter_10/*.md` |
| O | Bit Manipulation | `chapter_O/*.md` |
| F | Constexpr Functions | `chapter_F/*.md` |

## COMMANDS

```bash
# Build the project
cd 04-basic_data_type/build
cmake ..
make

# Run executables
./04-basic_data_type

# Update docs (if needed)
cd docs
python fetch_learncpp.py
```

## LEARNING RESOURCES

- **Local docs**: `docs/` folder (COMPLETE - all 356 tutorials downloaded)
- **Online backup**: https://learncpp.com.cn/
- **Site index**: https://learncpp.com.cn/learn-cpp-site-index/
- **Learning plan**: docs/LEARNING_PLAN.md

## IMPORTANT NOTES

1. **Download status**: ALL chapters fully downloaded (~242 files, 356 tutorials)
2. **All LearnCpp content should be read from LOCAL files** - Use `read` tool on local files first
3. **File naming**: Chapter files use descriptive names from URL (e.g., `docs/chapter_9/assert-and-static_assert.md`)
4. **User progress**: Currently at Chapter 9, systematically working through tutorials
5. **Interaction style**: User requests chapter summaries to verify understanding
6. **Summary format**: Core concepts, code examples, comparison tables, one-sentence summary
2. **All LearnCpp content should be read from LOCAL files** - Use `read` tool on local files first
2. **File naming**: Chapter X.Y is typically at `docs/chapter_X/X_Y.md`
3. **User progress**: Currently at Chapter 9, systematically working through tutorials
4. **Interaction style**: User requests chapter summaries to verify understanding
5. **Summary format**: Core concepts, code examples, comparison tables, one-sentence summary
