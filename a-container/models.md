## Users

| 項目      | 和名       | タイプ   | 備考                             | 
| --------- | ---------- | -------- | -------------------------------- | 
| id        | id         | integer  |                                  | 
| anyNumber | 任意番号   | integer  | ソート用。重複禁止。Null禁止。     | 
| anyName   | 任意名     | string   | 対応履歴機能用。重複禁止。Null禁止。| 
| name      | 名前       | string   | ログイン時のID                   | 
| password  | パスワード | string   | ログイン時のパスワード           | 
| group     | グループ   | string   | とりあえず入れておく             | 
| role      | 権限       | string   | 権限によって編集できる範囲を設定 | 
| createdAt | 作成日時   | datetime |                                  | 
| updatedAt | 更新日時   | datetime |                                  | 

<br>

## Customers

| 項目名           | 和名           | タイプ      |  備考                             | 
| --------------- | --------------- | -------    |  -------------------------------- | 
| id              | id              | integer    |                                   | 
| anyNumber       | 任意番号         | integer    | ソート用。重複禁止。Null禁止。     | 
| closingMonth    | 決算月           | integer    |                                  | 
| customerName    | 得意先名         | text       |                                   | 
| customerKana    | ふりがな         | text       |  ジャンル分けするためのもの         | 
| honorificTitle  | 敬称            | text       |                                   | 
| department      | 部署            | text       |                                   | 
| postNumber      | 郵便番号        | string(20) |  ハイフンが入ると思ったのでstring | 
| address         | 住所1           | text       |                                   | 
| addressSub      | 住所2           | text       |                                   | 
| telNumber       | 電話番号         | string(30) |  ハイフンが入ると思ったのでstring | 
| faxNumber       | FAX番号         | string(30) |  ハイフンが入ると思ったのでstring | 
| url             | ホームページURL  | text       |                                   | 
| email           | メールアドレス   | text       |                                   | 
| manager         | 担当者          | text       |                                   |
| representative  | 代表者名        | text       |                                   | 
| customerCategory| お客様区分      | text       |  個人か法人か                      | 
| isHide          | 表示状態        | boolean    |  得意先情報を隠すかどうか          | 
| isFavorite      | お気に入り      | boolean    |  よく取引する顧客                  | 
| memo            | メモ            | text       |                                   |
| createdAt       | 作成日時        | datetime   |  作成日時                          |
| updatedAt       | 更新日時        | datetime   |  更新日時                          | 

<br>

## Items

| 項目名    | 和名     | タイプ     |  備考                                                                                       | 
| -------- | -------- | --------  |  ------------------------------------------------------------------------------------------ | 
| id       | id       | integer   |                                                                                             | 
| itemName | 商品名   | text      |                                                                                             | 
| itemCode | 商品コード| text      |  JANコード等の使用も考えられるので独自にコードを決められるように自由入力できるようにする。      | 
| model    | 型式      | text      |                                                                                            | 
| category | カテゴリ  | text      |                                                                                             | 
| maker    | メーカー  | text      |                                                                                             | 
| supplier | 仕入れ先  | text      |                                                                                             | 
| unit     | 単位     | text      |  単位はユーザーが追加できるように単位テーブルを作成し、単位追加ページを作成した方が良いかも         | 
| basePrice| 単価     | integer   |  請求書にて商品選択時に参照のみ。                                                              | 
| baseCost | 原価単価  | integer   |  請求書にて商品選択時に参照のみ。                                                             | 
| isHide   | 表示状態  | boolean    |  商品を一覧から隠すかどうか                                                                  | 
| memo     | メモ     | text      |                                                                                             | 
| numberOfAttachments | 添付数 | integer | 添付されたファイル数                                                                   | 
| createdAt| 作成日時 | datetime  |                                                                                             | 
| updatedAt| 更新日時 | datetime  |                                                                                             |

<br>

## Invoices

| 項目名       | 和名           | タイプ    |  備考                                                     | 
| ----------- | -------------- | -------- |  -------------------------------------------------------- | 
| id          | id             | integer  |                                                           | 
| customerId  | 得意先ID       | integer  |  フォーリンキー。                                         | 
| customerName| 得意先名       | string   |  紐づいたものor入力 両対応できるように                      | 
| customerAnyNumber|得意先任意番号|integer |  得意先が選択された際に自動挿入。一覧でのソート用。          | 
| honorificTitle| 敬称         | text     |                                                          | 
| department  | 部署           | string   |                                                          | 
| manager     | 担当者         | string   |                                                          | 
| otherPartyManager| 先方担当者| string   |                                                          | 
| applyNumber | 請求番号       | integer  |  作成時にインクリメント。他の請求書と被らないようにする。 | 
| applyDate   | 日付           | datetime |  請求書作成日                                             | 
| deadLine    | 支払期限       | datetime |                                                           | 
| paymentDate | 支払日         | datetime |                                                           | 
| isPaid      | 入金済み       | boolean  |                                                           | 
| title       | 件名           | text     |                                                           | 
| memo        | メモ           | text     |  アプリ利用者に見えるもの                                 | 
| remarks     | 備考           | text     |  印刷時に表示されるもの                                   |
| tax         | 消費税         | integer   |                                                         |
| isTaxExp    | 内税・外税     | boolean   |  内税・外税のチェック                                      | 
| isDelete    | 削除済み       | boolean   |  請求書は削除するのではなく、これにチェックする               | 
| numberOfAttachments | 添付数 | integer | 添付されたファイル数                                          | 
| createdAt   | 作成日時       | datetime  |                                                           | 
| updatedAt   | 更新日時       | datetime  |                                                           | 

<br>

## Invoice_Items

| 項目名      | 和名     | タイプ    |  備考                   | 
| ---------- | -------- | -------- |  ---------------------- | 
| id         | id       | integer  |                         | 
| invoiceId  | 請求書ID | integer  |  請求書テーブルと紐づく | 
| itemId     | 商品ID   | integer  |  商品テーブルと紐づく   | 
| rowNum     | 行番号   | integer  |  明細の並びを制御するため  | 
| any        | 自由項目 | string   |  ユーザーが自由に書き込む参照項目      | 
| itemName   | 商品名   | string   |  紐づいたものor入力 両対応できるように | 
| price      | 値段     | integer  |  Itemsテーブルを参照可能             |
| cost       | 原価     | integer  |  Itemsテーブルを参照可能             |
| count      | 個数     | integer  |                         | 
| unit       | 単位     | string   |  Unitテーブルを参照      | 
| remarks    | 備考     | string   |                         | 
| createdAt  | 作成日時 | datetime |                         | 
| updatedAt  | 更新日時 | datetime |                         | 

<br>

## Invoice_Payments

| 項目名        | 和名       | タイプ   | 備考                           | 
| ------------- | ---------- | -------- | ------------------------------ | 
| id            | id         | integer  |                                | 
| invoiceId     | 請求書ID   | integer  | 請求書テーブルと紐づく         | 
| paymentDate   | 支払い日付 | date     |                                | 
| paymentMethod | 支払い方法 | string   | 口座振込・現金・クレジット        | 
| paymentAmount | 入金金額   | integer  |                                | 
| remarks       | 備考       | string   |                                | 
| createdAt     | 作成日時   | datetime |                                | 
| updatedAt     | 更新日時   | datetime |                                | 

<br>

## Quotations

| 項目名       | 和名           | タイプ    |  備考                                                     | 
| ----------- | -------------- | -------- | -------------------------------------------------------- | 
| id          | id             | integer  |                                                          | 
| customerId  | 得意先ID       | integer  | フォーリンキー。                                         | 
| customerName| 得意先名       | string   |  紐づいたものor入力 両対応できるように                     | 
| customerAnyNumber|得意先任意番号|integer |  得意先が選択された際に自動挿入。一覧でのソート用。          | 
| honorificTitle | 敬称        | text     |                                                          | 
| department  | 部署           | string   |                                                          | 
| manager     | 担当者         | string   |                                                          | 
| otherPartyManager| 先方担当者| string   |                                                          | 
| applyNumber | 見積番号       | integer  | 作成時にインクリメント。他の見積書と被らないようにする。 | 
| applyDate   | 日付           | datetime | 見積書作成日                                             | 
| expiry      | 有効期限       | string   | 2022/3/9 DateからStringに変更                            | 
| dayOfDelivery| 納品期日      | string   |                                                          | 
| termOfSale  | 取引条件       | string   |                                                          | 
| isConvert   | 変換済み       | boolean  | 請求書へ変換したタイミングでフラグを立てる                   | 
| title       | 件名           | text     |                                                          | 
| memo        | メモ           | text     | アプリ利用者に見えるもの                                 | 
| remarks     | 備考           | text     | 印刷時に表示されるもの                                   | 
| tax         | 消費税         | integer  |                                                         |
| isTaxExp    | 内税・外税      | boolean  | 内税・外税のチェック                                     | 
| isDelete    | 削除済み       | boolean  |  見積書は削除するのではなく、これにチェックする              | 
| numberOfAttachments | 添付数 | integer | 添付されたファイル数                                       | 
| createdAt   | 作成日時       | datetime |                                                          | 
| updatedAt   | 更新日時       | datetime |                                                          | 

<br>

## Quotation_Items

| 項目名       | 和名     | タイプ    |  備考                   | 
| ----------  | -------- | -------- |  ---------------------- | 
| id          | id       | integer  |                         | 
| quotationId | 見積書ID | integer  |  見積書テーブルと紐づく   | 
| itemId      | 商品ID   | integer  |  商品テーブルと紐づく     | 
| rowNum      | 行番号   | integer  |  明細の並びを制御するため  |
| any         | 自由項目 | string   |  ユーザーが自由に書き込む参照項目      | 
| itemName    | 商品名   | string   |  紐づいたものor入力 両対応できるように |
| price       | 値段     | integer  |  Itemsテーブルを参照可能             |
| cost        | 原価     | integer  |  Itemsテーブルを参照可能             |
| count       | 個数     | integer  |                         | 
| unit        | 単位     | string   |  Unitテーブルを参照      | 
| remarks     | 備考     | string   |                         | 
| createdAt   | 作成日時 | datetime |                         | 
| updatedAt   | 更新日時 | datetime |                         | 

<br>

## Memos

| 項目名    | 和名     | タイプ   | 備考 | 
| --------- | -------- | -------- | ---- | 
| id        | id       | integer  |      | 
| title     | 件名     | text     |      | 
| manager   | 担当者   | text     |      | 
| isFavorite| お気に入り| boolean  | お気に入りメモ | 
| content   | 内容     | text     |      | 
| createdAt | 作成日時 | datetime |      | 
| updatedAt | 更新日時 | datetime |      | 

<br>

## Units

| 項目名    | 和名     | タイプ    |  備考 | 
| -------- | -------- | -------- |  ---- | 
| id       | id       | integer  |       | 
| unitName | 単位名   | text     |       | 
| createdAt| 作成日時 | datetime |       | 
| updatedAt| 更新日時 | datetime |       | 

<br>

## Categories

| 項目         | 和名       | タイプ   | 備考 | 
| ------------ | ---------- | -------- | ---- | 
| id           | id         | integer  |      | 
| categoryName | カテゴリ名 | text      |      | 
| createdAt    | 作成日時   | datetime |      | 
| updatedAt    | 更新日時   | datetime |      |

<br>

## Makers

| 項目         | 和名       | タイプ   | 備考 | 
| ------------ | ---------- | -------- | ---- | 
| id           | id         | integer  |      | 
| makerName    | メーカー名  | text     |      | 
| createdAt    | 作成日時   | datetime |      | 
| updatedAt    | 更新日時   | datetime |      |

<br>

## History

| 項目名    | 和名       | タイプ   | 備考                             | 
| --------- | ---------- | -------- | -------------------------------- | 
| id        | id         | integer  |                                  | 
| userName  | ユーザー名 | string   | user.name                        | 
| modelName | モデル名   | string   | どのモデルに参照・変更を加えたか | 
| modelId   | モデルID   | integer  | どのIDに参照・変更を加えたか     | 
| action    | 行動       | string   | GET,POST,PUT,DELETE,LOGIN,LOGOUT | 
| createdAt | 作成日時   | datetime |                                  | 
| updatedAt | 更新日時   | datetime |                                  | 

<br>

## Setting

| 項目名                   | 和名             | タイプ       | 備考                     | 
| ----------------------- | ---------------- | --------    | ------------------------ | 
| companyName             | 会社名           | text        |                          | 
| registerNumber          | 登録番号         | integer(13) |                          | 
| representative          | 代表者名         | text        |                          | 
| administrator           | 管理者           | text        |                          | 
| postNumber              | 郵便番号         | string(20)  |                          | 
| address                 | 住所             | text        |                          | 
| telNumber               | 電話番号         | string(30)  |                          | 
| faxNumber               | FAX番号          | string(30)  |                          | 
| url                     | ホームページURL  | text        |                          | 
| email                   | メールアドレス   | text        |                          | 
| payee                   | 振込先          | text        |                          | 
| accountHolder           | 口座名義        | text        |                          | 
| accountHolderKana       | 口座名義カナ     | text        |                          | 
| logoFilePath            | ロゴファイルパス | text        |                          | 
| logoHeight              | ロゴ高さ        | integer     |                          | 
| logoWidth               | ロゴ幅          | integer     |                          | 
| stampFilePath           | 印鑑ファイルパス | text        |                          |
| stampHeight             | 印鑑高さ        | integer     |                          | 
| stampWidth              | 印鑑幅          | integer     |                          |  
| isDisplayQuotationLogo  | ロゴ見積書表示   | boolean     | 印刷時に表示するかどうか | 
| isDisplayInvoiceLogo    | ロゴ請求書表示   | boolean     | 印刷時に表示するかどうか | 
| isDisplayDeliveryLogo   | ロゴ納品書表示   | boolean     | 印刷時に表示するかどうか | 
| isDisplayQuotationStamp | 印鑑見積書表示   | boolean     | 印刷時に表示するかどうか | 
| isDisplayInvoiceStamp   | 印鑑請求書表示   | boolean     | 印刷時に表示するかどうか | 
| isDisplayDeliveryStamp  | 印鑑納品書表示   | boolean     | 印刷時に表示するかどうか | 
| defaultTax              | 初期消費税       | integer     | 請求・見積作成時に自動的に設定される消費税率 | 
| updatedAt               | 更新日時         | datetime    |                          | 
