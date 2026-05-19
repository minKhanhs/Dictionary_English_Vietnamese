---
phase: 5
title: "File persistence"
status: pending
priority: P1
effort: ""
dependencies: [2, 3]
---

# Phase 5: File persistence

## Overview

Xay dung `FileService` doc/ghi dictionary, history, favorites bang file text. Module nay chi lam persistence va parse, khong xu ly nghiep vu.

## Requirements

- Functional: co `ensure_data_folder`, `load_dictionary`, `save_dictionary`, `load_history`, `save_history`, `load_favorites`, `save_favorites`.
- Non-functional: file khong ton tai hoac dong sai format khong lam crash; dung config cho path/separator.

## Architecture

`FileService` tra ve cac object/list plain cho `DictionaryService` nap vao DynamicArray/HistoryList/FavoriteList. Dictionary format: `english|vietnamese|example|synonym1,synonym2`.

## Related Code Files

- Create/Modify: `services/file_service.py`
- Use: `models/word.py`
- Data: `data/dictionary.txt`, `data/history.txt`, `data/favorites.txt`

## Implementation Steps

1. Implement `ensure_data_folder()` tao `data/` va cac file rong neu thieu.
2. `load_dictionary()` doc tung dong, validate field count, parse bang `Word.from_file_line`, bo qua dong sai.
3. `save_dictionary(words)` nhan DynamicArray hoac list Word, ghi tung `word.to_file_line()`.
4. `load_history()` va `load_favorites()` doc moi dong la mot tu, trim/normalize, bo qua dong rong.
5. `save_history(history)` va `save_favorites(favorites)` ghi moi item mot dong.
6. Boc try/except co ban cho IO; loi doc/ghi nen duoc xu ly an toan va thong bao ngan gon neu can.

## Success Criteria

- [ ] Chay khi data files chua ton tai van tao/tra ve du lieu rong.
- [ ] Dong dictionary sai format bi bo qua, chuong trinh tiep tuc.
- [ ] Khong co business rule nhu "favorite phai ton tai trong dictionary" trong FileService.
- [ ] Save/load round-trip giu duoc english, vietnamese, example, synonyms.

## Risk Assessment

Can tranh lam FileService phu thuoc qua sau vao DynamicArray. Nen ho tro iterable/to_list de save linh hoat nhung van de DictionaryService quyet dinh cau truc nghiep vu.
