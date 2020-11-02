===========
exam-reader
===========


.. image:: https://img.shields.io/pypi/v/exam_reader.svg
        :target: https://pypi.python.org/pypi/exam_reader

.. image:: https://img.shields.io/travis/9kin/exam_reader.svg
        :target: https://travis-ci.com/9kin/exam_reader

.. image:: https://readthedocs.org/projects/exam-reader/badge/?version=latest
        :target: https://exam-reader.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/9kin/exam_reader/shield.svg
     :target: https://pyup.io/repos/github/9kin/exam_reader/
     :alt: Updates





exam-reader -  программа для извлечения и обработки данных из файлов и формирования разных отсчётов.

Файлы протоколов проверки результатов ЕГЭ/ОГЭ/ВПР с расширением ``pdf`` представляют собой общую своднуную таблицу по образовательной организации.

Применение
===========

Протоколы приходят каждый год и в огромном количестве.

Учителя должны отвечать минестерству образования различную статистику (по школе, по учителям, пл предметам, лично по ученикам).

На это тратится очень много времени, потому что всё надо делать всё вручную.

.. figure:: https://i.imgur.com/qePOzLL.png
        :align: center

        Пример картинка `полученая с помощью ghostscript <https://www.ghostscript.com>`_

Принцип работы
==================

.. image:: https://i.imgur.com/wSmq5Ko.png

Зависимости (библиотеки).

* `camelot <https://github.com/camelot-dev/camelot>`_ извлечение таблиц PDF. Единственная библиотека которая распознаёт данный вид таблиц правильно. `Сравнение с другими библиотеками и инструментами для извлечения таблиц PDF. <https://github.com/camelot-dev/camelot/wiki/Comparison-with-other-PDF-Table-Extraction-libraries-and-tools>`_
* `PyMupdf <https://github.com/pymupdf/PyMuPDF>`_ привязки Python для библиотеки рендеринга `MuPDF <https://mupdf.com>`_. Основная функция (которой нет у подобных библитек) `извлечение блоков текста <https://pymupdf.readthedocs.io/en/latest/textpage.html#TextPage.extractBLOCKS>`_.
* `peewee <https://github.com/coleifer/peewee>`_ очень удобная ORM (поддерживает postgres).
* `flask  <https://github.com/pallets/flask>`_  микро-фреймворк для создания веб-приложений.

Процесс разработки
========================

Уже добавлена обработка pdf файлов с помощью `multiprocessing JoinableQueue <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.JoinableQueue>`_ camelot и PyMupdf.

----------------------------

* Documentation: https://exam-reader.readthedocs.io.
