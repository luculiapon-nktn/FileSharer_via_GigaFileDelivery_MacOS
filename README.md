# FileSharer_via_GigaFileDelivery_MacOS
ファイルをギガファイル便にアップロードして、ダウンロードURLを自動的に返してくれるサービス。  
Finderのファイルを右クリックするとクイックアクションからアップロードしてくれます。  

## できないこと
・一度に複数のファイルをアップロードし、複数のファイルのダウンロードURLをクリップボードにコピーする  
・一度に複数のファイルをアップロードし、ひとつにまとめられたZipファイルのダウンロードURLをクリップボードにコピーする  
・削除キーの取得  
・ファイル保持期間変更（デフォルトでは5日）  

## 実行推奨環境
・MacOS Sonoma 14.0 以上  
・Visual Studio Code 1.83.1 以上  
・git 2.39.3 以上  
・Python 3.10.5 以上  
・Poetry 1.6.1 以上  
・pyenv 2.3.30 以上  
・Automator 2.10 以上  
・(Homebrew 4.1.17 以上)  

## 環境構築のための準備
__ここでは基本的なことしか述べていないので、わかる人は読み飛ばしても構いません。__
1. Viaual Studio Codeのインストール  
   下記URLよりインストーラーをダウンロードして、インストールを実行してください。  
   https://code.visualstudio.com/download
2. Pythonのバージョン確認  
   ターミナルを開いて下記コマンドを実行してください。  
   ```
   python --version
   ```
   下記のように表示されれば正常にインストールされているので、4及び5はスキップして構いません。  
   （ぶっちゃけバージョンはPython3であればたぶん動くと思うので、なんでもいいです。）  
   ```
   python 3.10.5
   ```
   もし、Pythonがインストールされていなければ下記コマンドのようになるので、Pythonをインストールするために3〜5に進みましょう。
   ```
   command not found: python
   ```
3. Homebrewのインストール  
   ターミナルを開いて下記コマンドを実行してください。  
   Homebrewのインストールはこの後の4及び6を実行するのに必要です。
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   [Homebrew公式](https://brew.sh)  
   M1Macの場合、更に下記の２つのコマンドを実行してください。
   ```
   echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
   ```
   ```
   source ~/.zshrc
   ```
   最後に下記コマンドを実行してHomebrewがインストールできているか確認しましょう。
   ```
   brew -v
   ```
4. （pyenvのインストール）  
   ターミナルを開いて下記コマンドを実行してください。
   ```
   brew install pyenv
   ```
   下記コマンドを実行してpyenvがインストールできているか確認しましょう。
   ```
   pyenv --version
   ```
   最後にpyenvの設定を行います。下記の4つのコマンドを実行してください。
   ```
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
   ```
   ```
   echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
   ```
   ```
   echo 'eval "$(pyenv init -)"' >> ~/.zshrc
   ```
   ```
   source ~/.zshrc
   ```
5. （Pythonのインストール）  
   ターミナルを開いて下記コマンドを実行してください。
   ```
   pyenv install --list
   ```
   下記のようにインストールできるPythonバージョンのリストが一覧表示されます。
   ```
   2.1.3
   2.2.3
   2.3.7
   …
   （中略）
   …
   3.11.5
   3.11.6
   3.12.0
   ```
   今回は3.10.5をインストールしようと思います。
   ターミナルにて下記コマンドを実行してください。
   ```
   pyenv install 3.10.5
   ```
7. Gitのインストール  
   ターミナルを開いて下記コマンドを実行してください。
   ```
   git --version
   ```
   バージョンが表示されれば無事インストールされているのでこの工程はスキップして構いません。
   エラー表示が出れば、未インストールなので下記コマンドを引き続きターミナルで実行しましょう。
   ```
   brew install git
   ```
   もう一度下記コマンドを実行してバージョン情報が表示されたらインストール完了です。
   ```
   git --version
   ```
8. Poetryのインストール  
   Poetryはたぶんデフォルトではインストールされていないと思うのでターミナルにて下記コマンドを実行しましょう。
   ```
   curl -sSL https://install.python-poetry.org | python -
   ```
   次に下記コマンドを実行。your_user_nameのところはあなたのPCの名前に置き換えてください。
   ```
   echo 'export PATH="/Users/your_user_name/.local/bin:$PATH"' >> ~/.zshrc
   ```
   ```
   source ~/.zshrc
   ```
   ターミナルにて下記コマンドを実行して正常にバージョン情報が表示されたらインストール完了です。
   ```
   poetry --version
   ```
   最後にPoetryの設定を変更しておきましょう。
   ```
   poetry config virtualenvs.in-project true
   ```
   これで作業ディレクトリ内に.venvファイルを生成することができるようになります。
9. GitHubアカウントの登録
   下記URLにてGitHubアカウントを登録してください。
   https://github.co.jp

   このままではまだGitでの操作はできません。ターミナルにて下記コマンドを実行しましょう。
   ```
   cd ~/.ssh
   ```
   ```
   ssh-keygen -t rsa
   ```
   すると、下記のような３つの質問をされます。何も入力せずに３回Return(Enter)キーを押しましょう。
   ```
   Generating public/private rsa key pair.
   Enter file in which tosave the key (/Users/your_user_name/.ssh/id_rsa):
   Enter passphrase (empty for no passphrase):
   Enter same passphrase again:
   ```
   Finderで/Users/your_user_name/.ssh/に移動してみましょう。
   （Macでは.sshフォルダは非表示化されています。なのでFinderの 移動>フォルダに移動 でフォルダパスを指定して移動すると良いです。）  
   id_rsa（秘密鍵）とid_rsa.pub（公開鍵）が生成されていることがわかります。  
   id_rsa.pub（公開鍵）をVisual Studio Codeで開いてみましょう。  
   何かしらの暗号のような文字列が一行目に表示されているのがわかります。  
   これを全選択(command+A)してコピー(command+C)しましょう。

   GitHubアカウントに戻ります。
   Dashboardに行くと右上にアカウントアイコンが表示されているのでクリックします。メニューが開くのでSettingsを選択します。
   左のメニューバーから Access > SSH and GPG keys を選択します。
   __New SSH key__をクリックしましょう。
   ![image1](img/20231028122811)