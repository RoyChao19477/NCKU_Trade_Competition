# DSAI-HW3-2021

## My thought:
### Step 1: 製作 predict model 
在參與競價之前，有個大前提，就是必須要有一個能夠準確預測用電與產電量的模型。  
  
最初，我是使用 Gradient Boosting Regression 來做這次的競賽，  
因此製作了`1_Preprocessing.ipynb`這份檔案。  
  
但是後來因為模型的效果沒有到非常好，因此又重新使用了另一個模型，  
也是最後參與競賽的模型 "lightGBM"，模型的製作在`3_lightGBM.ipynb`檔案中。  

### Step 2: Trading Strategy
要買電，或是賣電有一個很大的前提，就是預測電量必須要很準確。如果是缺電，卻還操控系統去賣電給別人，會賠很慘。  
因此，最重要的一步就是把 Step 1 做好。  
  
而後，由於交易機制是「賣價低」或者「買價高」的人可以保障以最後成交價購入，因此只要賣得超便宜或買得超貴，基本上一定就可以成功成交。  
但是這會造成一個風險，就是你有機率會以賠本的狀況買到比台電還貴的電，或是以太便宜價格賣出電力。
因此，我的保險機制是，將要賣出或買入的量，僅有少部分以「賣價超低」或「買價超高」的方式掛出交易單，而剩餘的數量以「不太會賠本」的價格掛出交易單。  
這樣能有效避免自己陷入危險中。  

但是還有另一個問題需要解決。由於這個交易競賽可以看到別人的出價，因此可以很容易的知道別人的交易策略。  
因此我做了一個有點壞的機制：所有「賣價超低、買價超高」的量的比例、出價的價格、都是用 random 一個區間的數值。也就是說，我的交易結果中將會看起來很混亂，無法輕易的猜出我的交易策略到底是啥鬼。
  
最後，我發覺早上 0:00 ~ 6:00 之間，還有晚上 18:00 後基本上是大家都缺電的狀況，所以如果要買電，只會買到超貴(可能高於台電價格)的電力。  
因此，我這段時間理論上不應該要以「賣價超低」或「買價超高」來進行交易，因為容易吃虧。  
但是我還是想要玩遊戲，所以我的策略是：在「買價超高」去買電的同時，也掛出相同數量的「最低賣價」去賣電。也就是說，就算是成交價很高，我也不會虧本。因為我是賣給我自己。  
不過有一個狀況我反而會賺大錢，就是如果有人傻傻上鉤，出價比我的「買價超高」還高的話，那就很可能變成我以超過台電的價格賣給他，而我自己卻不會買到自己賣出去的電。

## Requirements:
- python = 3.8 (**TA required**)
- Step 0 : use `pipenv install` to install dependency.

## How to run ?
- Step 1 : use `pipenv shell` to activate environment
- Step 2 : use `python main.py` to run

## Official Requirements:
### Source

  - [Slide](https://docs.google.com/presentation/d/1JW27_5HXYZhqWmgvDhtXBaFTOfksO_dS/edit#slide=id.p1)
  - [Dashboard](https://docs.google.com/spreadsheets/d/1cjhQewnXT2IbmYkGXRYNC5PlGRafcbVprCjgSFyDAaU/edit?pli=1#gid=0)

### Rules

- SFTP

```

┣━ upload/
┗━ download/
   ┣━ information/
   ┃  ┗━ info-{mid}.csv
   ┣━ student/
   ┃  ┗━ {student_id}/
   ┃     ┣━ bill-{mid}.csv
   ┃     ┗━ bidresult-{mid}.csv
   ┗━ training_data/
      ┗━ target{household}.csv  
      
```

1. `mid` 為每次媒合編號
2. `household` 為住戶編號，共 50 組
3. 請使用發給組長的帳號密碼，將檔案上傳至 `upload/`
4. 相關媒合及投標資訊皆在 `download/` 下可以找到，可自行下載使用


- File

```

┗━ {student_id}-{version}.zip
   ┗━ {student_id}-{version}/
      ┣━ Pipfile
      ┣━ Pipfile.lock
      ┣━ main.py
      ┗━ {model_name}.hdf5

```

1. 請務必遵守上述的架構進行上傳 (model 不一定要有)
2. 檔案壓縮請使用 `zip`，套件管理請使用 `pipenv`，python 版本請使用 `3.8`
3. 檔名：{學號}-{版本號}.zip，例：`E11111111-v1.zip`
4. 兩人一組請以組長學號上傳
5. 傳新檔案時請往上加版本號，程式會自動讀取最大版本
6. 請儲存您的模型，不要重新訓練

- Bidding

1. 所有輸入輸出的 csv 皆包含 header
2. 請注意輸入的 `bidresult` 資料初始值為空
3. 輸出時間格式為 `%Y-%m-%d %H:%M:%S` ，請利用三份輸入的 data 自行選一份，往後加一天即為輸出時間  
   例如: 輸入 `2018-08-25 00:00:00 ~ 2018-08-31 23:00:00` 的資料，請輸出 `2018-09-01 00:00:00 ~ 2018-09-01 23:00:00` 的資料(一次輸出`一天`，每筆單位`一小時`)
4. 程式每次執行只有 `120 秒`，請控制好您的檔案執行時間
5. 每天的交易量限制 `100 筆`，只要有超出會全部交易失敗，請控制輸出數量
