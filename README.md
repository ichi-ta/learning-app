# learning-app
実験実習で作成したアプリケーション

```
#DBの初期化
docker exec -it <コンテナ名> bash

cd ./test_app

export FLASK_APP=models.py
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```
