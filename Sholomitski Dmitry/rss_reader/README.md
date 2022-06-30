Final Task Final Task for EPAM Python Training by Sholomitski Dmitry

I am proposed to implement Python RSS-reader using python 3.10.

RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format. Format of the news console output: $ rss_reader.py https://people.onliner.by/feed

channel title:  Лайфстайл Onlíner
channel link:  https://people.onliner.by/
************************************************************************************************************************
Title: В шестнадцать лет выиграла Олимпиаду, а в семнадцать — попалась на магазинной краже. Рассказываем о несчастливом вундеркинде женского тенниса (спецпроект)
Description: Богатые тоже плачут. Даже если они успешны, знамениты и обожаемы сотнями тысяч поклонников. Это относится и к американской теннисистке Дженнифер Каприати, которую снабдила талантом сама природа. Еще в подростковом возрасте спортсменка начала выносить взрослых соперниц. Уже в девять лет юной Дженни предлагали сотрудничество производители теннисной формы и снаряжения. А ведущие американские СМИ стали наблюдать за карьерой Каприати задолго до того, как теннисистка окончила школу. Вместе с BETERA в нашем спортивном проекте рассказываем, как «золотая» девочка из спорта докатилась до магазинной кражи, марихуаны и мыслей о суициде.Читать далее…
Published: 2022-06-30 16:11:31
Image: https://content.onliner.by/news/thumbnail/19f511e02774f2c9d0c7d74e66342dbb.jpeg
Read more: https://people.onliner.by/2022/06/30/vunderkind
------------------------------------------------------------------------------------------------------------------------
'''
-h, --help     show this help message and exit
--version      Print version info and exit
--json         Save result as in JSON file
--limit LIMIT  Limit news if this parameter provided
-v, --verbose  Output verbose messages
--date DATE    Gets a date in YYYYMMDD format. Print news from the specified date.
--to-html      Convert news to HTML file (provide path to folder or file *.html)
--to-pdf       Convert news to PDF file (provide path to folder or file *.pdf)
'''


Utility provides the following interface: usage: rss_reader.py source [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date] [--to-html] [--to-pdf]

Pure Python command-line RSS reader.

positional arguments: source Input your RSS-link hear. Your link have to start with "https://"

JSON option prints news to stdout. Example:


{
    "rss_url": "https://people.onliner.by/feed",
    "channel_title": "Лайфстайл Onlíner",
    "channel_link": "https://people.onliner.by/",
    "item_title": "Украина, 126-й день",
    "item_pubdate": "2022-06-29 08:08:45",
    "item_description": "Вчера Минобороны России объяснило, что произошло в украинском Кременчуге: с самолетов высокоточным оружием был обстрелян склад с американской техникой. Украинское Минобороны публикует все новые снимки поставок... Продолжаем хронику. Читать далее…",
    "item_link": "https://people.onliner.by/2022/06/29/ukraina-126-j-den",
    "item_image": "https://content.onliner.by/news/thumbnail/1fee0b8254c5c24cf728800331bf6f5a.jpeg"
}

Installing the package (if Python is installed, check the version python=3.10)




'''create a folder, put files fo folder
create a virtual environment 
download virtualenv for win 'pip install virtualenv' and for Ubuntu 'sudo apt-get install python3-venv'
create the env for win 'python -m venv venv' and for linux '/usr/bin/python3 -m venv env')
activate the environment (for win 'env\Scripts\activate.bat', for Ubuntu 'source env/bin/activate')
pip install -r requirements.txt
pip setup.py install in folder with files
The package is ready to use'''

Note: if you are using Apple MacBook (or iMac) with M1(ARM) CPU converting to PDF works without pictures. It is bug connected with ARM architecture