# AILT (Assistant Intelligent Language Teacher)

AILT is a Django-based web application designed to act as a "Digital AI-Powered ALT" for Japanese Teachers of English (JTE). It utilizes ultra-low latency LLMs (Groq) and real-time AI avatars (D-ID) to provide students with interactive, stress-free English speaking practice.


## 💡 開発の背景と目的 (Background & Motivation)

私は10年間、ALT（外国語指導助手）として日本の教育現場に従事してきました。その中で直面した最大の課題は、**「生徒一人あたりの圧倒的なアウトプット不足」**です。

40人のクラスにALTが1人という環境では、1回の授業で一人の生徒が英語を話せる時間はせいぜい1分程度です。現場の先生方（JTE）も多忙を極めており、一人ひとりのスピーキング評価を正確に行う余裕がありません。また、生徒側も「間違えるのが恥ずかしい」と萎縮してしまう心理的なハードルがありました。

これらの課題をテクノロジーで解決するために、**「ALTの代替ではなく、ALTの力を何倍にも高めるツール（ALT Multiplier）」**としてAILTを開発しました。

* **1対1の練習環境:** AIアバターを相手にすることで、生徒は間違いを恐れず、24時間いつでも納得いくまでスピーキング練習ができます。
* **評価の自動化:** 会話ログと間違いの記録をバックエンド（Django/SQLite）で管理し、JTEがダッシュボードで一括確認できるようにしました。

AILTを「本物のALTと話す前のシミュレーター」として活用することで、生徒が自信を持ち、限られた人間同士の対面授業をより高次元で有意義なものに変えることを最終的な目標としています。


## 🛠 テックスタック (Tech Stack)
* **Backend:** Python, Django
* **Database:** SQLite (Django ORM)
* **Frontend:** HTML, JavaScript (Fetch API, Web Speech API), Tailwind CSS
* **Third-Party APIs:** * Groq API (Llama 3.3 70B for high-speed conversational logic)
  * D-ID API (Real-time Avatar Video Streaming via WebRTC)


## 🔑 事前準備 (Prerequisites)

アプリケーションを実行する前に、プロジェクトのルートディレクトリ（`manage.py`と同じ階層）に `.env` ファイルを作成し、以下のAPIキーを設定してください。


**【APIキーの取得方法】**
1. **Groq API Key:** [Groq Cloud](https://console.groq.com/keys) にアクセスし、アカウントを作成して「Create API Key」から取得します。
2. **D-ID API Key:** [D-ID Studio](https://studio.d-id.com/) にアクセスし、左下の「Settings」→「API」からキーを生成して取得します。

取得したキーを用いて、`.env` ファイルに以下のように記述してください：

```text
GROQ_API_KEY="your_groq_api_key_here"
D_ID_API_KEY="your_d_id_api_key_here"
```

## 🚀 実行方法 (How to Run)

### Linux / macOS
```bash
# 1. 仮想環境の作成と有効化
python3 -m venv venv
source venv/bin/activate

# 2. 必要なパッケージのインストール
pip install -r requirements.txt

# 3. データベースのマイグレーション
python manage.py migrate

# 4. サーバーの起動
python manage.py runserver
```

### Windows
```PowerShell
# 1. 仮想環境の作成と有効化
python -m venv venv
venv\Scripts\activate

# 2. 必要なパッケージのインストール
pip install -r requirements.txt

# 3. データベースのマイグレーション
python manage.py migrate

# 4. サーバーの起動
python manage.py runserver
```

## 🌐 画面へのアクセス (Endpoints)
サーバー起動後、ブラウザで以下のURLにアクセスしてください：
* **アバターチャット画面:** `http://127.0.0.1:8000/classroom/`
* **プレゼンテーションモード:** `http://127.0.0.1:8000/classroom/presentation/`
* **教師用ダッシュボード:** `http://127.0.0.1:8000/classroom/dashboard/`
* **Django管理画面:** `http://127.0.0.1:8000/admin/`


## 📂 ファイル構成 (File Structure)

```text
├── ailt_project
│   ├── classroom
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── templates
│   │   │   └── classroom
│   │   │       ├── dashboard.html
│   │   │       ├── index.html
│   │   │       └── presentation.html
│   │   ├── urls.py
│   │   └── views.py
│   ├── config
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── manage.py
├── README.md
└── requirements.txt
```