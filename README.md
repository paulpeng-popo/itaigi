# 愛台語爬蟲程式文件
## Prerequisite
+ selenium == 4.5.0
+ beautifulsoup4 == 4.11.1
+ webdriver-manager == 3.8.3
+ tqdm == 4.64.1

---

## 篩選規則(優先度)
1. 出處為 <span style="color: green"> **臺灣閩南語常用詞辭典** 或 **台文華文線頂辭典** </span>
   - `return` 華語具有與原輸入詞一致之翻譯
   - `return` **按呢講好** 數量最多
2. 出處 <span style="color: red">不為 **臺灣閩南語常用詞辭典** 或 **台文華文線頂辭典** </span>
   - `return` 華語具有與原輸入詞一致之翻譯
   - `return` **按呢講好** 數量最多
3. 其他
   1. `return (None, None)`

## Notes
+ 若 candidate 的台文為羅馬拼音，則取
  + 華語翻譯為台文，原本之台文為台羅
+ 若存在多種台文或羅馬拼音
  + 取第一個
---

## Usage

+ Example1

    program:
    ```python
    from ... import TaiGiTranslator

    translator = TaiGiTranslator()
    print(translator.translate('醫院'))
    translator.close()
    ```

    output:
    ```sh
    ('病院', 'pēnn-īnn')
    ```

+ Example2

    program:
    ```python
    from ... import TaiGiTranslator

    with open('input.txt', 'r', encoding='utf8') as f:
        test_cases = f.readlines()
        test_cases = [x.strip() for x in test_cases]

    translator = TaiGiTranslator()
    cands = translator.batch_translate(test_cases)
    translator.close()

    with open('output.txt', 'w', encoding='utf8') as f:
        for cand in cands:
            f.write(f'{cand[0]}\t{cand[1]}\n')
    ```

    input:
    ```sh
    東西
    事情
    太陽
    月亮
    樓下
    三餐
    地面
    樓上
    地震
    午後雷陣雨
    芒果
    奇異果
    ```

    output:
    ```sh
    物件	mi̍h-kiānn
    代誌	tāi-tsì
    日頭	ji̍t-thâu
    月	    gue̍h
    樓跤	lâu-kha
    正頓	tsiànn-tǹg
    塗跤    thôo-kha
    樓頂	lâu-tíng
    地動	tē-tāng
    西北雨	sai-pak-hōo
    檨仔	suāinn-á
    羊桃	iûnn-thô
    ```
---

## Source code
https://github.com/paulpeng-popo/itaigi
