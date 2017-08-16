+++
date = "2017-06-15T17:47:59+09:00"
draft = false
title = "ReadMe-CGE-LE"
slug = "redome_cgele"
categories = "ReadMe"
+++
Civ IV Gameplay Enhancements - Limited Edition (CGE-LE)

■概要
CGE for BtS3.19のMODMODです。

★変更点
CvMainInterface.py
AIとの相互通行条約が締結可能になると、スコア部分に雷アイコンが出ます。
一刻も早く宣教師を送ってもらいたい時などにご活用ください。
電力のアイコンなのは既存のアイコンの中から選んだためで、特に意味はありません。

黄金期の文明はスコアが黄金色になります。
イベントログを見返せば黄金期かどうかはわかりますが、僅かばかりの手間を省きます。

CvExoticForeignAdvisor.py
外交担当相の画面サイズを小さくし、技術タブを元のインターフェースに戻します。
CGEの技術タブで未知の技術の研究可能状態を見ることができないのが気になる方向けです。

TradeResourcePanel.py
TradeResourcePanelの一行表示に金銭取引額を追加します。

CvModSpecialDomesticAdvisor.py
vistaCheckを解除。都市ごとの建造物・遺産・プロジェクトの表が有効になります。
こちらでチェックした限りでは問題なく動作していますが、不具合が起きるようでしたら元に戻してください。

CvEventManager.py
パルチザンのバグフィックスのみです。

CvPediaCorporation.py
関数名の修正です。

CGEEventManager.py
TradeResourcePanelのオプションが設定可能です。
リマインダーに指導者名のプリセットを追加します。また、10ターンがデフォルトになります。
リマインダーはAlt+Mで呼び出すことができます。（CGEの機能です）

CIV4InterfaceModeInfos.xml
CIV4MissionInfos.xml
Action_Airbomb.dds
戦略爆撃アイコンです。

CvGameCoreDLL.dll
GlobalDefines.xml
以下の機能が追加されます。
・Colorized Slavery Mod（奴隷もしくは緊急生産が可能な都市の都市バーの色が変わります。）
・スコア表示部の指導者名にカーソルを合わせたときに最悪の敵を見ることができます。
・他国のスタックの旗にカーソルを合わせるとスタックが省略表示されます。（GlobalDefines.xmlで定義しています）
・スタックに昇進を付ける、スタックで殴るなどした際に音が大きくならないようにしました。

_CIV4GameTextInfos_Fix.xml
テキストの表現、スペースの有無の揺れなど細かいところを修正します。

■導入方法
CGEに上書きするだけです。変更したいファイルだけを個別に上書きしても動作しますが、
上記の変更点でセットになっているファイルは同時に入れる必要があります。

■Unofficial Patch対応版
rurunukoさん作成のUnofficial Patch対応版CGE-LEが公開されています。感謝感激です！
http://wikiwiki.jp/tohojojisi/?%C5%EC%CA%FD%BD%F6%BB%F6%BB%ED%A1%A6%C5%FD%B9%E7MOD%BE%D2%B2%F0%A1%A6%A5%C0%A5%A6%A5%F3%A5%ED%A1%BC%A5%C9
（上記ページのダウンロードリンクを開いた先の「オマケ・バニラ用」フォルダにあります）

■何かあったら
MODスレ、もしくはtwitterで鈴庭めた（@suzuniwa）に投げてください。

■バージョン履歴
1.04
外交画面でスパイポイント比の後に改行が入っていなかったのを修正しました。
音が大きくならない機能が昇進に適用されていなかったのを修正しました。
戦争中の文明と和平できる状態で他国の手一杯が表示されなくなる問題を修正しました。

1.03
リマインダーに指導者名のプリセットを追加しました。
戦略爆撃のアイコンとCvGameCoreDLLを追加しました。

1.02
SevoPediaの企業の項目で戻るを押した時にエラーが出る問題を修正しました。

1.01
Trade Resource Panelに余っていない資源も表示するオプションを付けました。

1.00
初期バージョンです。

■終わりに
CGEの作者様と、CGEを3.19用に調整された名無しさん、Unofficial Patch対応版を作られたrurunukoさんに深く感謝いたします。
