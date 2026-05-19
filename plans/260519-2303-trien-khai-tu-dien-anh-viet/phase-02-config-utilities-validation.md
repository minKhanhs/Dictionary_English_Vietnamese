---
phase: 2
title: "Config utilities validation"
status: completed
priority: P1
effort: ""
dependencies: [1]
---

# Phase 2: Config utilities validation

## Overview

Xay dung nen config, xu ly chuoi, va validation de cac phase sau khong hard-code rule. Day la lop phong ve cho input nguoi dung va du lieu file.

## Requirements

- Functional: `AppConfig`, `StringUtils`, `Validator` co du bien va method trong doc.
- Non-functional: khong crash voi `None`, chuoi rong, input sai kieu; khong hard-code separator/path/gioi han o module khac.

## Architecture

`AppConfig` la nguon cau hinh duy nhat. `StringUtils` normalize input truoc khi validate/search/save. `Validator` chi kiem tra hop le, khong xu ly nghiep vu va khong doc/ghi file.

## Related Code Files

- Create/Modify: `config/app_config.py`
- Create/Modify: `utils/string_utils.py`
- Create/Modify: `validation/validator.py`
- Modify: import references trong cac module lien quan

## Implementation Steps

1. Dinh nghia day du bien trong `AppConfig`: file path, max sizes, Levenshtein thresholds, separators, validation lengths, menu range, field count.
2. Dat `DATA_FOLDER = "data/"` va cac path con dua tren config, khong lay root tuy tien.
3. Implement `StringUtils.trim`, `to_lower_case`, `remove_extra_spaces`, `normalize_word`, `split`, `join`.
4. Implement `Validator.is_empty`, `is_length_in_range`, `is_valid_english_word`, `is_valid_vietnamese_meaning`, `is_valid_example`, `is_valid_synonym`, `is_valid_menu_choice`, `is_valid_dictionary_line`, `has_enough_fields`.
5. Cho phep English word gom `a-z`, khoang trang, dau gach ngang sau normalize; khong chap nhan so/ky tu la.
6. Chuan hoa method naming sang snake_case theo code style trong doc.

## Success Criteria

- [x] Khong co path, separator, gioi han max/min hard-code ngoai `AppConfig`.
- [x] Validator tra ve `False` thay vi raise exception voi input sai.
- [x] Normalize word cho ket qua lower-case, trim, va bo khoang trang du.
- [x] Menu choice validate duoc khoang `0..10` theo menu trong doc.

## Risk Assessment

Can can bang validation tieng Anh: doc noi `a-z`, khoang trang, gach ngang; nen tranh dung `char.isalpha()` vi co the chap nhan ky tu Unicode ngoai y muon.
