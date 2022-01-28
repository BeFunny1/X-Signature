# X-Signature

Идея `X-Signature` состоит в том, что на стороне клиента мы можем подписать строку вида: `f'{method}\n{canonical_url}\n{canonical_query}\n{canonical_headers}'` нашим секретным ключом, а на стороне сервера, при получении запроса, проверить, что доступ запрашивается к тем же данным и с теми же параметрами.

Реализация выполнена в рамках `Django` проекта.

Код в качестве `middleware` можно найти [здесь](https://github.com/BeFunny1/X-Signature/blob/master/src/app/middlewares.py).  
Скрипт для генерации заголовков - [клик](https://github.com/BeFunny1/X-Signature/tree/master/script).   
UI в виде НеВеРоЯтНоГо окошка на PyQt5- [клик](https://github.com/BeFunny1/X-Signature/tree/master/ui).   
