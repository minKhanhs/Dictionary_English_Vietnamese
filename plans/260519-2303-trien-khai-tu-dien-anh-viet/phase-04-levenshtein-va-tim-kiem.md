---
phase: 4
title: "Levenshtein va tim kiem"
status: completed
priority: P2
effort: ""
dependencies: [2, 3]
---

# Phase 4: Levenshtein va tim kiem

## Overview

Tu cai dat Levenshtein Distance va quy tac threshold de phuc vu tim kiem gan dung khi exact search that bai.

## Requirements

- Functional: `Levenshtein.distance(a, b)` va `get_threshold(word_length)` dung nhu doc.
- Non-functional: khong dung thu vien fuzzy search ngoai; code ro rang, de test.

## Architecture

`Levenshtein` nam rieng trong `algorithms/`. `DictionaryService.search_approximate` se goi algorithm nay khi duyet DynamicArray, loc theo threshold, sap xep distance tang dan, va cat theo `MAX_SUGGESTIONS`.

## Related Code Files

- Create/Modify: `algorithms/levenshtein.py`
- Later integration: `services/dictionary_service.py`
- Tests: `tests/levenshtein_test.py`

## Implementation Steps

1. Implement dynamic programming matrix cho distance.
2. Xu ly input `None` bang cach coi nhu chuoi rong hoac convert an toan theo convention.
3. Implement insert/delete/substitute cost = 1.
4. Implement `get_threshold`: short/medium/long dua tren `AppConfig`.
5. Them test cho equal, insertion, deletion, substitution, va `kitten` -> `sitting`.

## Success Criteria

- [x] `distance("hello", "hello") == 0`.
- [x] Mot thao tac them/xoa/thay ky tu tra ve `1`.
- [x] `distance("kitten", "sitting") == 3`.
- [x] Threshold tra ve dung theo do dai tu.

## Risk Assessment

Voi dictionary lon, DP moi tu co chi phi O(n*m). Vi bai tap console/file text nho, chap nhan duoc; khong them optimization phuc tap tru khi test performance that bai.
