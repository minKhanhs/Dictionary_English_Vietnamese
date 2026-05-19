---
title: "Trien khai tu dien Anh Viet theo SKILL.MD"
description: "Implementation roadmap to rebuild the English-Vietnamese console dictionary according to SKILL.MD."
status: pending
priority: P2
branch: "pham-dac-luc"
tags: []
blockedBy: []
blocks: []
created: "2026-05-19T16:03:14.959Z"
createdBy: "ck:plan"
source: skill
---

# Trien khai tu dien Anh Viet theo SKILL.MD

## Overview

Plan nay chia viec theo dung tai lieu `SKILL.MD`: tao lai cau truc module Python 3, tu cai dat data structures/algorithms, bo sung CRUD tu dien qua service layer, doc ghi file text, menu console, va test runner tu viet.

Pham vi chi gom chuong trinh console khong dung thu vien ngoai. Khong dung database, pytest, pandas, numpy, fuzzy-search package, hoac bat ky thu vien search san co nao.

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | [Audit va chuan hoa cau truc](./phase-01-audit-va-chuan-hoa-cau-truc.md) | Pending |
| 2 | [Config utilities validation](./phase-02-config-utilities-validation.md) | Pending |
| 3 | [Models va data structures](./phase-03-models-va-data-structures.md) | Pending |
| 4 | [Levenshtein va tim kiem](./phase-04-levenshtein-va-tim-kiem.md) | Pending |
| 5 | [File persistence](./phase-05-file-persistence.md) | Pending |
| 6 | [DictionaryService CRUD](./phase-06-dictionaryservice-crud.md) | Pending |
| 7 | [Menu main integration](./phase-07-menu-main-integration.md) | Pending |
| 8 | [Tests va verification](./phase-08-tests-va-verification.md) | Pending |

## Dependencies

Khong co plan project-local dang ton tai truoc do, nen plan nay khong bi block boi plan khac.

## Required Structure

Source tree can dat den sau khi implement:

```text
main.py
config/app_config.py
models/word.py
structures/trie.py
structures/dynamic_array.py
structures/history_list.py
structures/favorite_list.py
algorithms/levenshtein.py
services/dictionary_service.py
services/file_service.py
validation/validator.py
utils/string_utils.py
ui/menu.py
tests/test_runner.py
tests/all_tests.py
tests/*_test.py
data/dictionary.txt
data/history.txt
data/favorites.txt
```

## Success Criteria

- [ ] Chay `python main.py` hien menu chon application hoac unit tests.
- [ ] Application cho phep them tu, them synonym, tra cuu chinh xac, goi y gan dung, xem history, them/xoa/xem favorites, hien thi tat ca tu, luu du lieu.
- [ ] Du lieu duoc doc/ghi bang file text trong `data/`.
- [ ] Business logic nam trong `DictionaryService`; UI khong doc/ghi file truc tiep.
- [ ] Input sai kieu, rong, hoac file sai format khong lam chuong trinh crash.
- [ ] Tat ca test case trong `SKILL.MD` duoc bao phu bang test runner tu viet.

## Handoff

Lenh de tiep tuc implement:

```bash
cd /home/luc/Project/Dictionary_English_Vietnamese
ck plan status /home/luc/Project/Dictionary_English_Vietnamese/plans/260519-2303-trien-khai-tu-dien-anh-viet/plan.md
```
