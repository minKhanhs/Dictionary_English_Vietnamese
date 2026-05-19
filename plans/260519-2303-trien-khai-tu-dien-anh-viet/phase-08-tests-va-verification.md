---
phase: 8
title: "Tests va verification"
status: pending
priority: P1
effort: ""
dependencies: [1, 2, 3, 4, 5, 6, 7]
---

# Phase 8: Tests va verification

## Overview

Tao test runner tu viet va test files cho cac module bat buoc. Phase nay xac nhan chuong trinh dung theo doc va khong phu thuoc pytest/unittest.

## Requirements

- Functional: co `TestRunner`, `AllTests`, va test class cho Word, Trie, Levenshtein, Validator, DynamicArray, HistoryList, FavoriteList.
- Non-functional: khong dung pytest; test chay bang Python standard library.

## Architecture

`tests/test_runner.py` chua counter/assert helpers. `tests/all_tests.py` tao runner va goi tung `*Test.run(runner)`. Test uu tien core logic non-interactive; FileService can test bang temp data path hoac backup/restore data files de khong pha du lieu that.

## Related Code Files

- Create: `tests/test_runner.py`
- Create: `tests/all_tests.py`
- Create: `tests/word_test.py`
- Create: `tests/trie_test.py`
- Create: `tests/levenshtein_test.py`
- Create: `tests/validator_test.py`
- Create: `tests/dynamic_array_test.py`
- Create: `tests/history_list_test.py`
- Create: `tests/favorite_list_test.py`
- Optional Create: `tests/file_service_test.py`, `tests/dictionary_service_test.py` neu muon bao phu CRUD truc tiep tot hon

## Implementation Steps

1. Implement `TestRunner` voi `assert_true`, `assert_false`, `assert_equal`, `print_summary`.
2. Implement unit tests bat buoc trong doc cho Word, Trie, Levenshtein, Validator, DynamicArray, HistoryList, FavoriteList.
3. Them test CRUD service neu co thoi gian: them tu, tu trung, favorite phai ton tai, search exact them history, approximate suggestions.
4. Them test FileService khong crash khi file thieu/dong sai format bang cach dung temp folder hoac monkey-patch AppConfig tam thoi va restore.
5. Implement `AllTests.run_all()` goi toan bo test.
6. Chay `python main.py` chon unit tests hoac chay truc tiep `python -m tests.all_tests` neu ho tro.
7. Chay smoke test application: load data, hien menu, chon thoat de save.

## Success Criteria

- [ ] Tat ca test trong muc 17 cua `SKILL.MD` pass.
- [ ] Test runner in total/passed/failed ro rang.
- [ ] Chay test khong can cai thu vien ngoai.
- [ ] Test FileService khong pha du lieu nguoi dung.
- [ ] Manual smoke test menu khong crash.

## Risk Assessment

Test IO de lam ban data files. Nen dung data tam thoi hoac backup/restore trong test; khong ghi truc tiep len du lieu that ma khong khoi phuc.
