---
phase: 7
title: "Menu main integration"
status: pending
priority: P2
effort: ""
dependencies: [6]
---

# Phase 7: Menu main integration

## Overview

Ket noi service vao menu console va entrypoint `main.py`. Phase nay bien cac module da co thanh ung dung chay duoc.

## Requirements

- Functional: menu co dung cac lua chon 0..10 trong doc; khi thoat phai save data.
- Non-functional: Menu khong xu ly thuat toan, khong doc/ghi file truc tiep, khong crash khi user nhap chu thay vi so.

## Architecture

`main.py` hien menu dau vao: run application hoac run unit tests. `Menu` giu mot `DictionaryService`, goi `load_data()` khi bat dau, loop den khi chon `0`, va `save_data()` khi thoat.

## Related Code Files

- Create/Modify: `ui/menu.py`
- Create/Modify: `main.py`
- Use: `services/dictionary_service.py`, `tests/all_tests.py`

## Implementation Steps

1. Implement `Menu.show_main_menu()` dung 10 lua chon va `0. Thoat`.
2. Implement `Menu.input_choice()` doc input, validate bang Validator/AppConfig, xu ly sai kieu bang thong bao va lap lai hoac tra default an toan.
3. Implement `Menu.run()` map tung choice sang method trong DictionaryService.
4. Khi choice `10`, goi `save_data()` va tiep tuc menu.
5. Khi choice `0`, goi `save_data()` truoc khi ket thuc.
6. Implement `main.py`: hien `1. Run application`, `2. Run unit tests`; input sai mac dinh chay application.

## Success Criteria

- [ ] `python main.py` chay duoc menu application.
- [ ] `python main.py` co the chon run tests.
- [ ] Nhap chu o menu khong crash.
- [ ] Menu khong import FileService truc tiep.

## Risk Assessment

Console input de gay loop kho thoat neu validation qua chat. Can giu UX don gian: thong bao loi ngan gon va hien lai menu.
