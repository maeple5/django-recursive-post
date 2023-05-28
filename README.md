簡単な掲示板です。製作期間：約1日。

[これとは別の公開リポジトリ](https://github.com/maeple5/portfolio-CSS-practice)にあるJSファイルを活用し、取り入れています。
テンプレートをincludeを多用して管理することを心掛けました。
全く網羅はしていませんがいくつかテストを書いています。
認証機能にはdjango-allauthを使いました。なお、django-allauthのテンプレートは現時点では整えていません。

少し工夫したところとして、ヘッダーのナビのリスト（PICKUP, FEATURE, CONTACT, LOGIN, etc...）にあります。
トップページではPICKUP, FEATURE, CONTACTをクリックすることでページがスクロールするようにしてあります。
トップページ以外ではリストにPICKUP, FEATURE, CONTACTを含めないようにしました。
以下の部分になります。

    #django-recursive-post/templates/includes/header/header-nav.html
    
    <ul class="nav-menu">
      {% url 'top' as top_url %}
      {% if request.path == top_url %}
        <li><a href="#pickup">PICK UP</a></li>
        <li><a href="#feature">POSTS</a></li>
        <li><a href="#contact">CONTACT</a></li>
      {% endif %}
      {% if user.is_authenticated %}
        <li><a href="{% url "account_logout" %}">LOGOUT</a></li>
      {% else %}
        <li><a href="{% url "account_login" %}">LOGIN</a></li>
        <li><a href="{% url "account_signup" %}">SIGN UP</a></li>
      {% endif %}
    </ul>

その他こだわったポイントとして、記事へのコメント機能があります。
コメントへの返信、またその返信への返信を、再帰的な入れ子になるようにしてあります。


使用方法

    $ python -m venv venv
    $ .\venv\Scripts\activate
    $ cd django-recursive-post
    $ pip install -r requirements.txt
    $ python manange.py migrate
    $ python manage.py collectstatic
    $ python manage.py runserver
