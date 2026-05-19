---
phase: 3
title: "Models va data structures"
status: pending
priority: P1
effort: ""
dependencies: [2]
---

# Phase 3: Models va data structures

## Overview

Tao model `Word` va cac cau truc du lieu tu cai dat: DynamicArray, Trie, HistoryList, FavoriteList. Day la lop luu tru trong bo nho cho nghiep vu tu dien.

## Requirements

- Functional: method/behavior khop danh sach trong `SKILL.MD`.
- Non-functional: khong dung list truc tiep lam storage nghiep vu chinh cho tu dien; DynamicArray tu quan ly size/capacity.

## Architecture

`Word` chiu trach nhiem serialize/deserialize dong dictionary. `DynamicArray` luu danh sach Word. `HistoryList` va `FavoriteList` bao boc danh sach chuyen dung. `Trie` phuc vu exact search va luu `word_data` o node ket thuc.

## Related Code Files

- Create/Modify: `models/word.py`
- Create/Modify: `structures/dynamic_array.py`
- Create/Modify: `structures/trie.py`
- Create/Modify: `structures/history_list.py`
- Create/Modify: `structures/favorite_list.py`

## Implementation Steps

1. Implement `Word` voi getter/setter, `add_synonym`, `has_synonym`, `display`, `to_file_line`, `from_file_line`.
2. Bao ve synonym: khong trung, khong vuot `AppConfig.MAX_SYNONYMS`, normalize truoc khi so sanh.
3. Implement `DynamicArray` voi `data`, `size`, `capacity`, resize gap doi khi day, check index an toan.
4. Implement `TrieNode` va `Trie`: `insert(word)`, `search(english)`, `starts_with(prefix)`, `_get_index`, `_is_valid_char`.
5. Implement `HistoryList`: add moi, gioi han `MAX_HISTORY_SIZE`, neu day xoa cu nhat, khong crash khi rong.
6. Implement `FavoriteList`: add/remove/contains/display/get/clear/to_list, khong them trung.

## Success Criteria

- [ ] `Word.to_file_line()` dung `FIELD_SEPARATOR` va `LIST_SEPARATOR`.
- [ ] `Word.from_file_line()` bo qua dong sai format bang cach tra ve `None` hoac fail an toan theo convention chon.
- [ ] `DynamicArray` tu quan ly `size` va `capacity`.
- [ ] `Trie.search()` tra ve Word neu co, `None` neu khong co.
- [ ] History va Favorite khong crash khi rong.

## Risk Assessment

Trie trong doc noi chi a-z, trong khi validation cho phep khoang trang/gach ngang. Can quyet dinh ro: normalize va bo/tu choi ky tu khong phu hop khi insert/search Trie, hoac map them space/hyphen neu giu `ALPHABET_SIZE = 28`. Ghi decision trong code/test.
