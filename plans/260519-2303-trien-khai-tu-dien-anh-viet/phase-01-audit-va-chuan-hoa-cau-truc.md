---
phase: 1
title: "Audit va chuan hoa cau truc"
status: pending
priority: P1
effort: ""
dependencies: []
---

# Phase 1: Audit va chuan hoa cau truc

## Overview

Kiem tra repo hien tai va dua cau truc file ve dung ten thu muc/file trong `SKILL.MD`. Phase nay tao nen nen lam truoc moi implementation.

## Requirements

- Functional: tao day du package/module theo cau truc bat buoc.
- Non-functional: ten file/module dung snake_case, moi class o file rieng, khong xoa du lieu nguoi dung neu dang co file text cu.

## Architecture

Ung dung se dung package phan tang: `ui` -> `services` -> `models/structures/algorithms/validation/utils/config`. Data text nam trong `data/` thay vi root de tranh hard-code va de FileService quan ly tap trung.

## Related Code Files

- Create: `data/.gitkeep` neu can giu thu muc rong.
- Create: `config/app_config.py`, `models/word.py`, `structures/dynamic_array.py`, `structures/history_list.py`, `structures/favorite_list.py`, `validation/validator.py`, cac file test con thieu.
- Modify/Rename: cac file CamelCase hien co sang ten theo doc neu can.
- Preserve/Migrate: `dictionary.txt`, `history.txt`, `favourite.txt` sang `data/dictionary.txt`, `data/history.txt`, `data/favorites.txt`.

## Implementation Steps

1. Liet ke file hien co va so sanh voi cau truc bat buoc trong `SKILL.MD`.
2. Tao cac thu muc con thieu: `data/`, `tests/`, va cac package co `__init__.py`.
3. Chuan hoa ten module sang snake_case nhu `app_config.py`, `word.py`, `dictionary_service.py`.
4. Chuyen/tao data files dung ten: `dictionary.txt`, `history.txt`, `favorites.txt`.
5. Cap nhat import path theo ten module moi.
6. Dam bao khong con logic quan trong nam sai tang, dac biet UI khong doc/ghi file truc tiep.

## Success Criteria

- [ ] Cau truc thu muc khop voi `SKILL.MD`.
- [ ] Import module Python khong bi loi do doi ten file.
- [ ] Data files nam trong `data/` va co the rong nhung ton tai.
- [ ] Khong mat noi dung dictionary/history/favorites cu neu file cu da co du lieu.

## Risk Assessment

Rui ro lon nhat la doi ten file lam hong import. Giam rui ro bang cach chuan hoa theo tung nhom module va chay import smoke test sau phase.
