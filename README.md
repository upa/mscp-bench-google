
# benchmarking mscp on Google Cloud

VMのスペック

* e2-standard-16

リージョン情報

| VM名   | リージョン              | 東京からのRTT |
| :-:    |    :-:                  | :-            |
| tokyo  | asia-northeast1-b       | N/A           |
| osaka  | asia-northeast2-a       | 
| sydney | australia-southreast1-b |
| oregon | us-west1-c              |

RTTはGoogle内部ネットワーク経由で0.5秒間隔100回のpingの結果の平均。


10GBのファイルをtempfsにおいて転送。以下結果。

### 東京 -> 大阪


