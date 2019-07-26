Quick Start
#############

.. code:: powershell

    pipenv install
    pipenv shell
    cd Chapter06

    python setup_db.py

    nameko run temp_messenger.message_service --config config.yaml
    nameko run temp_messenger.user_service --config config.yaml

    $env:FLASK_APP="temp_messenger.web_server:app"
    flask run


已发现缺陷

- 用户登录时间太久，大约2秒
