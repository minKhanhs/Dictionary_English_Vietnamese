# Đặc Tả Module Hiện Tại

## Tổng Quan Kiến Trúc

Ứng dụng được tách thành các lớp chính:

- `main.py`: chọn chạy app hoặc test suite.
- `ui/`: menu console và input/output người dùng.
- `services/`: nghiệp vụ từ điển và persistence.
- `structures/`: cấu trúc dữ liệu tự cài đặt, gồm Trie, ArrayList và một bản `Word`.
- `models/`: model/list domain, gồm `HistoryList`, `FavoriteList` và một bản `Word`.
- `algorithms/`: Levenshtein và fuzzy search.
- `validate/`: validation input/file/menu.
- `config/`: hằng số cấu hình và response code.
- `utils/`: helper xử lý chuỗi.
- `tests/`: unit tests bằng `unittest`.

## Cấu Hình

`config/AppConfig.py` đang chứa:

| Nhóm | Hằng số |
| --- | --- |
| File dữ liệu | `DATA_FOLDER`, `DICTIONARY_FILE`, `HISTORY_FILE`, `FAVORITES_FILE` |
| Giới hạn list | `MAX_SYNONYMS`, `MAX_HISTORY_SIZE`, `MAX_SUGGESTIONS` |
| Trie | `ALPHABET_SIZE`, `FIRST_CHAR`, `LAST_CHAR` |
| Fuzzy search | `SHORT_WORD_LENGTH`, `MEDIUM_WORD_LENGTH`, `SHORT_WORD_DISTANCE`, `MEDIUM_WORD_DISTANCE`, `LONG_WORD_DISTANCE` |
| File format | `FIELD_SEPARATOR`, `LIST_SEPARATOR`, `MEANING_SEPARATOR`, `DICTIONARY_FILE_FIELD_COUNT` |
| Validation | `MIN_*`, `MAX_*` cho word/meaning/example/menu |

`DATA_FOLDER` hiện là root repo, nên các file dữ liệu nằm cạnh `main.py`.

## Entry Point: `main.py`

Vai trò:

- Thêm root repo vào `sys.path`.
- Hiển thị lựa chọn chạy ứng dụng hoặc test.
- `runApplication()` tạo `Menu` và gọi `run()`.
- `runTests()` discover test trong `tests/` với pattern `Test*.py`.
- Bắt `KeyboardInterrupt` và exception tổng quát để in response label.

## UI: `ui/Menu.py`

`Menu` chịu trách nhiệm vòng lặp console:

- Tạo `DictionaryService` và `MenuHandler`.
- Load dữ liệu trước khi vào vòng lặp.
- Hiển thị menu 0-11.
- Validate lựa chọn bằng `Validation.isValidMenuOption()`.
- Điều hướng sang handler theo option.
- Save dữ liệu khi chọn option 10 hoặc khi thoát bằng option 0.
- Bắt `KeyboardInterrupt`, `EOFError` và exception tổng quát trong vòng lặp.

## UI Handler: `ui/MenuHandler.py`

`MenuHandler` chứa thao tác nhập liệu cụ thể:

- `addWord()`: nhập english/vietnamese/example/synonyms, tạo `structures.Word.Word`, gọi `DictionaryService.addWordObject()`.
- `addSynonym()`: tìm chính xác từ, sau đó gọi trực tiếp `Word.addSynonym()`.
- `searchExact()`: tìm chính xác, hiển thị từ hoặc gọi gợi ý gần đúng.
- `searchApproximate()`: gọi `displaySuggestions()`.
- `addFavorite()`: kiểm tra từ tồn tại qua service trước khi thêm favorite.
- `removeFavorite()`, `showFavorites()`, `showHistory()`, `displayAllWords()`.
- `deleteWord()`: xác nhận rồi gọi `DictionaryService.deleteWord()`.

Handler vẫn có nhiều `print()` và `input()`, nhưng không trực tiếp đọc/ghi file.

## Service: `services/DictionaryService.py`

`DictionaryService` là tầng nghiệp vụ chính.

State nội bộ:

- `trie`: `Trie` phục vụ search chính xác và fuzzy search.
- `words`: `ArrayList` chứa các `Word` object.
- `history`: `HistoryList`.
- `favorites`: `FavoriteList`.
- `fileService`: `FileService`.
- `fuzzySearch`: cache `FuzzySearch`, build từ Trie root.

API hiện có:

| Method | Hành vi |
| --- | --- |
| `loadData()` | Reset state, load dictionary/history/favorites, build fuzzy search |
| `saveData()` | Save words/history/favorites, trả về bool tổng hợp |
| `addWordObject(word)` | Validate, chống trùng, thêm vào `ArrayList` và Trie |
| `importWordObject(word)` | Validate; nếu trùng english thì merge meanings/synonyms |
| `wordExists(word)` | Normalize và kiểm tra Trie |
| `searchExact(word)` | Search Trie, trả `Word`, ghi history nếu tìm thấy |
| `searchApproximate(word)` | Lấy suggestions từ `FuzzySearch`, trả danh sách `Word` |
| `getWord(english)` | Lấy word không ghi history |
| `deleteWord(english)` | Xóa khỏi Trie bằng `Trie.delete()`, xóa khỏi `ArrayList`, rebuild cache fuzzy search, xóa khỏi favorites nếu có |
| `getHistory()` | Trả `HistoryList` |
| `getFavorites()` | Trả `FavoriteList` |
| `getAllWords()` | Trả list từ `ArrayList` |

Lưu ý: `addWordObject()` hiện không kiểm tra return value của `trie.insert()`. Nếu validation cho phép ký tự mà Trie không nhận, word vẫn có thể nằm trong `ArrayList` nhưng không searchable.

## Service: `services/FileService.py`

`FileService` chịu trách nhiệm file text:

- `ensureDataFiles()`: tạo file dictionary/history/favorites nếu thiếu.
- `loadDictionary()`: parse từng dòng bằng `Word.fromFileLine()`, bỏ qua dòng invalid.
- `saveDictionary(wordsList)`: ghi từng `Word.toFileLine()`.
- `loadHistory()` / `saveHistory()`: đọc ghi file đơn giản một item mỗi dòng.
- `loadFavorites()` / `saveFavorites()`: tương tự history.

Simple file load/save normalize item bằng `StringUtils.normalizeWord()`.

## Domain: `Word`

Hiện có hai file cùng vai trò:

- `structures/Word.py`
- `models/Word.py`

Hai implementation gần như giống nhau. Khác biệt chính nằm ở `_splitMeanings()` và cách split synonyms:

- `structures.Word` dùng `StringUtils.splitAndClean()`.
- `models.Word` có chỗ tự split thủ công.

Code runtime của app dùng `structures.Word` trong `DictionaryService`, `FileService` và `MenuHandler`. Nhiều test đang import `models.Word`, nhưng vì API tương đương nên vẫn pass.

API chính của `Word`:

- Getter/setter: `getEnglish()`, `getVietnamese()`, `getExample()`, `getSynonyms()`.
- Meaning: `getMeaningList()`, `hasMeaning()`, `addMeaning()`, `mergeFrom()`.
- Synonym: `addSynonym()`, `hasSynonym()`, `getSynonymCount()`.
- Persistence: `toFileLine()`, `fromFileLine()`.
- Console: `display()`.

`Word` sanitize field separator `|` trong text để tránh hỏng format file.

## Data Structure: `structures/Trie.py`

`Trie` dùng `TrieNode` với dictionary `children`.

API:

- `insert(word, word_data=None)`: chỉ nhận chuỗi hợp lệ theo `_isValidWord()`.
- `search(english)`: trả bool.
- `searchData(english)`: trả `wordData` nếu node là end-of-word.
- `delete(word)`: bỏ dấu kết thúc từ, xóa `wordData` và prune các node không còn được dùng.
- `startsWith(prefix)`: kiểm tra prefix.

Trie hiện chỉ chấp nhận ký tự từ `AppConfig.FIRST_CHAR` đến `AppConfig.LAST_CHAR`, tức `a-z`.

## Data Structure: `structures/ArrayList.py`

`ArrayList` là mảng động tự quản lý:

- Capacity ban đầu `10`.
- `add()` resize gấp đôi khi đầy.
- `remove()` shift phần tử sau về trước, shrink khi size nhỏ hơn 1/4 capacity.
- `get()`, `set()`, `getSize()`, `isEmpty()`, `clear()`, `toList()`, `contains()`.
- `DynamicArray = ArrayList` là alias tương thích.

## Domain Lists

### `models/HistoryList.py`

- Lưu history trong list Python.
- `add()` normalize word và bỏ qua empty.
- Giới hạn bằng `AppConfig.MAX_HISTORY_SIZE`, eviction FIFO.
- Cung cấp `display()`, `getCount()`, `getItem()`, `clear()`, `toList()`.

### `models/FavoriteList.py`

- Lưu favorites trong list Python.
- `add()` normalize và chống trùng.
- `remove()` normalize rồi xóa nếu có.
- Cung cấp `contains()`, `display()`, `getCount()`, `getItem()`, `clear()`, `toList()`.

Việc chỉ cho favorite từ đã tồn tại đang nằm ở UI handler, không nằm trong `FavoriteList`.

## Algorithm: `algorithms/Levenshtein.py`

`Levenshtein` nhận `targetWord` khi khởi tạo:

- `getInitialRow()`: tạo row `[0..len(target)]`.
- `calculateNextRow(previousRow, currentLetter)`: tính row tiếp theo cho dynamic programming.
- `distance(inputWord)`: tính edit distance đầy đủ.

## Algorithm: `algorithms/FuzzySearch.py`

`FuzzySearch` nhận Trie root:

- `extractAllWords()` hiện thu thập toàn bộ từ trong Trie vào `allWords`, nhưng search chính dùng traversal đệ quy.
- `getMaxDistance(wordLength)` chọn threshold theo `AppConfig`.
- `searchRecursive()` duyệt Trie và dùng row Levenshtein để prune.
- `getSuggestions(targetWord)` trả tối đa `AppConfig.MAX_SUGGESTIONS`, sort theo `(distance, word)`.

## Validation: `validate/Validation.py`

API hiện có:

- `isEmpty()`
- `isLengthValid()`
- `isEnglishWord()`
- `isVietnameseMeaning()`
- `isValidExample()`
- `isValidSynonym()`
- `isValidMenuOption()`
- `hasEnoughFields()`
- `isValidDictionaryEntry()`

Điểm cần chú ý: `isEnglishWord()` cho phép chữ cái, dấu cách và dấu gạch ngang; Trie lại chỉ nhận `a-z`.

## Utils: `utils/StringUtils.py`

API:

- `join(items, separator)`
- `normalizeWord(word)`: `strip()`, lower, remove extra spaces.
- `removeExtraSpaces(text)`
- `splitAndClean(text, separator)`

Hiện `normalizeWord()` giả định input là string. Các caller chính thường guard trước khi gọi.

## Response Code

`config/ResponseCode.py` gom label và code trạng thái:

- Test labels: `PASS`, `FAIL`, `SKIP`.
- App codes: `SUCCESS`, `INFO`, `INPUT_INVALID`, `NOT_FOUND`, `DUPLICATE`, `FILE_ERROR`, `EMPTY`, `CANCELLED`, `ERROR`.
