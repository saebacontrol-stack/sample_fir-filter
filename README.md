# FIR Filter & Zero-Phase Filter Demo

PythonとMatplotlibを用いた、通常のFIRフィルタと零位相フィルタの時間応答の比較ツールです。  
（ローパスフィルタのみ）

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)


## 概要 (Overview)
FIRフィルタのタップ数を大きくするにつれ、通常のFIRフィルタでの遅れが大きくなっていく様子を観察できます。  
（加えて、フィルタのカットオフ周波数を変えたときの特性や応答波形の変化も確認できます）

- カットオフ周波数とフィルタのタップ数（次数）はスライダーで変更可能

---

## 実行方法 (Usage)

### 必要なライブラリ
```bash
pip install numpy matplotlib
```
### 実行手順
```bash
python sample_fir-filter
```
