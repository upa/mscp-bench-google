
# benchmarking mscp on Google Cloud

VMのスペック

* e2-standard-16

リージョン情報とテスト結果。

| VM名   | リージョン              | 東京からのRTT    | mscp    | scp      |
|:------:|:-----------------------:|:-----------------|:--------|:---------|
| tokyo  | asia-northeast1-b       | N/A              | N/A     | N/A      |
| osaka  | asia-northeast2-a       | 9.354/0.146 ms   | 12.481s | 53.37s   |
| oregon | us-west1-c              | 88.718/0.216 ms  | 20.555s | 473.665s |
| sydney | australia-southreast1-b | 106.266/0.171 ms | 23.632s | 581.707s |

RTTはGoogle内部ネットワーク経由で0.5秒間隔100回のpingの結果。


10GBのファイルをtempfsにおいて転送。以下結果。

`./osaka`, `./oregon`, `./sydney` はテスト実行。真の計測結果は
`dat/[region]/[scp|mscp]`の中。


