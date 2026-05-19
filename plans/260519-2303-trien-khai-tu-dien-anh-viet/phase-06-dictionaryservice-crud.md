---
phase: 6
title: "DictionaryService CRUD"
status: pending
priority: P1
effort: ""
dependencies: [3, 4, 5]
---

# Phase 6: DictionaryService CRUD

## Overview

Implement lop nghiep vu chinh cho CRUD tu dien, search, history, favorites va dieu phoi doc/ghi file. Day la phase trung tam cua ung dung.

## Requirements

- Functional: du method trong `SKILL.MD`, gom interactive va non-interactive API.
- Non-functional: UI chi goi service; service validate input va khong cho trung/du lieu sai.

## Architecture

`DictionaryService` so huu `trie`, `words`, `history`, `favorites`, `file_service`. Flow chinh: load file -> nap DynamicArray + Trie -> thao tac CRUD/search -> cap nhat structures -> save file.

## Related Code Files

- Create/Modify: `services/dictionary_service.py`
- Use: `services/file_service.py`, `models/word.py`, `structures/*`, `algorithms/levenshtein.py`, `validation/validator.py`, `utils/string_utils.py`, `config/app_config.py`

## Implementation Steps

1. Constructor khoi tao Trie, DynamicArray, HistoryList, FavoriteList, FileService.
2. `load_data()` load dictionary/history/favorites; moi Word phai vao ca DynamicArray va Trie.
3. `save_data()` goi FileService save dictionary/history/favorites.
4. `word_exists(word)` normalize va search exact bang Trie.
5. `add_word_object(word)` validate, check trung, them vao DynamicArray va Trie.
6. `add_word_interactive()` nhap english/vietnamese/example/synonyms, validate tung truong, tao Word, goi add object.
7. `add_synonym_interactive()` tim tu ton tai, validate synonym, khong trung, save vao object.
8. `search_exact(word)` normalize, search Trie, neu thanh cong them history, tra ve Word; neu that bai co the tra ve `None`.
9. `search_exact_interactive()` hien Word neu co; neu khong co thi goi goi y gan dung.
10. `search_approximate(word)` duyet DynamicArray, tinh Levenshtein, loc threshold, sap xep distance tang dan, cat `MAX_SUGGESTIONS`.
11. `add_favorite_interactive()` chi them khi tu ton tai trong dictionary.
12. `remove_favorite_interactive()`, `show_history()`, `show_favorites()`, `display_all_words()` xu ly an toan khi rong.

## Success Criteria

- [ ] Them tu moi thanh cong va khong cho them trung.
- [ ] Khong them tu rong hoac tu co so.
- [ ] Them synonym thanh cong va khong cho synonym trung/vuot gioi han.
- [ ] Exact search thanh cong them vao history.
- [ ] Exact search that bai co goi y gan dung duoc sap xep theo distance.
- [ ] Favorite chi nhan tu da ton tai.
- [ ] Save/load giu dung trang thai dictionary, history, favorites.

## Risk Assessment

Rui ro la logic interactive kho test. Giam rui ro bang cach tach core methods (`add_word_object`, `search_exact`, `search_approximate`, `word_exists`) de test truc tiep; interactive wrappers chi lo input/output.
