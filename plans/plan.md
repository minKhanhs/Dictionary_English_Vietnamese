# Plan: Implement Missing CRUD & Unit Tests

## Codebase Context

### Current State (feature/crud branch)

**Files WITH code — DO NOT MODIFY:**
| File | Lines | Notes |
|------|-------|-------|
| `config/AppConfig.py` | 38 | PascalCase imports, ALPHABET_SIZE=28, data files at project root |
| `structures/Trie.py` | 33 | `TrieNode` with dict-based children, `insert(word)`/`search(word)`→bool, `startsWith(prefix)`→bool |
| `structures/ArrayList.py` | 46 | `add/get/remove/contains/size/toString`, no `to_list()` |
| `algorithms/Levenshtein.py` | 40 | Instance-based: `Levenshtein(target).distance(input)` |
| `algorithms/FuzzySearch.py` | 74 | Uses Trie+Levenshtein for fuzzy suggestions |
| `utils/StringUtils.py` | 15 | `join()`, `normalizeWord()`, `removeExtraSpaces()` only |
| `validate/Validation.py` | 67 | `isEmpty/isLengthValid/isEnglishWord/isVietnameseMeaning/isValidExample/isValidSynonym/isValidMenuOption/hasEnoughFields/isValidDictionaryEntry` |
| `tests/TestFuzzySearch.py` | 101 | unittest.TestCase style, Vietnamese comments |

**Files EMPTY — need implementation:**
| File | Lines | Purpose |
|------|-------|---------|
| `models/Word.py` | 0 | Word model (english, vietnamese, example, synonyms) |
| `services/FileService.py` | 0 | Read/write txt files |
| `services/DictionaryService.py` | 0 | CRUD business logic |
| `ui/Menu.py` | 0 | Console menu |
| `main.py` | 0 | Entry point |

**Missing files — need creation:**
| File | Purpose |
|------|---------|
| `models/HistoryList.py` | History tracking with MAX_HISTORY_SIZE |
| `models/FavoriteList.py` | Favorite words, no duplicates |
| `tests/TestWord.py` | Unit tests for Word |
| `tests/TestHistoryList.py` | Unit tests for HistoryList |
| `tests/TestFavoriteList.py` | Unit tests for FavoriteList |
| `tests/TestArrayList.py` | Unit tests for ArrayList |
| `tests/TestValidation.py` | Unit tests for Validation |
| `tests/TestTrie.py` | Unit tests for Trie |
| `tests/TestDictionaryService.py` | Unit tests for DictionaryService CRUD |

### API Constraints (from existing code)

- **Imports use PascalCase:** `from config.AppConfig import AppConfig`, `from structures.Trie import TrieNode`, etc.
- **Trie.search() returns bool**, not Word objects → use ArrayList to store Word objects, Trie only for fast existence check
- **Levenshtein is instance-based** → `Levenshtein(target).distance(input)` not static
- **ArrayList** has `add/get/remove/contains/size/toString` but NO `to_list()`, `is_empty()`, `clear()`, `push_back()`, `set()`
- **StringUtils** has NO `trim()`, `split()`, `to_lower_case()` → use Python built-ins (`str.strip()`, `str.split()`) in new code
- **AppConfig** data files at project root (not in `data/` subfolder): `dictionary.txt`, `history.txt`, `favorites.txt`
- **AppConfig.MAX_MENU_OPTION = 9** (menu options 0-9, need to add delete → bump to 10)

---

## Phase 1: .gitignore & AppConfig Update

### 1.1 Update `.gitignore`
- Add `__pycache__/`, `*.pyc`

### 1.2 Update `config/AppConfig.py`
- Bump `MAX_MENU_OPTION` from 9 → 10 (to accommodate new delete option)
- This is a config-only change, not a logic change

---

## Phase 2: Implement Empty Model Files

### 2.1 `models/Word.py`
```
Imports: config.AppConfig, utils.StringUtils, validate.Validation
Class Word:
  - __init__(english, vietnamese, example, synonyms)
  - get_english/get_vietnamese/get_example/get_synonyms
  - get_synonym_count
  - set_english/set_vietnamese/set_example
  - add_synonym(synonym) → bool (no dupes, max MAX_SYNONYMS)
  - has_synonym(synonym) → bool
  - display() → print formatted
  - to_file_line() → str (FIELD_SEPARATOR joined)
  - from_file_line(line) → Word|None (static)
```

### 2.2 `models/HistoryList.py`
```
Imports: config.AppConfig, utils.StringUtils
Class HistoryList:
  - __init__()
  - add(word) → bool (limit MAX_HISTORY_SIZE, FIFO eviction)
  - display(), get_count(), get_item(index), clear(), to_list()
```

### 2.3 `models/FavoriteList.py`
```
Imports: utils.StringUtils
Class FavoriteList:
  - __init__()
  - add(word) → bool (no dupes)
  - remove(word) → bool
  - contains(word) → bool
  - display(), get_count(), get_item(index), clear(), to_list()
```

---

## Phase 3: Implement Service Layer

### 3.1 `services/FileService.py`
```
Imports: config.AppConfig, models.Word, utils.StringUtils, validate.Validation
Class FileService:
  - ensure_data_files() → create files if missing
  - load_dictionary() → list[Word]
  - save_dictionary(words) → bool
  - load_history() → list[str]
  - save_history(history) → bool
  - load_favorites() → list[str]
  - save_favorites(favorites) → bool
Note: Data files at project root (per AppConfig paths)
```

### 3.2 `services/DictionaryService.py`
```
Imports: structures.Trie, structures.ArrayList, algorithms.Levenshtein,
         models.*, services.FileService, utils.StringUtils, validate.Validation
Class DictionaryService:
  - __init__(file_service)
  - load_data() / save_data()
  - add_word_object(word) → bool
  - add_word_interactive() → bool (console input)
  - delete_word(english) → bool ← NEW CRUD FEATURE
  - delete_word_interactive() → bool
  - update_meaning_interactive() → bool ← NEW CRUD FEATURE
  - add_synonym_interactive() → bool
  - search_exact(word) → Word|None (adds to history on hit)
  - search_exact_interactive()
  - search_approximate(word) → list[Word]
  - search_approximate_interactive()
  - add_favorite_interactive() / remove_favorite_interactive()
  - show_history() / show_favorites() / display_all_words()
  - word_exists(word) → bool
Note: Trie for existence check only (returns bool).
      ArrayList stores Word objects. Linear scan for Word retrieval.
```

---

## Phase 4: UI & Entry Point

### 4.1 `ui/Menu.py`
```
Menu options (updated):
1. Thêm từ mới (Add word)
2. Thêm từ đồng nghĩa (Add synonym)
3. Sửa nghĩa từ (Edit meaning) ← NEW
4. Xóa từ (Delete word) ← NEW
5. Tra cứu chính xác (Exact search)
6. Tìm kiếm gần đúng (Approximate search)
7. Hiển thị lịch sử tra cứu (Show history)
8. Thêm từ vào Favorites (Add favorite)
9. Xóa từ khỏi Favorites (Remove favorite)
10. Hiển thị Favorites (Show favorites)
-- save on exit
0. Thoát (Exit + save)

Wait, this changes the menu numbering from original. Let me reconsider...
```

Actually, to minimize disruption, keep original menu + append delete at end:
```
1. Thêm từ mới
2. Thêm từ đồng nghĩa
3. Tra cứu chính xác
4. Tìm kiếm gần đúng
5. Hiển thị lịch sử
6. Thêm từ Favorites
7. Xóa từ Favorites
8. Hiển thị Favorites
9. Hiển thị tất cả từ
10. Xóa từ ← NEW
0. Thoát (auto-save)
```
- Remove explicit "Save data" option (auto-save on exit is cleaner)
- Add "Xóa từ" as option 10

### 4.2 `main.py`
```
Entry point:
  - Print menu: 1. Run app, 2. Run tests
  - Default: run app
  - If 2: discover and run all unittest test files
```

---

## Phase 5: Unit Tests (unittest.TestCase style)

All tests follow `TestFuzzySearch.py` pattern:
- Vietnamese comments
- `unittest.TestCase` subclass
- `setUp()` for fixtures
- `test*()` methods
- `if __name__ == "__main__": unittest.main()`
- sys.path manipulation for imports

### Test Files:

| File | Test Class | Key Test Cases |
|------|-----------|----------------|
| `tests/TestWord.py` | `TestWord` | Create word, add synonym, duplicate synonym rejected, synonym limit, to_file_line/from_file_line roundtrip, set methods |
| `tests/TestTrie.py` | `TestTrie` | Insert & search found, search not found, startsWith, empty string |
| `tests/TestArrayList.py` | `TestArrayList` | Add/get/remove/contains/size, index out of bounds, empty list |
| `tests/TestHistoryList.py` | `TestHistoryList` | Add/get items, MAX_HISTORY_SIZE limit (FIFO eviction), clear, empty display |
| `tests/TestFavoriteList.py` | `TestFavoriteList` | Add/remove/contains, duplicate rejected, clear, empty display |
| `tests/TestValidation.py` | `TestValidation` | isEmpty, isEnglishWord (valid/invalid chars), isVietnameseMeaning, isValidMenuOption, isValidDictionaryEntry |
| `tests/TestDictionaryService.py` | `TestDictionaryService` | Add word, reject duplicate, search exact (hit + miss), delete word, word_exists, history tracking |

---

## Open Questions

1. **AppConfig.MAX_MENU_OPTION**: Currently 9. Adding delete option requires bumping to 10. OK?
2. **Menu layout**: Keep original 9 options + add delete as option 10? Or reorganize?
3. **"Save data" explicit option**: Keep or remove (auto-save on exit)?
4. **Edit meaning/example**: Should I add "sửa nghĩa" (edit meaning) as a CRUD feature too, or just delete?
5. **Data file location**: Currently `dictionary.txt` etc at project root (not `data/` subfolder). Keep as-is?
