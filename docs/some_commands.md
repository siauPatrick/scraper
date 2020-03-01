создать окружение
```shell script
python3.7 -m venv ~/Projects/envs/cli_scraper
```

обновить pip
```shell script
pip install --upgrade pip
```

активировать окружние
```shell script
source ~/Projects/envs/cli-scraper/bin/activate
```

установить зависимости
```shell script
pip install -r requirements/dev.txt
```

---

загрузка страницы с командами
```shell script
python -m scraper fetch https://www.fifa.com/worldcup/teams/ > scraped/worldcup.html
```

запуск скрейпера
```shell script
python -m scraper crawl -f csv -o scraped/fifa.csv
```

XPath в браузере
```javascript
$x('//a[text()="Next Page"]')
```

CSS-query в браузере
```javascript
document.querySelector('.pagination a')
```
