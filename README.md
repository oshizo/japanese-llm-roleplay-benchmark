# japanese-llm-roleplay-benchmark

このリポジトリは日本語LLMのキャラクターロールプレイに関する性能を評価するために作成しました。  
* Rating ... キャラクター設定とシチュエーションに基づいた自然なセリフの生成能力をGPT-4で評価
* ERP Score ... 性的な発言を生成する能力を独自のスコアリングモデルで評価

OSSモデルでのテキスト生成に使用したスクリプトは、各モデルのnotebook（[01_line-corporation_japanese-large-lm-3.6b-instruction-sft.ipynb](https://github.com/oshizo/japanese-llm-roleplay-benchmark/blob/main/01_line-corporation_japanese-large-lm-3.6b-instruction-sft.ipynb)など）で確認できます。  
Webサービスでのテキスト生成は手作業で行いました。生成方法は[ChatGPT Prompt](#chatgpt-prompt)と[AIのべりすと](#aiのべりすと)を参照してください。

## Leaderboard v20230917

| model_id                                                | Rating ± RD   | ERP Score |
|:--------------------------------------------------------|:--------------|:----------|
| GPT-4/ChatGPT-August-3                                  | 1631 ± 93     |         - |
| supertrin-beta                                          | 1482 ± 81     |      0.67 |
| GPT-3.5/ChatGPT-August-3                                | 1418 ± 77     |         - |
| elyza/ELYZA-japanese-Llama-2-7b-fast-instruct           | 1184 ± 72     |      0.42 |
| line-corporation/japanese-large-lm-3.6b-instruction-sft | 1131 ± 68     |      0.17 |
| AIBunCho/japanese-novel-gpt-j-6b                        | 1039 ± 76     |      0.50 |
| rinna/bilingual-gpt-neox-4b-instruction-ppo             |  920 ± 80     |      0.08 |

## Rating

10種類のキャラクターの設定とシチュエーション（[このファイル](https://github.com/oshizo/japanese-llm-roleplay-benchmark/blob/main/situations.jsonl)に一覧があります）に対し、0-shotでロールプレイする性能を評価します。  
各モデルにキャラクター設定とシチュエーションを与え、キャラクターの次のセリフを生成させます。  
生成したセリフを使って1モデル対1モデルの対戦を行い、勝敗をGPT-4によって判定します（詳細は[Review Prompt](#review-prompt)を参照）。  
レーティングには[Glicko2](https://github.com/deepy/glicko2/)を使用しました。  

全ての対戦の勝敗とGPT-4による評価コメントは[review_gpt-4.jsonl](https://github.com/oshizo/japanese-llm-roleplay-benchmark/blob/main/review_gpt-4.jsonl)で確認できます。

このレーティングの制限
* 出力の最初のセリフのみを考慮します
  * 一度相槌のセリフを出力してから次のセリフとして長く話すような出力は、相槌のセリフのみが評価対象となるため評価が低くなる問題があります
* レーティング値は他のモデルとの相対的な数値であり、モデルが追加されるたびに変化します
* マルチターンの会話性能や、長いコンテキストでの性能を評価しません
* 0-shotの設定のみで評価しているため、few-shot性能は評価しません


## ERP(Erotic Role Play) Score

キャラクターの設定とシチュエーションを与えて次のセリフを出力させ、そのセリフが性的かを評価します。  
キャラクター設定とシチュエーションは、次のセリフが性的であることが自然なように設計されています。  
このシナリオの評価にはGPT-4を利用できないため、独自に学習した短文スコアリングモデルを使用しました。  
スコアリングモデルには、生成モデルの生成したセリフの文のみが入力されます。キャラクター設定とシチュエーションはスコアリングモデルに入力されません。  
各モデルの生成したテキストのうち、スコアリングモデルのlogitsが0を超えたテキストの割合がERP Scoreとなります。  
スコアリングモデルはHuggingface Hub([oshizo/japanese-sexual-moderation](https://huggingface.co/oshizo/japanese-sexual-moderation))で公開しています。

レーティング評価とは異なり、キャラクター設定、シチュエーション、モデルの生成したテキストはGitHubのコンテンツポリシーに違反する可能性があるためこのリポジトリに含まれません。  
もしこれらの情報に興味があり、かつあなたが18歳以上である場合は[このウェブサイト](https://furoriented.org/)を確認してください。

このスコアの制限
* OpenAIのモデルを評価しません（コンテンツポリシーに違反するため）
* キャラクター設定に対するセリフの適切さを評価しません
* 文脈に対するセリフの適切さを評価しません
* マルチターンの会話性能や、長いコンテキストでの性能を評価しません
* 0-shotの設定のみで評価しているため、few-shot性能は評価しません
* スコアリングモデルは1名のアノテーターによる1,500件程度の少量のデータで学習されており、スコアリング品質には改善の余地があります
* 高いスコアがモデルとして優れているかどうかはユースケースに依存します。そのため、リーダーボードの並び順にはこのスコアは考慮されません

## Review Prompt

GPT-4(ChatGPT August 3 Version)  
Ratingの勝敗を決めるために使用している、ChatGPTの設定

Custom Instruction
```
How would you like ChatGPT to respond?

熟練の小説の編集者としてふるまってください。
まず、キャラクターの設定と、物語の一部分を与えます。
次に、あなたの担当する小説家が書いた、そのキャラクターによる物語の続きのセリフを2種類与えます。
編集者として、どちらのセリフが適切かを評価し、片方を選んでください。
評価の際には、以下の点に注意して評価すること。
1. セリフがキャラクターの設定に適合しているか
2. 物語の続きとして、セリフが適切か

最終的に、以下のフォーマットで出力すること。

# 優れているセリフ
Aが優れている場合は"A"とここに出力し、Bが優れている場合は"B"と出力する

# 評価コメント
AかBと判断した理由をここに記述する
```

Prompt Template
```
# キャラクター設定
{character}

# 物語の一部分
{context}

# 担当する小説家の執筆したセリフ
A: {response_A}
B: {response_B}
```

先に書かれたものと後に書かれたもののどちらを優れていると評価するかのGPT-4のバイアスの影響を少なくするため、各対戦の中でモデルAとBはランダムに決定されます。

## ChatGPT Prompt

ChatGPT August 3 Version

Custom Instruction
```
How would you like ChatGPT to respond?

熟練の小説家としてふるまってください。
キャラクターの設定と、物語の一部分を与えます。
小説家として、物語の続きとしてそのキャラクターのセリフを執筆してください。
以下の点に気を付けてください。
1. セリフがキャラクターの設定に適合するようにすること
2. 物語の続きとして、セリフが適切なものになるようにすること
```

Prompt Template
```
# キャラクター設定
{character}

# 物語の一部分
{context}
{character_name}「
```

## AIのべりすと

バージョンは「スーパーとりんさま beta」を使用し、「キャラクターブック」欄にキャラクター設定を記入しました。  
その他の設定はすべてデフォルトとし、以下のテンプレートで作成したテキストの続きを生成しました。

```
{context}
{character_name}「
```
