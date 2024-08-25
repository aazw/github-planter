# github-planter

<img src="./github_activity_001.png" width="600px"/>

GitHubのActivityに草生やすやつ.


## Summary

* GitHubのActivityに草生やして見栄えを良くしたい
  * 自動で生やしたい
  * 草を生やす = いずれかのアクションを取る
    * コミットをする
    * コードレビューをする
    * Issueをつくる
    * Pull Requestをつくる
* GitHub Actionsの定期ジョブでコミットを1つ作成する
  * 1時間に1回実行
  * 毎回新しいファイルを生成してもリポジトリが巨大になりすぎるだけなので、必要最低限の更新に限定する
